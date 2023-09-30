from pathlib import Path
import pandas as pd
from pypdf import PdfReader
import psycopg2
import os
from datetime import datetime
import shutil
import re
from werkzeug.datastructures import MultiDict

class FileSystem:
    
    def __init__(self, finance_dir_path: Path, username: str) -> None:
        self.username = username
        self.finance_dir_path = finance_dir_path
        self.receipts_dir_path = finance_dir_path / Path("receipts") / Path(username)
        self.receipts_tmp_path = self.receipts_dir_path / Path("tmp")
        self.receipts_tmp_path.mkdir(parents=True, exist_ok=True)

    
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
                item_name = line_split[0].strip(' ^#')
                price = line_split[1].strip()
                if price.startswith("-"):
                    item_price_list[-1] = str(round(float(item_price_list[-1])+float(price), 2))
                    continue
                if item_name.startswith("PRICE REDUCED BY"):
                    continue
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
        data['payer'] = self.username

        return data
    

    def move_receipts(self):
        
        for receipt in os.listdir(str(self.receipts_tmp_path)):
            if not receipt.startswith("eReceipt"):
                continue
            
            receipt_date = receipt.split("_")[3] 
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

            pattern = re.compile(r'^\d+$')  # This regular expression matches strings that contain only digits

            numeric_files = [file for file in directory_path.glob("*/") if pattern.match(file.name)]

            directory_path = max(numeric_files)

        return directory_path


    def get_recent_receipt_date(self):
        """
        Returns the date of the most recent Everyday Rewards downloaded receipt in a given directory
        :return: datetime "%d%b%Y"
        """
        try:
            directory_path = self.iterate_largest_numeric_dir_name(self.receipts_dir_path,2)
        except ValueError as e:
            print("No existing receipts found: downloading all previous receipts")
            recent_date_str = "01Jan2000" 
        else:
            receipt_name_list = os.listdir(directory_path)
            receipt_date_list = [receipt_name.split("_")[3] for receipt_name in receipt_name_list]
            recent_date_str = max(receipt_date_list)
        return recent_date_str  
                  
    
class DatabaseConnection:
    def __init__(self, connection_details: dict):
        self.connection_details = connection_details
        self.conn = None
        self.cursor = None


    def __enter__(self):
        self.conn = psycopg2.connect(**self.connection_details)
        self.cursor = self.conn.cursor()


    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        if exc_type is not None:
            print(f"An exception of type {exc_type} occurred")

    
    def insert_df_items_into_table(self, df: pd.DataFrame, schema: str, table_name: str) -> None:
        data_values = [tuple(row) for row in df.to_numpy()]
        insert_statement = f"""INSERT INTO {schema}.{table_name} (item, price, payer) VALUES (%s, %s, %s)"""
        self.cursor.executemany(insert_statement,data_values)


    def get_empty_weightings(self, household: str, view_name: str) -> list:
        sql_query = f"""SELECT DISTINCT item FROM {household}.{view_name} WHERE persist IS NULL"""
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        empty_weightings = [row[0] for row in result]
        return empty_weightings


    def weightings_dict_to_df(self, weightings_dict: MultiDict) -> pd.DataFrame:
        keys = weightings_dict.keys()
        dataframe_dict = {}
        for item_person in keys:

            value = weightings_dict.get(item_person)
            item_person_list = item_person.split('[')
            item = item_person_list[0]
            person = item_person_list[1]

            if dataframe_dict.get(item) == None:
                dataframe_dict[item] = list()
                dataframe_dict[item].append(item)
                    
            try:
                dataframe_dict[item].append(float(value))
            except ValueError:
                dataframe_dict[item].append(True)

        for item in dataframe_dict:
            if len(dataframe_dict[item]) == 4:
                dataframe_dict[item].append(False)

        list_for_df = dataframe_dict.values()

        df = pd.DataFrame(list_for_df, columns = ['item', 'adam', 'alex', 'tyler', 'persist'])
        return df


    def insert_weightings_into_table(self, df: pd.DataFrame, household:str, table_name:str) -> None:
        data_values = [tuple(row) for row in df.to_numpy()]
        insert_statement = f"""INSERT INTO {household}.{table_name} (item, adam, alex, tyler, persist) VALUES (%s, %s, %s, %s, %s)"""
        self.cursor.executemany(insert_statement,data_values)

    def get_expenses_table(self, household:str, table_name:str) -> list: # list of dicts
        sql_query = f"""SELECT * FROM {household}.{table_name}"""
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        list_of_dict = []
        keys = [
            'id',
            'item',
            'price',
            'payer',
            'adam',
            'alex',
            'tyler'
        ]
        for row in result:
            row_dict = dict(zip(keys, row))
            list_of_dict.append(row_dict)
        return list_of_dict

    def delete_expenses_row(self, input:MultiDict, household:str, table_name:str) -> None:
        """
        Function to delete a row for expenses table after receive input id
        """
        sql_query = f"""DELETE FROM {household}.{table_name} where id = {input['id']}"""
        self.cursor.execute(sql_query)
    
    def insert_expenses_into_table(self, input: MultiDict, household:str, table_name:str) -> None:
        list_values = list(input.values())
        print(list_values)
        insert_statement = f"""INSERT INTO {household}.{table_name} (item, price, payer, adam, alex, tyler) VALUES (%s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(insert_statement,list_values)
    
    def commit_changes(self):
        self.conn.commit()


class Calculations:
    def __init__(self, finance_table: pd.DataFrame) -> None:
        self.finance_table = finance_table
        self.household_members = ['adam', 'alex', 'tyler']
        pass


    def get_spent_tally(self) -> dict:
        """method to return a dictionary outlining the running total of each person's spending across items brought from everyone in household"""
        spend_tally = {}
        self.finance_table['weighting_total'] = self.finance_table[self.household_members].sum(axis=1)
        for member in self.household_members:   
            spend_tally[member] = self.finance_table[member]/self.finance_table['weighting_total'] @ self.finance_table['price']
        return spend_tally
    

    def get_paid_tally(self) -> dict:
        """method to return a dictionary outlining the running total of how much a person has paid in items for the household"""
        paid_tally = {}
        for member in self.household_members:
            member_filter_table = self.finance_table[self.finance_table['payer'] == member]
            paid_tally[member] = member_filter_table['price'].sum()
        return paid_tally


    def get_owes_tally(self) -> dict:
        """method to return a dctionary outlining the owings tally. Positive number means people are owed that amount while negative means people need to fork up"""
        spent_tally = self.get_spent_tally()
        paid_tally = self.get_paid_tally()
        owes_tally = {}
        for member in self.household_members:
            owes_tally[member] =  spent_tally[member] - paid_tally[member]
        return owes_tally

