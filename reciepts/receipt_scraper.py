import time

import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime

import login_details


def receipt_scraper(date_up_to: datetime):
    if not isinstance(date_up_to, datetime):
        raise TypeError("Expected argument 'date_up_to' to be a datetime object.")

    driver = webdriver.Chrome()

    url = 'https://www.woolworthsrewards.com.au/#login'
    driver.get(url)

    # Switch to the iframe (assuming the iframe has a name or ID attribute)
    iframe = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="WXLoginIFrameObject"]')))
    driver.switch_to.frame(iframe)

    # input login email
    email_input = WebDriverWait(driver, 31).until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="emailCardNumber"]')))
    email_input.send_keys(login_details.email)
    driver.find_element(By.XPATH,
                        '/html/body/erl-root/div/erl-validate-user/div/div/erl-user-email-card-number/form/div['
                        '3]/button[1]').click()

    # click sms verification button
    verify_check_confirm = WebDriverWait(driver, 10).until(ec.presence_of_element_located(
        (By.XPATH, '/html/body/erl-root/div/erl-validate-user/div/div/erl-choose-login/form/div[3]/button[1]')))
    verify_check_confirm.click()

    # input otp
    otp = input('Enter SMS OTP:')
    driver.find_element(By.XPATH, '//*[@id="otp"]').send_keys(otp)
    driver.find_element(By.XPATH,
                        '/html/body/erl-root/div/erl-validate-user/div/div/erl-one-time-pass/form/div[5]/button[1]').click()

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

        # need a try except here
        receipt_date_string = WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.XPATH, receipt_date_xpath))).text
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
        date_string = receipt_date_day+receipt_date_month+str(receipt_date_year)
        receipt_date = datetime.strptime(date_string, date_format)
        # if the current year is not the same as the inputted year and something about january
        if receipt_date > date_up_to:
            print(receipt_xpath)
            receipt_banner = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, receipt_xpath)))
            receipt_banner.click()
            receipt_download = WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, '//*[@id="ereceiptSidesheet"]/div/div/div[1]/a/img')))
            receipt_download.click()
            x_click_out = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, '//*[@id="ereceiptSidesheet"]/div/a/img')))
            x_click_out.click()

        else:
            break

    time.sleep(20)  # add a 5-second delay
    driver.quit()
