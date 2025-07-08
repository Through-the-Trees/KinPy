import os
import re

from datetime import datetime as dt, date, timezone, timedelta
import logging

import httpx
from key import DEVICE_AUTH, SQUARE_KEY
from interfaces import KintonePortal, KTApp, QueryString

# Ping healthchecks.io
httpx.get("https://hc-ping.com/42570a12-f6f9-478d-8aa0-eb423bb1c706")

# Specefy custom dates
# start_date: list[str] = [int(string) for string in "07-01-2025".split("-")]
# end_date: list[str] = [int(string) for string in "07-08-2025".split("-")]
EST_TIMEZONE = timezone(timedelta(hours=-5))
now_est: dt = dt.now(tz=EST_TIMEZONE)
start_dt: dt = dt(year=now_est.year, month=now_est.month, day=now_est.day, hour=0, minute=0, second=0, tzinfo=EST_TIMEZONE)
end_dt: dt = dt(year=now_est.year, month=now_est.month, day=now_est.day, hour=23, minute=59, second=59, tzinfo=EST_TIMEZONE)

# Specefy custom date range (override):
start_dt: dt = dt(year=2025, month=7, day=1, hour=0, minute=0, second=0, tzinfo=EST_TIMEZONE)
end_dt: dt = dt(year=2025, month=7, day=8, hour=23, minute=59, second=59, tzinfo=EST_TIMEZONE)

LOG_FILE = 'square.log'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d-%y %H:%M',
                    filename=LOG_FILE,
                    filemode='a')

logger = logging.getLogger(__name__)

def dt_readable(datetime_obj: dt) -> str:
    return f'{datetime_obj.strftime("%B")} {datetime_obj.day}, {datetime_obj.year} at {datetime_obj.hour%12}:{datetime_obj.minute}'

def kintone_date(datetime_obj: dt) -> str:
    return f'{datetime_obj.year}-{ str(datetime_obj.month).zfill(2) }-{ str(datetime_obj.day).zfill(2) }'

# TODO: Adjust to check start to end of current day
headers = {
    "Square-Version": "2025-05-21",
    "Authorization": f"Bearer {SQUARE_KEY}",
    "Content-Type": "application/json"
}

body = {
    "location_ids": ["LMFF68Y330SJR"], # Location ID for "Through the Trees"
    "limit": 1000,
    "query": {
        "filter": {
            "date_time_filter": {
                "created_at": {
                "start_at": f"{start_dt.strftime("%Y-%m-%dT%H:%M:%SZ")}",
                "end_at": f"{end_dt.strftime("%Y-%m-%dT%H:%M:%SZ")}"
                }
            }
        }
    }
}

# Key = Asset Tag
# Value = dict[ field name, field value ]
unique_sold_items: dict[ str, dict[str, str] ] = {}

cursor = None
more_items: bool = True
while more_items:
    body["cursor"] = cursor
    response: dict = httpx.post("https://connect.squareup.com/v2/orders/search", headers=headers, json=body).json()
    if 'cursor' in response:
        cursor = response['cursor']
        logger.info(f"Cursor ID: {cursor}")
    else:
        more_items = False
    if 'orders' not in response:
        break
    orders: list[dict] = response['orders']
    for order in orders:
        created_datetime: dt = dt.fromisoformat(order['created_at'])
        if 'line_items' not in order:
            continue
        items = order['line_items']
        for item in items:
            if 'note' not in item:
                continue
            sold_assets = re.findall(r"(?<!\d)\d{4}(?!\d)", item['note'])
            for sold_asset in sold_assets:
                sold_item = {
                    'created_datetime': created_datetime,
                    'name': item['name'] if 'name' in item else 'Unknown Item Type',
                    'price': item['base_price_money']['amount'] / 100,
                    'full_note': item['note']
                }
                if sold_asset not in unique_sold_items or (sold_asset in unique_sold_items and unique_sold_items[sold_asset]['created_datetime'] < created_datetime):
                    unique_sold_items[sold_asset] = sold_item

# Remove donations from sold items (no need for record)
unique_sold_items = {k: v for k, v in unique_sold_items.items() if v['name'] != 'Donation'}

kintone_portal = KintonePortal('https://throughthetrees.kintone.com/k/v1/', DEVICE_AUTH, True)
devices_app = KTApp(kintone_portal, 4)

