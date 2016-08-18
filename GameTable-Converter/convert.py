import os
from excel2table import Converter

EXPORT_PATH = './'

converter = Converter(True, EXPORT_PATH)

for path, dirs, files in os.walk('./'):
    for file in files:
        # ignore temporary excel file
        if '~$' in str(file):
            continue

        if os.path.splitext(file)[1].lower() == '.xlsx':
            converter.convert(file)

input()
