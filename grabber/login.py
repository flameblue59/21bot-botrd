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
import random
import sys
import json
import pyautogui
import shutil
import os

def getInit():
    # check account
    global userEmail
    path = 'C://temp'
    accountList = os.listdir(path)
    for account in accountList:
        if(account==userEmail):
            return False
        
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
        
def doLogin():
    driver.implicitly_wait(10)
    time.sleep(2)
        #when user is not logged in
    if logged==False:
        p = driver.find_element(By.XPATH,"//span[contains(text(),\'Login/Daftar')]")
        action.move_to_element(p)
        # move to specific position
        #pyautogui.moveTo(50, 70, duration=1)
        # perform an left click of mouse
        #pyautogui.rightClick()        
        p.click()
        time.sleep(2)
        try:
            driver.implicitly_wait(5)
            go = driver.find_element(By.XPATH,'//*[@data-aut-id="emailLogin"]')
            go.click()    
            time.sleep(3)
            try:
                driver.implicitly_wait(5)
                email = driver.find_element(By.ID,'email_input_field')
                email.send_keys(userEmail)
            except:
                driver.quit()
            time.sleep(3)
            em = driver.find_element(By.XPATH,"//span[contains(text(),\'Lanjut')]")
            em.click()
            time.sleep(3)            
            driver.implicitly_wait(10)
            password = driver.find_element(By.ID,'password')
            password.send_keys(userPass)
            em = driver.find_element(By.XPATH,'//*[@data-aut-id="login-form-submit"]')
            em.click()
            time.sleep(3)
            verify =""
            return True
        #already logged in
        except:
            return False

#credentials
userEmail = 'ibrahim.grady@doitups.com'
userPass = '@bobby123@'
logged = False

options = webdriver.ChromeOptions()

# setting profile
options.user_data_dir = "c:\\temp\\profile"

# another way to set profile is the below (which takes precedence if both variants are used
options.add_argument('--no-sandbox')
options.add_argument('--user-data-dir=c:\\temp\\'+userEmail)
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
print('membuka chrome')  
if __name__ == "__main__":  
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(800, 600)
    action = ActionChains(driver)
    #driver.maximize_window()

    with driver:
        
        #open olx homepage
        print('membuka olx homepage')
        try:
            driver.get('https://www.olx.co.id')
        except:
            driver.get('https://www.olx.co.id')
        
        # check login
        try:
            driver.implicitly_wait(20)
            p = driver.find_element(By.XPATH,'//*[@data-aut-id="iconProfile"]')
            driver.quit()
            print('akun sudah login, program keluar')
            quit()
        except:
            print('melakukan login')
            doLogin()
        print('checking login once again')
        # check login again [its already login, if its not then quit driver]
        try:
            driver.implicitly_wait(20)
            p = driver.find_element(By.XPATH,'//*[@data-aut-id="iconProfile"]')
        except:
            #shutil.rmtree('C://temp//'+userEmail)
            driver.quit()
            print('gagal login,folder dihapus')  
            quit()
        print('berhasil login')
        
        #define url sample
        urlSample = 'https://www.olx.co.id/item/dijual-ruko-salmon-golden-city-bengkong-laut-ruko-golden-prawn-iid-879809681'
        driver.get(urlSample)
        print('mencoba mengambil data nomor')
        getUrl(urlSample)
        
        print('menutup program')
        driver.quit()
        print('program tertutup')
        quit()