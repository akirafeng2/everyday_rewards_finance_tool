from ...src.backend import backend
import pytest
import pandas as pd
from pypdf import PdfReader
import shutil
from pathlib import Path
import os
import numpy as np
from datetime import datetime
from unittest.mock import patch, Mock
from werkzeug.datastructures import MultiDict


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


@pytest.fixture
def test_expenses_data():
    test_data = {'item': ['eggs', 'bread', 'chicken'], 'price': [3, 7, 5], 'payer': ['tyler', 'alex', 'tyler'], 'adam': [1, 0.5, 2], 'alex': [1, 1, 3], 'tyler': [1, 2, 0]}
    test_dataframe = pd.DataFrame(data=test_data)    
    return test_dataframe


@pytest.fixture
def calculations(test_expenses_data):
    return backend.Calculations(test_expenses_data)

def get_different_rows(source_df: pd.DataFrame, new_df: pd.DataFrame) -> pd.DataFrame:
    """Returns just the rows from the new dataframe that differ from the source dataframe"""
    merged_df = source_df.merge(new_df, indicator=True, how='outer')
    changed_rows_df = merged_df[merged_df['_merge'] == 'right_only']
    return changed_rows_df.drop('_merge', axis=1)    


class TestFileSystem:
    
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

    def create_numbered_dir_in_path(self, dir: Path, x: int):
        """creates numbered directories from 0 to x in the specified dir"""
        for i in range(x):
            dir_file = dir / str(i)
            dir_file.mkdir(parents=True)

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

        diff = get_different_rows(df, test_df)

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

        diff = get_different_rows(df, test_df)        

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

        diff = get_different_rows(df, test_df)        

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

        diff = get_different_rows(df, test_df)        

        # Then
        assert diff.empty

        # Tests for move_receipts
    
    
    def test_move_receipts_empty_tmp_folder(self, file_system, tmp_path, username):
        # Given
        temp_location = tmp_path / Path("receipts") / Path(username)
        # When
        file_system.move_receipts()
        objects_in_dir = len([x for x in temp_location.iterdir()])
        # Then
        assert objects_in_dir == 1

    
    def test_move_receipts_normal_function(self, file_system, datadir, tmp_path, username):
        # Given
        receipt_list = [
            "eReceipt_1248_Town Hall_10Jun2023__xbkgs.pdf",
            "eReceipt_1638_Green Square Town Centre_08Apr2023__fckor.pdf",
            "eReceipt_1638_Green Square Town Centre_14Apr2023__ljkod.pdf",
            "eReceipt_1638_Green Square_05Jul2023__nrbqp.pdf",
            "eReceipt_1638_Green Square Town Centre_08Apr2022__dfcxc.pdf"
            ]
        
        expected_path_list = [
            file_system.receipts_dir_path / Path("2023/6/eReceipt_1248_Town Hall_10Jun2023__xbkgs.pdf"),
            file_system.receipts_dir_path / Path("2023/4/eReceipt_1638_Green Square Town Centre_08Apr2023__fckor.pdf"),
            file_system.receipts_dir_path / Path("2023/4/eReceipt_1638_Green Square Town Centre_14Apr2023__ljkod.pdf"),
            file_system.receipts_dir_path / Path("2023/7/eReceipt_1638_Green Square_05Jul2023__nrbqp.pdf"),
            file_system.receipts_dir_path / Path("2022/4/eReceipt_1638_Green Square Town Centre_08Apr2022__dfcxc.pdf"),
        ]
        for receipt in receipt_list:
            self.copy_file_into_temp_path_location(receipt, datadir, tmp_path, username)

        # When
        file_system.move_receipts()

        # Then
        for expected_path in expected_path_list:
            assert expected_path.exists()
    

    def test_move_receipts_skips_non_receipt(self, file_system, datadir, tmp_path, username):
        # Given
        not_a_receipt = "file-sample_150kB.pdf"
        self.copy_file_into_temp_path_location(not_a_receipt, datadir, tmp_path, username)

        # When
        file_system.move_receipts()
        objects_in_dir = len([x for x in file_system.receipts_dir_path.iterdir()])
        # Then
        assert objects_in_dir == 1


    def test_delete_tmp(self, file_system):
        # Given

        # When
        file_system.delete_tmp()

        # Then
        assert not file_system.receipts_tmp_path.exists()


    def test_iterate_largest_numeric_dir_name_one_level(self, file_system):
        # Given
        first_dir = file_system.receipts_dir_path
        self.create_numbered_dir_in_path(first_dir, 5)

        # When 
        greatest_file = file_system.iterate_largest_numeric_dir_name(first_dir, 1)

        # Then 
        assert greatest_file == first_dir / "4"

    def test_iterate_largest_numeric_dir_name_two_levels(self, file_system):
        # Given
        first_dir = file_system.receipts_dir_path

        # When
        self.create_numbered_dir_in_path(first_dir, 5)
        second_dir = first_dir / "4"
        self.create_numbered_dir_in_path(second_dir, 6)

        

        # Then
        assert file_system.iterate_largest_numeric_dir_name(first_dir, 2) == second_dir / "5"


    def test_iterate_largest_numeric_dir_name_non_numeric_files_and_dir(self, file_system):
        # Given
        first_dir = file_system.receipts_dir_path

        # When
        self.create_numbered_dir_in_path(first_dir, 8)
        non_numeric_dir_name_list = ["abc", "15x", "-99"]
        for dir_name in non_numeric_dir_name_list:
            dir_file = first_dir / dir_name
            dir_file.mkdir(parents=True) 
        with open(first_dir / '999.txt', 'w') as creating_new_txt_file:
            pass
        
        # Then
        assert file_system.iterate_largest_numeric_dir_name(first_dir,1) == first_dir / "7"


    def test_get_recent_receipt_date_simple(self, file_system):
        # Given
        directory = file_system.receipts_dir_path / "1" / "1"
        # When
        pdfs = [
            'eReceipt_1248_Town Hall_10Jun2023__abted.txt', 
            'eReceipt_1248_Town Hall_10Jun2022__fftzg.txt', 
            'eReceipt_1638_Green Square Town Centre_03May2023__dfbev.txt', 
            'eReceipt_1638_Green Square Town Centre_08Apr2023__bbynf.txt'
            ]
        for file_name in pdfs:
            file_path = directory /file_name
            file_path.mkdir(parents=True)

        # Then
        assert file_system.get_recent_receipt_date() == "10Jun2023"


    def test_get_recent_receipt_date_no_existing_receipts(self,file_system):
        # Given
        # When
        # Then
        assert file_system.get_recent_receipt_date() == "01Jan2000"


