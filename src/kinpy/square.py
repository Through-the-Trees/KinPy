import httpx

import datetime
import re

headers = {
    "Square-Version": "2025-05-21",
    "Authorization": "Bearer ",
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
#     time: datetime.datetime = datetime.datetime.fromisoformat(payment['created_at'])
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
                "start_at": "2019-01-01T00:00:00Z",
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
earliest_datetime = datetime.datetime.now(datetime.timezone.utc)
latest_datetime = datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)
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
        created_datetime: datetime.datetime = datetime.datetime.fromisoformat(order['created_at'])
        if created_datetime < earliest_datetime:
            earliest_datetime = created_datetime
        if created_datetime > latest_datetime:
            latest_datetime = created_datetime

        if 'line_items' in order:
            items = order['line_items']
            for item in items:
                if 'note' in item:
                    all_notes += item['note'] + '~'

sold_assets = re.findall(r"\d{4}", all_notes)

print(f'First transaction: {earliest_datetime.strftime("%B")} {earliest_datetime.day}, {earliest_datetime.year} @ {earliest_datetime.hour%12}:{earliest_datetime.minute}')
print(f'Last transaction: {latest_datetime.strftime("%B")} {latest_datetime.day}, {latest_datetime.year} @ {latest_datetime.hour%12}:{latest_datetime.minute}')

from interfaces import KintonePortal, KTApp, QueryString
from key import DEVICE_AUTH

kintone_portal = KintonePortal('https://throughthetrees.kintone.com/k/v1/', DEVICE_AUTH, True)
devices_app = KTApp(kintone_portal, 4)
# Field translation
ASSET_TAG = "Text"
ITEM_STATUS = "Drop_down_2"
records: list = []
for i in range(0, len(sold_assets), 100):
    chunk = sold_assets[i:i + 100]
    query = QueryString(f'{ASSET_TAG} in ({', '.join([f'\"{s}\"' for s in chunk])})')
    records.extend( devices_app.get_records([ASSET_TAG, ITEM_STATUS], query) )

for record in records:
    if record[ITEM_STATUS] != 'Sold':
        print(f'Asset {record[ASSET_TAG]} marked {record[ITEM_STATUS]}!')

print(len(sold_assets))
print(len(records))

found_assets: list[str] = [record[ASSET_TAG] for record in records]

missing_assets: list[str] = [asset for asset in sold_assets if asset not in found_assets]

print(f'{len(found_assets)} found records: XX{[]}')
print(f'{len(missing_assets)} missing records: {[missing_assets]}')

from collections import Counter
duplicates = duplicates = [item for item, count in Counter(sold_assets).items() if count > 1]
print(f'{len(duplicates)} duplicates sold: {[duplicates]}')