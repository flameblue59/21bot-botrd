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
import mysql.connector
import time
import requests
import random
import sys
import json
import math
import myConn
import os
#importing our custom files
import group
from fbtool.main import fbtool
import main

class main:
    def postStatus(driver,statusText):
        elem = "//div[contains(text(),\'Apa yang Anda pikirkan sekarang?')]"
        #click status box
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
        except:
            print('WebDriver box status tidak ada')    
        finally:
            try:
                box = driver.find_element(By.XPATH,"//div[contains(text(),\'Apa yang Anda pikirkan sekarang?')]")
                fbtool.customClick(driver,box)
            except:
                print('gagal klik box status')
                return False
        #type status
        elem = "//textarea[@class='composerInput mentions-input']"
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
        except:
            print('WebDriver mengirimkan status tidak ada')    
        finally:
            try:
                status = driver.find_element(By.XPATH,elem)
                status.send_keys(statusText)
            except:
                print('tidak bisa mengirimkan status')
                return False
        #click from filter list
        elem = "//div[contains(@aria-label,\'background')]"
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
        except:
            print('WebDriver membaca filter tidak ada')    
        finally:
            try:
                listFilter = driver.find_elements(By.XPATH,elem)
                sum = len(listFilter)-1
                rand = random.randint(0,sum)
                fbtool.customClick(driver,listFilter[rand])
            except:
                print('tidak bisa klik filter')
                return False        
        #click posting button
        elem = "//button[@value='Posting']"
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
        except:
            print('WebDriver tombol posting tidak ada')    
        finally:
            try:
                button = driver.find_element(By.XPATH,elem)
                fbtool.customClick(driver,button)
            except:
                print('tidak bisa post status')
                return False
        return True
            
    def postStatusPhoto(driver,statusText,email):
        #setup image
        imagePath,filename = fbtool.getPhoto(email)    
        elem = "//div[contains(text(),\'Apa yang Anda pikirkan sekarang?')]"
        #click status box
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
        except:
            print('gagal klik box status')   
            return False 
        finally:
            box = driver.find_element(By.XPATH,"//div[contains(text(),\'Apa yang Anda pikirkan sekarang?')]")
            fbtool.customClick(driver,box)
        #type status
        elem = "//textarea[@class='composerInput mentions-input']"
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
        except:
            print('gagal mengirimkan status')
            return False
        finally:
            status = driver.find_element(By.XPATH,elem)
            status.send_keys(statusText)
        #submit image
        elem = "//input[@data-sigil='photo-input']"
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
        except:
            print('gagal mengunggah foto')
            return False
        finally:
            upload = driver.find_element(By.XPATH,elem)
            upload.send_keys(imagePath)
        #waiting for uploads      
        time.sleep(6)  
        #click posting button
        elem = "//button[@value='Posting']"
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
        except:
            print('tombol posting tidak ada')
            return False
        finally:
            button = driver.find_element(By.XPATH,elem)
            fbtool.customClick(driver,button)
        #send posted image to server [so it wont posted anymore]
        mycursor = myConn.mydb.cursor(dictionary=True)
        sql = "INSERT INTO posted_profile_image(email,filename) VALUES(%s,%s)"
        val = [email,filename]
        mycursor.execute(sql,val)
        myConn.mydb.commit()      
        return True      
    
    def doLogin(driver,emailText,passwordText):
        #type email
        try:
            driver.implicitly_wait(3)
            email = driver.find_element(By.XPATH,"//input[@name='email']")
            email.send_keys(emailText)
        except:
            print('gagal mengambil input email[1]')  
        #type password
        try:
            driver.implicitly_wait(3)
            password = driver.find_element(By.XPATH,"//input[@name='pass']")
            password.send_keys(passwordText)
        except:
            print('gagal mengambil input password')
        #send login
        try:
            driver.implicitly_wait(3)
            button = driver.find_element(By.XPATH,"//button[@name='login']")
            button.click()
        except:
            print('gagal klik tombol login')
        #when contain landing page screen [one click login]
        try:
            driver.implicitly_wait(3)
            button = driver.find_element(By.XPATH,"//button[@value='OK']")
            button.click()
        except:
            print('gagal klik tombol lain kali')
        try:
            driver.implicitly_wait(3)
            buttonVerif = driver.find_element(By.XPATH,"//button[@value='Lanjutkan']")
            buttonVerif.click()
            #send error to backend since there are verification
        except:
            print('tidak ada masalah verif')
            
    def openNotification(driver):
        fbtool.superGet(driver,'https://m.facebook.com/notifications.php')
        time.sleep(fbtool.randomNumber(4))
    
    def doLike(driver):
        try:
            driver.implicitly_wait(3)
            fbtool.superGet(driver,'https://m.facebook.com/')
            driver.implicitly_wait(3)
            like = driver.find_elements(By.XPATH,"//a[contains(text(),\'Suka')]")
            sum = len(like)-1
            rand = random.randint(0,sum)
            like[rand].click()
            return True
        except:
            print('terdapat kesalahan saat like')
        return False

    def doComment(driver,commentText):
        try:
            driver.implicitly_wait(3)
            comment = driver.find_elements(By.XPATH,"//a[contains(text(),\'Komentari')]")
            sum = len(comment)-1
            rand = random.randint(0,sum)        
            comment[rand].click()
        except:
            print('gagal klik komentar')
            return False
        try:
            time.sleep(2)
            driver.implicitly_wait(3)
            commentBox = driver.find_element(By.XPATH,"//div[@data-sigil='m-mentions-root']")
            commentBox.click()
            driver.implicitly_wait(3)
            commentBox = driver.find_element(By.XPATH,"//textarea[@id='composerInput']")
            commentBox.send_keys(commentText)
        except:
            print('gagal isi komentar [0]')     
            return False   
        try:
            driver.implicitly_wait(3)
            time.sleep(2)
            postComment = driver.find_element(By.XPATH,"//button[@value='Posting']")
            postComment.click()
        except:
            print('gagal klik tombol komentar[0]')     
            return False   
        return True

