from ...src.backend import backend
import pytest
import pandas as pd
from pypdf import PdfReader
import shutil
from pathlib import Path
import os
import numpy as np
from unittest.mock import patch, Mock


CONNECTION_DETAILS = {
    "dbname":"finance_db",
    "user":"root",
    "password":"root",
    "host":"localhost",
    "port":"5432"
}

@pytest.fixture
def username():
    """sets the username used for FileSystem object"""
    return 'bob'

@pytest.fixture
def file_system(tmp_path, username):
    """establishes an instance of FileSystem object"""
    return backend.FileSystem(tmp_path, username)


@pytest.fixture
def database_connection():
    return backend.DatabaseConnection(CONNECTION_DETAILS)


@pytest.fixture
def receipt_dataframe(username):
    test_data = [
        ["Toblerone Milk Chocolate Bar 50g", 0.9],
        ["Rexona Men Roll On Invisible Dry 50ml", 5.5]
    ]

    test_df = pd.DataFrame(test_data, columns = ['item', 'price'])

    test_df['payer'] = username

    return test_df

    


class TestFileSystem:

    def get_different_rows(self, source_df: pd.DataFrame, new_df: pd.DataFrame) -> pd.DataFrame:
        """Returns just the rows from the new dataframe that differ from the source dataframe"""
        merged_df = source_df.merge(new_df, indicator=True, how='outer')
        changed_rows_df = merged_df[merged_df['_merge'] == 'right_only']
        return changed_rows_df.drop('_merge', axis=1)
    
    def add_col_to_df(self, df: pd.DataFrame, username: str) -> pd.DataFrame:
        """Adds processing columns to dataframe"""
        df['payer'] = username
        return df
    
    def copy_file_into_temp_path_location(self, file_name: str, data_directory: Path, tmp_path_instance: Path, username: str) -> None:
        """copy files in test files to the */receipt/<username>/tmp path for FileSystem to mimic download directory"""
        test_receipt = data_directory / Path(file_name)
        temp_location = tmp_path_instance / Path("receipts") / Path(username) / Path("tmp")
        os.makedirs(os.path.dirname(temp_location), exist_ok=True)
        shutil.copy(test_receipt, temp_location)

    # Tests
    def test_receipts_to_dataframe_nothing_in_dir(self, file_system):
        
        df = file_system.receipts_to_dataframe()
        assert df.empty


    def test_receipts_to_dataframe_receipt_column_types(self, file_system, datadir, tmp_path, username):
        # Given        
        ## Setup the folder with the receipt
        test_file = "eReceipt_1638_Green Square Town Centre_14Apr2023__ljkod.pdf"
        self.copy_file_into_temp_path_location(test_file, datadir, tmp_path, username)

        # When
        df = file_system.receipts_to_dataframe()

        # Then
        assert df['item'].dtype == "object"
        assert df['price'].dtype == "float64"


    def test_receipts_to_dataframe_receipt_test(self, file_system, datadir, tmp_path, username):
        # Given
        ## Setup data to test against
        test_data = [
            ['WW Frozen Mixed Berries 1kg', 11],
            ['Bega Peanut Butter Smooth 375g', 5.4],
            ['Nestle Choc Bits Dark 200g', 5],
            ['Spring Onions', 2.9]
            ]
        
        test_df = pd.DataFrame(test_data, columns = ['item', 'price'])

        test_df = self.add_col_to_df(test_df, username)

        ## Setup the folder with the receipt
        test_file = "eReceipt_1638_Green Square Town Centre_14Apr2023__ljkod.pdf"
        self.copy_file_into_temp_path_location(test_file, datadir, tmp_path, username)

        # When
        df = file_system.receipts_to_dataframe()

        diff = self.get_different_rows(df, test_df)

        # Then
        assert diff.empty


    def test_receipts_to_dataframe_prefixed_item(self, file_system, datadir, tmp_path, username):
        # Given
        ## Setup data to test against
        test_data = [
            ["Toblerone Milk Chocolate Bar 50g", 0.9],
            ["Rexona Men Roll On Invisible Dry 50ml", 5.5]
        ]

        test_df = pd.DataFrame(test_data, columns = ['item', 'price'])

        test_df = self.add_col_to_df(test_df, username)

        ## Setup the folder with the receipt
        test_file = "eReceipt_1248_Town Hall_10Jun2023__xbkgs.pdf"
        self.copy_file_into_temp_path_location(test_file, datadir, tmp_path, username)

        # When
        df = file_system.receipts_to_dataframe()

        diff = self.get_different_rows(df, test_df)        

        # Then
        assert diff.empty
    
    
    def test_receipts_to_dataframe_quantity(self, file_system, datadir, tmp_path, username):
        # Given
        ## Setup data to test against
        test_data = [
            ["LM Hny Rstd PistchioFzn Dsrt Mochi 6pk", 10],
            ["Danone YoPRO Plain 700g", 14.1]
        ]

        test_df = pd.DataFrame(test_data, columns = ['item', 'price'])

        test_df = self.add_col_to_df(test_df, username)

        ## Setup the folder with the receipt
        test_file = "eReceipt_1638_Green Square Town Centre_08Apr2023__fckor.pdf"
        self.copy_file_into_temp_path_location(test_file, datadir, tmp_path, username)

        # When
        df = file_system.receipts_to_dataframe()

        diff = self.get_different_rows(df, test_df)        

        # Then
        assert diff.empty


    def test_receipts_to_dataframe_offer_discount(self, file_system, datadir, tmp_path, username):
        # eReceipt_1638_Green%20Square_05Jul2023__nrbqp.pdf
        # Given
        ## Setup data to test against
        test_data = np.array(['Primo Double Smoked Leg Ham 100G', 6.3, username])

        ## Setup the folder with the receipt
        test_file = "eReceipt_1638_Green Square_05Jul2023__nrbqp.pdf"
        self.copy_file_into_temp_path_location(test_file, datadir, tmp_path, username)

        # When
        df = file_system.receipts_to_dataframe()

        # Then
        assert (df==test_data).all(1).any()


    def test_receipts_to_dataframe_markdown_price_reduction(self, file_system, datadir, tmp_path, username):
        # Given
        ## Setup data to test against
        test_data = [
            ["Ansell Handy Clean Gloves 24Pk", 6.85],
            ["Arnotts Tiny Teddy Variety 15pk 375g", 5.5],
            ["Quilton Tuffy P/Twl Triple Length 2pk", 6.00],
            ["Woolworths Mini Dbl Choc Muffin 8pk 320g", 3.31]
        ]

        test_df = pd.DataFrame(test_data, columns = ['item', 'price'])

        test_df = self.add_col_to_df(test_df, username)

        ## Setup the folder with the receipt
        test_file = "eReceipt_1638_Green Square Town Centre_28Sep2022__enirr.pdf"
        self.copy_file_into_temp_path_location(test_file, datadir, tmp_path, username)

        # When
        df = file_system.receipts_to_dataframe()

        diff = self.get_different_rows(df, test_df)        

        # Then
        assert diff.empty

        # Tests for move_receipts
    def test_move_receipts_empty_tmp_folder(self, file_system, tmp_path, username):
        # Given
        temp_location = tmp_path / Path("receipts") / Path(username)
        os.makedirs(os.path.dirname(temp_location), exist_ok=True)
        # When
        file_system.move_receipts()
        objects_in_dir = len([x for x in temp_location.iterdir()])
        # Then
        assert objects_in_dir == 1



class TestDatabaseConnection:

    # tests
    @patch('psycopg2.connect')
    def test_insert_df_items_into_table_dataframe_to_list(self, mock_connect,database_connection, receipt_dataframe, username):
        # Given
        ## setting up test arguements
        test_list_input = [
            ("Toblerone Milk Chocolate Bar 50g", 0.9, username),
            ("Rexona Men Roll On Invisible Dry 50ml", 5.5, username)
            ]
        test_query_input = f"""INSERT INTO test_table (item, price, payer) VALUES (%s, %s, %s)"""


        ## setting up the mock
        mock_exe = mock_connect.return_value.cursor.return_value.executemany
        scratch = mock_exe.return_value
        # When
        with database_connection:
            print("hi")
            database_connection.insert_df_items_into_table(receipt_dataframe,'test_table')
        
        # Then
        mock_exe.assert_called_once_with(test_query_input, test_list_input)
