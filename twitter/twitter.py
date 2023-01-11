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
    mycursor = myConn.mydb.cursor(dictionary=True)
    sql = "SELECT email,password FROM instagram_account WHERE nextRun < NOW() ORDER BY nextRun ASC"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    if len(result)==0:
        return False
    return result[0]['email'],result[0]['password']

def updateAccount(email):
    #update next run
    mycursor = myConn.mydb.cursor(dictionary=True)
    sql = "UPDATE instagram_account SET nextRun=DATE_ADD(NOW(),INTERVAL 3 MINUTE) WHERE email=%s"
    value = [email]
    mycursor.execute(sql,value)
    myConn.mydb.commit()

def sendActivity(email,type,activityId):
    mycursor = myConn.mydb.cursor()
    sql = "UPDATE instagram_account SET "+type+"="+type+"+1 WHERE email=%s"
    val = [email]
    mycursor.execute(sql,val)
    myConn.mydb.commit()
    #delete activity
    mycursor = myConn.mydb.cursor()
    sql = "DELETE FROM instagram_activity WHERE id=%s"
    val = [activityId]
    mycursor.execute(sql,val)
    myConn.mydb.commit()

def getActivity(email):
    mycursor = myConn.mydb.cursor(dictionary=True)
    sql = "SELECT id,activity FROM instagram_activity WHERE done=0 and runAt < NOW() and email=%s ORDER BY runAt ASC"
    val = [email]
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    return result

def runActivity(activity,activityId):
    status = False
    if activity=='likes':
        status = doLike()
    elif activity=='follow':
        status = main.doFollow(driver)
    elif activity=='unfollow':
        status = main.doUnfollow(driver)
    elif activity=='post':
        statusText = tool.getStatus('thesimlife','id') 
        status = doPost(statusText)
    elif activity=='comment':
        commentText = tool.getComment('general','id')
        status = doComment(commentText) 
    #send activity
    if status==True:
        sendActivity(email,activity,activityId)
    
    return status

def doPost(statusText):
    #setup image
    imagePath,filename = tool.getPhoto(email,'thesimlife')
    found = False
    #click new post button [version1]
    if found==False:
        elem = "//div[contains(text(),\'Create')]"
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
        except:
            print('kesalahan webdriver add new post [version1]')
        else:
            try:
                newPost = driver.find_element(By.XPATH,elem)
                tool.customClick(driver,newPost)
                found = True
            except Exception as e:
                print('tidak dapat menemukan tombol add new post'+str(e))
    
    #click new post button [version2]
    if found==False:
        elem = "//nav/div[2]/div/div/div[3]/div/div[3]/div/button"
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
        except:
            print('kesalahan webdriver add new post [version2]')
            return False
        else:
            try:
                newPost = driver.find_element(By.XPATH,elem)
                tool.customClick(driver,newPost)
                found = True                
            except Exception as e:
                print('tidak dapat menemukan tombol add new post'+str(e))
                return False        
        
    
    #uploading image
    time.sleep(tool.randomNumber(4))
    elem = "//div[@role='dialog']//input[@accept='image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver upload image')
        return False
    else:
        try:
            newPost = driver.find_element(By.XPATH,elem)
            newPost.send_keys(imagePath)
        except Exception as e:
            print('tidak dapat menemukan input upload image'+str(e))
            return False
            
    #next button
    time.sleep(tool.randomNumber(4))
    elem = "//div[@role='dialog']//button[contains(text(),\'Next')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver next button [next]')
        return False
    else:
        try:
            nextButton = driver.find_element(By.XPATH,elem)
            tool.customClick(driver,nextButton)
        except Exception as e:
            print('tidak dapat menemukan next button [next]'+str(e))   
            return False  

    #next button
    time.sleep(tool.randomNumber(4))
    elem = "//div[@role='dialog']//button[contains(text(),\'Next')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver next button [filter]')
        return False
    else:
        try:
            nextButton = driver.find_element(By.XPATH,elem)
            tool.customClick(driver,nextButton)
        except Exception as e:
            print('tidak dapat menemukan next button [filter]'+str(e)) 
            return False   
            
    #sent status [check div]
    statusFound = False
    time.sleep(tool.randomNumber(4))     
    elem = "//div[@role='dialog']//div[@aria-label='Write a caption...']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver status box [div]')
    else:
        try:
            statusBox = driver.find_element(By.XPATH,elem)
            statusBox.send_keys(statusText)
            statusFound = True
        except Exception as e:
            print('tidak dapat menemukan status box div'+str(e)) 
            return False
          
    #sent status [check textarea]
    elem = "//div[@role='dialog']//textarea[@aria-label='Write a caption...']"
    if statusFound == False:
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
        except:
            print('kesalahan webdriver status box [textarea]')
        else:
            try:
                statusBox = driver.find_element(By.XPATH,elem)
                statusBox.send_keys(statusText)
            except Exception as e:
                print('tidak dapat menemukan status box textarea'+str(e)) 
                return False        
            
    #share button
    time.sleep(tool.randomNumber(4))
    elem = "//div[@role='dialog']//button[contains(text(),\'Share')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver share button')
        return False
    else:
        try:
            shareButton = driver.find_element(By.XPATH,elem)
            tool.customClick(driver,shareButton)
            time.sleep(tool.randomNumber(8))
            #send posted image to server [so it wont posted anymore]
            mycursor = myConn.mydb.cursor(dictionary=True)
            sql = "INSERT INTO posted_instagram_image(email,filename) VALUES(%s,%s)"
            val = [email,filename]
            mycursor.execute(sql,val)
            myConn.mydb.commit()
            return True
        except Exception as e:
            print('tidak dapat menemukan share button'+str(e))   
            return False                       

