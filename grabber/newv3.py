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
    #read from php input
    after_json = sys.argv[1].replace("[","").replace("]","").replace("\\","")
    after_json = json.loads(after_json)
    return after_json 

#To get banned account
def getBanned():
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT email FROM banned_account")
    result = mycursor.fetchall()

    bannedAccount = []
    for row in result:
        bannedAccount.append(row['email'])
        
    return bannedAccount


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
    return userEmail
    
#To sync account usage
def updateLastSync(account):
    mycursor = mydb.cursor()
    sql = "UPDATE account_data SET lastSync=NOW() WHERE email=%s"
    val = [account]
    mycursor.execute(sql,val)
    mydb.commit()   

#We need to state UID in order to read User API Data
def getUrl(targetUrl,uid):
    try:
        url = 'https://www.olx.co.id/api/users/'+uid
        driver.get(url)
        time.sleep(1)
    except:
        return
    #Getting json data
    try:
        driver.implicitly_wait(5)
        #Getting json data
        content = driver.find_element(By.TAG_NAME,'body').text
        result = json.loads(content)
    except:
        print('gagal mengambil json')
        pass
    try:
        if result['error']:
            print('opss.. nampaknya akun telah dibanned')  
            return
    except:
        print('json valid, melanjutkan program')
    try:
        if len(result['data'])==0:
            print('data kosong, kemungkinan akun dibanned.. mengecek status login')
            scriptError = True
            return
    except:
        print('data member tidak ditemukan..')  
        return
    #Getting number              
    try:
        if result['data']['phone'] is None:
            print('nomor handphone tidak ditemukan')
            scriptError = True
            return
    except:
        print('nomor handphone ditemukan')
        return
    try:
        phone = result['data']['phone']
        name = result['data']['name']
        if name is None:
            name = 'user'
        if "+62" in phone:
            phone = phone.replace('+62','0')      
    except:
        print('gagal mendapatkan nomor telepon')
        return
    #define tel number
    print(phone)
    if phone!=None:
        return targetUrl,phone,uid,name
    
#To send banned
def sendBanned(account):
    mycursor = mydb.cursor()
    sql = "INSERT INTO banned_account(email) VALUES(%s) ON DUPLICATE KEY UPDATE tries=tries+1"
    val = [account]
    mycursor.execute(sql,val)
    mydb.commit()

#bundling url
urlList = bundleUrl()
#credentials
userEmail = getExisting()
userPass = '@bobby123@'
logged = False
numberList = []

if userEmail=='error':
    print('tidak ada data akun')
    quit()

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
    errorScript = False
    updateLastSync(userEmail)
    #open olx homepage
    try:
        driver.get('https://www.olx.co.id')
    except:
        driver.get('https://www.olx.co.id')
        
    # check login again [its already login, if its not then quit driver]
    try:
        driver.implicitly_wait(5)
        p = driver.find_element(By.XPATH,'//*[@data-aut-id="iconProfile"]')
    except:
        print('output==>banned:'+userEmail);
        sendBanned(userEmail)
        errorScript = True
        driver.quit()
    
    if errorScript==False:
        try:
            for uid in urlList:
                url = urlList[uid]
                tel = getUrl(url,uid)
                if tel!=None:
                    numberList.append(tel)
            
            data=[]
            for obj in numberList:
                url,tel_num,uid,name = obj
                data.append({
                    "website":url,
                    "telnumber":tel_num,
                    "uid":uid,
                    "name":name
                })
                
            objJson = json.dumps(data)
            print('==>'+objJson)
        except:
            driver.quit()
    quit()