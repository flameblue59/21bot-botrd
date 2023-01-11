import undetected_chromedriver as uc
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
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import mysql.connector
import time
import requests
import random
import sys
import json

mydb = mysql.connector.connect(
    host="localhost",
    username="root",
    password="",
    database="bot_number"
)


def getPath():
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT value FROM settings WHERE type='filePath'"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result[0]['value']

def getSlashDir():
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT value FROM settings WHERE type='slashDir'"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result[0]['value']
    

filePath = getPath()
slashDir = getSlashDir()

options = webdriver.ChromeOptions()
# setting profile
options.user_data_dir = filePath

# another way to set profile is the below (which takes precedence if both variants are used
options.add_argument('--no-sandbox')
options.add_argument('--user-data-dir='+filePath+'chromeprofile'+slashDir+'rumah123')
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
    # define max page to go
    maxPage = 1;
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
            
        phone = []
        
        for i in range(maxPage):
            query = ''
            page = str(i)
            #define query
            if i > 1:
                query = '&hlmn='+page
            driver.implicitly_wait(5)
            #open rumah.com homepage
            try:
                driver.get('https://www.99.co/id/jual/rumah?urut=2'+query)
                time.sleep(100)
            except:
                print('terjadi kesalahan saat membuka homepage rumah.com')
                driver.quit()
                
            #convert page source into beautiful soup
            pageSource = driver.page_source
            print(pageSource)
            soup = BeautifulSoup(pageSource, 'html.parser')
            try:
                #get number
                elem = soup.select("a[class='hidden-sm hidden-md phone-call-button phone-call-action-tracking col-xs-6 col-sm-8 featured-action']")
                for obj in elem:
                    number = obj.getText().strip()
                    if number!='':
                        phone.append(obj.getText())            
            except:
                print('tidak ada data')

        objJson = json.dumps(phone)
        print(objJson)
        driver.quit()