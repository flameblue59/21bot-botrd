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

def renderUrlProfile(page):
    urlProfile = []
    driver.get('https://www.rumahku.com/properties/find/page:'+str(page)+'/')
    #Klik di jual
    elem = "//a[contains(@href,\'/u/')]"
    try:
        WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver link profil')
    else:
        #read url profile
        try:
            profile = driver.find_elements(By.XPATH,elem)
            sum = len(profile)-1
            if sum <= 0:
                print('tidak ada profile')
                #next page
            for obj in profile:
                link = obj.get_attribute('href')
                if link not in urlProfile:
                    urlProfile.append(obj.get_attribute('href'))
        except:
            print('terjadi kesalahan saat membaca profil')
    return urlProfile

def readNumber(url):
    nomor = []
    #go to profile
    driver.get(url)
    #read whatsapp
    elem = "//a[contains(@href,\'whatsapp')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver shortcut whatsapp')
    else:
        try:
            whatsapp = driver.find_elements(By.XPATH,elem)
            #read all numbers
            for obj in whatsapp:
                link = obj.get_attribute('href')
                phone = link.split('=+')[1]
                phone = phone.split('&text')[0]
                nomor.append(phone)
        except:
            print('nampaknya nomor whatsapp tidak ada')
            
    #when we have phone number then return
    if len(nomor) > 0:
        return nomor
    
    #read phone
    elem = "//a[contains(@href,\'tel:')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver shortcut nomor handphone')
    else:
        try:
            number = driver.find_elements(By.XPATH,elem)
            for obj in number:
                link = obj.get_attribute('href')
                phone = link.split('tel:')[1]
                phone = phone.replace('/','')
                nomor.append(phone)
        except:
            print('nampaknya nomor handphone tidak ada')
            
    return nomor
    
def sendUrlProfile(urlProfile,lastPage):
    query = []
    val = []
    for url in urlProfile:
        query.append('(%s)')
        val.append(url)
    query = ','.join(query)
    myCursor = mydb.cursor(buffered=True)
    sql = "INSERT INTO rumahku_profile(url) VALUES "+str(query)+" ON DUPLICATE KEY UPDATE id=id"
    myCursor.execute(sql,val)
    mydb.commit()
    #to update current page
    updateCurentPage(lastPage)
    
def getUrlProfile(limit):
    urlProfile = []
    myCursor = mydb.cursor(dictionary=True)
    sql = "SELECT url FROM rumahku_profile WHERE rendered=0 LIMIT %s"
    val = [limit]
    myCursor.execute(sql,val)
    result = myCursor.fetchall()
    for row in result:
        urlProfile.append(row['url'])
    return urlProfile
    
def getCurrentPage():
    myCursor = mydb.cursor(dictionary=True)
    sql = "SELECT value FROM settings WHERE type='rumahkuCurrent'"
    myCursor.execute(sql)
    result = myCursor.fetchall()
    return result[0]['value']

def getMaxPage():
    myCursor = mydb.cursor(dictionary=True)
    sql = "SELECT value FROM settings WHERE type='rumahkuMax'"
    myCursor.execute(sql)
    result = myCursor.fetchall()
    return result[0]['value']

def updateCurentPage(page):
    #update page
    if page > 100:
        page = 0    
    myCursor = mydb.cursor(dictionary=True)
    val = [page]
    sql = "UPDATE settings SET value=%s WHERE type='rumahkuCurrent'"
    myCursor.execute(sql,val)
    mydb.commit()
    
def setRendered(urlProfile):
    myCursor = mydb.cursor(dictionary=True)
    query = []
    val = []
    for url in urlProfile:
        query.append('(%s)')
        val.append(url)
    query = ','.join(query)
    sql = "UPDATE rumahku_profile SET rendered=true WHERE url IN("+query+")"
    myCursor.execute(sql,val)
    mydb.commit()
    
    
filePath = getPath()
slashDir = getSlashDir()

options = webdriver.ChromeOptions()
# setting profile
options.user_data_dir = filePath

# another way to set profile is the below (which takes precedence if both variants are used
options.add_argument('--no-sandbox')
options.add_argument('--user-data-dir='+filePath+'chromeprofile'+slashDir+'rumahku')
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

#define current page
current = int(getCurrentPage())
maxPage = int(getMaxPage())
max = 20
nomor = []
page = 0

#get url profile
urlProfile = getUrlProfile(20)

if __name__ == "__main__":  
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
        #get profile [it would run until max 20 pages]
        if len(urlProfile) <= 0:
            #define url profile
            urlProfile = []
            #when current page has not reached max
            while page < max:
                page += 1
                current += 1
                #open rumahku search page
                output = renderUrlProfile(current)
                urlProfile.extend(output)
            
            #send url profile
            if len(urlProfile) > 0:
                sendUrlProfile(urlProfile,current)
            else:
                print('tidak ada url profile untuk dikirim')
        #render number
        elif len(urlProfile) > 0:
            #render number
            for link in urlProfile:
                output = readNumber(link)
                nomor.extend(output)
                time.sleep(2)
            #set rendered url profile
            setRendered(urlProfile)
            
        objJson = json.dumps(nomor)
        print('=>'+objJson)
        driver.quit()
        quit()