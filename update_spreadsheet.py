from receipts.receipt_scraper import receipt_scraper
from datetime import datetime
from receipts.checking_directories import get_recent_receipt_date, largest_numeric_dir_name
import os

if __name__ == "__main__":

    # all this was to get the date of the most recent receipt so why dont we make it a function

    
    receipts_directory_path = r"C:\Users\Alex\Documents\Finances\receipts"

    latest_year = largest_numeric_dir_name(receipts_directory_path)
    latest_year_directory_path = os.path.join(receipts_directory_path, latest_year)

    latest_month = largest_numeric_dir_name(latest_year_directory_path)
    latest_month_directory_path = os.path.join(latest_year_directory_path, latest_month)

    recent_receipt_date = get_recent_receipt_date(latest_month_directory_path)

    receipt_scraper(recent_receipt_date)



    # Log in

    # Scrape receipts checking most recent date of local file system


    # Move receipts (delete receipts of processes below were to fail)
    # (maybe receipts should be moved to a temp location first for processing and at the very end, moved to archive)

    # Read receipts into dataframe


    # Add weightings from existing weighting file from drive

    # Prompt user to fill out weighting for new items

    # update weighting file with new weighting

    # move dataframe to drive

    pass


