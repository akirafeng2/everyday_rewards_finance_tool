from ...src.backend.backend import FileSystem
import pytest
import pandas as pd

@pytest.fixture
def file_system(tmp_path):
    return FileSystem(tmp_path, "bob")



class TestFileSystem:

    def test_receipts_to_dataframe_nothing_in_dir(self, file_system):
        df = file_system.receipts_to_dataframe()
        assert df.empty


    def test_receipts_to_dataframe_receipt_test(self, file_system):
        pass


    def test_receipts_to_dataframe_non_receipt_file(self, file_system):
            pass