from pathlib import Path
import pandas as pd
from pypdf import PdfReader
import os

class FileSystem:
    
    def __init__(self, finance_dir_path: Path, username: str) -> None:
        self.username = username
        self.finance_dir_path = finance_dir_path
        self.receipts_dir_path = finance_dir_path / Path("receipts") / Path(username)
        self.receipts_tmp_path = self.receipts_dir_path / Path("tmp")


    
    def receipts_to_dataframe(self) -> pd.DataFrame:

        item_name_list = []
        item_price_list = []
        multiple_item_indicator = False

        for receipt in self.receipts_tmp_path.iterdir():
            string_path = str(receipt)
            reader = PdfReader(string_path)
            page = reader.pages[0]
            receipt_text = page.extract_text()
            items_string = receipt_text.splitlines()[2]
            item_list = [items_string[i:i + 56] for i in range(0, len(items_string), 56)]

            for line in item_list:
                line_split = line.split("   ", 1)
                item_name = line_split[0].strip('^#')
                price = line_split[1].strip()
                if price.startswith("-"):
                    item_price_list[-1] = str(round(float(item_price_list[-1])+float(price), 2))
                    continue
                if item_name.startswith(" PRICE REDUCED BY"):
                    continue
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
        data['payer'] = self.username
        data['persist'] = 'no'

        return data






    
