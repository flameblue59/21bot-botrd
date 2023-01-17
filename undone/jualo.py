from  selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import random
import sys
import json

options = webdriver.ChromeOptions()

# setting profile
options.user_data_dir = "c:\\temp\\profile"

# another way to set profile is the below (which takes precedence if both variants are used
options.add_argument('--no-sandbox')
options.add_argument('--user-data-dir=c:\\temp\\testBrowser')
#options.add_argument('--incognito')
#options.add_argument('--start-fullscreen')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-infobars')
options.add_argument('--disable-gpu')
options.add_argument('--disable-blink-features=AutomationControlled')
#options.add_argument('--start-maximized')
options.add_experimental_option("excludeSwitches", ["enable-automation","enable-logging"])
options.add_experimental_option('useAutomationExtension', False)
# just some options passing in to skip annoying popups
options.add_argument('--no-first-run --no-service-autorun --password-store=basic')   
if __name__ == "__main__":  
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(800, 600)
    #driver.minimize_window()
    action = ActionChains(driver)

    with driver:
        #buka halaman masuksini
        driver.get('https://www.jualo.com/properti-hunian')
        #ambil link iklan
        links = []
        elem = "//a[@class='nav-link stretched-link']"
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
        except:
            print('link WebDriverWait bermasalah')
        else:
            try:
                link = driver.find_elements(By.XPATH,elem)
                #klik link
                for obj in link:
                    links = obj.get_attribute('href')
            except:
                print('link tidak ada')