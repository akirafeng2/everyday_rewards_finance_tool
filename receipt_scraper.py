from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import login_details
import undetected_chromedriver as webdriver
import time

driver = webdriver.Chrome()

url = 'https://accounts.woolworthsrewards.com.au/er-login/validate-user?referrer=REWARDS_CP&state=state123'
driver.get(url)
driver.implicitly_wait(10) # gives an implicit wait for 20 seconds
# html_source = driver.page_source
# soup = BeautifulSoup(html_source, 'html.parser')
# pretty_html = soup.prettify()
# print(pretty_html)


driver.find_element(By.XPATH, '//*[@id="emailCardNumber"]').send_keys(login_details.email)
driver.find_element(By.XPATH, '/html/body/erl-root/div/erl-validate-user/div/div/erl-user-email-card-number/form/div['
                              '3]/button[1]').click()


time.sleep(20)  # add a 5-second delay
driver.quit()
