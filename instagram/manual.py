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
import myConn
import time
import requests
import random
import sys
import json
import math
import os
#importing our custom files
import myConn
from tool.main import tool
import main

def filePath():
    mycursor = myConn.mydb.cursor(dictionary=True)
    sql = "SELECT value FROM settings WHERE type='filePath'"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result[0]['value']

def superGet(url):
    driver.get(url)

def getAccount():
    email = sys.argv[1]
    mycursor = myConn.mydb.cursor(dictionary=True)
    sql = "SELECT email,password FROM instagram_account WHERE email=%s ORDER BY nextRun ASC"
    val = [email]
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    if len(result)==0:
        return False
    return result[0]['email'],result[0]['password']
    
filePath = filePath()
slashDir = '/'

#get account
account = getAccount()
if account==False:
    print('terjadi kesalahan akun')
    quit()
    
email,password = account

options = webdriver.ChromeOptions()
# setting profile
options.user_data_dir = filePath

prefs = {"profile.default_content_setting_values.notifications" : 2}
# another way to set profile is the below (which takes precedence if both variants are used
options.add_argument('--no-sandbox')
options.add_argument('--user-data-dir='+filePath+'chromeprofile'+slashDir+'instagram'+slashDir+email)
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
if __name__ == "__main__":  
    driver = webdriver.Chrome(options=options)
    #driver.minimize_window()
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win64",
            webgl_vendor="ANGLE (Apple, Apple M1 Pro, OpenGL 4.1)",
            renderer="AMD Iris OpenGL Engine",
            fix_hairline=True,
            )    
    action = ActionChains(driver)

    with driver:
            
        tool.superGet(driver,'https://instagram.com')
        
        time.sleep(1800)