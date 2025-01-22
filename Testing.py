import psutil
import sys
import subprocess

# Get total memory in bytes and convert to GB
total_memory_gb = psutil.virtual_memory().total / (1024 ** 3)

# Round to the nearest GB
rounded_memory_gb = round(total_memory_gb)

print(f"Total RAM: {rounded_memory_gb} GB")

import win32com.client

def get_disk_type():
    wmi = win32com.client.GetObject("winmgmts:")
    for disk in wmi.InstancesOf("Win32_DiskDrive"):
        media_type = disk.MediaType  # E.g., "Fixed hard disk media"
        if "SSD" in disk.Model or "Solid State" in media_type:
            print(f"Disk: {disk.Model} - SSD")
        else:
            print(f"Disk: {disk.Model} - HDD {media_type}")

get_disk_command = 'powershell -NoProfile -ExecutionPolicy Bypass -Command "& { Get-PhysicalDisk | Select-Object DeviceID, MediaType }"'

# Run system command to get serial number
result = subprocess.run(get_disk_command, capture_output=True, text=True, shell=True)

# Get last "word" from the command output
# serial_number = result.stdout.strip().split()[-1]

sys.exit()
# NOW BROKEN ---FIX WITH NEW RECORD DATA STRUCTURE

import tkinter as tk
from tkinter import messagebox

from Kintone import App as Kintone_App

# Function to show the popup
def show_popup(text: str=""):
    messagebox.showinfo("Popup Title", text)

# Create the main application window
# root = tk.Tk()
# root.title("Main Window")
# root.geometry("300x200")

# # Add a button to trigger the popup
# button = tk.Button(root, text="Show Popup", command=show_popup)
# button.pack(pady=20)

# Run the application
# root.mainloop()

test_app = Kintone_App('https://throughthetrees.kintone.com/k/v1/', api_token='', app_id=13)


# devices_app = Kintone_App('https://throughthetrees.kintone.com/k/v1/', api_token='', app_id=4)
# Fields
# Drop_down_1: Battery Status
# Text_7: Model
# Bay : Bay
# Drop_down_2: Item Status
# Text: Asset Tag

query = ''

records: list[ dict[str, dict[str, str] ] ] = test_app.get_records(['Text'], query)


# Get records and print info out
all_fields = []
asset_tags: list[str] = []
for record in records:
    # print('=======================')
    # print(record)
    for field, value in record.items():
        if field not in all_fields:
            all_fields.append(field)
        if field == 'Text':
            asset_tags += value

# print( sorted(records, key=lambda x: int(x)) )
print(all_fields)
print(len(records))

# Update records
# devices_app.update_records('Bay', 'Needs Parts Shelf', shelf_query)

# Create 500 ton of records
# duped_rows = [
#     {
#         'Record_Status': {'value': 'Need to Order'},
#         'Text_1': {'value': i},
#     }
#     for i in range(501)
# ]
# chunk_size = 100
# for i in range(0, len(duped_rows), 100):
#     chunk = duped_rows[i:i+100]
#     payload = {
#         "app": "13", # API Test App
#         "records": chunk
#     }
#     response: BaseHTTPResponse = http.request(
#         "POST", "https://throughthetrees.kintone.com/k/v1/records.json",
#         headers={"X-Cybozu-API-Token": "",
#             "Content-Type": "application/json"},
#         body=json.dumps(payload).encode('utf-8')
#     )
#     print(response.data)