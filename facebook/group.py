import undetected_chromedriver as uc
from  selenium import webdriver
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
import time
import requests
import random
import sys
import json
import math
from fbtool.main import fbtool

def groupGoToProfile(driver):
    try:
        time.sleep(fbtool.randomNumber(3))
        #go to group profile [bridge]
        driver.implicitly_wait(3)
        profile = driver.find_elements(By.XPATH,"//a[contains(@href,\'groupid')]")
        print(len(profile))
        sum = len(profile)-1
        rand = random.randint(0,sum)
        profile[rand].click()
        time.sleep(fbtool.randomNumber(3))
        #go to profile page 
        driver.implicitly_wait(3)
        profile = driver.find_element(By.XPATH,"//a[@aria-label='Lihat Profil Utama']")
        profile.click()
    except:
        print('gagal pergi ke profil')
        
def groupPostStatus(driver,statusText):
    #write status
    try:
        driver.implicitly_wait(3)
        status = driver.find_element(By.XPATH,"//div[contains(text(),'Tulis sesuatu...')]")
        status.click()
    except:
        print('gagal merender textarea')
        return False
    time.sleep(fbtool.randomNumber(4))    
    try:
        driver.implicitly_wait(3)
        textarea = driver.find_element(By.XPATH,"//textarea[@class='composerInput mentions-input']")
        textarea.send_keys(statusText)
    except:
        print('gagal mengetik status')
        return False
    time.sleep(fbtool.randomNumber(4))    
    #click from filter list
    try:
        listFilter = driver.find_elements(By.XPATH,"//div[contains(@aria-label,\'background image')]")
        sum = len(listFilter)-1
        rand = random.randint(0,sum)
        fbtool.customClick(driver,listFilter[rand])
    except:
        print('gagal membaca status filter')
        return False
    time.sleep(fbtool.randomNumber(4))    
    #button status send
    try:
        driver.implicitly_wait(3)
        postStatus = driver.find_element(By.XPATH,"//button[@value='Posting']")
        #implementing custom click
        fbtool.customClick(driver,postStatus)
        alert = driver.switch_to.alert
        alert.accept()        
    except:
        print('gagal klik tombol posting')
        return False
    return True
        
def groupPostPhoto(driver,statusText,email):
    #setup image
    imagePath,filename = fbtool.getPhoto(email)
    print(imagePath)
    #click status box
    try:
        driver.implicitly_wait(3)
        status = driver.find_element(By.XPATH,"//div[contains(text(),'Tulis sesuatu...')]")
        status.click()
    except:
        print('gagal merender box status')
        return False
    time.sleep(fbtool.randomNumber(4))
    #write status
    try:
        driver.implicitly_wait(3)
        textarea = driver.find_element(By.XPATH,"//textarea[@class='composerInput mentions-input']")
        textarea.send_keys(statusText)
    except:
        print('gagal mengetik status')
        return False
    time.sleep(fbtool.randomNumber(4))
    #submit image
    try:
        upload = driver.find_element(By.XPATH,"//input[@data-sigil='photo-input']")
        upload.send_keys(imagePath)
    except:
        print('gagal mengunggah foto')
        return False
    #waiting for uploads      
    time.sleep(6)  
    #button status send
    elem = "//button[@value='Posting']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('web driver tombol posting tidak ditemukan')
        return False
    else:
        try:
            postStatus = driver.find_element(By.XPATH,elem)
            #implementing custom click
            fbtool.customClick(driver,postStatus)
        except:
            print('gagal klik tombol posting')
            return False
    #send posted image to server [so it wont posted anymore]
    mycursor = myConn.mydb.cursor(dictionary=True)
    sql = "INSERT INTO posted_group_image(email,filename) VALUES(%s,%s)"
    val = [email,filename]
    mycursor.execute(sql,val)
    myConn.mydb.commit()
    return True

