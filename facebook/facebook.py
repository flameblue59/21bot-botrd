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
import group
import myConn
from fbtool.main import fbtool
from main import main

def getAccount(server):
    mycursor = myConn.mydb.cursor(dictionary=True)
    sql = "SELECT email,password FROM facebook_account WHERE server=%s and nextRun < NOW() ORDER BY nextRun ASC"
    val = [server]
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    if len(result)==0:
        return False
    return result[0]['email'],result[0]['password']

def updateAccount(email):
    #update next run
    mycursor = myConn.mydb.cursor(dictionary=True)
    sql = "UPDATE facebook_account SET nextRun=DATE_ADD(NOW(),INTERVAL 3 MINUTE) WHERE email=%s"
    value = [email]
    mycursor.execute(sql,value)
    myConn.mydb.commit()

def checkBanned():
    try:
        driver.implicitly_wait(3)
        #check first condition
        driver.find_element(By.XPATH,"//select[@name='country_code']")
        #check second condition
        driver.find_element(By.XPATH,"//input[@name='contact_point']")
        #send banned to server
    except Exception as e:
        #account normal
        print('account in normal state'+str(e))
        

def hasLogin():
    #check input email
    try:
        driver.implicitly_wait(3)
        driver.find_element(By.XPATH,"//input[@name='email']")
        return False;
    except Exception as e:
        print('kamu sudah login')  
    return True

def addFriend(email):
    profileLink = {}
    #klik friend menu
    elem = "//a[@name='Permintaan Pertemanan']"
    try:
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,elem)))
    except Exception as e:
        print('web driver bermasalah friend menu'+str(e))
    else:
        try:
            menu = driver.find_element(By.XPATH,elem)
            fbtool.customClick(driver,menu)
        except:
            print('tidak bisa klik menu pertemanan')
            return False
    time.sleep(fbtool.randomNumber(4))    
    #klik recommended
    elem = "//a[contains(@href,\'center/suggestions')]"
    try:
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,elem)))
    except Exception as e:
        print('webdriver recommended bermasalah'+str(e))
    else:
        try:
            suggestion = driver.find_element(By.XPATH,elem)
            fbtool.customClick(driver,suggestion)
        except Exception as e:
            print('tidak bisa klik saran'+str(e))
            return False
    #read box add friend (contain same friend) & add friend
    time.sleep(fbtool.randomNumber(4))    
    elem = "//div[contains(@data-sigil,\'undoable-action')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except Exception as e:
        print('tidak ada saran pertemanan'+str(e))
    else:
        try:
            suggestion = driver.find_elements(By.XPATH,elem)
            for obj in suggestion:
                add = obj.find_element(By.XPATH,".//div[@data-sigil='m-add-friend-source-replaceable']")
                show = add.text
                if 'teman yang sama' in show:
                    addButton = obj.find_element(By.XPATH,".//button[@value='Tambah Teman']")
                    fbtool.customClick(driver,addButton)
                    return True
        except Exception as e:
            print('tidak ditemukan'+str(e))
     
    fbtool.superGet(driver,'https://m.facebook.com/home.php')
    time.sleep(fbtool.randomNumber(4))   
    #go to post which has comment
    elem = "//span[@data-sigil='comments-token']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except Exception as e:
        print('webdriver go to post bermasalah'+str(e))
    else:
        try:
            post = driver.find_elements(By.XPATH,elem)
            sum = len(post)-1
            rand = random.randint(0,sum)
            fbtool.customClick(driver,post[rand])
        except Exception as e:
            print('tidak ada postingan dengan komentar ditemukan'+str(e))   
            return False    
    time.sleep(fbtool.randomNumber(4))
    #go to reaction
    elem = "//a[contains(@href,\'reaction/')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except Exception as e:
        print('webdriver go to reaction bermasalah'+str(e))        
    else:
        try:
            reaction = driver.find_element(By.XPATH,elem)
            fbtool.customClick(driver,reaction)
        except Exception as e:
            print('tidak ada profil ditemukan'+str(e))            
            return False
    #check for invalid activity
    elem = "//a[@data-sigil='MPageError:retry']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except Exception as e:
        print('webdriver invalid activity bermasalah'+str(e))        
    else:
        try:
            retry = driver.find_element(By.XPATH,elem)
            fbtool.customClick(driver,retry)
        except Exception as e:
            print('gagal klik coba lagi')+e            
            return False
    time.sleep(fbtool.randomNumber(4))                
    #read profile
    elem = "//div[@data-sigil='undoable-action marea']//a"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except Exception as e:
        print('webdriver read profile bermasalah'+str(e))        
    else:
        try:
            profile = driver.find_elements(By.XPATH,elem)
        except Exception as e:
            print('tidak ada profil ditemukan'+str(e))
            return False
        try:
            for obj in profile:
                link = obj.get_attribute('href')
                profileId = link.split('?id=')[1]
                profileId = profileId.split('&eav')[0]
                profileLink[profileId] = link
        except Exception as e:
            print('terjadi masalah saat parsing link'+str(e))
    time.sleep(fbtool.randomNumber(4))   
    #when profileLink found
    if len(profileLink) == 0:
        return False
    
    #go to profile
    try:
        sum = len(profile)-1
        rand = random.randint(0,sum)
        fbtool.customClick(driver,profile[rand])
    except Exception as e:
        print('kesalahan saat pergi ke profil'+str(e))
        return False
    time.sleep(fbtool.randomNumber(4))   
    #add friend
    elem = "//a[contains(@href,\'profile/add/')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except Exception as e:
        print('webdriver add friend bermasalah'+str(e))        
    else:
        try:
            add = driver.find_element(By.XPATH,elem)
            fbtool.customClick(driver,add)
            print('berhasil menambahkan pertemanan')       
        except Exception as e:
            print('tidak ada tombol add friend'+str(e))        
            return False    
    time.sleep(fbtool.randomNumber(4))   
    #confirm add
    elem = "//button[@value='Konfirmasi']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except Exception as e:
        print('tidak perlu konfirmasi')        
    else:
        try:
            confirm = driver.find_element(By.XPATH,elem)
            fbtool.customClick(driver,confirm)
            print('berhasil melakukan konfirmasi saat menambahkan pertemanan')
        except:
            return False 
    return False        

