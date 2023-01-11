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
    def tiktokPath(email):
        mycursor = myConn.mydb.cursor(dictionary=True)
        sql = "SELECT value FROM settings WHERE type='filePath'"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        return result[0]['value']+'tiktok/'+email+'/'
    #to scroll once
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