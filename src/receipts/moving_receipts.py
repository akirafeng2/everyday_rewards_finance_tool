import os
import shutil
import datetime

"""
Moving receipts from downloads to specified folder
"""
# Set path of downloads folder
downloads_directory = r'C:\Users\Alex\Downloads'

# Getting current year and month
now = datetime.datetime.now()
year = str(now.year)
month = str(now.month)

# Setting destination directory
destination_folder = fr'C:\Users\Alex\Documents\Finances\receipts\{year}\{month}'

# Creating the destination directory if it does not exist
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Loop through the files in the downloads folder
for filename in os.listdir(downloads_directory):
    if filename.startswith("eReceipt"):
        file_path = os.path.join(downloads_directory, filename)

        file_creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        if file_creation_time.date() == now.date():
            # Move the file to the destination folder
            shutil.move(file_path, destination_folder)
            print(f"Processing file: {filename}, created on {file_creation_time}")