def unFriend(email):
    #klik friend menu
    elem = "//a[@name='Permintaan Pertemanan']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except Exception as e:
        print('webdriver friend menu bermasalah'+str(e))        
    else:
        try:
            menu = driver.find_element(By.XPATH,elem)
            fbtool.customClick(driver,menu)
        except Exception as e:
            print('tidak bisa klik menu pertemanan'+str(e))
            return False
    time.sleep(fbtool.randomNumber(2))
    #klik icon other option [>]
    elem = "//i[@aria-label='Opsi lainnya']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except Exception as e:
        print('webdriver icon other option bermasalah'+str(e))        
    else:
        try:
            menu = driver.find_element(By.XPATH,elem)
            fbtool.customClick(driver,menu)
        except:
            print('tidak ada tombol opsi lainnya')
            return False
    time.sleep(fbtool.randomNumber(2))
    #go to pending friend list
    elem = "//a[contains(@href,\'center/requests/outgoing')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('webdriver pending friend list bermasalah')        
    else:
        try:
            menu = driver.find_element(By.XPATH,elem)
            fbtool.customClick(driver,menu)
        except:
            print('tidak ada tombol opsi lainnya')
            return False        
    time.sleep(fbtool.randomNumber(4))   
    #scroll to down
    fbtool.scrollToDown(driver)
    #get latest element
    elem = "//button[@value='Batalkan']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('webdriver latest element bermasalah')        
    else:
        try:
            cancelButton = driver.find_elements(By.XPATH,elem)
            last = len(cancelButton)-1
            totalPending = len(cancelButton)
            #set max only 100 friend requests
            if totalPending >= 100:
                fbtool.customClick(driver,cancelButton[last])
            elif totalPending < 100:
                print('tidak perlu unfriend, pertemanan menunggu masih: '+str(totalPending))
        except:
            print('tombol batalkan pertemanan tidak ditemukan')
    return True

def confirmFriend():
    time.sleep(fbtool.randomNumber(4))   
    #klik friend menu
    elem = "//a[@name='Permintaan Pertemanan']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('webdriver friend menu bermasalah')        
    else:
        try:
            menu = driver.find_element(By.XPATH,elem)
            fbtool.customClick(driver,menu)
        except:
            print('tidak bisa klik menu pertemanan')
            return False
    time.sleep(fbtool.randomNumber(4))   
    #go to all
    fbtool.superGet(driver,'https://m.facebook.com/friends/center/requests/all/')
    time.sleep(fbtool.randomNumber(4))    
    #klik confirm button
    elem = "//button[@value='Konfirmasi']"
    try:
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,elem)))
    except Exception as e:
        print('webdriver confirm button bermasalah:'+str(e))        
    else:
        try:
            confirm = driver.find_element(By.XPATH,elem)
            fbtool.customClick(driver,confirm)
        except:
            print('tidak ada yang perlu di konfirmasi')
    return True
    