def goToGroup(driver):
    try:
        driver.implicitly_wait(3)
        menu = driver.find_element(By.XPATH,"//a[@name='Lainnya']")
        menu.click()
    except:
        print('gagal klik menu [list]')
    time.sleep(fbtool.randomNumber(4))
    try:
        time.sleep(fbtool.randomNumber(4))
        driver.implicitly_wait(3)
        link = driver.find_element(By.XPATH,"//div[contains(text(),\'Grup')]")
        link.click()
    except:
        print('gagal klik menu grup')
    time.sleep(fbtool.randomNumber(4))
    try:
        time.sleep(fbtool.randomNumber(2))
        groupTab = driver.find_element(By.XPATH,"//a[@aria-label='Grup']")
        groupTab.click()
    except:
        print('gagal memilih grup')
    time.sleep(fbtool.randomNumber(4))
    try:
        #group list
        time.sleep(fbtool.randomNumber(2))
        groupList = driver.find_elements(By.XPATH,"//a[contains(@href,\'/groups/')]")
        #need to remove thesimlife group since we do not need to go there
        for obj in groupList:
            link = obj.get_attribute('href')
            if '372219174991684' in link:
                groupList.remove(obj)
        sum = len(groupList)-1
        rand = random.randint(0,sum)
        groupList[rand].click()
    except:
        print('gagal menuju grup')
        
def groupInvite(driver,numberInvite):
    time.sleep(fbtool.randomNumber(4))
    #click invite button
    elem = "//div[@aria-label='Undang']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('webdriver invite button bermasalah')
    else:
        try:
            inviteButton = driver.find_element(By.XPATH,elem)
            fbtool.customClick(driver,inviteButton)
        except:
            print('gagal klik go to button') 
    time.sleep(fbtool.randomNumber(4))
    
    #confirm invite button
    elem = "//span[contains(text(),\'Undang teman Facebook')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('webdriver confirm invite bermasalah')
    else:
        try:
            confirmButton = driver.find_element(By.XPATH,elem)
            fbtool.customClick(driver,confirmButton)
        except:
            print('gagal klik confirm invite button') 
    time.sleep(fbtool.randomNumber(4))    
    
    #invite friend clicking checkbox
    elem = "//div[@aria-label='Undang teman ke grup ini']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('webdriver invite parent dialog bermasalah')
    else:
        try:
            parent = driver.find_element(By.XPATH,elem)
            childElem = ".//div[@role='checkbox']"
            checkBox = parent.find_elements(By.XPATH,childElem)
            time.sleep(fbtool.randomNumber(4))
            #define max invite
            max = numberInvite
            for obj in checkBox:
                max -= 1
                fbtool.customClick(driver,obj)
                if max <= 0:
                    break 
                time.sleep(fbtool.randomNumber(2))
                
            #sent invite
            time.sleep(fbtool.randomNumber(4))
            sendElem = ".//span[contains(text(),\'Kirim Undangan')]"
            sendInvite = parent.find_element(By.XPATH,sendElem)
            fbtool.customClick(driver,sendInvite)
        except:
            print('gagal membaca invite parent dialog'+e) 
            
    return True
        
        
def goToGroupTarget(driver,groupId):
    try:
        fbtool.superGet(driver,'https://facebook.com')
    except:
        print('kesalahan url driver')
    time.sleep(fbtool.randomNumber(4))
    #go to group section [theme1]
    isFound = False
    elem = "//a[@aria-label='Grup']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('webdriver group section [theme1] bermasalah')
    else:
        try:
            goToButton = driver.find_element(By.XPATH,elem)
            fbtool.customClick(driver,goToButton)
            isFound = True
        except:
            print('gagal klik go to button')

    #go to group section [theme2]
    if isFound==False:
        elem = "//a[@aria-label='Lihat semua grup']"
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
        except:
            print('webdriver group section [theme2] bermasalah')
        else:
            try:
                goToButton = driver.find_element(By.XPATH,elem)
                fbtool.customClick(driver,goToButton)
            except:
                print('gagal klik go to button')
    

    #go to thesimlife group
    elem = "//span[contains(text(),\'TheSimLife - Aplikasi Penghasil Uang')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('webdriver thesimlife group bermasalah')
    else:
        try:
            goToGroup = driver.find_element(By.XPATH,elem)
            fbtool.customClick(driver,goToGroup)
        except:
            print('gagal klik go to button')  