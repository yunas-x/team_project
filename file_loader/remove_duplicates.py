from pathlib import Path
import re

path = "C:/Users/Me/Desktop/annual"
if Path(path).exists():
    for item in Path(path).glob('*.pdf'):
        if re.match(r'.*\(\d+\).*', item.name):
            print(item)
            #item.unlink()
