import sys
import os
from excel2table import Converter

# Need python ver 3.5 or later
REQUIRE_VERSION = (3, 5)

# File path
EXCEL_PATH = '../Excel/'
<<<<<<< HEAD:GameTable-AutomaticConverter/Editor/Program/convert.py
EDITOR_JSON_PATH  = '../Json/'
RESOURCES_JSON_PATH = '../../../Resources/JsonTable/'
=======
JSON_PATH = '../../Sample/Resources/Table/'
>>>>>>> 78c259f25739534086cc1c234cb0e003b07ac9af:GameTable-Unity/Assets/GameTable-Converter/Converter/convert.py

# Get current python version
current_version = sys.version_info

# Check version
if current_version < REQUIRE_VERSION:
    print('You Need Python 3.5 or later')
    input()
    sys.exit()

converter = Converter(True, JSON_PATH)
    
for path, dirs, files in os.walk(EXCEL_PATH):
    for file in files:
        if file[0] is "~":
            continue
        
        if os.path.splitext(file)[1].lower() == '.xlsx':
            converter.convert(EXCEL_PATH + file)
            
            
#Assets\TableSystem\Resources\JsonTable
