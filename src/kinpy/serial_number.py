from typing import Any

from KinPy_old import App as Kintone_App

import sys
import subprocess

import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

devices_app = Kintone_App(
    'https://throughthetrees.kintone.com/k/v1/',
    api_token=DEVICE_APP_KEY,
    app_id=4
)

serial_command = 'powershell -NoProfile -ExecutionPolicy Bypass -Command "& { Get-CimInstance -ClassName Win32_BIOS | Select-Object SerialNumber }"'

# Run powershell command to get serial number
result = subprocess.run(serial_command, capture_output=True, text=True, shell=True)

# Get last "word" from the command output
serial_number = result.stdout.strip().split()[-1]

print("Serial Number:", serial_number)

root = tk.Tk()
root.withdraw()

# "Text" is the internal name of the asset tag field
# "Text_5" = serial number
asset_tag = simpledialog.askstring("Kintone Data", "Enter device asset tag:")
query = f'Text like "%{asset_tag}%"' 

matching_devices: list[ dict[str, Any] ] = devices_app.get_records(['Text', 'Text_5'], query)

if not asset_tag:
    sys.exit()

if not matching_devices or len(matching_devices) < 1:
    messagebox.showerror("Info", f"Asset {asset_tag} not found!")
elif matching_devices[0]['Text_5'] == serial_number:
    messagebox.showinfo("Info", "This record has the correct serial number.")
elif devices_app.update_record(query, 'Text_5', serial_number):
    output = f"Device Serial Number: {serial_number}"
    output = f"Original Value: {matching_devices[0]['Text_5']}\n" + output if matching_devices[0]['Text_5'] else output
    messagebox.showinfo("Serial Number Updated", output)