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

# To clean accountCreator[x] folder
def cleanFolder():
    path = "D://low-account"
    listAccount = os.listdir(path)
    if len(listAccount) > 0:
        for account in listAccount:
            if "accountCreator" in account:
                shutil.rmtree(path+'/'+account)

# To sync account data from /temp folder to sql
def syncAccount():
    path = "D://low-account"
    listAccount = os.listdir(path)
    mycursor = mydb.cursor()
    for account in listAccount:
        if "accountCreator" not in account:
            sql = "INSERT INTO account_data_low(email,password) VALUES(%s,%s) ON DUPLICATE KEY UPDATE email=VALUES(email)"
            val = [account,"@bobby123@"]
            mycursor.execute(sql,val)
            mydb.commit()

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
        
def doRegister(userEmail):
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
        driver.implicitly_wait(5)            
        try:
            error = driver.find_element(By.XPATH,'//*[@data-aut-id="error-email"]')
            #String
            accountStatus = error.text
            if "ditangguhkan" in accountStatus:
                return False
            elif "Kesalahan login" in accountStatus:
                return False
        except:
            time.sleep(1)             
        verify =""
        return True
    #already logged in
    except:
        return False
    
def completeRegister(code):
    try:      
        #ENTERING OTP
        driver.implicitly_wait(10)
        try:
            otp1 = driver.find_element(By.XPATH,'//*[@data-aut-id="otp-box-1"]')
            otp1.send_keys(code[0])    
            time.sleep(1)
            otp2 = driver.find_element(By.XPATH,'//*[@data-aut-id="otp-box-2"]')
            otp2.send_keys(code[1])
            time.sleep(1)
            otp3 = driver.find_element(By.XPATH,'//*[@data-aut-id="otp-box-3"]')
            otp3.send_keys(code[2])
            time.sleep(1)
            otp4 = driver.find_element(By.XPATH,'//*[@data-aut-id="otp-box-4"]')
            otp4.send_keys(code[3])
            time.sleep(1)
        except:
            print('kesalahan input OTP')
            time.sleep(100)
        #Entering password
        driver.implicitly_wait(10)
        try:
            password1 = driver.find_element(By.ID,"password")    
            password1.send_keys('@bobby123@')
            password2 = driver.find_element(By.ID,"password-confirm")    
            password2.send_keys('@bobby123@')  
        except:
            print('gagal input password')
        time.sleep(2)
        try:
            driver.find_element(By.ID,'wzrk-cancel').click()
        except:
            print('gagal klik push notif button')
        time.sleep(2)
        try:
            driver.find_element(By.XPATH,"//button[.//span[contains(text(),'Buat kata sandi')]]").click()
            print('berhasil klik tombol sandi')
        except:
            print('gagal klik tombol password')            
        time.sleep(2)      
        try:
            driver.implicitly_wait(10)
            button = driver.find_element(By.XPATH,'//*[@data-aut-id="continueButton"]').click()
            time.sleep(1)
            button = driver.find_element(By.XPATH,'//*[@data-aut-id="continueButton"]').click()
            time.sleep(1)
            button = driver.find_element(By.XPATH,'//*[@data-aut-id="continueButton"]').click()
            time.sleep(1)
            button = driver.find_element(By.XPATH,'//*[@data-aut-id="continueButton"]').click()
            time.sleep(1)
        except:
            print('gagal melakukan finishing')
        verify =""
        return True
    #already logged in
    except:
        return False

print('<== MASS LOGIN LOW ACCOUNTS ==>')

programError = False
grabUrl = True
userPass = "@bobby123@"

print('membersihkan folder tidak terpakai')
cleanFolder()
print('STARTING PROGRAM')

for i in range(5):
    ###### OPENING ACCOUNT CREATOR BROWSER ######

    options = webdriver.ChromeOptions()

    # setting profile
    options.user_data_dir = "D:\\low-account\\profile"

    # another way to set profile is the below (which takes precedence if both variants are used
    options.add_argument('--no-sandbox')
    options.add_argument('--user-data-dir=D:\\low-account\\accountCreator'+str(i))
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
    print('<=== membuka program chrome ===>') 
    if __name__ == "__main__":  
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(800, 600)
        #driver.minimize_window()
        action = ActionChains(driver)

        with driver:
            
            #open disposable service
            driver.get('https://www.disposablemail.com/delete')
            #driver.get('https://www.disposablemail.com/')
            
            # check login
            try:
                driver.implicitly_wait(5)
                p = driver.find_element(By.ID,"email")
                userEmail = p.text
            except:
                print('terjadi kesalahan mengambil data email')
            
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            #open disposable service
            print('membuka homepage olx')
            driver.get('https://www.olx.co.id')
            status = doRegister(userEmail)
            if status==False:
                print('menutup program, karena terjadi kesalahan')
        
            #open disposable service [getting code]
            driver.switch_to.window(driver.window_handles[0])
            print('membuka email')    
            driver.implicitly_wait(5)
            driver.get('https://www.disposablemail.com/email/id/2')
            try:
                code = driver.find_element(By.TAG_NAME,"strong").text
            except:
                print('error')  
            #open disposable service
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(2)
            status = completeRegister(code)
            if status==False:
                print('menutup program, karena terjadi kesalahan')
            driver.quit()             
            time.sleep(3)                
            print('melanjutkan ke tahap login dalam 3 detik')            

    ###### LOGIN IN USER ######

    options = webdriver.ChromeOptions()

    # setting profile
    options.user_data_dir = "D:\\low-account\\profile"

    # another way to set profile is the below (which takes precedence if both variants are used
    options.add_argument('--no-sandbox')
    options.add_argument('--user-data-dir=D:\\low-account\\'+userEmail)
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
    print('<=== membuka program chrome ===>') 
    if __name__ == "__main__":  
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(800, 600)
        #driver.minimize_window()
        action = ActionChains(driver)

        with driver:
            
            #open olx homepage
            print('melakukan login')
            driver.get('https://www.olx.co.id')
            status = doLogin(userEmail)
            
            # check login again [its already login, if its not then quit driver]
            try:
                driver.implicitly_wait(20)
                p = driver.find_element(By.XPATH,'//*[@data-aut-id="iconProfile"]')
                print('berhasil login')
            except:
                print('gagal login'+userEmail)
                driver.get('https://www.olx.co.id')
                doLogin(userEmail)
                grabUrl = False
                programError = True
            
            #define url sample
            if grabUrl==True:
                urlSample = 'https://www.olx.co.id/item/samsung-a51-silver-8128-garansi-resmi-sein-iid-881274840'
                driver.get(urlSample)
                print('mencoba mengambil data nomor')
                getUrl(urlSample)
            if programError==False:
                print('valid: '+userEmail)
                syncAccount()
            else:
                print('invalid '+userEmail)
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