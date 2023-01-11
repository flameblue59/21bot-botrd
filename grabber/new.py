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

def set_page_load_timeout(self, time_to_wait):
    driver.refresh()

@retry(TimeoutError, tries=3)
@timeout(30)
def get_with_retry(driver, url):
    driver.get(url)

def bundleUrl():
    global urlList
    #read from php input
    after_json = sys.argv[1].replace("[","").replace("]","").replace("\\","")
    #define url list
    for i in range(len(after_json.split(","))):
        urlList.append(after_json.split(",")[i])
    return True 

#To get banned account
def getBanned():
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT email FROM banned_account")
    result = mycursor.fetchall()

    bannedAccount = []
    for row in result:
        bannedAccount.append(row['email'])
        
    return bannedAccount

def getNew():
    global userEmail,userPass
    #define username
    userEmail = sys.argv[3]
    #define password
    userPass = sys.argv[4]


def getExisting():
    global userEmail,urlList
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT email FROM account_data ORDER BY lastSync ASC"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    path = 'C://temp'
    accountFolder = os.listdir(path)    
    listAccount = []
    for row in result:
        if row['email'] in accountFolder:
            listAccount.append(row['email'])
    #get banned account
    listBanned = getBanned()
    for account in listAccount:
        if account in listBanned:
            listAccount.remove(account)        
    userEmail = random.choice(listAccount)
    
#To sync account usage
def updateLastSync(account):
    mycursor = mydb.cursor()
    sql = "UPDATE account_data SET lastSync=NOW() WHERE email=%s"
    val = [account]
    mycursor.execute(sql,val)
    mydb.commit()    

def getUrl(url):
    try:
        driver.implicitly_wait(10)
        time.sleep(1)
        driver.get(url)
    except:
        pass
    #define tel number
    tel_num=""
    try:
        tel_clic = driver.find_element(By.XPATH,'//*[@id="container"]/main/div/div/div/div[5]/div[2]/div/div/div[3]/div[2]')
        if tel_clic!=None:
            tel_clic.click()
            time.sleep(4)
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
            print('gagal')

#credentials
urlList = []
userEmail = 'test@gmail.com'
userPass = '1234'
logged = False
numberList = []

#initial state [set userEmail, userPass and urlList]
choice = random.randint(0,100)
if choice > 100:
    getNew()
else:
    getExisting()
    
#bundling url
bundleUrl()

options = webdriver.ChromeOptions()

# setting profile
options.user_data_dir = "c:\\temp\\profile"

# another way to set profile is the below (which takes precedence if both variants are used
options.add_argument('--user-data-dir=c:\\temp\\'+userEmail)
options.add_argument('--start-maximized')
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
driver = webdriver.Chrome(options=options)
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
        
    # if password is not set then quit
    if userPass=='1234' and logged==False:
        # delete directory since its session already over
        print('banned=>'+userEmail);
        shutil.rmtree('C://temp/'+userEmail)
        driver.quit()
        
    # check login again [its already login, if its not then quit driver]
    try:
        driver.implicitly_wait(20)
        p = driver.find_element(By.XPATH,'//*[@data-aut-id="iconProfile"]')
    except:
        print('banned=>'+userEmail);
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
        updateLastSync(userEmail)
        print(objJson)
    except:
        driver.quit()