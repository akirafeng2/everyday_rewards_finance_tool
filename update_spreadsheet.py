from receipts.receipt_scraper import receipt_scraper
from datetime import datetime
from receipts.checking_directories import get_recent_receipt_date, largest_numeric_dir_name

if __name__ == "__main__":
    date = "30Jun2023"  # TODO: incorporate the checking directories functions
    date_format = "%d%b%Y"
    date_datetime = datetime.strptime(date, date_format)
    receipt_scraper(date_datetime)

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
