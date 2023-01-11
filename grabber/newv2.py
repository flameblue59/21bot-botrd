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


def getExisting():
    global userEmail,urlList
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT email FROM account_data_low WHERE logout=false and banned=false ORDER BY lastSync ASC"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    path = 'D://low-account'
    accountFolder = os.listdir(path)    
    listAccount = []
    for row in result:
        if row['email'] in accountFolder:
            listAccount.append(row['email'])    
    if len(listAccount) > 0:
        userEmail = random.choice(listAccount)
    else:
        userEmail = 'error'
    return userEmail
    
#To sync account usage
def updateLastSync(account):
    mycursor = mydb.cursor()
    sql = "UPDATE account_data_low SET lastSync=NOW() WHERE email=%s"
    val = [account]
    mycursor.execute(sql,val)
    mydb.commit()    

def getUrl(url):
    try:
        driver.get(url)
    except:
        pass
    try:
        driver.implicitly_wait(5)        
        profileLink = driver.find_element(By.XPATH,'//*[@data-aut-id="profileCard"]//a').get_attribute('href')
        list = profileLink.split('profile/')
        uid = list[1]        
        if uid != None:
            urlProfile = 'https://www.olx.co.id/api/users/'+uid
            driver.get(urlProfile)
        else:
            pass        
    except:
        print('gagal mengambil link profil')
        return
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
            pass
    except:
        print('melanjutkan program')
        pass
    try:
        if len(result['data'])==0:
            print('data kosong, kemungkinan akun dibanned.. mengecek status login')
            scriptError = True
            pass
    except:
        print('nomor handphone ditemukan, kembali mengecek status login..')  
    #Getting number              
    try:
        if result['data']['phone'] is None:
            print('nomor handphone tidak ditemukan')
            scriptError = True
            pass
    except:
        print('nomor handphone ditemukan')
    try:
        phone = result['data']['phone']
        name = result['data']['name']
        if name is None:
            name = 'user'
        if "+62" in phone:
            phone = phone.replace('+62','0')   
    except:
        print('gagal mendapatkan nomor telepon')
        pass 
    #define tel number
    if phone!=None:
        return url,phone
    
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
            
#To send banned
def sendBanned(account):
    mycursor = mydb.cursor()
    sql = "UPDATE account_data_low SET logout=true WHERE email=%s"
    val = [account]
    mycursor.execute(sql,val)
    mydb.commit()

#credentials
urlList = []
userEmail = getExisting()
userPass = '@bobby123@'
logged = False
numberList = []

if userEmail=='error':
    print('tidak ada data akun')
    quit()

#initial state [set userEmail, userPass and urlList]
choice = random.randint(0,100)
#bundling url
bundleUrl()

print(urlList)

options = webdriver.ChromeOptions()

# setting profile
options.user_data_dir = "D:\\low-account\\\\profile"

# another way to set profile is the below (which takes precedence if both variants are used
options.add_argument('--user-data-dir=D:\\low-account\\'+userEmail)
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
            print('==>'+objJson)
        except:
            driver.quit()
    quit()