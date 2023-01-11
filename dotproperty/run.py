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

def checkLogin():
    hasLogin = False
    elem = "//a[contains(@href,\'dotproperty.id/dashboard/setting/changepass')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kamu belum masuk')
        hasLogin = False
    else:
        try:
            registerMenu = driver.find_element(By.XPATH,elem)
            print('kamu sudah masuk, melanjutkan aktifitas')
            hasLogin = True
        except:
            print('kamu belum masuk')
            hasLogin = False    
    
    return hasLogin

def doRegister(name,email,password):
    #click registration link
    elem = "//a[@class='register-link']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver klik menu register')
        return False
    else:
        try:
            registerMenu = driver.find_element(By.XPATH,elem)
            registerMenu.click()
        except:
            print('menu register tidak ditemukan')
            return False
        
    #click register button
    time.sleep(2)
    elem = "//a[@id='callRegisterBtn']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver tombol daftar')
        return False
    else:
        try:
            registerButton = driver.find_element(By.XPATH,elem)
            registerButton.click()
        except:
            print('tombol daftar tidak ditemukan')
            return False
        
    #click register with email
    time.sleep(2)
    elem = "//a[@class='signup-button email-signup']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver tombol daftar dengan email')
        return False
    else:
        try:
            registerEmail = driver.find_element(By.XPATH,elem)
            registerEmail.click()
        except:
            print('tombol daftar dengan email tidak ditemukan')
            return False    
         
    #get form parent
    elem = "//form[contains(@action,\'dotproperty.id/ajaxRegister')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver formulir pendaftaran')
        return False
    else:
        try:
            parent = driver.find_element(By.XPATH,elem)
        except:
            print('formulir pendaftaran tidak ditemukan')
            return False            
        
    #filling [form] input name
    time.sleep(2)
    elem = ".//input[@name='name']"
    try:
        WebDriverWait(parent,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver input name')
        return False
    else:
        try:
            input = parent.find_element(By.XPATH,elem)
            input.send_keys(name)
        except:
            print('input name tidak ditemukan')
            return False    
        
    #filling [form] input email
    time.sleep(2)
    elem = ".//input[@name='email']"
    try:
        WebDriverWait(parent,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver input email')
        return False
    else:
        try:
            input = parent.find_element(By.XPATH,elem)
            input.send_keys(email)
        except:
            print('input email tidak ditemukan')
            return False      
        
    #filling [form] input password
    time.sleep(2)
    elem = ".//input[@name='password']"
    try:
        WebDriverWait(parent,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver input password')
        return False
    else:
        try:
            input = parent.find_element(By.XPATH,elem)
            input.send_keys(password)
        except:
            print('input password tidak ditemukan')
            return False          
        
    #click register button    
    time.sleep(2)
    elem = ".//button[@id='registerPopupBtn']"      
    try:
        WebDriverWait(parent,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver tombol lakukan daftar')
        return False
    else:
        try:
            registerEmail = parent.find_element(By.XPATH,elem)
            registerEmail.click()
        except:
            print('tombol lakukan daftar tidak ditemukan')
            return False    
        
    return True           
    
def getCurrentPage():
    myCursor = mydb.cursor(dictionary=True)
    sql = "SELECT value FROM settings WHERE type='dotpropertyCurrent'"
    myCursor.execute(sql)
    result = myCursor.fetchall()
    return result[0]['value']

def updateCurentPage(page):
    #update page
    if page > 50:
        page = 0
    myCursor = mydb.cursor(dictionary=True)
    val = [page]
    sql = "UPDATE settings SET value=%s WHERE type='dotpropertyCurrent'"
    myCursor.execute(sql,val)
    mydb.commit()
    
def getUrlToRender(limit):
    urlToRender = []
    myCursor = mydb.cursor(dictionary=True)
    sql = "SELECT url FROM dotproperty_url WHERE rendered=0 LIMIT %s"
    val = [limit]
    myCursor.execute(sql,val)
    result = myCursor.fetchall()
    for row in result:
        urlToRender.append(row['url'])
    return urlToRender

def readNumber(urlToRender):
    phone = []
    for url in urlToRender:
        #open ad
        driver.get(url)
        elem = "//button[@class='btn btn-green btn-block getAgentBtn phoneNumberBtn']"
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
        except:
            print('kesalahan webdriver klik phone')
            continue
        else:
            try:
                button = driver.find_element(By.XPATH,elem)
                button.click()
            except:
                print('phone tidak ditemukan')
                continue
        
        #read phone
        elem = "//a[contains(@href,\'tel:')]"
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
        except:
            print('kesalahan webdriver ambil nomor')
            continue
        else:
            try:
                button = driver.find_element(By.XPATH,elem)
                link = button.get_attribute('href')
                number = link.split('tel:')[1]
                number = number.replace('/','')
                number = number.replace('-','')
                if number not in phone:
                    phone.append(number)
            except:
                print('nomor tidak ditemukan')
                continue    
    return phone    
    
def saveUrl(urlList):
    query = []
    val = []
    for url in urlList:
        query.append("(%s)")
        val.append(url)
    query = ','.join(query)
    myCursor = mydb.cursor(dictionary=True)
    sql = "INSERT INTO dotproperty_url(url) VALUES "+query+" ON DUPLICATE KEY UPDATE id=id"
    myCursor.execute(sql,val)
    mydb.commit()

def updateRenderedUrl(urlToRender):
    query = []
    val = []
    for url in urlToRender:
        query.append("(%s)")
        val.append(url)
    query = ','.join(query)
    myCursor = mydb.cursor()
    sql = "UPDATE dotproperty_url SET rendered=1 WHERE url IN("+query+")"
    myCursor.execute(sql,val)
    mydb.commit()

filePath = getPath()
slashDir = getSlashDir()

phone = []
page = int(getCurrentPage())
max = 50
pageQuery = ''
urlToRender = getUrlToRender(50)

options = webdriver.ChromeOptions()
# setting profile
options.user_data_dir = filePath

# another way to set profile is the below (which takes precedence if both variants are used
options.add_argument('--no-sandbox')
options.add_argument('--user-data-dir='+filePath+'chromeprofile'+slashDir+'dotproperty')
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
        
        #create credentials
        name = 'Johan Prasetya'
        email = 'johanpras'+str(random.randint(100,999))+'@gmail.com'
        password = '@johan123@'
        
        driver.get('https://www.dotproperty.id/properties-for-sale?sort=newest')
        #check login
        status = checkLogin()
        if status==False:
            doRegister(name,email,password)
            
        #check login again
        status = checkLogin()
        if status==False:
            doRegister(name,email,password)           
        
        if len(urlToRender)==0:
            #when there are no url to render [get url]
            while page < max:
                time.sleep(3)
                #insert page
                page += 1
                
                if page > 1:
                    pageQuery = '&page='+str(page)
                    
                #open rumah.com homepage
                try:
                    driver.get('https://www.dotproperty.id/properties-for-sale?sort=newest'+pageQuery)
                except:
                    print('terjadi kesalahan saat membuka homepage rumah.com')
                    driver.quit()
                    
                #get url
                elem = "//a[contains(@href,\'dotproperty.id/ads/')]"
                try:
                    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
                except:
                    print('kesalahan webdriver get url')
                else:
                    try:
                        urls = driver.find_elements(By.XPATH,elem)
                        #when no urls found
                        if len(urls) == 0:
                            break
                        #when there are urls
                        for obj in urls:
                            link = obj.get_attribute('href')
                            #inserting into urlToRender
                            if link not in urlToRender:
                                urlToRender.append(link)
                        #save url
                        saveUrl(urlToRender)
                    except:
                        print('tidak menemukan url')
        elif len(urlToRender) > 0:
            output = readNumber(urlToRender)
            phone.extend(output)
            updateRenderedUrl(urlToRender)
                                      
                
        objJson = json.dumps(phone)
        updateCurentPage(page)
        print('=>'+objJson)
        driver.quit()