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

class tool:
    def getPhoto(email,path):
        #randomize image
        dir = tool.instagramPath(path)
        listImage = os.listdir(dir)
        #check for uniqueness
        mycursor = myConn.mydb.cursor(dictionary=True)
        sql = "SELECT filename FROM posted_instagram_image WHERE email=%s"
        val = [email]
        mycursor.execute(sql,val)
        result = mycursor.fetchall()
        for row in result:
            listImage.remove(row['filename'])
        sum = len(listImage)-1
        rand = random.randint(0,sum)
        filename = listImage[rand]
        return dir+''+filename,filename     
    def getStatus(category,language):
        mycursor = myConn.mydb.cursor(dictionary=True)
        sql = "SELECT text FROM instagram_status WHERE category=%s and language=%s ORDER BY RAND()"
        val = [category,language]
        mycursor.execute(sql,val)
        result = mycursor.fetchall()
        return result[0]['text']
    def getComment(category,language):
        mycursor = myConn.mydb.cursor(dictionary=True)
        sql = "SELECT text FROM instagram_comment WHERE category=%s and language=%s ORDER BY RAND()"
        val = [category,language]
        mycursor.execute(sql,val)
        result = mycursor.fetchall()
        return result[0]['text']      
    def superGet(driver,url):
        driver.get(url)
    def customClick(driver,object):
        driver.execute_script('arguments[0].click();',object)
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
    def instagramPath(path):
        mycursor = myConn.mydb.cursor(dictionary=True)
        sql = "SELECT value FROM settings WHERE type='filePath'"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        return result[0]['value']+'instagram/'+path+'/'
    #to scroll down
    def scrollDown(driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  
    #to scroll down
    def scrollToDown(driver):
        pauseTime = tool.randomNumber(4)
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
            
    #to scroll following dialog
    def scrollFollowingDown(driver):
        elem = "//div[@role='dialog']/div/div/div[3]/div[1]"
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
        except:
            print('kesalahan webdriver following down')
        else:
            scroll = driver.find_element(By.XPATH,elem)
            driver.execute_script("arguments[0].scroll(0, arguments[0].scrollHeight);", scroll)