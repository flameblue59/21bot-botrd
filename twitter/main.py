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

def doLogin(driver,email,password):
    elem = "//input[@name='username']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver input email')
    else:
        try:
            loginEmail = driver.find_element(By.XPATH,elem)
            loginEmail.send_keys(email)
        except Exception as e:
            print(e)
            
    elem = "//input[@name='password']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver input password')
    else:
        try:
            loginPassword = driver.find_element(By.XPATH,elem)
            loginPassword.send_keys(password)
        except Exception as e:
            print(e)
            
    #click login button
    time.sleep(tool.randomNumber(6))    
    elem = "//div[contains(text(),\'Log in')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver button login')
    else:
        try:
            button = driver.find_element(By.XPATH,elem)
            tool.customClick(driver,button)
        except Exception as e:
            print(e)
            
    #not now button
    time.sleep(tool.randomNumber(6))    
    elem = "//button[contains(text(),\'Not Now')]"
    try:
        WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver not now button')
    else:
        try:
            button = driver.find_element(By.XPATH,elem)
            tool.customClick(driver,button)
        except Exception as e:
            print(e)            

def checkLogin(driver):
    elem = "//input[@name='username']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kamu sudah masuk')
        return True
    else:
        try:
            loginEmail = driver.find_element(By.XPATH,elem)
        except Exception as e:
            print(e)
            return True
    return False

def doUnfollow(driver):
    #open instagram profile
    elem = "//img[contains(@alt,\'profile picture')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver instagram profile')
        return False
    else:
        try:
            explorer = driver.find_element(By.XPATH,elem)
            tool.customClick(driver,explorer)
        except Exception as e:
            print(e)
            return False
            
    #click following
    time.sleep(tool.randomNumber(4))
    elem = "//div[contains(text(),\'following')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver following button')
        return False
    else:
        try:
            explorer = driver.find_element(By.XPATH,elem)
            tool.customClick(driver,explorer)
        except Exception as e:
            print(e)
            return False    
    
    #scroll 10 times
    scroll = 10
    while scroll > 0:
        scroll -= 1
        tool.scrollFollowingDown(driver)
    
    #click unfollow button [random]
    time.sleep(tool.randomNumber(4))
    elem = "//div[@role='dialog']//div[contains(text(),\'Following')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver unfollow button')
        return False
    else:
        try:
            unfollowButton = driver.find_elements(By.XPATH,elem)
            sum = len(unfollowButton)-1
            if sum > random.randint(300,500):
                rand = random.randint(0,sum)
                tool.customClick(driver,unfollowButton[rand])
            else:
                print('tidak ada yang perlu di unfollow, saat ini: '+sum)
        except Exception as e:
            print('tidak bisa menemukan unfollow button'+str(e))      
            return False   
            
    #click unfollow confirmation button [random]
    time.sleep(tool.randomNumber(4))
    elem = "//div[@role='dialog']//button[contains(text(),\'Unfollow')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver unfollow confirmation button')
    else:
        try:
            unfollowButton = driver.find_elements(By.XPATH,elem)
            sum = len(unfollowButton)-1
            rand = random.randint(0,sum)
            tool.customClick(driver,unfollowButton[rand])
            return True
        except Exception as e:
            print('tidak bisa menemukan unfollow confirmation button'+str(e))   
            return False 
    

def doFollow(driver):
    #open instagram explorer
    elem = "//a[@href='/explore/']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver instagram explorer')
        return False
    else:
        try:
            explorer = driver.find_element(By.XPATH,elem)
            tool.customClick(driver,explorer)
        except Exception as e:
            print(e)
            return False

    time.sleep(tool.randomNumber(4))
    #click photo
    elem = "//a[contains(@href,\'/p/')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver photo list')
        return False
    else:
        try:
            photoList = driver.find_elements(By.XPATH,elem)
            sum = len(photoList)-1
            rand = random.randint(0,sum)
            tool.customClick(driver,photoList[rand])
        except Exception as e:
            print('gagal klik photo'+str(e))
            return False
    
    #click like button [random] //div[@role='presentation']
    time.sleep(tool.randomNumber(4))
    elem = "//div[contains(text(),\'likes')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver like button')
    else:
        try:
            likeButton = driver.find_elements(By.XPATH,elem)
            sum = len(likeButton)-1
            rand = random.randint(0,sum)
            tool.customClick(driver,likeButton[rand])
        except Exception as e:
            print('gagal klik tombol like'+str(e))
            return False

    #click follow button [random]
    time.sleep(tool.randomNumber(4))
    elem = "//div[@role='dialog']//div[contains(text(),\'Follow')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver follow button')
        return False
    else:
        try:
            followButton = driver.find_elements(By.XPATH,elem)
            sum = len(followButton)-1
            rand = random.randint(0,sum)
            tool.customClick(driver,followButton[rand])
            return True
        except Exception as e:
            print('tidak bisa menemukan follow button'+str(e))
            return False   