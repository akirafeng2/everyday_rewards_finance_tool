from reciepts.receipt_scraper import receipt_scraper
from datetime import datetime

if __name__ == "__main__":

    date = "09Jun2023"
    date_format = "%d%b%Y"
    date_datetime = datetime.strptime(date, date_format)
    receipt_scraper(date_datetime)

    # Log in

    # Scrape receipts

    # Move receipts

    # Read receipts into table from drive

    # Add weightings from existing weighting file

    # Prompt user to fill out weighting for new items

    # update weighting file with new weighting

    pass
