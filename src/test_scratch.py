
import undetected_chromedriver as webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from PyPDF2 import PdfReader

import time
import os

def scraper_t():

    driver = webdriver.Chrome()    

    params = {
        "behavior": "allow",
        "downloadPath": str("/Finances/")
        }
    driver.execute_cdp_cmd("Page.setDownloadBehavior", params)




    url = 'https://freetestdata.com/document-files/pdf/'
    driver.get(url)

    download_button = WebDriverWait(driver, 120).until(ec.presence_of_element_located((By.XPATH, '//*[@id="post-81"]/div/div/section[4]/div/div[1]/div/section[1]/div/div[2]/div/div/div/div/a')))
    download_button.click()

    time.sleep(20)  # add a 5-second delay
    driver.quit()

if __name__ == "__main__":
    # x = input("Test")

    # scraper_t()
    path = "/app/Finances/receipts/tmp/"
    # path = os.getcwd()
    print(os.path.isfile("/app/Finances/receipts/tmp/eReceipt_1638_Green Square_17Aug2023__atixs.pdf"))
    debug = os.listdir(path)
    for file in debug:
        print(file)
    # print(os.getcwd())
    pdf = PdfReader("/app/Finances/receipts/tmp/eReceipt_1638_Green Square_17Aug2023__atixs.pdf")
    # print(pdf)
    print(pdf.pages[0].extract_text())
    
    
