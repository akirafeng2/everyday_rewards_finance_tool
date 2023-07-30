from datetime import datetime
import os



class file_system:
    
    def __init__(self, local_finance_file_path: str) -> None:
        self.local_receipts_file_path = local_finance_file_path + r"\Finances\receipts"
        pass

    def iterate_largest_numeric_dir_name(self, directory_path: str, iterate_number: int) -> str:
        """
        Returns the file or directory in a given directory that has the largest numeric value for its name
        :param iterate_number: int
        :return: str
        """
        
        for x in range(iterate_number):
            
            max_dir_name = None

            # Iterate over the directories in the specified path
            for dir_name in os.listdir(directory_path):

                try:
                    dir_name = int(dir_name)
                except ValueError:
                    continue

                if max_dir_name is None or dir_name > max_dir_name:
                    max_dir_name = dir_name

            directory_path = rf"{directory_path}\{str(max_dir_name)}"

        return directory_path

    def get_recent_receipt_date(self) -> datetime:
        """
        Returns the date of the most recent Everyday Rewards downloaded receipt in a given directory
        :param directory_path: str
        :return: datetime "%d%b%Y"
        """
        directory_path = self.iterate_largest_numeric_dir_name(self.local_receipts_file_path,2)
        receipt_name_list = os.listdir(directory_path)
        receipt_date_list = [receipt_name.split("_")[3] for receipt_name in receipt_name_list]
        recent_date_str = max(receipt_date_list)
        date_format = "%d%b%Y"
        recent_date = datetime.strptime(recent_date_str, date_format)
        return recent_date        


class user:

    def __init__(self, name: str, email: str, local_finance_file_path) -> None:
        self.name = name
        self.email = email
        self.file_root = file_system(local_finance_file_path)
        pass

    def update_spreadsheet(self) -> None:
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


class admin(user):

    def settle_up(self):
        pass

    def reset_spreadsheets(self):
        pass


class household:
    def __init__(self, household_name, admin):
        self.household_name = household_name
        self.members = []
        self.admin = admin #Question 1: Do i need this? or should i just put the admin methods into household

    def add_user(self, user):
        self.members.append(user)


# test to retrive the date of most recent receipt
if __name__=="__main__":

    user1 = user("alex", "alexander.feng2@gmail.com", r"C:\Users\Alex\Documents")
    print(user1.file_root.get_recent_receipt_date())
