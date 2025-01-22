from cx_Freeze import setup, Executable
from cx_Freeze import hooks
import urllib3

# Ensure urllib3 submodules are included
# hooks.Module.load_hook("urllib3")
# hooks.load_package("urllib3")

# Define the build options
build_options = {
    "packages": ["urllib3"],
    "excludes": [],
    "include_files": []  # Add any data files if required
}

# Define the executable
executables = [
    Executable("SerialNumberWin.py", target_name="SerialNumber.exe", base="Win32GUI", icon="icon.ico")
]

# Setup script
setup(
    name="Kintone Serial Number Entry",
    version="1.0",
    description="Kintone Serial Number Entry",
    options={"build_exe": build_options},
    executables=executables
)