def profileWalk():
    time.sleep(fbtool.randomNumber(4))   
    #go to profile
    elem = "//a[contains(@href,\'profile.php?id=')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('tidak ada profil yang bisa dilihat')        
    else:
        try:
            profile = driver.find_element(By.XPATH,elem)
            fbtool.customClick(driver,profile)
        except:
            print('tidak ada profile yang ditemukan')
    return True
        
def sendActivity(email,type,activityId,amount):
    mycursor = myConn.mydb.cursor()
    sql = "UPDATE facebook_account SET "+type+"="+type+"+%s WHERE email=%s"
    val = [amount,email]
    mycursor.execute(sql,val)
    myConn.mydb.commit()
    #delete activity
    mycursor = myConn.mydb.cursor()
    sql = "DELETE FROM facebook_activity WHERE id=%s"
    val = [activityId]
    mycursor.execute(sql,val)
    myConn.mydb.commit()
    
def getActivity(email):
    mycursor = myConn.mydb.cursor(dictionary=True)
    sql = "SELECT id,activity FROM facebook_activity WHERE done=0 and runAt < NOW() and email=%s ORDER BY runAt ASC"
    val = [email]
    mycursor.execute(sql,val)
    result = mycursor.fetchall()
    return result
        
def insertProfile(profileLink):
    mycursor = myConn.mydb.cursor()
    query = []
    val = []
    keys = profileLink.keys()
    for obj in keys:
        query.append('(%s,%s)')
        val.append('obj')
        val.append(profileLink[obj])
    sql = "INSERT INTO facebook_profile(profileId,profileLink) VALUES "+query.join(',')+" ON DUPLICATE KEY UPDATE waktu=CURRENT_TIMESTAMP()"
    mycursor.execute(sql,val)
    myConn.mydb.commit()
    
def runActivity(activity,activityId):
    status = False
    amount = 1
    if activity=='likes':
        status = main.doLike(driver)
    elif activity=='comment':
        commentText = fbtool.getComment('general','id')
        status = main.doComment(driver,commentText)
    elif activity=='addFriend':
        status = addFriend(email)
    elif activity=='unFriend':
        status = unFriend(email)        
    elif activity=='confirmFriend':
        status = confirmFriend()
    elif activity=='profileWalk':
        status = profileWalk()
    elif activity=='profilePostStatus':
        statusText = fbtool.getStatus('jodoh','id')
        status = main.postStatus(driver,statusText)
    elif activity=='profilePostPhoto':
        statusText = fbtool.getStatus('jodoh','id')
        status = main.postStatusPhoto(driver,statusText,email)
    elif activity=='groupInvite':
        group.goToGroupTarget(driver,'372219174991684')
        numberInvite = random.randint(3,5)
        status = group.groupInvite(driver,numberInvite)   
        amount = numberInvite
    elif activity=='groupPostStatus':
        statusText = fbtool.getStatus('jodoh','id')
        group.goToGroup(driver)
        status = group.groupPostStatus(driver,statusText)
    elif activity=='groupPostPhoto':
        statusText = fbtool.getStatus('jodoh','id')
        group.goToGroup(driver)
        status = group.groupPostPhoto(driver,statusText,email)
        
    #send activity
    if status==True:
        sendActivity(email,activity,activityId,amount)
    
    return status

def randomActivity(driver):
    activity = random.randint(2,4)
    while activity > 0:
        try:
            walk = random.randint(0,100)
            if walk > 70:
                profileWalk()
                time.sleep(fbtool.randomNumber(10))
            fbtool.scrollDown(driver)
            time.sleep(fbtool.randomNumber(4))
            activity -= 1
        except:
            print('opps terjadi kesalahan random activity')
            continue
    
filePath = fbtool.filePath()
slashDir = '/'

server = sys.argv[1]
#get account
account = getAccount(server)
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
options.add_argument('--user-data-dir='+filePath+'chromeprofile'+slashDir+'facebook'+slashDir+email)
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
            
        fbtool.superGet(driver,'https://m.facebook.com/home.php')
        
        login = hasLogin() #True/False
        
        if login==False:
            main.doLogin(driver,email,password)
            
        #openNotification()
        #status = tool.getStatus('jodoh','id')
        for obj in activityList:
            try:
                time.sleep(fbtool.randomNumber(4))
                print('melakukan pekerjaan: '+obj['activity'])
                fbtool.superGet(driver,'https://m.facebook.com/');
                time.sleep(fbtool.randomNumber(6))
                #run activity
                status = runActivity(obj['activity'],obj['id'])
                if status==True:
                    randomActivity(driver)
            except Exception as e:
                print(e)
        #postStatus('salam kenal') belum selesai
        #doLike()
        #doComment('ok kak')
        
        #login success
        fbtool.scrollDown(driver)
        print('keluar dari program')
        time.sleep(10)
        driver.quit()
        quit()