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
import os
import sys
import json
import shutil

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

def getCurrentPage():
    myCursor = mydb.cursor(dictionary=True)
    sql = "SELECT value FROM settings WHERE type='rumahcomCurrent'"
    myCursor.execute(sql)
    result = myCursor.fetchall()
    return result[0]['value']

def updateCurentPage(page):
    #update page
    if page > 50:
        page = 0
    myCursor = mydb.cursor(dictionary=True)
    val = [page]
    sql = "UPDATE settings SET value=%s WHERE type='rumahcomCurrent'"
    myCursor.execute(sql,val)
    mydb.commit()
    
def removeUnusedBrowser():
    path = filePath+'chromeprofile'
    listDir = os.listdir(path)
    for dir in listDir:
        if 'rumahcom' in dir:
            shutil.rmtree(path+slashDir+dir)    

filePath = getPath()
slashDir = getSlashDir()

#removing unused browser to save disk space
removeUnusedBrowser()

options = webdriver.ChromeOptions()
# setting profile
options.user_data_dir = filePath

# another way to set profile is the below (which takes precedence if both variants are used
options.add_argument('--no-sandbox')
options.add_argument('--user-data-dir='+filePath+'chromeprofile'+slashDir+'rumahcom'+str(random.randint(0,10000)))
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
    driver.minimize_window()
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
        page = int(getCurrentPage())
        pageQuery = ''
        
        #insert page
        page += 1
        
        if page > 1:
            pageQuery = '/'+str(page)
            
        #open rumah.com homepage
        try:
            driver.get('https://www.rumah.com/properti-dijual'+pageQuery+'?sort=date&order=desc')
        except:
            print('terjadi kesalahan saat membuka homepage rumah.com')
            driver.quit()
            
        #convert page source into beautiful soup
        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, 'html.parser')
        try:
            #get number
            elem = soup.select("a[class='hidden-sm hidden-md phone-call-button phone-call-action-tracking col-xs-6 col-sm-8 featured-action']")
            for obj in elem:
                number = obj.get("href")
                number = number.split('tel:+')
                number = number[1]
                phone.append(number)
        except:
            print('tidak ada data')                
                
        objJson = json.dumps(phone)
        updateCurentPage(page)
        print(objJson)
        driver.quit()