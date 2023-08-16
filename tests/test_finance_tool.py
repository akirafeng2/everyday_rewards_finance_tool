from ..src.finance_tool import FileSystem
import pytest
from datetime import datetime

@pytest.fixture
def file_system(tmp_path):
    return FileSystem(tmp_path)

class TestFileSystem:

    def create_numbered_dir_in_path(self, dir, x):
        for i in range(x):
            dir_file = dir / str(i)
            dir_file.mkdir(parents=True)


    def test_iterate_largest_numeric_dir_name_one_level(self, file_system):
        first_dir = file_system.local_receipts_file_path
        self.create_numbered_dir_in_path(first_dir, 5)

        assert file_system.iterate_largest_numeric_dir_name(first_dir,1) == first_dir / "4"


    def test_iterate_largest_numeric_dir_name_two_levels(self, file_system):
        first_dir = file_system.local_receipts_file_path
        self.create_numbered_dir_in_path(first_dir, 5)
        second_dir = first_dir / "4"
        self.create_numbered_dir_in_path(second_dir, 6)

        assert file_system.iterate_largest_numeric_dir_name(first_dir, 2) == second_dir / "5"


    def test_iterate_largest_numeric_dir_name_non_numeric_files_and_dir(self, file_system):
        first_dir = file_system.local_receipts_file_path
        self.create_numbered_dir_in_path(first_dir, 8)
        non_numeric_dir_name_list = ["abc", "15x", "-99"]
        for dir_name in non_numeric_dir_name_list:
            dir_file = first_dir / dir_name
            dir_file.mkdir(parents=True) 
        with open(first_dir / '999.txt', 'w') as creating_new_txt_file:
            pass

        assert file_system.iterate_largest_numeric_dir_name(first_dir,1) == first_dir / "7"


    def test_get_recent_receipt_date_simple(self, file_system):
        directory = file_system.local_receipts_file_path / "1" / "1"
        pdfs = [
            'eReceipt_1248_Town Hall_10Jun2023__abted.txt', 
            'eReceipt_1248_Town Hall_10Jun2022__fftzg.txt', 
            'eReceipt_1638_Green Square Town Centre_03May2023__dfbev.txt', 
            'eReceipt_1638_Green Square Town Centre_08Apr2023__bbynf.txt'
            ]
        for file_name in pdfs:
            file_path = directory /file_name
            file_path.mkdir(parents=True)
        assert file_system.get_recent_receipt_date() == datetime.strptime("10Jun2023", "%d%b%Y")


    def test_get_recent_receipt_date_no_existing_receipts(self,file_system):
        assert file_system.get_recent_receipt_date() == datetime.strptime("01Jan2000", "%d%b%Y")
    





