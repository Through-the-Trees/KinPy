from typing import Any

import httpx
from key import DEVICE_AUTH, DIRECTUS_KEY
from interfaces import KintonePortal, KTApp, QueryString

from directus_sdk_py import DirectusClient

from key import DIRECTUS_KEY

client = DirectusClient(url='http://directus.throughthetrees.local/', token=DIRECTUS_KEY)

print( client.get_users() )

import sys
sys.exit()


kintone_portal = KintonePortal('https://throughthetrees.kintone.com/k/v1/', DEVICE_AUTH, True)
devices_app = KTApp(kintone_portal, 4)

ASSET_TAG = "Text"
ITEM_STATUS = "Drop_down_2"
LOCATION = "Drop_down_4"
ITEM_TYPE = "Drop_down"
DISTRIBUTION_DATE = "Date_distribution"
PRICE = "Number_0"
NOTES = "Text_area"

device_fields: dict[str, Any] = devices_app.get_form_fields()

# print(device_fields)

fields_by_type: dict[str, list] = {}

for name, properties in device_fields['properties'].items():
    # print("------")
    # print(f'"{k}": "{v["label"]}",')
    if properties["type"] not in fields_by_type:
        fields_by_type[properties["type"]] = [device_fields['properties'][name]]
    else:
        fields_by_type[properties['type']].append(device_fields['properties'][name])

for field_type, fields in fields_by_type.items():
    print(f'** Type: {field_type}')
    for field in fields:
        print(f'- Label: {field["label"]} (noLabel: {field['noLabel'] if 'noLabel' in field else ''})')
        print(f'  - Field Code: {field["code"]}')
        if 'options' in field:
            print(f'  - Options:')
            for option in field['options']:
                print(f'    - {option}')

