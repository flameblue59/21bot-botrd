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
import mysql.connector
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

def getCurrentPage():
    myCursor = mydb.cursor(dictionary=True)
    sql = "SELECT value FROM settings WHERE type='brightonCurrent'"
    myCursor.execute(sql)
    result = myCursor.fetchall()
    return result[0]['value']

def updateCurentPage(page):
    #get max page
    myCursor = mydb.cursor(dictionary=True,buffered=True)
    sql = "SELECT value FROM settings WHERE type='brightonMax'"
    myCursor.execute(sql);
    result = myCursor.fetchall()
    maxPage = int(result[0]['value'])
    #update page
    if page > maxPage:
        page = 1
    myCursor = mydb.cursor(dictionary=True,buffered=True)
    val = [page]
    sql = "UPDATE settings SET value=%s WHERE type='brightonCurrent'"
    myCursor.execute(sql,val)
    mydb.commit()

def getAccount(site):
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT email,password FROM property_account WHERE site=%s and active=1 ORDER BY lastSync ASC"
    val = [site]
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    return result[0]['email'],result[0]['password']

def updateAccount(email,site):
    mycursor = mydb.cursor()
    sql = "UPDATE property_account SET lastSync=NOW() WHERE email=%s and site=%s"
    val = [email,site]
    mycursor.execute(sql,val)
    mydb.commit()


def goLogin(email,password):
    #click navbar button
    elem = "//button[@class='navbar-toggler d-block d-lg-none p-0']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver navbar button')
    else:
        try:
            menu = driver.find_element(By.XPATH,elem)
            menu.click()
        except:
            print('menu tidak di temukan')
            
    #click profil
    time.sleep(3)
    elem = "//div[@class='wrapper-login']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver profile button')
    else:
        try:
            profile = driver.find_element(By.XPATH,elem)
            profile.click()
        except:
            print('profile tidak di temukan')
            
    #send email
    time.sleep(2)
    elem = "//div[@id='formLoginPublicMemberMob']//input[@name='Username']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver email input')
    else:
        try:
            inputEmail = driver.find_element(By.XPATH,elem)
            inputEmail.send_keys(email)
        except:
            print('email input tidak di temukan')
            
    #send password
    elem = "//div[@id='formLoginPublicMemberMob']//input[@name='Password']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver password input')
    else:
        try:
            inputPassword = driver.find_element(By.XPATH,elem)
            inputPassword.send_keys(password)
        except:
            print('password input tidak di temukan')
            
    #click login button
    elem = "//div[@id='formLoginPublicMemberMob']//button[@class='btn btn-login-user mobile']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver login button')
    else:
        try:
            login = driver.find_element(By.XPATH,elem)
            login.click()
        except:
            print('login button tidak di temukan')    
            
    #click confirmation button
    elem = "//button[@class='swal2-confirm swal2-styled']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver confirm button')
    else:
        try:
            confirm = driver.find_element(By.XPATH,elem)
            confirm.click()
        except:
            print('confirm button tidak di temukan')                

def checkLogin():
    driver.get('https://www.brighton.co.id/visitor/')
    time.sleep(2)
    elem = "//h1[@class='text-greet-visitor']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver check login')
    else:
        try:
            login = driver.find_element(By.XPATH,elem)
            print('kamu sudah login')
            return True
        except:
            print('kamu belum login')
    return False

filePath = getPath()
slashDir = getSlashDir()
arrPhone = []
page = int(getCurrentPage())
max = 10+page
site = 'brighton.co.id'

email,password = getAccount(site)

updateAccount(email,site)

options = webdriver.ChromeOptions()
# setting profile
options.user_data_dir = filePath

# another way to set profile is the below (which takes precedence if both variants are used
options.add_argument('--no-sandbox')
options.add_argument('--user-data-dir='+filePath+'chromeprofile'+slashDir+'brighton'+slashDir+email)
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
        #buka home brighton
        driver.get('https://www.brighton.co.id/')
        goLogin(email,password)     
        #check login
        login = checkLogin()
        if login==False:
            goLogin(email,password)
        time.sleep(3)
        #render number
        while page < max:
            if page==1:
                driver.get('https://www.brighton.co.id/dijual/')
            else:
                driver.get('https://www.brighton.co.id/dijual/?page='+str(page))
            #ambil nomor
            elem = "//div[@data-classname='PropertyData']"
            try:
                WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
            except:
                print('WebDriverWait scrape nomor bermasalah')
            else:
                try:
                    objNomor = driver.find_elements(By.XPATH,elem)
                    for obj in objNomor:
                        nomor = obj.get_attribute('data-phone')
                        if nomor not in arrPhone:
                            arrPhone.append(nomor)
                except:
                    print('scrape nomor tidak di temukan')
            #increase page
            page += 1
            time.sleep(1)
        
        updateCurentPage(page)
        objJson = json.dumps(arrPhone)
        print('done=>'+objJson)
        driver.quit();
        quit();