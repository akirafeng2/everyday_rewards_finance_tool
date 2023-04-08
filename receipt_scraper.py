from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service('C:\\Users\\Alex Feng\\chromedriver_win32\\chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get('https://www.google.com/')