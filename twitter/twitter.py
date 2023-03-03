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
import time
import requests
import random
import sys
import json
import math
import os
#importing our custom files
import myConn
from tool.main import tool
import main

filePath = tool.filePath()
slashDir = '/'

def getAccount():
    mycursor = myConn.mydb.cursor(dictionary=True,buffered=True)
    sql = "SELECT email,password FROM twitter_account WHERE nextRun < NOW() ORDER BY nextRun ASC"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    if len(result)==0:
        return False
    return result[0]['email'],result[0]['password']

def updateAccount(email):
    #update next run
    mycursor = myConn.mydb.cursor(dictionary=True,buffered=True)
    sql = "UPDATE twitter_account SET nextRun=DATE_ADD(NOW(),INTERVAL 3 MINUTE) WHERE email=%s"
    value = [email]
    mycursor.execute(sql,value)
    myConn.mydb.commit()

def sendActivity(email,type,activityId):
    mycursor = myConn.mydb.cursor()
    sql = "UPDATE twitter_account SET "+type+"="+type+"+1 WHERE email=%s"
    val = [email]
    mycursor.execute(sql,val)
    myConn.mydb.commit()
    #delete activity
    mycursor = myConn.mydb.cursor()
    sql = "DELETE FROM twitter_activity WHERE id=%s"
    val = [activityId]
    mycursor.execute(sql,val)
    myConn.mydb.commit()

def getActivity(email):
    res = []
    mycursor = myConn.mydb.cursor(dictionary=True,buffered=True)
    sql = "SELECT id,activity FROM twitter_activity WHERE done=0 and runAt < NOW() and email=%s ORDER BY runAt ASC"
    val = [email]
    mycursor.execute(sql,val)
    if mycursor.rowcount > 0:
        res = mycursor.fetchall()
    return res

def runActivity(activity,activityId):
    status = False
    if activity=='likes':
        status = main.doLike(driver)
    elif activity=='follow':
        words = ['berita','lucu','penghasil uang']
        word = random.choice(words)
        tool.superGet(driver,'https://twitter.com/search?q='+word+'&src=typed_query&f=top')
        status = main.doFollow(driver)
    elif activity=='unfollow':
        status = main.doUnfollow(driver)
    elif activity=='tweet':
        #randomize between image and video
        media = ['image','video']
        mediaType = random.choice(media)        
        statusText = tool.getStatus('thesimlife','id') 
        status = doTweet(mediaType,statusText)
    elif activity=='retweet':
        status = doRetweet()
    elif activity=='comment':
        commentText = tool.getComment('general','id')
        status = main.doComment(driver,commentText) 
    #send activity
    if status==True:
        sendActivity(email,activity,activityId)
    
    return status

def doTweet(mediaType,statusText):
    if mediaType=='image':
        #setup image
        imagePath,filename = tool.getPhoto(email,'thesimlifeImage')
    elif mediaType=='video':
        #setup video
        imagePath,filename = tool.getVideo(email,'thesimlifeVideo')
        
    #send status
    elem = "//div[@class='public-DraftStyleDefault-block public-DraftStyleDefault-ltr']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver send status text')
    else:
        try:
            statusBox = driver.find_element(By.XPATH,elem)
            statusBox.send_keys(statusText)
        except Exception as e:
            print('tidak dapat menemukan send status text')
    
    #uploading image
    time.sleep(tool.randomNumber(4))
    elem = "//input[@accept='image/jpeg,image/png,image/webp,image/gif,video/mp4,video/quicktime']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver upload image')
        return False
    else:
        try:
            uploadImage = driver.find_element(By.XPATH,elem)
            uploadImage.send_keys(imagePath)
        except Exception as e:
            print('tidak dapat menemukan input upload image'+str(e))
            return False
        
    #when it is video, we need to wait up to 20 seconds since we have not set the callback
    #span[contains(text(),\'Uploaded')])
    if mediaType=='video':
        elem = "//span[contains(text(),\'Uploaded')]"
        try:
            WebDriverWait(driver,60).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
        except:
            print('kesalahan saat upload, sudah lebih dari 60 detik')
            return False
        else:
            try:
                print('berhasil melakukan upload video')
            except Exception as e:
                print('gagal melakukan upload')
                return False        
    #next button [wait for uploading image]
    elif mediaType=='image':
        time.sleep(tool.randomNumber(8))
    elem = "//div[@data-testid='toolBar']//span[contains(text(),\'Tweet')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver next button [next]')
        return False
    else:
        try:
            nextButton = driver.find_element(By.XPATH,elem)
            tool.customClick(driver,nextButton)
            #send posted image to server [so it wont posted anymore]
            mycursor = myConn.mydb.cursor(dictionary=True)
            sql = "INSERT INTO posted_twitter(email,mediaType,filename) VALUES(%s,%s,%s)"
            val = [email,mediaType,filename]
            mycursor.execute(sql,val)
            myConn.mydb.commit()
            print('berhasil memosting')            
            return True
        except Exception as e:
            print('tidak dapat menemukan next button [next]'+str(e))   
            return False    

