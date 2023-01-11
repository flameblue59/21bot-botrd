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
from retry import retry
from timeout_decorator import timeout, TimeoutError
import time
import mysql.connector
import requests
import random
import sys
import json
import pyautogui
import shutil
import os

session = requests.Session()

mydb = mysql.connector.connect(
    host="localhost",
    username="root",
    password="",
    database="bot_number"
)

# To sync account data from /temp folder to sql
def syncAccount():
    path = "D://low-account"
    listAccount = os.listdir(path)
    mycursor = mydb.cursor()
    for account in listAccount:
        sql = "INSERT INTO account_data_low(email,password) VALUES(%s,%s) ON DUPLICATE KEY UPDATE email=VALUES(email)"
        val = [account,"@bobby123@"]
        mycursor.execute(sql,val)
        mydb.commit()

#To get new account from server
def getAccount():
    
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT email FROM account_data_low")
    result = mycursor.fetchall()
    listAccount = []
    for row in result:
        listAccount.append(row['email'])
    
    #Get new account data
    url = "https://beyondlimit.co/api.php?f=olxMassLow"
    headers = {"accept": "application/json", 
            "content-type": "application/json", 
            }

    response = session.get(url, headers=headers)
    obj = response.json()
    accountNew = []
    for account in obj:
        #check if its already added
        state = account not in listAccount
        if state==True:
            accountNew.append(account)
    return accountNew

def getUrl(url):
    try:
        driver.implicitly_wait(20)
        time.sleep(3)
        driver.get
    except:
        pass
    #define tel number
    tel_num=""
    try:
        tel_clic = driver.find_element(By.XPATH,'//*[@id="container"]/main/div/div/div/div[5]/div[2]/div/div/div[3]/div[2]')
        if tel_clic!=None:
            tel_clic.click()
            time.sleep(6)
            #get tel num text
            tel_num = driver.find_element(By.XPATH,'//*[@id="container"]/main/div/div/div/div[5]/div[2]/div/div/div[3]/div').text
        
    except:
        pass
    
    if tel_num!="":
        return url,tel_num        
        
def doLogin(userEmail):
    driver.implicitly_wait(10)
    time.sleep(2)
    #when user is not logged in
    print('mencoba klik login/daftar')
    p = driver.find_element(By.XPATH,"//span[contains(text(),\'Login/Daftar')]")
    print('berhasil')
    action.move_to_element(p)
    # move to specific position
    #pyautogui.moveTo(50, 70, duration=1)
    # perform an left click of mouse
    #pyautogui.rightClick()        
    p.click()
    time.sleep(2)
    try:
        driver.implicitly_wait(5)
        print('mencoba klik login dengan email')
        go = driver.find_element(By.XPATH,'//*[@data-aut-id="emailLogin"]')
        go.click()    
        print('berhasil')
        time.sleep(3)
        try:
            driver.implicitly_wait(5)
            print('mengisi email')
            email = driver.find_element(By.ID,'email_input_field')
            email.send_keys(userEmail)
        except:
            driver.quit()
        time.sleep(3)
        print('mencoba klik tombol lanjut')
        em = driver.find_element(By.XPATH,"//span[contains(text(),\'Lanjut')]")
        em.click()
        time.sleep(3)            
        driver.implicitly_wait(10)
        print('mengisi password')
        password = driver.find_element(By.ID,'password')
        password.send_keys(userPass)
        print('mengirimkan login')
        em = driver.find_element(By.XPATH,'//*[@data-aut-id="login-form-submit"]')
        em.click()
        time.sleep(3)
        verify =""
        return True
    #already logged in
    except:
        return False

print('<== MASS LOGIN LOW ACCOUNTS ==>')

#To sync account from folder to sql
syncAccount()
#To get new account
accountList = getAccount()
userPass = '@bobby123@'
numberList = []

for account in accountList:
    programError = False
    grabUrl = True
    options = webdriver.ChromeOptions()

    # setting profile
    options.user_data_dir = "D:\\low-account\\profile"

    # another way to set profile is the below (which takes precedence if both variants are used
    options.add_argument('--no-sandbox')
    options.add_argument('--user-data-dir=D:\\low-account\\'+account)
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
    print('<==='+account+' membuka program chrome ===>') 
    if __name__ == "__main__":  
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(800, 600)
        #driver.minimize_window()
        action = ActionChains(driver)

        with driver:
            
            #open olx homepage
            print('membuka halaman utama olx')
            try:
                driver.get('https://www.olx.co.id')
            except:
                driver.get('https://www.olx.co.id')
            
            # check login
            try:
                driver.implicitly_wait(5)
                p = driver.find_element(By.XPATH,'//*[@data-aut-id="iconProfile"]')
                print('sudah login')
                grabUrl = False
            except:
                print('mencoba login')
                doLogin(account)
            
            # check login again [its already login, if its not then quit driver]
            try:
                driver.implicitly_wait(20)
                p = driver.find_element(By.XPATH,'//*[@data-aut-id="iconProfile"]')
                print('berhasil login')
            except:
                print('gagal login'+account)
                grabUrl = False
                programError = True
            
            #define url sample
            if grabUrl==True:
                urlSample = 'https://www.olx.co.id/item/dijual-bassura-city-apartment-2-br-iid-881358857'
                driver.get(urlSample)
                print('mencoba mengambil data nomor')
                getUrl(urlSample)
            if programError==False:
                print('valid: '+account)
                syncAccount()
            else:
                print('invalid '+account)
            print('menutup program')
            driver.quit()
            print('program tertutup')
            #To sync account from folder to sql
            syncAccount()
            print('menunggu 20 detik sebelum program selanjutnya berjalan\n\n')
            time.sleep(20)
            
print('program telah selesai, tertutup dalam 2 menit')
time.sleep(120)
quit()