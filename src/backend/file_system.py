from pathlib import Path
import pandas as pd
from pypdf import PdfReader
import os
from datetime import datetime, date
import shutil
import re


class FileSystem:
    def __init__(self, finance_dir_path: Path, env: str, username: str, household: str) -> None:
        self.finance_dir_path = finance_dir_path / Path(env) / Path(household)

        # Establish and create archive path
        self.expenses_archive = self.finance_dir_path / Path("archive")
        self.expenses_archive.mkdir(parents=True, exist_ok=True)

        # Establish and create a user receipt path
        self.receipts_dir_path = self.finance_dir_path / Path("receipts") / Path(username)
        self.receipts_tmp_path = self.receipts_dir_path / Path("tmp")
        self.receipts_tmp_path.mkdir(parents=True, exist_ok=True)

    def get_receipt_names(self) -> iter:
        receipt_name_iterator = os.listdir(self.receipts_tmp_path)
        return receipt_name_iterator

    def receipt_to_dataframe(self, receipt: str) -> pd.DataFrame:

        item_name_list = []
        item_price_list = []
        multiple_item_indicator = False

        path = self.receipts_tmp_path / Path(receipt)
        string_path = str(path)
        reader = PdfReader(string_path)
        page = reader.pages[0]
        receipt_text = page.extract_text()
        print(receipt_text)

        # get items on the 3rd line of the receipt
        items_string = receipt_text.splitlines()[2]

        # split items into list - each item and it's price is 56 characters long
        item_list = [items_string[i:i + 56] for i in range(0, len(items_string), 56)]

        # collecting item name and price
        for line in item_list:
            # Sample line string -> '#Cenovis Tablts Vit C Sgarls500mg300pk             18.50'
            line_split = line.split("   ", 1)
            item_name = line_split[0].strip(' ^#')  # all lines starts with one a combination of ' ^#'
            price = line_split[1].strip()  # remove extra spaces

            # handling discounts applied on the followng line
            if price.startswith("-"):
                item_price_list[-1] = str(round(float(item_price_list[-1]) + float(price), 2))
                continue

            # skipping markdowns info - Markdown have second line announcing discount amount to reduced price
            if item_name.startswith("PRICE REDUCED BY"):
                continue

            # handle cases where discounts have one line for the original price, and another for the discount
            if not multiple_item_indicator:
                item_name_list.append(item_name)
                if price == "":
                    multiple_item_indicator = True
                else:
                    item_price_list.append(float(price))
            elif multiple_item_indicator:
                item_price_list.append(float(price))
                multiple_item_indicator = False

        data = pd.DataFrame({"item": item_name_list, 'price': item_price_list})
        return data

    def move_receipts(self):
        for receipt in os.listdir(str(self.receipts_tmp_path)):
            if not receipt.startswith("eReceipt"):
                continue

            receipt_date = receipt.split("_")[3]  # example: 'eReceipt_1638_Green Square_07Aug2023__fooaa'
            date_format = "%d%b%Y"
            receipt_datetime = datetime.strptime(receipt_date, date_format)
            month = str(receipt_datetime.month)
            year = str(receipt_datetime.year)

            destination_path = self.receipts_dir_path / Path(f"{year}/{month}")
            receipt_path = self.receipts_tmp_path / receipt

            destination_path.mkdir(parents=True, exist_ok=True)
            shutil.move(str(receipt_path), str(destination_path))

    def delete_tmp(self):
        self.receipts_tmp_path.rmdir()

    def iterate_largest_numeric_dir_name(self, directory_path: Path, iterate_number: int):
        """
        Returns the Path of the directory that has largest numeric value for its name in the given directory
        :param directory_path: Path
        :param iterate_number: int
        :return: Path
        """

        for x in range(iterate_number):

            pattern = re.compile(r'\b\d+\b')  # This regular expression matches strings that contain only digits

            numeric_files = [file for file in directory_path.glob("*/") if pattern.match(file.name)]
            dir_names = [path.name for path in numeric_files]
            largest_int_dir_name = max(list(map(int, dir_names)))
            directory_path = [file for file in numeric_files if file.name == str(largest_int_dir_name)][0]

        return directory_path

    def get_receipt_date(self, receipt_name: str) -> str:
        """Takes the name of a ER receipt and returns the date of the receipt"""
        receipt_date_str = receipt_name.split("_")[3]
        return receipt_date_str

    def get_recent_receipt_date(self):
        """
        Returns the date of the most recent Everyday Rewards downloaded receipt in a given directory
        :return: datetime "%d%b%Y"
        """
        try:
            directory_path = self.iterate_largest_numeric_dir_name(self.receipts_dir_path, 2)
        except ValueError:
            print("No existing receipts found: downloading all previous receipts")
            recent_date_str = "01Jan2000"
        else:
            receipt_name_list = os.listdir(directory_path)
            receipt_date_list = [self.get_receipt_date(receipt_name) for receipt_name in receipt_name_list]
            recent_date_str = max(receipt_date_list)
        return recent_date_str

    def save_to_csv(self, df: pd.DataFrame) -> None:
        destination_path = self.expenses_archive / Path(f"{date.today()}.csv")
        df.to_csv(destination_path, index=False)
