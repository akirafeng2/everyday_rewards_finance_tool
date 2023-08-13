from datetime import datetime
import os
import time
import undetected_chromedriver as webdriver
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime

class file_system:
    
    def __init__(self, local_finance_file_path: str) -> None:
        self.local_receipts_file_path = local_finance_file_path + r"\Finances\receipts"

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

    def __init__(self, name: str, email: str, password: str, local_finance_file_path: str) -> None:
        self.name = name
        self.email = email
        self.password = password
        self.file_root = file_system(local_finance_file_path)

    def scraper(self, date_up_to: datetime):
        """
        Function that initiates receipt scraping process from everyday rewards website up to the date specified by the user
        :param date_up_to: datetime
        :return: None
        """
        if not isinstance(date_up_to, datetime):
            raise TypeError("Expected argument 'date_up_to' to be a datetime object.")

        driver = webdriver.Chrome()

        params = {
            "behavior": "allow",
            "downloadPath": r'C:\Users\Alex\Documents\Finances\receipts\tmp'
            }
        driver.execute_cdp_cmd("Page.setDownloadBehavior", params)

        url = 'https://www.woolworthsrewards.com.au/#login'
        driver.get(url)

        # Switch to the iframe (assuming the iframe has a name or ID attribute)
        iframe = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="WXLoginIFrameObject"]')))
        driver.switch_to.frame(iframe)

        # input login email
        email_input = WebDriverWait(driver, 31).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="emailCardNumber"]')))
        email_input.send_keys(self.email)

        password_input = WebDriverWait(driver, 31).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
        password_input.send_keys(self.password)
        driver.find_element(By.XPATH, '//*[@id="login-submit"]').click()

        # input otp
        otp = input('Enter SMS OTP:')
        driver.find_element(By.XPATH, '//*[@id="otp"]').send_keys(otp)
        driver.find_element(By.XPATH,
                            '/html/body/erl-root/div/erl-validate-user/div/div/erl-one-time-pass/form/div[4]/button[1]').click()

        # get to receipt page
        my_account = WebDriverWait(driver, 20).until(ec.presence_of_element_located(
            (By.XPATH, '/html/body/div[4]/div[1]/header[1]/nav[1]/div/div/div[1]/ul/li[5]/a')))
        my_account.click()
        my_activity = WebDriverWait(driver, 20).until(
            ec.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[1]/header[1]/nav[2]/div/div/div/ul/li[1]/a')))
        my_activity.click()

        # Downloading receipts

        max_counter = 10

        for receipt_num in range(2, max_counter):
            receipt_xpath = '//*[@id="angular-view-div"]/div/div[5]/wr-my-activity-new-element/div/div/div[3]/div[' + str(
                receipt_num) + ']'
            receipt_date_xpath = receipt_xpath + '/div[1]/div/div/div[1]'

            try:
                receipt_date_string = WebDriverWait(driver, 3).until(
                    ec.presence_of_element_located((By.XPATH, receipt_date_xpath))).text
            except selenium.common.exceptions.TimeoutException as e:
                print(receipt_xpath)
                print(e)
                continue
            receipt_date_month = receipt_date_string[-3:]
            receipt_date_day = receipt_date_string[4:6]
            if receipt_date_month == "Dec":
                if datetime.now().year != date_up_to.year:
                    receipt_date_year = date_up_to.year
                else:
                    receipt_date_year = datetime.now().year
            else:
                receipt_date_year = datetime.now().year

            date_format = "%d%b%Y"
            date_string = receipt_date_day + receipt_date_month + str(receipt_date_year)
            receipt_date = datetime.strptime(date_string, date_format)
            # if the current year is not the same as the inputted year and something about january
            if receipt_date > date_up_to:
                receipt_banner = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, receipt_xpath)))
                receipt_banner.click()
                time.sleep(2)
                receipt_download = WebDriverWait(driver, 30).until(
                    ec.presence_of_element_located((By.XPATH, '//*[@id="ereceiptSidesheet"]/div/div/div[1]/a/img')))
                receipt_download.click()
                x_click_out = WebDriverWait(driver, 20).until(
                    ec.presence_of_element_located((By.XPATH, '//*[@id="ereceiptSidesheet"]/div/a/img')))
                x_click_out.click()

            else:
                break

        time.sleep(20)  # add a 5-second delay
        driver.quit()

    def update_spreadsheet(self) -> None:
        self.scraper(self.file_root.get_recent_receipt_date())

        # Scrape receipts checking most recent date of local file system

        # Move receipts (delete receipts of processes below were to fail)
        # (maybe receipts should be moved to a temp location first for processing and at the very end, moved to archive)

        # Read receipts into dataframe

        # Add weightings from existing weighting file from drive

        # Prompt user to fill out weighting for new items

        # update weighting file with new weighting

        # move dataframe to drive    
        pass


class household:
    def __init__(self, household_name, admin: user):
        self.household_name = household_name
        self.members = [admin]
        self.admin = admin 

    def add_user(self, user: user):
        if user not in self.members:
            self.members.append(user)

    def appoint_admin(self, user: user):
        if user in self.members:
            self.admin = user
        else:
            raise Exception("User not in household")
    
    def admin_check(self, user: user):
        if user is not self.admin:
            raise Exception("User does not have permission")
        else:
            pass
    
    def settle_up(self, user: user):
        self.admin_check(user)
        pass

    def reset_spreadsheets(self):
        self.admin_check(user)
        pass


#modification test