"""

** Type: DROP_DOWN
- Label: Disk Type (noLabel: False)
  - Field Code: Drop_down_5
  - Options:
    - NVMe SSD
    - SSD
    - M.2 SSD
    - Hard Drive
    - Other
- Label: Wipe Status (noLabel: False)
  - Field Code: Drop_down_6
  - Options:
    - Wiped
    - Soft wipe
    - Not wiped
- Label: Battery Status (noLabel: False)
  - Field Code: Drop_down_1
  - Options:
    - N/A
    - Acceptable (%10 - %20 Drop)
    - New Battery Installed
    - Fail (Not Charging)
    - Missing/Damaged
    - Great (< 10% Drop)
    - Fail (> 20% Drop)
- Label: Item Status (noLabel: False)
  - Field Code: Drop_down_2
  - Options:
    - Password Needed
    - Waiting on Parts (Ordered)
    - Lost
    - Needs Inspection/Imaging
    - Ready to Distribute
    - Needs Price
    - Use for parts
    - Exchanged
    - Needs Cleaning
    - Recycled
    - Data Backup
    - Being worked on
    - In use for TtT
    - Sold
    - Waiting on Repair
    - Needs QC
    - Distributed
    - Waiting on Parts
- Label: Location (noLabel: False)
  - Field Code: Drop_down_4
  - Options:
    - Shop
    - Refurbisher
    - Out
- Label: Login @ Dropoff (noLabel: False)
  - Field Code: Drop_down_0
  - Options:
    - No
    - N/A
    - Yes
- Label: Out With (noLabel: False)
  - Field Code: Out_With
  - Options:
    - Gary Morgan
    - Jay Williams
    - Josh Oakley
    - Nate Simpson
    - Terry
    - Daniel R
    - Steve Young
    - Galen Bolin
    - Cory Nicholson
    - Daniel Sockwell
    - Dave Clark
    - Yvette
    - Henry W
    - Jim B
    - Josh Andrews
    - Stephen Shumaker
    - Gram Beasley
    - Danny Schuster
    - Libann
    - Ari
    - Dean J
- Label: Type (noLabel: False)
  - Field Code: Drop_down
  - Options:
    - Projector
    - TV
    - Tablet: Windows
    - Tablet: Android
    - Phone: Apple iPhone
    - Printer
    - Phone: Android
    - Desktop: Windows
    - Desktop Part
    - Monitor
    - Keyboard or Mouse
    - iPod / MP3 Player
    - Desktop: Apple
    - Laptop: Windows
    - Camera
    - Tablet: Apple iPad
    - Laptop: Apple
    - Desktop: Linux
    - Router
    - Phone: Other
    - Laptop: Linux
    - Game Console
    - Hot Spot
    - Laptop: Chromebook
    - Other
- Label: Bay (noLabel: False)
  - Field Code: Bay_0
  - Options:
    - Matt's Desk
    - Order Shelf
- Label: Carrier Lock Status (noLabel: False)
  - Field Code: Carrier_Lock_Status
  - Options:
    - Locked
    - Unlocked
** Type: FILE
- Label: Attachment (noLabel: False)
  - Field Code: Attachment
** Type: CHECK_BOX
- Label: Video Port Types (noLabel: False)
  - Field Code: Check_box
  - Options:
    - VGA
    - Component (RCA, etc.)
    - USB C
    - Display Port
    - DVI
    - HDMI
    - Other
- Label: Cell Network (noLabel: False)
  - Field Code: Check_box_0
  - Options:
    - T-Mobile
    - Cricket
    - Track Phone
    - Verizon
    - Sprint
    - Assurance Wireless
    - Net 10
    - U.S. Cellular
    - AT&T
    - Other
** Type: SINGLE_LINE_TEXT
- Label: Graphics Card (noLabel: False)
  - Field Code: GPU
- Label: Quality Control (noLabel: False)
  - Field Code: Quality_Control
- Label: Tester (noLabel: False)
  - Field Code: Health_Check
- Label: Order Number (Parts) (noLabel: False)
  - Field Code: Order_Number
- Label: Brand (noLabel: False)
  - Field Code: Text_6
- Label: Model (noLabel: False)
  - Field Code: Text_7
- Label: Disk Storage (noLabel: False)
  - Field Code: Text_4
- Label: Product Serial Number (noLabel: False)
  - Field Code: Text_5
- Label: Processor (noLabel: False)
  - Field Code: Text_2
- Label: RAM (Memory) (noLabel: False)
  - Field Code: Text_3
- Label: OS (noLabel: False)
  - Field Code: Text_0
- Label: Imager (noLabel: False)
  - Field Code: Imager
- Label: Asset Tag (noLabel: False)
  - Field Code: Text
- Label: IMEI Number (noLabel: False)
  - Field Code: IMEI
- Label: Year (noLabel: False)
  - Field Code: Apple_Year
** Type: MODIFIER
- Label: Updated by (noLabel: False)
  - Field Code: Updated_by
** Type: CREATED_TIME
- Label: Created datetime (noLabel: False)
  - Field Code: Created_datetime
** Type: NUMBER
- Label: Donor ID (noLabel: False)
  - Field Code: Number
- Label: Price (noLabel: False)
  - Field Code: Number_0
** Type: RECORD_NUMBER
- Label: Record number (noLabel: False)
  - Field Code: Record_number
** Type: CREATOR
- Label: Created by (noLabel: False)
  - Field Code: Created_by
** Type: STATUS
- Label: Status (noLabel: )
  - Field Code: Status
** Type: STATUS_ASSIGNEE
- Label: Assignee (noLabel: )
  - Field Code: Assignee
** Type: CATEGORY
- Label: Categories (noLabel: )
  - Field Code: Categories
** Type: SUBTABLE
- Label: Refurbishing Costs (noLabel: False)
  - Field Code: Refurbishing_Costs
** Type: DATE
- Label: Distribution Date (noLabel: False)
  - Field Code: Date_distribution
** Type: MULTI_LINE_TEXT
- Label: Notes: (noLabel: False)
  - Field Code: Text_area
- Label: Purchasing Notes (noLabel: False)
  - Field Code: Text_area_0
- Label: Record Number Search Support (noLabel: True)
  - Field Code: Text_area_1
** Type: UPDATED_TIME
- Label: Updated datetime (noLabel: False)
  - Field Code: Updated_datetime

"""