# Kintone field translation
ASSET_TAG = "Text"
ITEM_STATUS = "Drop_down_2"
LOCATION = "Drop_down_4"
ITEM_TYPE = "Drop_down"
DISTRIBUTION_DATE = "Date_distribution"
PRICE = "Number_0"
NOTES = "Text_area"

# Square category translation
# TODO: Update square categories
type_conversion_dict: dict[str, str] = {
    'Other': 'Other',
    'Computer': 'Laptop: Windows',
    'Tablet': 'Tablet: Apply iPad',
    'Phone': 'Phone: Apple iPhone',
    'Battery Bank': 'Other',
    'Speaker': 'Speaker',
    'Camera': 'Camera',
    'Unknown Item Type': 'Other',
    'Ereader': 'Other',
    'Mouse': 'Keyboard or Mouse',
    'TV': 'TV',
    'Monitor': 'Monitor',
    'Earbuds': 'Other',
    'iPod': 'Other',
    'Printer': 'Printer',
    'Radio': 'Other'
}

unique_sold_assets = [k for k in unique_sold_items.keys()]
records: list = []
for i in range(0, len(unique_sold_assets), 100):
    chunk = unique_sold_assets[i:i + 100]
    query = QueryString(f"{ASSET_TAG} in ({', '.join(str(s) for s in chunk)})")
    records.extend( devices_app.get_records([ASSET_TAG, ITEM_STATUS, LOCATION, ITEM_TYPE, DISTRIBUTION_DATE, PRICE], query) )

logger.info(f"{len(unique_sold_items)} unique items sold between {dt_readable(start_dt)} and {dt_readable(end_dt)}")
logger.info(f"{len(records)} corresponding records found in Kintone")

found_assets: list[str] = [record[ASSET_TAG] for record in records]
missing_records: dict[str, dict[str, str]] = {k: v for k, v in unique_sold_items.items() if k not in found_assets}

if missing_records:
    logger.error(f'{len(missing_records)} missing records: {list(missing_records.keys())}')

for asset, sales_record in missing_records.items():
    new_record = {
        ASSET_TAG: asset,
        ITEM_STATUS: 'Sold',
        LOCATION: 'Out',
        ITEM_TYPE: type_conversion_dict[sales_record['name']],
        NOTES: f"Record created automatically based on square sales\nSquare Category: {sales_record['name']}\nSquare item note: {sales_record['full_note']}",
        DISTRIBUTION_DATE: kintone_date(sales_record['created_datetime']),
        PRICE: int(sales_record['price'])
    }

    # devices_app.add_record(new_record)

record_status_errors: dict[str, list[str]] = {}
record_location_errors: list[str] = []
record_price_errors: list[str] = []
for record in records:
    update_record: bool = False
    
    record_asset_tag = record[ASSET_TAG]
    sales_record = unique_sold_items[record_asset_tag]

    # Check record status
    if record[ITEM_STATUS] != 'Sold':
        record_status_errors.setdefault(record[ITEM_STATUS], []).append(record_asset_tag)
        record[ITEM_STATUS] = 'Sold'
        update_record = True
    
    if record[LOCATION] != "Out":
        record_location_errors.append(record_asset_tag)
        record[LOCATION] = "Out"
        update_record = True
    
    if record[PRICE] != sales_record['price']:
        record_price_errors.append(record_asset_tag)
        record[PRICE] = sales_record['price']
        update_record = True

    # Test distribution date
    if record[DISTRIBUTION_DATE] == kintone_date(sales_record['created_datetime']):
        pass
    else:
        print(f'{record[DISTRIBUTION_DATE]} does not match {kintone_date(sales_record['created_datetime'])}!')
        record[DISTRIBUTION_DATE] = kintone_date(sales_record['created_datetime'])
        update_record = True
    
    # if update_record:
    #     devices_app.update_record(record)

for status, record_list in record_status_errors.items():
    logger.warning(f'Status updated from "{status}" to "Sold" for Records: {record_list}')

if record_location_errors:
    logger.warning(f'Location change to "Out" for records: {record_location_errors}')
if record_price_errors:
    logger.warning(f'Price updated to match sales for records: {record_price_errors}')