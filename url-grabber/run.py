from  selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import time
import shutil
import random
import sys
import json
import os
import mysql.connector
import pyautogui

mydb = mysql.connector.connect(
host="localhost",
user="root",
password="",
database="bot_number"
)

def getProxy():
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT proxy FROM proxy_data ORDER BY lastSync ASC"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    proxy = result[0]['proxy'] 
    #update proxy lastSync
    mycursor = mydb.cursor()
    sql = "UPDATE proxy_data SET lastSync=CURRENT_TIMESTAMP() WHERE proxy=%s"
    val = [proxy]
    mycursor.execute(sql,val)
    mydb.commit()
    return proxy
    

def getAccount():
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT account FROM grabber_account ORDER BY lastSync ASC"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result[0]['account']

def getInit():
    url = sys.argv[1].replace("[","").replace("]","").replace("\\","")
    return url

def sendLastSync(account):
    mycursor = mydb.cursor()
    sql = "UPDATE grabber_account SET lastSync=CURRENT_TIMESTAMP() WHERE account=%s"
    val = [account]
    mycursor.execute(sql,val)
    mydb.commit()

#define account
targetUrl = getInit()
account = getAccount()
sendLastSync(account)

options = webdriver.ChromeOptions()

ip = getProxy()

# setting profile
options.user_data_dir = "C:\\urlGrabber\\profile"

# another way to set profile is the below (which takes precedence if both variants are used
options.add_argument('--user-data-dir=C:\\urlGrabber\\'+account)
#options.add_argument('--start-maximized')
#options.add_argument('--incognito')
#options.add_argument('--start-fullscreen')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-infobars')
options.add_argument('--disable-blink-features=AutomationControlled')
#options.add_argument('--start-maximized')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# just some options passing in to skip annoying popups
options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
#options.add_argument('--proxy-server=%s' % ip)
driver = webdriver.Chrome(options=options)
driver.minimize_window()
#driver.switch_to.new_window('window')
action = ActionChains(driver)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win64",
        webgl_vendor="NVIDIA.",
        renderer="AMD Iris OpenGL Engine",
        fix_hairline=True,
        )
#driver.maximize_window()

targetUrl = getInit()
result = {}
urlList = []

with driver:
    
    driver.implicitly_wait(10)
    try:
        driver.get(targetUrl)
    except:
        driver.quit()
        quit()
    #give delay for 4 seconds
    time.sleep(4)
    elem = "//a[contains(@href,\'/item/')]"
    try:
        WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        driver.quit()
        quit()
    else:
        try:
            urlDom = driver.find_elements(By.XPATH,elem)
            if len(urlDom)==0:
                driver.quit()
                quit()
            #sending all urls
            for url in urlDom:
                url = url.get_attribute('href')
                urlList.append(url)            
        except:
            driver.quit()
            quit()

    #opening all ad to get profile UID
    for url in urlList:
        #going to the ad page
        driver.get(url)
        #read profile
        try:
            profile = driver.find_element(By.XPATH,"//div[@data-aut-id='profileCard']/a[1]")
            profileUID = profile.get_attribute('href').split('/profile/')[1]
        except:
            continue
        #send to url list
        result[profileUID] = url  
    else:
        pass
    objJson = json.dumps(result)
    print(objJson)
    driver.quit()