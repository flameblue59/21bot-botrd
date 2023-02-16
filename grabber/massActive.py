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
import requests

session = requests.Session()

mydb = mysql.connector.connect(
    host="localhost",
    username="root",
    password="",
    database="bot_number"
)

#To delete account from banned server
def sendDelete(account):
    mycursor = mydb.cursor()
    sql = "DELETE FROM banned_account WHERE email=%s"
    val = [account]
    mycursor.execute(sql,val)
    mydb.commit()

#To send banned if the account permanently banned
def sendBanned(account):
    mycursor = mydb.cursor()
    sql = "UPDATE banned_account SET banned=true,bannedTime=CURRENT_TIMESTAMP() WHERE email=%s"
    val = [account]
    mycursor.execute(sql,val)
    mydb.commit()

#To get new account from server
def getAccount():
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT email FROM banned_account WHERE banned=false")
    result = mycursor.fetchall()
    listAccount = []
    for row in result:
        listAccount.append(row['email'])
    
    return listAccount

def getUrl(url):
    try:
        driver.implicitly_wait(20)
        time.sleep(3)
        driver.get(url)
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
        try:
            error = driver.find_element(By.XPATH,'//*[@data-aut-id="error-email"]')
            #String
            accountStatus = error.text
            if "ditangguhkan" in accountStatus:
                sendBanned(userEmail)
                return False
            elif "Kesalahan login" in accountStatus:
                return False
        except:
            time.sleep(1)        
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
    

#To get new account [LIST]
accountList = getAccount()
userPass = '@bobby123@'
numberList = []
grabUrl = True
options = webdriver.ChromeOptions()

for account in accountList:
    programError = False
    try:
        # setting profile
        options.user_data_dir = "D:\\olx\\profile"

        # another way to set profile is the below (which takes precedence if both variants are used
        #options.add_argument('--no-sandbox')
        options.add_argument('--user-data-dir=D:\\olx\\'+account)
        #options.add_argument('--incognito')
        #options.add_argument('--start-fullscreen')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('disable-infobars')
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-blink-features")
        options.add_argument('--disable-blink-features=AutomationControlled')
        #options.add_argument('--start-maximized')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # just some options passing in to skip annoying popups
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')   
        driver = webdriver.Chrome(options=options)
    except:
        print('terjadi kesalahan pada akun '+account)
    driver.minimize_window()
    #driver.switch_to.new_window('window')
    action = ActionChains(driver)
    #driver.set_window_size(800, 600)
    driver.maximize_window()
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win64",
        webgl_vendor="NVIDIA.",
        renderer="AMD Iris OpenGL Engine",
        fix_hairline=True,
    )

    print('<==='+account+' membuka program chrome ===>') 
    
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
            urlSample = 'https://www.olx.co.id/item/dijual-ruko-salmon-golden-city-bengkong-laut-ruko-golden-prawn-iid-879809681'
            driver.get(urlSample)
            print('mencoba mengambil data nomor')
            getUrl(urlSample)
        if programError==False:
            #delete account
            sendDelete(account)
            print('valid: '+account)
        else:
            print('invalid '+account)
        print('menutup program')
        driver.quit()
        print('program tertutup')
        print('menunggu 20 detik sebelum program selanjutnya berjalan\n\n')
        time.sleep(20)
            
print('program telah selesai, tertutup dalam 2 menit')
time.sleep(120)
quit()