from finance_tool import file_system, user
import login_details

if __name__ == "__main__":

    # Log in

    # Scrape receipts checking most recent date of local file system
    user_1 = user(*login_details.alex_user_info)
    recent_receipt_date = user_1.file_root.get_recent_receipt_date()
    user_1.scraper(recent_receipt_date)
    

    # Move receipts (delete receipts of processes below were to fail)
    # (maybe receipts should be moved to a temp location first for processing and at the very end, moved to archive)

    # Read receipts into dataframe


    # Add weightings from existing weighting file from drive

    # Prompt user to fill out weighting for new items

    # update weighting file with new weighting

    # move dataframe to drive

    pass


