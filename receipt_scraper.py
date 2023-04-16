import time

import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime

import login_details

month_dict = dict([(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'),
                   (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (0, 'Dec')])

driver = webdriver.Chrome()

url = 'https://www.woolworthsrewards.com.au/#login'
driver.get(url)

# Switch to the iframe (assuming the iframe has a name or ID attribute)
iframe = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="WXLoginIFrameObject"]')))
driver.switch_to.frame(iframe)

# input login email
driver.find_element(By.XPATH, '//*[@id="emailCardNumber"]').send_keys(login_details.email)
driver.find_element(By.XPATH, '/html/body/erl-root/div/erl-validate-user/div/div/erl-user-email-card-number/form/div['
                              '3]/button[1]').click()

# click sms verification button
verify_check_confirm = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '/html/body/erl-root/div/erl-validate-user/div/div/erl-choose-login/form/div[3]/button[1]')))
verify_check_confirm.click()

# input otp
otp = input('Enter SMS OTP:')
driver.find_element(By.XPATH, '//*[@id="otp"]').send_keys(otp)
driver.find_element(By.XPATH, '/html/body/erl-root/div/erl-validate-user/div/div/erl-one-time-pass/form/div[5]/button[1]').click()

# get to receipt page
my_account = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[1]/header[1]/nav[1]/div/div/div[1]/ul/li[5]/a')))
my_account.click()
my_activity = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[1]/header[1]/nav[2]/div/div/div/ul/li[1]/a')))
my_activity.click()

# Downloading receipts
max_counter = 10
current_month = datetime.now().month
previous_month_dict_key = current_month-1
current_month_str = month_dict[current_month]
previous_month_str = month_dict[previous_month_dict_key]

for receipt_num in range(2, max_counter):
    receipt_xpath = '//*[@id="angular-view-div"]/div/div[6]/wr-my-activity-new-element/div/div/div[3]/div[' + str(receipt_num) + ']'
    receipt_date_xpath = receipt_xpath + '/div[1]/div/div/div[1]'
    receipt_date = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, receipt_date_xpath))).text
    receipt_date_month = receipt_date[-3:]

    if receipt_date_month == current_month_str:
        receipt_banner = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, receipt_xpath)))
        receipt_banner.click()
        receipt_download = WebDriverWait(driver, 20)\
            .until(ec.presence_of_element_located((By.XPATH, '//*[@id="ereceiptSidesheet"]/div/div/div[1]/a/img')))
        receipt_download.click()
        x_click_out = WebDriverWait(driver, 20)\
            .until(ec.presence_of_element_located((By.XPATH, '//*[@id="ereceiptSidesheet"]/div/a/img')))
        x_click_out.click()

    elif receipt_date_month == previous_month_str:
        break



# //*[@id="angular-view-div"]/div/div[6]/wr-my-activity-new-element/div/div/div[3]/div[2]
# //*[@id="angular-view-div"]/div/div[6]/wr-my-activity-new-element/div/div/div[3]/div[3]
# //*[@id="angular-view-div"]/div/div[6]/wr-my-activity-new-element/div/div/div[3]/div[6]

# //*[@id="angular-view-div"]/div/div[6]/wr-my-activity-new-element/div/div/div[3]/div[2]/div[1]/div/div/div[1]

# //*[@id="angular-view-div"]/div/div[6]/wr-my-activity-new-element/div/div/div[3]/div[3]/div[1]/div/div/div[1]
"""
The way I see this happening is a conditional statement based on the html that check that the month in the html is
the current month. if it is it'll go through the selenium motions to download and collect the pdfs
"""
time.sleep(20)  # add a 5-second delay
driver.quit()


