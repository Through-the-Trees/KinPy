from typing import Any

import sys
import subprocess

import tkinter
from tkinter import simpledialog, messagebox

# TODO: Fix imports
# from kinpy import KintonePortal, KTApp
from interfaces import KintonePortal, KTApp
from utils import QueryString
from key import DEVICE_AUTH, TEST_AUTH

kintone_portal = KintonePortal('https://throughthetrees.kintone.com/k/v1/', DEVICE_AUTH, True)

# test_app = KTApp(kintone_portal, 13)
# records = test_app.get_records(fields=['Record_Status'])
# my_record = test_app.get_record(1)

devices_app = KTApp(kintone_portal, 4)

serial_command = 'powershell -NoProfile -ExecutionPolicy Bypass -Command "& { Get-CimInstance -ClassName Win32_BIOS | Select-Object SerialNumber }"'

# Run powershell command to get device serial number
result = subprocess.run(serial_command, capture_output=True, text=True, shell=True)

# Pull serial number from output
serial_number = result.stdout.strip().split()[-1] if result else ''

print("Serial Number:", serial_number)

root = tkinter.Tk()
root.withdraw() # Hide main window

# Device app field names
class Fields:
    asset_tag = 'Text'
    serial_number = 'Text_5'

asset_tag = simpledialog.askstring("Kintone Data", "Enter device asset tag:")

# Allow user to cancel
if not asset_tag:
    root.destroy()
    sys.exit()

fields = [Fields.asset_tag, Fields.serial_number]
query = QueryString(f'Text like "%{asset_tag}%"')
matching_devices: list[ dict[str, Any] ] = devices_app.get_records(fields, query)

device: dict[str, Any] = None
if not matching_devices:
    messagebox.showerror("Info", f"Asset {asset_tag} not found!")
elif len(matching_devices) != 1:
    messagebox.showerror("Info", f"Multiple devices found with asset {asset_tag}! Fix manually.")
else:
    device = matching_devices[0]

if not device:
    root.destroy()
    sys.exit()

device[Fields.serial_number] = serial_number

output = devices_app.update_record(device)

print(output)

sys.exit()

if device[Fields.serial_number] == serial_number:
    messagebox.showinfo("Info", "This record has the correct serial number.")
elif devices_app.update_record(query, 'Text_5', serial_number):
    output = f"Device Serial Number: {serial_number}"
    output = f"Original Value: {matching_devices[0]['Text_5']}\n" + output if matching_devices[0]['Text_5'] else output
    messagebox.showinfo("Serial Number Updated", output)