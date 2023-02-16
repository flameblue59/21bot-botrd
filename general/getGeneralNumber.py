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

def checkLogin():
    #open olx homepage
    try:
        driver.get('https://www.olx.co.id')
    except:
        driver.get('https://www.olx.co.id')
    
    time.sleep(2)

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
        driver.quit()

def getUID():
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT id,start,end FROM olx_pool WHERE done=false ORDER BY rendered ASC"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    mycursor = mydb.cursor()
    sql = "UPDATE olx_pool SET rendered=CURRENT_TIMESTAMP() WHERE id=%s"
    val = [result[0]['id']]
    mycursor.execute(sql,val)
    mydb.commit()
    return result[0]

def updateUID(uid,poolId):
    mycursor = mydb.cursor()
    sql = "UPDATE olx_pool SET start=%s WHERE id=%s"
    val = [uid,poolId]
    mycursor.execute(sql,val)
    mydb.commit()
    mycursor = mydb.cursor()
    sql = "UPDATE olx_pool SET done=true WHERE start >= end and id=%s"
    val = [poolId]
    mycursor.execute(sql,val)
    mydb.commit()

def getExisting():
    global userEmail,urlList
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT email FROM account_data_low WHERE logout=false ORDER BY lastSync ASC"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    path = 'D://low-account'
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
    
#To send number
def sendNumber(source,uid,name,number):
    mycursor = mydb.cursor()
    sql = "INSERT INTO number_vault(category,subCategory,source,uid,name,number) VALUES ('general','general',%s,%s,%s,%s) ON DUPLICATE KEY UPDATE number=number"
    val = [source,uid,name,number]
    mycursor.execute(sql,val)
    mydb.commit()
    
#To get banned account
def getBanned():
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT email FROM banned_account")
    result = mycursor.fetchall()

    bannedAccount = []
    for row in result:
        bannedAccount.append(row['email'])
        
    return bannedAccount

#To sync account usage
def updateLastSync(account):
    mycursor = mydb.cursor()
    sql = "UPDATE account_data_low SET lastSync=NOW() WHERE email=%s"
    val = [account]
    mycursor.execute(sql,val)
    mydb.commit()
    
#To send banned
def sendBanned(account):
    mycursor = mydb.cursor()
    sql = "UPDATE account_data_low SET logout=true WHERE email=%s"
    val = [account]
    mycursor.execute(sql,val)
    mydb.commit()

#credentials
uid = 0;
urlList = []
userEmail = 'test@gmail.com'
userPass = '1234'
logged = False
delayTime = 2

#get init, to get UID
objectUID = getUID()
poolID = objectUID['id']
currentUID = int(objectUID['start'])
#initial state [set userEmail, userPass and urlList]
userEmail = getExisting()

options = webdriver.ChromeOptions()

# setting profile
options.user_data_dir = "D:\\low-account\\profile"

# another way to set profile is the below (which takes precedence if both variants are used
options.add_argument('--user-data-dir=D:\\low-account\\'+userEmail)
#options.add_argument('--start-maximized')
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
#driver.switch_to.new_window('window')
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
    
    checkLogin()
        
    # check login again [its already login, if its not then quit driver]
    try:
        driver.implicitly_wait(20)
        p = driver.find_element(By.XPATH,'//*[@data-aut-id="iconProfile"]')
    except:
        print('banned=>'+userEmail);
        sendBanned(userEmail)
        driver.quit()       
    try:
        scriptError = False
        for i in range(10):
            if scriptError:
                scriptError = False
                checkLogin()
            uid = str(currentUID+i)
            url = 'https://www.olx.co.id/api/users/'+uid
            driver.get(url)
            print('<== membuka url ==>')
            print(url)
            #Getting json data
            content = driver.find_element(By.TAG_NAME,'body').text
            result = json.loads(content)
            try:
                if result['error']:
                    print('opss.. nampaknya akun telah dibanned')      
                    continue
            except:
                print('melanjutkan program')
            try:
                if len(result['data'])==0:
                    print('data kosong, kemungkinan akun dibanned.. mengecek status login')
                    scriptError = True
                    continue
            except:
                print('nomor handphone ditemukan, kembali mengecek status login..')  
            #Getting number              
            try:
                if result['data']['phone'] is None:
                    print('nomor handphone tidak ditemukan')
                    scriptError = True
                    continue
            except:
                print('nomor handphone ditemukan')
            phone = result['data']['phone']
            name = result['data']['name']
            if name is None:
                name = 'user'
            if "+62" in phone:
                phone = phone.replace('+62','0')
            sendNumber('olx.co.id',uid,name,phone)
            updateUID(currentUID+i,poolID)
            print('mengirimkan nomor '+phone+' ke database')
            print('menunggu '+str(delayTime)+' detik untuk berjalan kembali')
            time.sleep(delayTime)
    except:
        driver.quit()
    updateLastSync(userEmail)        
    driver.quit()
    quit()
    