from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import myConn
from tool.main import tool
import time
import requests
import random
import sys
import json
import math
import os
    
filePath = tool.filePath()
slashDir = '/'

def getAccount():
    mycursor = myConn.mydb.cursor(dictionary=True)
    sql = "SELECT email,password FROM tiktok_account WHERE nextRun < NOW() ORDER BY nextRun ASC"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    if len(result)==0:
        return False
    return result[0]['email'],result[0]['password']

def updateAccount(email):
    #update next run
    mycursor = myConn.mydb.cursor(dictionary=True)
    sql = "UPDATE tiktok_account SET nextRun=DATE_ADD(NOW(),INTERVAL 3 MINUTE) WHERE email=%s"
    value = [email]
    mycursor.execute(sql,value)
    myConn.mydb.commit()

def sendActivity(email,type,activityId):
    mycursor = myConn.mydb.cursor()
    sql = "UPDATE tiktok_account SET "+type+"="+type+"+1 WHERE email=%s"
    val = [email]
    mycursor.execute(sql,val)
    myConn.mydb.commit()
    #delete activity
    mycursor = myConn.mydb.cursor()
    sql = "DELETE FROM tiktok_activity WHERE id=%s"
    val = [activityId]
    mycursor.execute(sql,val)
    myConn.mydb.commit()
    
def getActivity(email):
    mycursor = myConn.mydb.cursor(dictionary=True)
    sql = "SELECT id,activity FROM tiktok_account WHERE done=0 and runAt < NOW() and email=%s ORDER BY runAt ASC"
    val = [email]
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    return result

def checkLogin():
    elem = "//a[contains(@href,\'/messages')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('webdriver check login error')
    finally:
        try:
            login = driver.find_element(By.XPATH,elem)
            return True             
        except:
            print('tidak menemukan input email')          
    
    return False
    

def doLogin():
    tool.superGet(driver,'https://www.tiktok.com/login/phone-or-email/email')     
    
    #fill detail
    elem = "//input"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    finally:
        try:
            input = driver.find_elements(By.XPATH,elem)
            for obj in input:
                name = obj.get_attribute('name')
                if name=='username':
                    obj.send_keys(email)
                elif name=='':
                    obj.send_keys(password)                        
        except:
            print('tidak menemukan input email')            
    
    #click login button
    elem = "//button[@data-e2e='login-button']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    finally:
        try:
            goLogin = driver.find_element(By.XPATH,elem)
            tool.customClick(driver,goLogin)
        except:
            print('tidak menemukan login button')     

#get account
account = getAccount()
if account==False:
    print('tidak ada akun yang tersedia')
    quit()
    
email,password = account

#updateAccount(email)
    
#get activity [LATER]
#activityList = getActivity(email)

options = webdriver.ChromeOptions()
# setting profile
options.user_data_dir = filePath

prefs = {"profile.default_content_setting_values.notifications" : 2}
# another way to set profile is the below (which takes precedence if both variants are used
options.add_argument('--no-sandbox')
options.add_argument('--user-data-dir='+filePath+'chromeprofile'+slashDir+'tiktok'+slashDir+email)
#options.add_argument('--incognito')
#options.add_argument('--start-fullscreen')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-infobars')
options.add_argument('--disable-notifications')
options.add_argument('--disable-gpu')
options.add_argument('--disable-blink-features=AutomationControlled')
#options.add_argument('--start-maximized')
options.add_experimental_option("excludeSwitches", ["enable-automation","enable-logging"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("prefs",prefs)
# just some options passing in to skip annoying popups
options.add_argument('--no-first-run --no-service-autorun --password-store=basic')   
if __name__ == "__main__":  
    driver = webdriver.Chrome(options=options)
    #driver.minimize_window()
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win64",
            webgl_vendor="ANGLE (Apple, Apple M1 Pro, OpenGL 4.1)",
            renderer="AMD Iris OpenGL Engine",
            fix_hairline=True,
            )    
    action = ActionChains(driver)

    with driver:
        
        #go to homepage
        tool.superGet(driver,'https://www.tiktok.com/en/')
        time.sleep(tool.randomNumber(5)) 
        
        #check login
        status = checkLogin()
        if status==False:
            doLogin()
            
        #go to profile
        tool.superGet(driver,'https://www.tiktok.com/@dsimlife')
        time.sleep(tool.randomNumber(10))
        
        #go back to homepage
        tool.superGet(driver,'https://www.tiktok.com/en/')  
            
        #start like
        elem = "//span[@data-e2e='like-icon']"
        try:
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,elem)))
        except Exception as e:
            print('kesalahan webdriver start like => '+str(e))
        else:
            try:
                goLike = driver.find_elements(By.XPATH,elem)
                for obj in goLike:
                    time.sleep(tool.randomNumber(10))
                    tool.customClick(driver,obj)
                    time.sleep(tool.randomNumber(5))
                    tool.scrollDown(driver)
            except:
                print('kesalahan saat like')

        activity = 10
        while activity > 0:
            activity += 1
            tool.superGet(driver,'https://www.tiktok.com/en/')
            time.sleep(tool.randomNumber(20))
            #try to click for you
            elem = '//a[data-e2e="nav-foryou"]'
            try:
                WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,elem)))
            except Exception as e:
                print('kesalahan webdriver start following => '+str(e))
            finally:
                try:
                    forYou = driver.find_element(By.XPATH,elem)
                    tool.customClick(driver,forYou)
                except:
                    print('tombol for you tidak ada')
            time.sleep(tool.randomNumber(10))
            #start following
            elem = "//span[@data-e2e='comment-icon']"
            try:
                WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.XPATH,elem)))
            except Exception as e:
                print('kesalahan webdriver start following => '+str(e))
            else:
                try:
                    goVideo = driver.find_elements(By.XPATH,elem)
                    sum = len(goVideo)-1
                    rand = random.randint(0,sum)
                    tool.customClick(driver,goVideo[rand])
                except:
                    print('tidak bisa menemukan video')
                    
            #collecting profiles
            elem = "//a[@data-e2e='comment-avatar-1']"
            try:
                WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,elem)))
            except Exception as e:
                print('kesalahan webdriver collecting profiles => '+str(e))            
            else:
                try:
                    #watch 4-5 video
                    watch = random.randint(4,5)
                    while watch > 0:
                        watch -= 1
                        time.sleep(tool.randomNumber(60))
                        elem = '//button[data-e2e="arrow-right"]'
                        next = driver.find_element(By.XPATH,elem)
                        tool.customClick(driver,next)
                    profile = driver.find_elements(By.XPATH,elem)
                    sum = len(profile)-1
                    rand = random.randint(0,sum)
                    tool.customClick(driver,profile[rand])
                except:
                    print('tidak bisa menemukan list profile') 
                    
            #follow user
            elem = "//button[@data-e2e='follow-button']"
            try:
                WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,elem)))
            except Exception as e:
                print('kesalahan webdriver follow user => '+str(e))            
            else:
                try:
                    follow = driver.find_element(By.XPATH,elem)
                    tool.customClick(driver,follow)
                except:
                    print('tidak tombol follow')        
                    
            driver.refresh()
            
            time.sleep(tool.randomNumber(10))
            print('mengecek follow lagi')
            #follow user
            elem = "//button[@data-e2e='follow-button']"
            try:
                WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,elem)))
            except Exception as e:
                print('kesalahan webdriver follow user => '+str(e))            
            else:
                try:
                    follow = driver.find_element(By.XPATH,elem)
                    tool.customClick(driver,follow)
                except:
                    print('tidak tombol follow')                
                    
        #login success
        time.sleep(500)