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
import myConn
import os
import math
import random
import time

class fbtool:
    def superGet(driver,url):
        driver.get(url)
    def getStatus(category,language):
        mycursor = myConn.mydb.cursor(dictionary=True)
        sql = "SELECT text FROM facebook_status WHERE category=%s and language=%s ORDER BY RAND()"
        val = [category,language]
        mycursor.execute(sql,val)
        result = mycursor.fetchall()
        return result[0]['text']
    def getComment(category,language):
        mycursor = myConn.mydb.cursor(dictionary=True)
        sql = "SELECT text FROM facebook_comment WHERE category=%s and language=%s ORDER BY RAND()"
        val = [category,language]
        mycursor.execute(sql,val)
        result = mycursor.fetchall()
        return result[0]['text']
    def getPhoto(email,postType):
        #define table list
        tableList = {
            'group':'posted_group_image',
            'profile':'posted_profile_image'
        }
        #define table
        table = tableList[postType]
        #randomize image
        dir = fbtool.facebookPath(email)
        listImage = os.listdir(dir)
        #check for uniqueness
        mycursor = myConn.mydb.cursor(dictionary=True,buffered=True)
        sql = "SELECT filename FROM "+table+" WHERE email=%s"
        val = [email]
        mycursor.execute(sql,val)
        result = mycursor.fetchall()
        for row in result:
            if row['filename'] in listImage:
                listImage.remove(row['filename'])
        #reset image when empty
        if len(listImage) <= 0:
            #reset image
            fbtool.resetImage(email,table)
            #just loop its function to make sure we get the result
            return fbtool.getPhoto(email,postType)
        sum = len(listImage)-1
        rand = random.randint(0,sum)
        filename = listImage[rand]
        return dir+''+filename,filename    
    def customClick(driver,object):
        driver.execute_script('arguments[0].click();',object)
    def resetImage(email,table):
        myCursor = myConn.mydb.cursor(buffered=True)
        sql = "DELETE FROM "+table+" WHERE email=%s"
        val = [email]
        myCursor.execute(sql,val)
        myConn.mydb.commit()
    def randomNumber(max):
        min = math.floor(max/2)
        interval = random.randint(min,max)
        return interval
    def filePath():
        mycursor = myConn.mydb.cursor(dictionary=True)
        sql = "SELECT value FROM settings WHERE type='filePath'"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        return result[0]['value']
    def facebookPath(email):
        mycursor = myConn.mydb.cursor(dictionary=True)
        sql = "SELECT value FROM settings WHERE type='filePath'"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        return result[0]['value']+'facebook/'+email+'/'
    #to scroll down
    def scrollDown(driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  
    #to scroll down
    def scrollToDown(driver):
        pauseTime = fbtool.randomNumber(4)
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(pauseTime)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height 