import undetected_chromedriver as webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions

from datetime import datetime

import time

class EverydayRewardsScraper():
    
    def __init__(self):
        self.url = 'https://www.woolworthsrewards.com.au/#login'
        self.driver = webdriver.Chrome()


    # Pre MFA methods

    def set_downloads(self, name: str):
        params = {
            "behavior": "allow",
            "downloadPath": f"/app/Finances/receipts/{name}/tmp"
            }
        self.driver.execute_cdp_cmd("Page.setDownloadBehavior", params) 


    def start(self):
        self.driver.get(self.url)
        print("2")


    def switch_to_iframe(self):
        iframe = WebDriverWait(self.driver, 20).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="WXLoginIFrameObject"]')))
        self.driver.switch_to.frame(iframe)
        print("3")


    def input_login_details(self, email: str, password):
        # input login email
        email_input = WebDriverWait(self.driver, 60).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="emailNumber"]')))
        email_input.send_keys(email)

        # input Password
        password_input = WebDriverWait(self.driver, 60).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
        password_input.send_keys(password)

        # press enter
        self.driver.find_element(By.XPATH, '//*[@id="login-submit"]').click()
        time.sleep(10)
        print("4")

    
    # Post MFA methods

    def input_mfa_code(self, mfa_code: str):
        self.driver.find_element(By.XPATH, '//*[@id="otp"]').send_keys(mfa_code)
        self.driver.find_element(By.XPATH,
                            '/html/body/erl-root/div/erl-validate-user/div/div/erl-one-time-pass/form/div[4]/button[1]').click()    

    
    def navigate_to_receipt_page(self):
        my_account = WebDriverWait(self.driver, 60).until(ec.presence_of_element_located(
            (By.XPATH, '/html/body/div[4]/div[1]/header[1]/nav[1]/div/div/div[1]/ul/li[5]/a')))
        my_account.click()
        my_activity = WebDriverWait(self. driver, 60).until(
            ec.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[1]/header[1]/nav[2]/div/div/div/ul/li[1]/a')))
        my_activity.click()


    def download_receipts(self, date_up_to: datetime, max_iterations: int):
        
        # error counter to find end of receipt log
        error_counter = 0

        for receipt_num in range(2, max_iterations):
            receipt_xpath = '//*[@id="angular-view-div"]/div/div[5]/wr-my-activity-new-element/div/div/div[3]/div[' + str(
                receipt_num) + ']'
            receipt_date_xpath = receipt_xpath + '/div[1]/div/div/div[1]'

            try:
                receipt_date_string = WebDriverWait(self.driver, 60).until(
                    ec.presence_of_element_located((By.XPATH, receipt_date_xpath))).text
            except selenium.common.exceptions.TimeoutException as e:
                # the end of the document is denoted by 3 div rows without a date attribute. Between months will only have two empty div rows
                print(f"{e} | Parsed XPath: {receipt_xpath} with no date attribute")                
                if error_counter < 3:
                    error_counter += 1
                else:
                    break

                continue

            # reset empty div row counter if row has a valid receipt date
            error_counter = 0

            # woolies doesn't display year, so need to add year to the date accounting for the fact that if we're in Jan, parsing Dec receipts, year will be current year -1
            receipt_date_month = receipt_date_string[-3:]
            receipt_date_day = receipt_date_string[4:6]
            if receipt_date_month == "Dec":
                if datetime.now().year != date_up_to.year:
                    receipt_date_year = date_up_to.year
                else:
                    receipt_date_year = datetime.now().year
            else:
                receipt_date_year = datetime.now().year

            # combining scraped data as Datetime attribute
            date_format = "%d%b%Y"
            date_string = receipt_date_day + receipt_date_month + str(receipt_date_year)
            receipt_date = datetime.strptime(date_string, date_format)

            # download receipt if the date is after specified date_up_to parameter
            if receipt_date > date_up_to:
                receipt_banner = WebDriverWait(self.driver, 60).until(ec.presence_of_element_located((By.XPATH, receipt_xpath)))
                receipt_banner.click()
                time.sleep(2)
                receipt_download = WebDriverWait(self.driver, 60).until(
                    ec.presence_of_element_located((By.XPATH, '//*[@id="ereceiptSidesheet"]/div/div/div[1]/a/img')))
                try:
                    receipt_download.click()
                except selenium.common.exceptions.ElementNotInteractableException as e:
                    # if this exception occurs, it means the item has no receipt to download
                    continue
                else:
                    x_click_out = WebDriverWait(self.driver, 60).until(
                        ec.presence_of_element_located((By.XPATH, '//*[@id="ereceiptSidesheet"]/div/a/img')))
                    x_click_out.click()

            else:
                break        

        pass 


    def stop(self):
        time.sleep(20)
        self.driver.quit()