def doComment(commentText):
    time.sleep(tool.randomNumber(8))
    tool.scrollDown(driver)
    time.sleep(tool.randomNumber(4))
    
    #find form comment, need to random them
    elem = "//div[@role='presentation']//form"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver textarea comment')
        return False
    else:
        try:
            form = driver.find_elements(By.XPATH,elem)
            sum = len(form)-1
            rand = random.randint(0,sum)
            form = form[rand]
        except Exception as e:
            print('tidak dapat menemukan textarea comment'+str(e))
            return False
        
    #to find textarea and send comment
    elem = ".//textarea[@aria-label='Add a comment…']"
    try:
        WebDriverWait(form,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver textarea comment')
        return False
    else:
        try:
            commentBox = form.find_element(By.XPATH,elem)
            commentBox.send_keys(commentText)
        except Exception as e:
            print('tidak dapat menemukan textarea comment'+str(e))
            return False    
            
    #do post comment
    time.sleep(tool.randomNumber(4))
    elem = ".//div[contains(text(),'Post')]"
    try:
        WebDriverWait(form,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver post button')
        return False
    else:
        try:
            postButton = form.find_element(By.XPATH,elem)
            tool.customClick(driver,postButton)
            return True
        except Exception as e:
            print('tidak dapat menemukan post button') 
            return False   

def doLike():
    time.sleep(tool.randomNumber(8))
    tool.scrollDown(driver)
    time.sleep(tool.randomNumber(8))
    elem = "//div[@role='presentation']/div/section[1]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver like box')
        return False
    else:
        try:
            likeBox = driver.find_elements(By.XPATH,elem)
            sum = len(likeBox)-1
            rand = random.randint(0,sum)
            likeBox = likeBox[rand]
        except Exception as e:
            print('tidak dapat menemukan box like'+str(e))  
            return False    
        
    #click like button
    time.sleep(tool.randomNumber(4))
    elem = ".//span/button"
    try:
        WebDriverWait(likeBox,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver tombol like')
        return False
    else:
        try:
            likeButton = likeBox.find_element(By.XPATH,elem)
            tool.customClick(driver,likeButton)
            return True
        except Exception as e:
            print('tidak dapat menemukan tombol like'+str(e))  
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
        
def checkTempBanned(driver,email):
    banned = True
    elem = "//div[@role='presentation']//form//textarea[@aria-label='Add a comment…']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver textarea comment')
    else:
        try:
            commentBox = driver.find_elements(By.XPATH,elem)
            if len(commentBox) > 0:
                banned = False
        except Exception as e:
            print('tidak dapat menemukan textarea comment'+str(e))
            
    if banned==True:
        tries = 1
        #check number tries
        myCursor = myConn.mydb.cursor(dictionary=True,buffered=True)
        sql = "SELECT email,tries,waktu FROM instagram_temp_banned WHERE email=%s"
        value = [email]
        myCursor.execute(sql,value)
        rows = myCursor.rowcount
        if rows > 0:
            result = myCursor.fetchall()[0]
            tries = result['tries']
            print('akun sudah gagal '+str(tries+1))
        
        #insert tries, if exists then +1
        myCursor = myConn.mydb.cursor(buffered=True)
        sql = "INSERT INTO instagram_temp_banned(email,tries) VALUES(%s,%s) ON DUPLICATE KEY UPDATE tries=tries+1"
        value = [email,tries]
        myCursor.execute(sql,value)
        myConn.mydb.commit()
        
        #insert tries
        tries += 1
        
        #send instagram account take rest if error >= 3
        if tries >= 3:
            myCursor = myConn.mydb.cursor(buffered=True)
            sql = "UPDATE instagram_account SET nextRun=DATE_ADD(NOW(),INTERVAL 2 DAY) WHERE email=%s"
            value = [email]
            myCursor.execute(sql,value)
            myConn.mydb.commit()
    
    return banned
            

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
options.add_argument('--user-data-dir='+filePath+'chromeprofile'+slashDir+'instagram'+slashDir+email)
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
            
        tool.superGet(driver,'https://instagram.com')
        
        #check for temporary ban
        status = checkTempBanned(driver,email)
        if status==True:
            driver.quit()
            quit()
        
        #start doing login
        check = main.checkLogin(driver)
        if check==False:
            main.doLogin(driver,email,password)
        
        for obj in activityList:
            try:
                time.sleep(tool.randomNumber(4))
                print('melakukan pekerjaan: '+obj['activity'])
                tool.superGet(driver,'https://instagram.com');
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