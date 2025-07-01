from typing import Any

import httpx

from datetime import datetime as dt, timezone, timedelta

import re
from collections import Counter

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
start_date: list[str] = [int(string) for string in "06-20-2025".split("-")]
end_date: list[str] = [int(string) for string in "06-20-2025".split("-")]
start_dt: dt = dt(year=start_date[2], month=start_date[0], day=start_date[1], hour=0, minute=0, second=0, tzinfo=est_timezone)
end_dt: dt = dt(year=end_date[2], month=end_date[0], day=end_date[1], hour=23, minute=59, second=59, tzinfo=est_timezone)

headers = {
    "Square-Version": "2025-05-21",
    "Authorization": f"Bearer {SQUARE_KEY}",
    "Content-Type": "application/json"
}

body = {
    "location_ids": ["LMFF68Y330SJR"],
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

sales_by_date: dict[str, list] = {}
date_by_sales: dict[str, str] = {}

sold_items: list[ dict[str, Any] ] = []

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
        sales_by_date[kintone_date(created_datetime)] = []
        for item in items:
            if 'note' not in item:
                continue
            sold_assets = re.findall(r"\d{4}", item['note'])
            for sold_asset in sold_assets:
                sold_item = {
                    'asset_tag': sold_asset,
                    'created_at': order['created_at'],
                    'name': item['name'],
                    'full_note': item['note'] # REMOVE
                }
                sold_items.append(sold_item)
                if sold_asset not in date_by_sales or (sold_asset in date_by_sales and date_by_sales[sold_asset] < created_datetime):
                    date_by_sales[sold_asset] = created_datetime
            sales_by_date[kintone_date(created_datetime)].extend(sold_assets)
            
unique_sold_assets = [k for k in date_by_sales.keys()]

print(sold_items)

from interfaces import KintonePortal, KTApp, QueryString

kintone_portal = KintonePortal('https://throughthetrees.kintone.com/k/v1/', DEVICE_AUTH, True)
devices_app = KTApp(kintone_portal, 4)
# Field translation
ASSET_TAG = "Text"
ITEM_STATUS = "Drop_down_2"
DISTRIBUTION_DATE = "Date_distribution"
records: list = []
record_errors: dict[str, list[str]] = {}
for i in range(0, len(unique_sold_assets), 100):
    chunk = unique_sold_assets[i:i + 100]
    query = QueryString(f"{ASSET_TAG} in ({', '.join(str(s) for s in chunk)})")
    records.extend( devices_app.get_records([ASSET_TAG, ITEM_STATUS, DISTRIBUTION_DATE], query) )

correct_date: int = 0
incorreect_date: int = 0
date_mismatches: list = []
for record in records:
    # Check rocord status
    if record[ITEM_STATUS] != 'Sold':
        if record[ITEM_STATUS] not in record_errors:
            record_errors[record[ITEM_STATUS]] = []
        record_errors[record[ITEM_STATUS]].append(record[ASSET_TAG])
    
    # Test distribution date
    record_date = record[DISTRIBUTION_DATE]
    if record_date == kintone_date(date_by_sales[record[ASSET_TAG]]):
        correct_date += 1
    else:
        incorreect_date += 1
        date_mismatches.append(f'Asset {record[ASSET_TAG]} | Record: {record_date} | Sale: { kintone_date(date_by_sales[record[ASSET_TAG]]) }')

for k, v in record_errors.items():
    print(f'{len(v)} records erroneously marked as {k}: {v}')

found_assets: list[str] = [record[ASSET_TAG] for record in records]
missing_assets: list[str] = [asset for asset in unique_sold_assets if asset not in found_assets]
print(f'{len(missing_assets)} missing records: {missing_assets}')

print(f'{correct_date} records with correct date input\n{incorreect_date} incorrect dates:')
for string in date_mismatches:
    print(string)