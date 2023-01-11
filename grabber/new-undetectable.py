import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.common.action_chains import ActionChains
from retry import retry
from timeout_decorator import timeout, TimeoutError
import time
import random
import sys
import json
import pyautogui

def set_page_load_timeout(self, time_to_wait):
    driver.refresh()

@retry(TimeoutError, tries=3)
@timeout(30)
def get_with_retry(driver, url):
    driver.get(url)

def getInit():
    global userEmail,userPass,urlList
    after_json = sys.argv[1].replace("[","").replace("]","").replace("\\","")
    #define username
    userEmail = sys.argv[3]
    #define password
    userPass = sys.argv[4]
    #define url list
    for i in range(len(after_json.split(","))):
        urlList.append(after_json.split(",")[i])
    return True 

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
            driver.implicitly_wait(30)
            go = driver.find_element(By.XPATH,'//*[@data-aut-id="emailLogin"]')
            go.click()    
            time.sleep(3)
            email = driver.find_element(By.ID,'email_input_field')
            email.send_keys(userEmail)
            time.sleep(3)
            em = driver.find_element(By.XPATH,"//span[contains(text(),\'Lanjut')]")
            em.click()
            driver.implicitly_wait(20)
            time.sleep(3)
            password = driver.find_element(By.ID,'password')
            password.send_keys(userPass)
            em = driver.find_element(By.XPATH,'//*[@data-aut-id="login-form-submit"]')
            em.click()
            time.sleep(3)
            verify =""
            return True
        #already logged in
        except:
            print('gagal')

#credentials
urlList = []
userEmail = 'test@gmail.com'
userPass = '1234'
logged = False
numberList = []

#initial state [set userEmail, userPass and urlList]
getInit()

options = uc.ChromeOptions()

# setting profile
options.user_data_dir = "c:\\temp\\profile"

# another way to set profile is the below (which takes precedence if both variants are used
options.add_argument('--user-data-dir=c:\\temp\\'+userEmail)
#options.add_argument('--start-maximized')

# just some options passing in to skip annoying popups
options.add_argument('--no-first-run --no-service-autorun --password-store=basic enable_console_log = True')
if __name__ == "__main__":
    driver = uc.Chrome(options=options,version_main=94,use_subprocess=True)
    action = ActionChains(driver)
    #driver.maximize_window()

    with driver:
        
        #open olx homepage
        try:
            driver.get('https://www.olx.co.id')
        except:
            driver.get('https://www.olx.co.id')
        
        time.sleep(5)

        # to check if user logged in
        try:
            p = driver.find_element(By.XPATH,'//*[@data-aut-id="iconProfile"]')
            logged = True
        except:
            logged = False
            
        #do login (if not logged in)
        try:
            if logged==False:
                time.sleep(2)
                doLogin()
        except:
            driver.quit()
            
        # check login again [its already login, if its not then quit driver]
        try:
            driver.implicitly_wait(20)
            p = driver.find_element(By.XPATH,'//*[@data-aut-id="iconProfile"]')
        except:
            driver.quit()       
        
        try:
            for i in range(len(urlList)):
                url = urlList[i]
                tel = getUrl(url)
                if tel!=None:
                    numberList.append(tel)
            
            data=[]
            for obj in numberList:
                url,tel_num = obj
                data.append({
                    "website":url,
                    "telnumber":tel_num
                })
                
            objJson = json.dumps(data)
            print(objJson)
        except:
            driver.quit()