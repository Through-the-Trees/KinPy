from typing import Any

import httpx

from datetime import datetime as dt, timezone, timedelta

import re
from collections import Counter

from interfaces import KintonePortal, KTApp, QueryString

from key import DEVICE_AUTH, SQUARE_KEY

est_timezone = timezone(timedelta(hours=-5))
def dt_readable(datetime_obj: dt) -> str:
    datetime_obj = datetime_obj.astimezone(est_timezone)
    return f'{datetime_obj.strftime("%B")} {datetime_obj.day}, {datetime_obj.year} @ {datetime_obj.hour%12}:{datetime_obj.minute}'

def kintone_date(datetime_obj: dt) -> str:
    return f'{datetime_obj.year}-{ str(datetime_obj.month).zfill(2) }-{ str(datetime_obj.day).zfill(2) }'

# Prompt user for date
# start_date: list[str] = [int(string) for string in input("Please enter start date in format MM-DD-YYYY:").split("-")]
# end_date: str = input("Please enter end date in format MM-DD-YYYY (Press enter for single day):")
# end_date: list[str] = start_date if not end_date else [int(string) for string in end_date.split('-')]

# Override
start_date: list[str] = [int(string) for string in "01-01-2022".split("-")]
end_date: list[str] = [int(string) for string in "07-01-2025".split("-")]
start_dt: dt = dt(year=start_date[2], month=start_date[0], day=start_date[1], hour=0, minute=0, second=0, tzinfo=est_timezone)
end_dt: dt = dt(year=end_date[2], month=end_date[0], day=end_date[1], hour=23, minute=59, second=59, tzinfo=est_timezone)

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

unique_sold_items: dict[ str, dict[str, str] ] = {}

cursor = None
more_items: bool = True
while more_items:
    body["cursor"] = cursor
    response: dict = httpx.post("https://connect.squareup.com/v2/orders/search", headers=headers, json=body).json()
    if 'cursor' in response:
        cursor = response['cursor']
    else:
        more_items = False
    print(cursor)
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

# Square type: Kintone type
# TODO: update square types


kintone_portal = KintonePortal('https://throughthetrees.kintone.com/k/v1/', DEVICE_AUTH, True)
devices_app = KTApp(kintone_portal, 4)
# Field translation
ASSET_TAG = "Text"
ITEM_STATUS = "Drop_down_2"
LOCATION = "Drop_down_4"
ITEM_TYPE = "Drop_down"
DISTRIBUTION_DATE = "Date_distribution"
PRICE = "Number_0"
NOTES = "Text_area"

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

# Remove donations from sold items
unique_sold_items = {k: v for k, v in unique_sold_items.items() if v['name'] != 'Donation'}

unique_sold_assets = [k for k in unique_sold_items.keys()]

records: list = []
record_errors: dict[str, list[str]] = {}
for i in range(0, len(unique_sold_assets), 100):
    chunk = unique_sold_assets[i:i + 100]
    query = QueryString(f"{ASSET_TAG} in ({', '.join(str(s) for s in chunk)})")
    records.extend( devices_app.get_records([ASSET_TAG, ITEM_STATUS, LOCATION, ITEM_TYPE, DISTRIBUTION_DATE, PRICE], query) )

correct_date: int = 0
incorrect_date: int = 0
date_mismatches: list = []
location_fixed: int = 0
price_fixied: int = 0
for record in records:
    record_date = record[DISTRIBUTION_DATE]
    record_asset_tag = record[ASSET_TAG]
    sales_record = unique_sold_items[record_asset_tag]
    update_record: bool = False
    # Check record status
    if record[ITEM_STATUS] != 'Sold':
        if record[ITEM_STATUS] not in record_errors:
            record_errors[record[ITEM_STATUS]] = []
        record_errors[record[ITEM_STATUS]].append(record[ASSET_TAG])
        record[ITEM_STATUS] = 'Sold'
        update_record = True
    
    if record[LOCATION] != "Out":
        record[LOCATION] = "Out"
        update_record = True
        location_fixed += 1
    
    if record[PRICE] != sales_record['price']:
        record[PRICE] = sales_record['price']
        update_record = True
        price_fixied += 1

    # Test distribution date
    if record_date == kintone_date(sales_record['created_datetime']):
        correct_date += 1
    else:
        record[DISTRIBUTION_DATE] = kintone_date(sales_record['created_datetime'])
        update_record = True
        incorrect_date += 1
    
    # if update_record:
    #     devices_app.update_record(record)

for k, v in record_errors.items():
    print(f'{len(v)} records erroneously marked as {k}: {v} - Status changed to "Sold"')

print(f"{location_fixed} records' location updated to Out")
print(f"{price_fixied} records' prices updated")

print(Counter(r[ITEM_TYPE] for r in records))

found_assets: list[str] = [record[ASSET_TAG] for record in records]
missing_records: dict[str, dict[str, str]] = {k: v for k, v in unique_sold_items.items() if k not in found_assets}

print(f'{len(missing_records)} missing records: {list(missing_records.keys())}')

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

print(f'{correct_date} records with correct date input\n{incorrect_date} incorrect dates')