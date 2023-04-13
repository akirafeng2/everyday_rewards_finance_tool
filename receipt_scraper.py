import time

import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import login_details

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
"""
The way I see this happening is a conditional statement based on the html that check that the month in the html is
the current month. if it is it'll go through the selenium motions to download and collect the pdfs
"""
time.sleep(20)  # add a 5-second delay
driver.quit()


