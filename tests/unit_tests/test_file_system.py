from ...src.backend.file_system import FileSystem
import pytest
import pandas as pd
import shutil
from pathlib import Path
import os
import numpy as np
from datetime import date
from pandas.testing import assert_frame_equal
from .common_fixtures import username, household, env


@pytest.fixture
def file_system(tmp_path, username, env, household):
    """establishes an instance of FileSystem object"""
    FS = FileSystem(tmp_path, env, username, household)
    return FS


@pytest.fixture
def test_expenses_data():
    test_data = {
        'item': ['eggs', 'bread', 'chicken'],
        'price': [3, 7, 5],
        'payer': ['tyler', 'alex', 'tyler'],
        'adam': [1, 0.5, 2], 'alex': [1, 1, 3],
        'tyler': [1, 2, 0]
    }
    test_dataframe = pd.DataFrame(data=test_data)
    return test_dataframe


class TestFileSystem:

    def copy_file_into_temp_path_location(
            self, file_name: str,
            data_directory: Path,
            tmp_path_instance: Path,
            username: str,
            env: str,
            household: str) -> None:
        """copy files in test files to the */receipt/<username>/tmp path for FileSystem to mimic download directory"""
        test_receipt = data_directory / Path(file_name)
        temp_location = tmp_path_instance / Path(env) / Path(household) / \
            Path("receipts") / Path(username) / Path("tmp")
        os.makedirs(os.path.dirname(temp_location), exist_ok=True)
        shutil.copy(test_receipt, temp_location)

    def create_numbered_dir_in_path(self, dir: Path, x: int):
        """creates numbered directories from 0 to x in the specified dir"""
        for i in range(x):
            dir_file = dir / str(i)
            dir_file.mkdir(parents=True)

    # Tests
    def test_get_receipt_names(self, file_system, shared_datadir, tmp_path, username, env, household):
        # Given
        test_files = [
            "eReceipt_1638_Green Square Town Centre_14Apr2023__ljkod.pdf",
            "eReceipt_1248_Town Hall_10Jun2023__xbkgs.pdf",
            "eReceipt_1638_Green Square Town Centre_08Apr2023__fckor.pdf"
        ]

        for file in test_files:
            self.copy_file_into_temp_path_location(file, shared_datadir, tmp_path, username, env, household)

        test_files.sort()
        # When
        output = file_system.get_receipt_names()
        output_list = [file for file in output]
        output_list.sort()
        # Then
        assert output_list == test_files

    def test_receipt_to_dataframe_receipt_column_types(self, file_system, shared_datadir, tmp_path, username, env,
                                                       household):
        # Given
        # # Setup the folder with the receipt
        test_file = "eReceipt_1638_Green Square Town Centre_14Apr2023__ljkod.pdf"
        self.copy_file_into_temp_path_location(test_file, shared_datadir, tmp_path, username, env, household)

        # When
        df = file_system.receipt_to_dataframe(test_file)

        # Then
        assert df['item'].dtype == "object"
        assert df['price'].dtype == "float64"

    def test_receipt_to_dataframe_receipt_test(self, file_system, shared_datadir, tmp_path, username, env, household):
        # Given
        # # Setup data to test against
        test_data = [
            ['WW Frozen Mixed Berries 1kg', 11],
            ['Bega Peanut Butter Smooth 375g', 5.4],
            ['Nestle Choc Bits Dark 200g', 5],
            ['Spring Onions', 2.9]
        ]

        test_df = pd.DataFrame(test_data, columns=['item', 'price'])

        # # Setup the folder with the receipt
        test_file = "eReceipt_1638_Green Square Town Centre_14Apr2023__ljkod.pdf"
        self.copy_file_into_temp_path_location(test_file, shared_datadir, tmp_path, username, env, household)

        # When
        df = file_system.receipt_to_dataframe(test_file)

        # Then
        assert_frame_equal(df, test_df)

    def test_receipt_to_dataframe_prefixed_item(self, file_system, shared_datadir, tmp_path, username, env, household):
        # Given
        # # Setup data to test against
        test_data = [
            ["Toblerone Milk Chocolate Bar 50g", 0.9],
            ["Rexona Men Roll On Invisible Dry 50ml", 5.5]
        ]

        test_df = pd.DataFrame(test_data, columns=['item', 'price'])

        # # Setup the folder with the receipt
        test_file = "eReceipt_1248_Town Hall_10Jun2023__xbkgs.pdf"
        self.copy_file_into_temp_path_location(test_file, shared_datadir, tmp_path, username, env, household)

        # When
        df = file_system.receipt_to_dataframe(test_file)

        # Then
        assert_frame_equal(df, test_df)

    def test_receipt_to_dataframe_quantity(self, file_system, shared_datadir, tmp_path, username, env, household):
        # Given
        # # Setup data to test against
        test_data = [
            ["LM Hny Rstd PistchioFzn Dsrt Mochi 6pk", 10],
            ["Danone YoPRO Plain 700g", 14.1]
        ]

        test_df = pd.DataFrame(test_data, columns=['item', 'price'])

        # # Setup the folder with the receipt
        test_file = "eReceipt_1638_Green Square Town Centre_08Apr2023__fckor.pdf"
        self.copy_file_into_temp_path_location(test_file, shared_datadir, tmp_path, username, env, household)

        # When
        df = file_system.receipt_to_dataframe(test_file)

        # Then
        assert_frame_equal(df, test_df)

    def test_receipt_to_dataframe_offer_discount(self, file_system, shared_datadir, tmp_path, username, env,
                                                 household):
        # eReceipt_1638_Green%20Square_05Jul2023__nrbqp.pdf
        # Given
        # # Setup data to test against
        test_data = np.array(['Primo Double Smoked Leg Ham 100G', 6.3])

        # # Setup the folder with the receipt
        test_file = "eReceipt_1638_Green Square_05Jul2023__nrbqp.pdf"
        self.copy_file_into_temp_path_location(test_file, shared_datadir, tmp_path, username, env, household)

        # When
        df = file_system.receipt_to_dataframe(test_file)

        # Then
        assert (df == test_data).all(1).any()

    def test_receipt_to_dataframe_markdown_price_reduction(self, file_system, shared_datadir, tmp_path, username, env,
                                                           household):
        # Given
        # # Setup data to test against
        test_data = [
            ["Ansell Handy Clean Gloves 24Pk", 6.85],
            ["Arnotts Tiny Teddy Variety 15pk 375g", 5.5],
            ["Quilton Tuffy P/Twl Triple Length 2pk", 6.00],
            ["Woolworths Mini Dbl Choc Muffin 8pk 320g", 3.31]
        ]

        test_df = pd.DataFrame(test_data, columns=['item', 'price'])

        # # Setup the folder with the receipt
        test_file = "eReceipt_1638_Green Square Town Centre_28Sep2022__enirr.pdf"
        self.copy_file_into_temp_path_location(test_file, shared_datadir, tmp_path, username, env, household)

        # When
        df = file_system.receipt_to_dataframe(test_file)

        # Then
        assert_frame_equal(df, test_df)

        # Tests for move_receipts

    def test_move_receipts_empty_tmp_folder(self, file_system, tmp_path, username, env, household):
        # Given
        temp_location = tmp_path / Path(env) / Path(household) / Path("receipts") / Path(username)
        # When
        file_system.move_receipts()
        objects_in_dir = len([x for x in temp_location.iterdir()])
        # Then
        assert objects_in_dir == 1

    def test_move_receipts_normal_function(self, file_system, shared_datadir, tmp_path, username, env, household):
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
            self.copy_file_into_temp_path_location(receipt, shared_datadir, tmp_path, username, env, household)

        # When
        file_system.move_receipts()

        # Then
        for expected_path in expected_path_list:
            assert expected_path.exists()

    def test_move_receipts_skips_non_receipt(self, file_system, shared_datadir, tmp_path, username, env, household):
        # Given
        not_a_receipt = "file-sample_150kB.pdf"
        self.copy_file_into_temp_path_location(not_a_receipt, shared_datadir, tmp_path, username, env, household)

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
        self.create_numbered_dir_in_path(first_dir, 12)

        # When
        greatest_file = file_system.iterate_largest_numeric_dir_name(first_dir, 1)

        # Then
        assert greatest_file == first_dir / "11"

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
        assert file_system.iterate_largest_numeric_dir_name(first_dir, 1) == first_dir / "7"

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
            file_path = directory / file_name
            file_path.mkdir(parents=True)

        # Then
        assert file_system.get_recent_receipt_date() == "10Jun2023"

    def test_get_recent_receipt_date_no_existing_receipts(self, file_system):
        # Given
        # When
        # Then
        assert file_system.get_recent_receipt_date() == "01Jan2000"

    def test_save_to_csv(self, file_system, test_expenses_data, tmp_path, env, household):
        # Given
        csv_file_path = tmp_path / Path(env) / Path(household) / Path("archive") / Path(f"{date.today()}.csv")
        # When
        file_system.save_to_csv(test_expenses_data)
        # Then
        assert csv_file_path.exists()
