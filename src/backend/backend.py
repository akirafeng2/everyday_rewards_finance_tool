from pathlib import Path
import pandas as pd
from pypdf import PdfReader
import psycopg2
import os
from datetime import datetime, date
import shutil
import re
from werkzeug.datastructures import MultiDict

class FileSystem:
    
    def __init__(self, finance_dir_path: Path) -> None:
        self.finance_dir_path = finance_dir_path
        self.expenses_archive = finance_dir_path / Path("archive")
        self.expenses_archive.mkdir(parents=True, exist_ok=True)
        
    def setup(self, username:str):
        self.username = username
        self.receipts_dir_path = self.finance_dir_path / Path("receipts") / Path(username)
        self.receipts_tmp_path = self.receipts_dir_path / Path("tmp")
        self.receipts_tmp_path.mkdir(parents=True, exist_ok=True)
    
    
    def get_receipt_names(self) -> iter:
        receipt_name_iterator = os.listdir(self.receipts_tmp_path)
        return receipt_name_iterator

    def receipt_to_dataframe(self, receipt:str) -> pd.DataFrame:

        item_name_list = []
        item_price_list = []
        multiple_item_indicator = False
        
        path = self.receipts_tmp_path / Path(receipt)
        string_path = str(path)
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

            pattern = re.compile(r'\b\d+\b')  # This regular expression matches strings that contain only digits

            numeric_files = [file for file in directory_path.glob("*/") if pattern.match(file.name)]
            dir_names = [path.name for path in numeric_files]
            largest_int_dir_name = max(list(map(int, dir_names)))
            directory_path = [file for file in numeric_files if file.name == str(largest_int_dir_name)][0]

        return directory_path
    

    def get_receipt_date(self, receipt_name: str) -> str:
        receipt_date_str = receipt_name.split("_")[3]
        return receipt_date_str


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
            receipt_date_list = [self.get_receipt_date(receipt_name) for receipt_name in receipt_name_list]
            recent_date_str = max(receipt_date_list)
        return recent_date_str  
    

    def save_to_csv(self, df: pd.DataFrame) -> None:
        destination_path = self.expenses_archive / Path(f"{date.today()}.csv")
        df.to_csv(destination_path, index=False)
                  
    
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
        insert_statement = f"""INSERT INTO {household}.{table_name} (item, price, payer, adam, alex, tyler) VALUES (%s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(insert_statement,list_values)

    def get_combined_expenses_as_df(self, household:str, view_name:str) -> pd.DataFrame:
        sql_query = f"""SELECT * FROM {household}.{view_name}"""
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]
        df  = pd.DataFrame(result, columns=column_names)
        return df
    
    def delete_from_table(self, household:str, table_name: str, where_cond = None) -> None:
        """
        Function to delete all rows from given table
        """
        sql_query = f"""DELETE FROM {household}.{table_name}"""
        if where_cond:
            sql_query = sql_query + f" {where_cond}"
        self.cursor.execute(sql_query)

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
            spend_tally[member] = round(self.finance_table[member]/self.finance_table['weighting_total'] @ self.finance_table['price'].astype(float),2)
        return spend_tally
    

    def get_paid_tally(self) -> dict:
        """method to return a dictionary outlining the running total of how much a person has paid in items for the household"""
        paid_tally = {}
        for member in self.household_members:
            member_filter_table = self.finance_table[self.finance_table['payer'] == member]
            paid_tally[member] = member_filter_table['price'].astype(float).sum()
        return paid_tally


    def get_owes_tally(self) -> dict:
        """method to return a dctionary outlining the owings tally. Positive number means people are owed that amount while negative means people need to fork up"""
        spent_tally = self.get_spent_tally()
        paid_tally = self.get_paid_tally()
        owes_tally = {}
        for member in self.household_members:
            owes_tally[member] =  round(spent_tally[member] - paid_tally[member],2)
        return owes_tally


class DatabaseConnection2:
    def __init__(self, connection_details: dict, env, profile_id: str):
        self.connection_details = connection_details
        self.conn = None
        self.cursor = None
        self.env = env
        self.profile_id = profile_id


    def __enter__(self):
        self.conn = psycopg2.connect(**self.connection_details)
        self.cursor = self.conn.cursor()
        search_path_execute = """
        SET search_path TO %s;
        """
        self.cursor.execute(search_path_execute, (self.env,))


    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        if exc_type is not None:
            print(f"An exception of type {exc_type} occurred")


    def insert_receipt_into_receipt_table(self, receipt_date: str, source: str) -> None:
        """Function to insert a given receipt_date, payer, and source into receipt table and also inserts the receipt_id into a the temp table new_receipt for later processing"""
        insert_statement = """
        CREATE TEMP TABLE new_receipt (new_receipt_id INT);

        WITH inserted_row AS(
            INSERT INTO receipt (receipt_date, profile_id, source) 
            VALUES (%s, %s, %s) 
            RETURNING receipt_id
        )
        INSERT INTO new_receipt (new_receipt_id)
        SELECT receipt_id FROM inserted_row;
        """ # Need to add a household_id filter aswell to the profile Query
        self.cursor.execute(insert_statement, (receipt_date, self.profile_id, source))


    def insert_into_transactions(self, item_df: pd.DataFrame) -> None:
        """Function to insert the items from the list of tuples into transactions table. Uses the new_receipt_id from the insert_receipt_into_receipt_table method and also inserts item into the item table if it doens't already exist. 
        Needs to run in the same session of insert_receipt_into_receipt_table
        Start of the function gets the item_df into right form for the executemany query"""

        item_df['item_dupe'] = item_df.loc[:, 'item']
        item_df = item_df[['item', 'item_dupe', 'price']]
        data_values = [tuple(row) for row in item_df.to_numpy()]

        insert_statement = """
        WITH ins AS(
            INSERT INTO item(item_name)
            VALUES (%s)
            ON CONFLICT (item_name) DO NOTHING
            RETURNING item_id
        )
        INSERT INTO transactions (item_id, receipt_id, price)
        VALUES ((SELECT item_id FROM ins UNION ALL SELECT item_id FROM item WHERE item_name = %s), (SELECT MAX(new_receipt_id) FROM new_receipt), %s);
        """

        self.cursor.executemany(insert_statement, data_values)


    def get_household_names(self) -> list:
        """Returns the list names within a household"""
        select_statement = """
        SELECT profile_id, nickname
        FROM profile
        WHERE household_id = (
            SELECT household_id
            FROM profile
            WHERE profile_id = %s)
        ORDER BY profile_id
        """
        self.cursor.execute(select_statement, (self.profile_id,))
        result = self.cursor.fetchall()
        household_names = [(row[0], row[1]) for row in result]
        return household_names
    
    def get_items_with_null_weightings_no_persistent_weights(self, receipt_id: int) -> list:
        """Returns a list of tuples of length two. tuple[0] is the transaction number of the item with no weighting, and tuple[1] is the item name"""
        select_statement = """
        SELECT transactions.transaction_id, item.item_name
        FROM transactions
        LEFT JOIN item ON transactions.item_id = item.item_id
        LEFT JOIN (
            SELECT *
            FROM transactions
            WHERE weighting_persist = true
            AND receipt_id in (
                SELECT receipt_id
                FROM receipt
                WHERE profile_id in (
                    SELECT profile_id
                    FROM profile
                    WHERE household_id = (
                        SELECT household_id
                        FROM PROFILE
                        WHERE profile_id = %s
                    )
                )
            )
        ) as household_persist_weight ON transactions.item_id = household_persist_weight.item_id
        WHERE transactions.weighting_id is null
        AND household_persist_weight.weighting_id is null
        AND transactions.receipt_id = %s;
        """
        self.cursor.execute(select_statement, (self.profile_id, receipt_id))
        result = self.cursor.fetchall()
        item_list = [(row[0], row[1]) for row in result]
        return item_list


    def get_items_with_null_weightings_with_persistent_weights(self, receipt_id: int) -> list:
        """Returns a list of tuples of length <household size> + 1 with weightings of each household member and item_id """
        select_statement = """
        SELECT transactions.transaction_id, item.item_name, profile.profile_id, MAX(weighting.weighting) as weighting
        FROM transactions
        LEFT JOIN item ON transactions.item_id = item.item_id
        LEFT JOIN (
            SELECT *
            FROM transactions
            WHERE weighting_persist = true
            AND receipt_id in (
                SELECT receipt_id
                FROM receipt
                WHERE profile_id in (
                    SELECT profile_id
                    FROM profile
                    WHERE household_id = (
                        SELECT household_id
                        FROM PROFILE
                        WHERE profile_id = %s
                    )
                )
            )
        ) as household_persist_weight ON transactions.item_id = household_persist_weight.item_id
        INNER JOIN weighting ON household_persist_weight.weighting_id = weighting.weighting_id
        LEFT JOIN profile ON weighting.profile_id = profile.profile_id
        WHERE transactions.weighting_id is null
        AND transactions.receipt_id = %s
        GROUP BY (transactions.transaction_id, item.item_name, profile.profile_id)
        ORDER BY transactions.transaction_id, profile.profile_id
        """
        self.cursor.execute(select_statement, (self.profile_id, receipt_id))
        result = self.cursor.fetchall()

        # convert table from long to wide in Pandas
        column_names = [desc[0] for desc in self.cursor.description]
        df  = pd.DataFrame(result, columns=column_names)
        df_wide = df.pivot(index=['transaction_id', 'item_name'], columns='profile_id', values='weighting')
        df_wide.reset_index(inplace=True)
        weighting_list = [tuple(row) for row in df_wide.to_numpy()]
        return weighting_list


    def get_new_receipts(self) -> list:
        """Returns a list of tuples. Each tuple is in the form (<receipt_id>, <receipt_date>) and represents receipts that have been added to transactions and have yet to been assigned weightings"""
        select_statement = """
        SELECT DISTINCT receipt.receipt_id, receipt.receipt_date
        FROM transactions
        LEFT JOIN (
            SELECT * 
            FROM receipt
            WHERE profile_id = %s
        ) as receipt ON transactions.receipt_id = receipt.receipt_id
        WHERE transactions.weighting_id is null 
        """
        self.cursor.execute(select_statement, (self.profile_id,))
        result = self.cursor.fetchall()
        receipt_list = [(row[0], row[1]) for row in result]
        return receipt_list
    

    def update_transaction_persistence(self, transaction_id: str) -> None:
        """Updates the transactions table to override old weighting_id for a particular item in a household"""
        update_statement = """
        UPDATE transactions
        SET weighting_persist = False
        WHERE receipt_id in (
            SELECT receipt_id
            FROM receipt
            WHERE profile_id in (
                SELECT profile_id
                FROM profile
                WHERE household_id = (
                    SELECT household_id
                    FROM PROFILE
                    WHERE profile_id = %s
                )
            )
        )
        AND item_id = (
            SELECT item_id 
            FROM transactions
            WHERE transaction_id = %s
            AND weighting_persist = True
        );

        UPDATE transactions
        SET weighting_persist = True
        WHERE transaction_id = %s;
        """
        self.cursor.execute(update_statement, (self.profile_id, transaction_id, transaction_id))

    
    def get_weighting_id(self, transaction_id: str) -> str:
        """Returns the weighting_id associated to a paticular transaction_id in the transactions table. If weighting_id does not yet exists, returns the next highest weighting_id number in the weightings table"""

        query = """
        WITH NextAvailableWeighting AS (
        SELECT
            COALESCE(MAX(weighting_id) + 1, 1) AS next_weighting_id
        FROM weighting
        )
        SELECT
        CASE
            WHEN t.weighting_id IS NOT NULL THEN t.weighting_id
            ELSE n.next_weighting_id
        END AS final_weighting_id
        FROM transactions t
        LEFT JOIN NextAvailableWeighting n ON t.weighting_id IS NULL
        WHERE t.transaction_id = %s;
        """
        self.cursor.execute(query, (transaction_id,))
        result = self.cursor.fetchone()
        weighting_id = result[0]
        return weighting_id

    
    def insert_and_update_weighting(self, profile_id: str, weight: str, transaction_id: str) -> None:
        """Inserts entry into weighting table and updates transaction table with weighting_ID"""
        weighting_id = self.get_weighting_id(transaction_id)
        query = """
        INSERT INTO weighting 
        VALUES (%s, %s, %s);

        UPDATE transactions
        SET weighting_id = %s
        WHERE transaction_id = %s;
        """
        self.cursor.execute(query, (weighting_id, profile_id, weight, weighting_id, transaction_id))


    def commit_changes(self):
        self.conn.commit()