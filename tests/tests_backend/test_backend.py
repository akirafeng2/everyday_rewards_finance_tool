from ...src.backend.backend import FileSystem
import pytest
import pandas as pd
from PyPDF2 import PdfReader
import shutil
from pathlib import Path
import os

@pytest.fixture
def username():
    """sets the username used for FileSystem object"""
    return 'bob'

@pytest.fixture
def file_system(tmp_path, username):
    """establishes an instance of FileSystem object"""
    return FileSystem(tmp_path, username)
    


class TestFileSystem:

    def get_different_rows(self, source_df: pd.DataFrame, new_df: pd.DataFrame) -> pd.DataFrame:
        """Returns just the rows from the new dataframe that differ from the source dataframe"""
        merged_df = source_df.merge(new_df, indicator=True, how='outer')
        changed_rows_df = merged_df[merged_df['_merge'] == 'right_only']
        return changed_rows_df.drop('_merge', axis=1)
    
    def add_col_to_df(self, df: pd.DataFrame, username: str) -> pd.DataFrame:
        """Adds processing columns to dataframe"""
        df['payer'] = username
        df['persist'] = 'no'
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

    def test_receipts_to_dataframe_receipt_test(self, file_system, datadir, tmp_path, username):
        # Given
        ## Setup data to test against
        test_data = [
            ['WW Frozen Mixed Berries 1kg', 11],
            ['Bega Peanut Butter Smooth 375g', 5.4],
            ['Nestle Choc Bits Dark 200g', 5],
            ['Spring Onions', 2.9]
            ]
        
        test_df = pd.DataFrame(test_data, columns = ['item_name', 'price'])

        test_df = self.add_col_to_df(test_df, username)

        ## Setup the folder with the receipt
        test_file = "eReceipt_1638_Green Square Town Centre_14Apr2023__ljkod.pdf"
        self.copy_file_into_temp_path_location(test_file, datadir, tmp_path, username)

        # When
        df = file_system.receipts_to_dataframe()

        diff = self.get_different_rows(df, test_df)

        # Then
        assert diff.empty


    def test_receipts_to_dataframe_receipt_column_types(self, file_system, datadir, tmp_path, username):
        # Given
        ## Setup the folder with the receipt
        test_file = "eReceipt_1638_Green Square Town Centre_14Apr2023__ljkod.pdf"
        self.copy_file_into_temp_path_location(test_file, datadir, tmp_path, username)

        # When
        df = file_system.receipts_to_dataframe()

        # Then
        assert df['item_name'].dtype == "object"
        assert df['price'].dtype == "float64"




    def test_receipts_to_dataframe_prefixed_item(self, file_system):
        # eReceipt_1248_Town%20Hall_10Jun2023__wtjzz.pdf
        pass
    
    
    def test_receipts_to_dataframe_quantity(self, file_system):
        # eReceipt_1638_Green%20Square%20Town%20Centre_08Apr2023__naaxs.pdf
        pass


    def test_receipts_to_dataframe_offer_discount(self, file_system):
        # eReceipt_1638_Green%20Square_05Jul2023__nrbqp.pdf
        pass


    # the function to read receipts to text and to read text to dataframe should be separate
