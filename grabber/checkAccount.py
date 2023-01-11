import undetected_chromedriver.v2 as uc
from  selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
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
    global accountList
    path = 'C://temp'
    accountList = os.listdir(path)
    
        
def doLogin():
    driver.implicitly_wait(10)
    time.sleep(4)
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
accountList = []
accountInvalid = []
# to read account list from C://temp folder
status = getInit()

for account in accountList:
    options = webdriver.ChromeOptions()

    # setting profile
    options.user_data_dir = "c:\\temp\\profile"

    # another way to set profile is the below (which takes precedence if both variants are used
    options.add_argument('--user-data-dir=c:\\temp\\'+account)
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
    if __name__ == "__main__":
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(800, 600)
        action = ActionChains(driver)
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win64",
                webgl_vendor="NVIDIA.",
                renderer="AMD Iris OpenGL Engine",
                fix_hairline=True,
                )

        with driver:
            driver.implicitly_wait(15)
            driver.get('https://www.olx.co.id')
            time.sleep(2)
            # to check if user logged in
            try:
                p = driver.find_element(By.XPATH,'//*[@data-aut-id="iconProfile"]')
                print('valid :'+account)
            except:
                # shutil.rmtree('C://temp/'+account)
                print('invalid :'+account)
            driver.quit()
            time.sleep(5)