import os
from excel2table import Converter


converter = Converter(True)

for path, dirs, files in os.walk('./'):
    for file in files:
        if os.path.splitext(file)[1].lower() == '.xlsx':
            converter.convert(file)

input()