class TestDatabaseConnection:

    # tests
    @patch('psycopg2.connect')
    def test_insert_df_items_into_table_dataframe_to_list(self, mock_connect, database_connection, receipt_dataframe, username):
        # Given
        ## setting up test arguements
        test_list_input = [
            ("Toblerone Milk Chocolate Bar 50g", 0.9, username),
            ("Rexona Men Roll On Invisible Dry 50ml", 5.5, username)
            ]
        test_query_input = f"""INSERT INTO test_schema.test_table (item, price, payer) VALUES (%s, %s, %s)"""


        ## setting up the mock
        mock_exe = mock_connect.return_value.cursor.return_value.executemany
        scratch = mock_exe.return_value
        # When
        with database_connection:
            print("hi")
            database_connection.insert_df_items_into_table(receipt_dataframe, 'test_schema', 'test_table')
        
        # Then
        mock_exe.assert_called_once_with(test_query_input, test_list_input)


    def test_weightings_tuples_to_df_persist_on(self, database_connection):
        # Given
        ## setting up examples weightings_tuples
        test_weightings_dict = MultiDict([
            ('eggs[adam]', '0.01'), 
            ('eggs[alex]', '0.02'), 
            ('eggs[tyler]', '0.03'),
            ('eggs[persist]', 'on')
        ])

        test_weightings_data = [
            ["eggs", 0.01, 0.02, 0.03, True]
        ]

        test_df = pd.DataFrame(test_weightings_data, columns = ['item', 'adam', 'alex', 'tyler', 'persist'])

        # When
        df = database_connection.weightings_dict_to_df(test_weightings_dict)

        diff = get_different_rows(df, test_df)        

        # Then
        assert diff.empty


    def test_weightings_tuples_to_df_no_persist(self, database_connection):
        # Given
        ## setting up examples weightings_tuples
        test_weightings_dict = MultiDict([
            ('eggs[adam]', '0.01'), 
            ('eggs[alex]', '0.02'), 
            ('eggs[tyler]', '0.03')
        ])

        test_weightings_data = [
            ["eggs", 0.01, 0.02, 0.03, False]
        ]

        test_df = pd.DataFrame(test_weightings_data, columns = ['item', 'adam', 'alex', 'tyler', 'persist'])

        # When
        df = database_connection.weightings_dict_to_df(test_weightings_dict)

        diff = get_different_rows(df, test_df)        

        # Then
        assert diff.empty


    @patch("psycopg2.connect")
    def test_get_expenses_table(self, mock_connect, database_connection):
        # Given
        mock_connect.return_value.cursor.return_value.execute.return_value = "hi"
        mock_connect.return_value.cursor.return_value.fetchall.return_value = [
            (1, 'rent', 50, 'alex', 14.1, 13.02, 15), 
            (2, 'gyg', 41, 'adam', 1, 1, 1), 
            (3, 'ice cream', 13, 'tyler', 0, 1, 0), 
            ]
        
        expected_list = [
            {
                'id': 1,
                'item': 'rent',
                'price': 50,
                'payer': 'alex',
                'adam': 14.1,
                'alex': 13.02,
                'tyler': 15
            },
            {
                'id': 2,
                'item': 'gyg',
                'price': 41,
                'payer': 'adam',
                'adam': 1,
                'alex': 1,
                'tyler': 1
            },
            {
                'id': 3,
                'item': 'ice cream',
                'price': 13,
                'payer': 'tyler',
                'adam': 0,
                'alex': 1,
                'tyler': 0
            },
        ]
        # When
        with database_connection:
            data = database_connection.get_expenses_table('bob', 'bob')
        # Then
        assert data == expected_list


class TestCalculations:

    def test_get_spent_tally(self, calculations):
        # Given
        expected_data = {'adam': 4, 'alex': 6, 'tyler': 5}
        # When
        spent_tally = calculations.get_spent_tally()
        # Then
        assert spent_tally == expected_data


    def test_get_paid_tally(self, calculations):
        # Given
        expected_data = {'adam': 0, 'alex': 7, 'tyler': 8}
        # When
        paid_tally = calculations.get_paid_tally()
        # Then
        assert paid_tally == expected_data


    def test_get_owes_tally(self, calculations):
        # Given
        expected_data = {'adam': 4, 'alex': -1, 'tyler': -3}
        # When
        owes_tally = calculations.get_owes_tally()
        # Then
        assert owes_tally == expected_data
