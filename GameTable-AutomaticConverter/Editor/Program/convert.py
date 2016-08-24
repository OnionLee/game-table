import sys
import os
from excel2table import Converter

# Need python ver 3.5 or later
REQUIRE_VERSION = (3, 5)

# File path
EXCEL_PATH = '../Excel/'
EDITOR_JSON_PATH  = '../Json/'
RESOURCES_JSON_PATH = '../../../TableSystem/Resources/JsonTable/'

# Get current python version
current_version = sys.version_info

# Check version
if current_version < REQUIRE_VERSION:
    print('You Need Python 3.5 or later')
    input()
    sys.exit()

# Editor ver & Resources ver 
editor_converter = Converter(True, EDITOR_JSON_PATH)
resources_converter = Converter(True, RESOURCES_JSON_PATH)

# Find Excel File
for path, dirs, files in os.walk(EXCEL_PATH):
    for file in files:
        if file[0] is "~":
            continue

        # Convert
        if os.path.splitext(file)[1].lower() == '.xlsx':
            editor_converter.convert(EXCEL_PATH + file)
            resources_converter.convert(EXCEL_PATH + file)
