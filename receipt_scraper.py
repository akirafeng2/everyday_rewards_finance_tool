from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import login_details
import undetected_chromedriver as webdriver
import time
from gmail_get_recent_email import main

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

# find enter password and click
# password_check_box = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="mat-radio-2"]')))
# password_check_box.click()

password_check_confirm = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '/html/body/erl-root/div/erl-validate-user/div/div/erl-choose-login/form/div[3]/button[1]')))
password_check_confirm.click()

# input password
# password_input = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
# password_input.send_keys(login_details.password)
# driver.find_element(By.XPATH, '/html/body/erl-root/div/erl-validate-user/div/div/erl-password/form/div[4]/button[1]').click()

# time.sleep(5)
# driver.find_element(By.XPATH, '/html/body/erl-root/div/erl-validate-user/div/div/erl-password-secure-verification/form/div[3]/form/button').click()
# time.sleep(15)
otp = input('Enter SMS OTP:')
# email_verification_otp = main()
driver.find_element(By.XPATH, '//*[@id="otp"]').send_keys(otp)
driver.find_element(By.XPATH, '/html/body/erl-root/div/erl-validate-user/div/div/erl-one-time-pass/form/div[5]/button[1]').click()

time.sleep(20)  # add a 5-second delay
driver.quit()


