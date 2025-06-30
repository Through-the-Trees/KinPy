import httpx

import datetime
from datetime import datetime as dt
import re
from collections import Counter

from key import DEVICE_AUTH, SQUARE_KEY

headers = {
    "Square-Version": "2025-05-21",
    "Authorization": f"Bearer {SQUARE_KEY}",
    "Content-Type": "application/json"
}

# payments_endpoint = "https://connect.squareup.com/v2/payments"
# response: httpx.Response = httpx.get(payments_endpoint, headers=headers)
# response_dict: dict = response.json()
# payments: list[dict] = response_dict['payments']
# for payment in payments[0:5]:
#     print('\n')
#     print(payment['created_at'])
#     print(payment['device_details'])
#     print(payment['application_details'])
#     time: dt = dt.fromisoformat(payment['created_at'])
#     print(f'{time.strftime("%B")} {time.day} @ {time.hour%12}:{time.minute}')
# response: dict = httpx.get("https://connect.squareup.com/v2/locations", headers=headers).json()
# locations = response

# # Print all location IDs and names
# for loc in locations.get("locations", []):
#     print(f"Name: {loc['name']} - ID: {loc['id']}")

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
search_orders_endpoint = "https://connect.squareup.com/v2/orders/search"

more_items: bool = True
cursor = None
all_notes: str = ''
test_dict: dict[dt, list] = {}

earliest_datetime = dt.now(datetime.timezone.utc)
latest_datetime = dt.min.replace(tzinfo=datetime.timezone.utc)
while more_items:
    body["cursor"] = cursor
    response: dict = httpx.post(search_orders_endpoint, headers=headers, json=body).json()
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

        if 'line_items' in order:
            items = order['line_items']
            test_dict[created_datetime] = []
            for item in items:
                if 'note' in item:
                    test_dict[created_datetime].extend(re.findall(r"\d{4}", item['note']))
                    all_notes += item['note'] + '~'

print(f'First transaction: {earliest_datetime.strftime("%B")} {earliest_datetime.day}, {earliest_datetime.year} @ {earliest_datetime.hour%12}:{earliest_datetime.minute}')
print(f'Last transaction: {latest_datetime.strftime("%B")} {latest_datetime.day}, {latest_datetime.year} @ {latest_datetime.hour%12}:{latest_datetime.minute}')
sold_assets = re.findall(r"\d{4}", all_notes)
print(f'{len(sold_assets)=}\n{len([asset for assets in test_dict.values() for asset in assets])=}')
# print([asset for assets in test_dict.values() for asset in assets])
# sold_assets = [w for w in re.findall(r'\b\w+\b', all_notes) if len(re.findall(r'\d', w)) == 4]
# Ignore items returned and sold multiple times / record duplicates
unique_sold_assets = [asset for asset, _ in Counter(sold_assets).items()]

from interfaces import KintonePortal, KTApp, QueryString

kintone_portal = KintonePortal('https://throughthetrees.kintone.com/k/v1/', DEVICE_AUTH, True)
devices_app = KTApp(kintone_portal, 4)
# Field translation
ASSET_TAG = "Text"
ITEM_STATUS = "Drop_down_2"
records: list = []
record_errors: dict[str, list[str]] = {}
for i in range(0, len(unique_sold_assets), 100):
    chunk = unique_sold_assets[i:i + 100]
    query = QueryString(f"{ASSET_TAG} in ({', '.join(str(s) for s in chunk)})")
    records.extend( devices_app.get_records([ASSET_TAG, ITEM_STATUS], query) )

for record in records:
    if record[ITEM_STATUS] != 'Sold':
        if record[ITEM_STATUS] not in record_errors:
            record_errors[record[ITEM_STATUS]] = []
        record_errors[record[ITEM_STATUS]].append(record[ASSET_TAG])
        # print(f'Asset {record[ASSET_TAG]} marked {record[ITEM_STATUS]}!')

for k, v in record_errors.items():
    print(f'{len(v)} records marked as {k}: {v}')

found_assets: list[str] = [record[ASSET_TAG] for record in records]
missing_assets: list[str] = [asset for asset in sold_assets if asset not in found_assets]
print(f'{len(missing_assets)} missing records: {missing_assets}')