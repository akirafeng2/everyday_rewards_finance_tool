from ...src.backend.backend import FileSystem
import pytest
import pandas as pd
from PyPDF2 import PdfReader

@pytest.fixture
def file_system(tmp_path):
    return FileSystem(tmp_path, "bob")


@pytest.fixture
def datadir(tmp_path, request):

    return 
    


class TestFileSystem:

    def get_different_rows(self, source_df, new_df):
        """Returns just the rows from the new dataframe that differ from the source dataframe"""
        merged_df = source_df.merge(new_df, indicator=True, how='outer')
        changed_rows_df = merged_df[merged_df['_merge'] == 'right_only']
        return changed_rows_df.drop('_merge', axis=1)
    
    def add_col_to_df(self, df):
        df['payer'] = 'bob'
        df['persist'] = 'no'
        return df

    def test_receipts_to_dataframe_nothing_in_dir(self, file_system):
        df = file_system.receipts_to_dataframe()
        assert df.empty


    def test_receipts_to_dataframe_receipt_test(self, file_system):
        # Given
        test_data = [
            ['WW Frozen Mixed Berries 1kg', 11],
            ['Bega Peanut Butter Smooth 375g', 5.4],
            ['Nestle Choc Bits Dark 200g', 5],
            ['Spring Onions', 2.9]
            ]
        
        test_df = pd.DataFrame(test_data, columns = ['item_name', 'price'])

        test_df = self.add_col_to_df(test_df)

        # When
        df = file_system.receipts_to_dataframe()

        diff = self.get_different_rows(df, test_df)

        assert diff.empty




        # eReceipt_1638_Green%20Square%20Town%20Centre_14Apr2023__ujxpj.pdf
        pass


    def test_receipts_to_dataframe_receipt_column_types(self, file_system):
        # Given
        test_data = [['WW Frozen Mixed Berries 1kg', 11.00]]
        # eReceipt_1638_Green%20Square%20Town%20Centre_14Apr2023__ujxpj.pdf
        pass


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
