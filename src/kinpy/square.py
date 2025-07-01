import httpx

import datetime
from datetime import datetime as dt, timezone, timedelta

import re
from collections import Counter

from key import DEVICE_AUTH, SQUARE_KEY

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
                "start_at": "2020-01-01T00:00:00Z",
                "end_at": "2025-06-28T23:59:59Z"
                }
            }
        }
    }
}


est_timezone = timezone(timedelta(hours=-5))
def dt_readable(datetime_obj: dt) -> str:
    datetime_obj = datetime_obj.astimezone(est_timezone)
    return f'{datetime_obj.strftime("%B")} {datetime_obj.day}, {datetime_obj.year} @ {datetime_obj.hour%12}:{datetime_obj.minute}'

def kintone_date(datetime_obj: dt) -> str:
    return f'{datetime_obj.year}-{ str(datetime_obj.month).zfill(2) }-{ str(datetime_obj.day).zfill(2) }'

all_notes: str = ''
sales_by_date: dict[str, list] = {}
date_by_sales: dict[str, str] = {}
earliest_datetime = dt.now(datetime.timezone.utc)
latest_datetime = dt.min.replace(tzinfo=datetime.timezone.utc)

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
    orders: list[dict] = response['orders']

    for order in orders:
        created_datetime: dt = dt.fromisoformat(order['created_at'])
        if created_datetime < earliest_datetime:
            earliest_datetime = created_datetime
        if created_datetime > latest_datetime:
            latest_datetime = created_datetime

        if 'line_items' not in order:
            continue
        items = order['line_items']
        sales_by_date[kintone_date(created_datetime)] = []
        for item in items:
            if 'note' not in item:
                continue
            sold_assets = re.findall(r"\d{4}", item['note'])
            for sold_asset in sold_assets:
                if sold_asset not in date_by_sales or (sold_asset in date_by_sales and date_by_sales[sold_asset] < created_datetime):
                    date_by_sales[sold_asset] = created_datetime
            sales_by_date[kintone_date(created_datetime)].extend(sold_assets)
            all_notes += item['note'] + '~'

print( dt_readable(earliest_datetime) )
print( dt_readable(latest_datetime) )
all_sold_assets = re.findall(r"\d{4}", all_notes)
duplicates = [[item, count] for item, count in Counter(all_sold_assets).items() if count > 1]
print(f'{len(duplicates)} items sold multiple times: {duplicates}')
print(f'{len(date_by_sales.keys())=}')
print(f'{len(all_sold_assets)=}')
# Ignore items returned and sold multiple times / record duplicates
unique_sold_assets = [asset for asset, _ in Counter(all_sold_assets).items()]

# for sold_dt, assets in sales_by_date.items():
#     if assets:
#         print(f'Items sold on {sold_dt}:\n{assets}')

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
    print(f'{len(v)} records marked as {k}: {v}')

found_assets: list[str] = [record[ASSET_TAG] for record in records]
missing_assets: list[str] = [asset for asset in all_sold_assets if asset not in found_assets]
print(f'{len(missing_assets)} missing records: {missing_assets}')

print(f'{len(date_mismatches)=}')

# print(f'{correct_date} records with correct date input\n{incorreect_date} incorrect dates')
# for string in date_mismatches:
#     print(string)