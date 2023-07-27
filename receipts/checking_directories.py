from datetime import datetime
import os


def get_recent_receipt_date(directory_path):
    """
    Returns the date of the most recent Everyday Rewards downloaded receipt in a given directory
    :param directory_path: str
    :return: datetime "%d%b%Y"
    """
    receipt_name_list = os.listdir(directory_path)
    receipt_date_list = [receipt_name.split("_")[3] for receipt_name in receipt_name_list]
    recent_date_str = max(receipt_date_list)
    date_format = "%d%b%Y"
    recent_date = datetime.strptime(recent_date_str, date_format)
    return recent_date


def largest_numeric_dir_name(directory_path):
    """
    Returns the file or directory in a given directory that has the largest numeric value for its name
    :param directory_path: str
    :return: str
    """
    max_dir_name = None

    # Iterate over the directories in the specified path
    for dir_name in os.listdir(directory_path):

        try:
            dir_name = int(dir_name)
        except ValueError:
            continue

        if max_dir_name is None or dir_name > max_dir_name:
            max_dir_name = dir_name

    return str(max_dir_name)