def doRetweet():
    tool.scrollDown(driver)
    time.sleep(tool.randomNumber(4))    
    #get random post and click retweet button
    elem = "//div[contains(@aria-label,\'Retweet')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver retweet button')
    else:
        try:
            retweetButton = driver.find_elements(By.XPATH,elem)
            sum = len(retweetButton)-1
            rand = random.randint(0,sum)
            tool.customClick(driver,retweetButton[rand])
        except Exception as e:
            print('tidak dapat menemukan retweet button')    
            
    #confirm retweet
    time.sleep(tool.randomNumber(4))
    elem = "//div[@data-testid='retweetConfirm']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver confirm retweet')
    else:
        try:
            confirmRetweet = driver.find_element(By.XPATH,elem)
            tool.customClick(driver,confirmRetweet)
            return True
        except Exception as e:
            print('tidak dapat menemukan confirm retweet')     
    return False  

def randomActivity(driver):
    activity = random.randint(2,4)
    while activity > 0:
        try:
            walk = random.randint(0,100)
            if walk > 70:
                #profileWalk()
                time.sleep(tool.randomNumber(10))
            tool.scrollDown(driver)
            time.sleep(tool.randomNumber(4))
            activity -= 1
        except:
            print('opps terjadi kesalahan random activity')
            continue      
        
#get account
account = getAccount()
if account==False:
    print('tidak ada akun yang tersedia')
    quit()
    
email,password = account

updateAccount(email)
    
#get activity
activityList = getActivity(email)
if len(activityList)==0:
    print('tidak ada aktifitas saat ini')
    time.sleep(2)
    quit()
options = webdriver.ChromeOptions()
# setting profile
options.user_data_dir = filePath

prefs = {"profile.default_content_setting_values.notifications" : 2}
# another way to set profile is the below (which takes precedence if both variants are used
options.add_argument('--no-sandbox')
options.add_argument('--user-data-dir='+filePath+'chromeprofile'+slashDir+'twitter'+slashDir+email)
#options.add_argument('--incognito')
#options.add_argument('--start-fullscreen')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-infobars')
options.add_argument('--disable-notifications')
options.add_argument('--disable-gpu')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--start-maximized')
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
            
        tool.superGet(driver,'https://twitter.com')

        #start doing login
        check = main.checkLogin(driver)
        if check==False:
            tool.superGet(driver,'https://twitter.com/login')
            main.doLogin(driver,email,password)
            #return back to homepage
            tool.superGet(driver,'https://twitter.com/home')
        
        for obj in activityList:
            try:
                time.sleep(tool.randomNumber(4))
                print('melakukan pekerjaan: '+obj['activity'])
                tool.superGet(driver,'https://twitter.com/home');
                time.sleep(tool.randomNumber(6))
                #run activity
                status = runActivity(obj['activity'],obj['id'])
                if status==True:
                    randomActivity(driver)
                else:
                    time.sleep(tool.randomNumber(20))
            except Exception as e:
                print(e)
        
        time.sleep(10);
        driver.quit()
        quit()