from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import time
import requests
import random
import sys
import json
import math
import os
import myConn

def getFilePath():
    mycursor = myConn.mydb.cursor(dictionary=True)
    sql = "SELECT value FROM settings WHERE type='filePath'"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result[0]['value']

#To sync account usage
def updateLastSync(account):
    mycursor = myConn.mydb.cursor()
    sql = "UPDATE account_data SET lastSync=NOW() WHERE email=%s"
    val = [account]
    mycursor.execute(sql,val)
    myConn.mydb.commit()   

userEmail = 'nathan@gmail.com'

filePath = getFilePath()
slashDir = '/'

print(filePath)

options = webdriver.ChromeOptions()

# setting profile
options.user_data_dir = filePath+''+slashDir+'olx'+slashDir+'profile'

# another way to set profile is the below (which takes precedence if both variants are used
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_argument('--no-sandbox')
options.add_argument('--user-data-dir='+filePath+''+slashDir+'olx'+slashDir+userEmail)
#options.add_argument('--incognito')
#options.add_argument('--start-fullscreen')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-infobars')
options.add_argument('--disable-notifications')
options.add_argument('--disable-gpu')
options.add_argument('--disable-blink-features=AutomationControlled')
#options.add_argument('--start-maximized')
options.add_experimental_option("excludeSwitches", ["enable-automation","enable-logging"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("prefs",prefs)
# just some options passing in to skip annoying popups
options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
print(options)
if __name__ == "__main__": 
    driver = webdriver.Chrome(options=options)
    
    with driver:
        errorScript = False
        updateLastSync(userEmail)
        #open olx homepage
        try:
            driver.get('https://www.olx.co.id')
        except:
            driver.get('https://www.olx.co.id')    
        time.sleep(300)