import pandas as pd
from PyPDF2 import PdfReader
import os

from tabulate import tabulate

# out of program stuff to be automated
year = "2023"
month = "04"

item_name_list = []
item_price_list = []
multiple_item_indicator = False

directory = rf'C:\Users\Alex Feng\Documents\Bitches_Finance\{year}\{month}\receipts'

for file in os.scandir(directory):
    reader = PdfReader(file.path)
    page = reader.pages[0]
    receipt_text = page.extract_text()
    items_string = receipt_text.splitlines()[2]
    item_list = [items_string[i:i + 56] for i in range(0, len(items_string), 56)]

    for line in item_list:
        line_split = line.split("  ", 1)
        item_name = line_split[0].strip('^#')
        price = line_split[1].strip()
        if not multiple_item_indicator:
            item_name_list.append(item_name)
            if price == "":
                multiple_item_indicator = True
            else:
                item_price_list.append(price)
        elif multiple_item_indicator:
            item_price_list.append(price)
            multiple_item_indicator = False

data = pd.DataFrame({"item": item_name_list, 'price': item_price_list})
print(tabulate(data, headers='keys', tablefmt='psql'))


"""
Next Steps
1) create a weighting file
2) dont connect to google drive, do it last and just copy the whole folder in. keep the weighting stuff local
"""