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
    #input username
    elem = "//input[@autocomplete='username']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver input email')
    else:
        try:
            loginEmail = driver.find_element(By.XPATH,elem)
            loginEmail.send_keys(email)
        except Exception as e:
             print('login email tidak ditemukan')
    
    #next button
    time.sleep(tool.randomNumber(4))        
    elem = "//span[contains(text(),\'Next')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver next button')
    else:
        try:
            nextButton = driver.find_element(By.XPATH,elem)
            tool.customClick(driver,nextButton)
        except Exception as e:
            print('next button tidak ditemukan')    
    
    #input password
    elem = "//input[@autocomplete='current-password']"
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
    time.sleep(tool.randomNumber(4))    
    elem = "//span[contains(text(),\'Log in')]"
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
                   

def checkLogin(driver):
    elem = "//span[contains(text(),\'Log in')]"
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

def doLike(driver):
    tool.scrollDown(driver)
    time.sleep(tool.randomNumber(4))
    #click like button randomly
    elem = "//div[@data-testid='like']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver like button')
        return False
    else:
        try:
            likeButton = driver.find_elements(By.XPATH,elem)
            sum = len(likeButton)-1
            rand = random.randint(0,sum)
            tool.customClick(driver,likeButton[rand])
            return True
        except Exception as e:
            print('tidak dapat menemukan box like'+str(e))  
            return False       
        
def doComment(driver,commentText):
    tool.scrollDown(driver)
    time.sleep(tool.randomNumber(4))
    
    #find comment button randomly
    elem = "//div[contains(@aria-label,\'Reply')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver textarea comment')
        return False
    else:
        try:
            commentButton = driver.find_elements(By.XPATH,elem)
            sum = len(commentButton)-1
            rand = random.randint(0,sum)
            tool.customClick(driver,commentButton[rand])
        except Exception as e:
            print('tidak dapat menemukan textarea comment'+str(e))
            return False
        
    #get parent
    elem = "//div[@aria-labelledby='modal-header']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver dialog comment')
        return False
    else:
        try:
            dialog = driver.find_element(By.XPATH,elem)
        except Exception as e:
            print('tidak dapat menemukan dialog comment')
            return False        
        
    #to find textarea and send comment
    elem = ".//div[@class='public-DraftStyleDefault-block public-DraftStyleDefault-ltr']"
    try:
        WebDriverWait(dialog,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver textarea comment')
        return False
    else:
        try:
            commentBox = dialog.find_element(By.XPATH,elem)
            commentBox.send_keys(commentText)
        except Exception as e:
            print('tidak dapat menemukan textarea comment'+str(e))
            return False    
            
    #do post comment
    time.sleep(tool.randomNumber(4))
    elem = ".//span[contains(text(),'Reply')]"
    try:
        WebDriverWait(dialog,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan webdriver post button')
        return False
    else:
        try:
            postButton = dialog.find_element(By.XPATH,elem)
            tool.customClick(driver,postButton)
            return True
        except Exception as e:
            print('tidak dapat menemukan post button') 
            return False   



def doUnfollow(driver):
    #open twitter profile
    elem = "//a[@aria-label='Profile']"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver twitter profile')
        return False
    else:
        try:
            profile = driver.find_element(By.XPATH,elem)
            tool.customClick(driver,profile)
        except Exception as e:
            print('tidak bisa klik profil')
            return False
            
    #click following
    time.sleep(tool.randomNumber(4))
    elem = "//a[contains(@href,\'/following')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver following button')
        return False
    else:
        try:
            following = driver.find_element(By.XPATH,elem)
            tool.customClick(driver,following)
        except Exception as e:
            print(e)
            return False    
    
    #scroll 2 times
    scroll = 2
    while scroll > 0:
        scroll -= 1
        tool.scrollDown(driver)
    
    #click unfollow button [random]
    canUnfollow = False
    time.sleep(tool.randomNumber(4))
    elem = "//span[contains(text(),\'Following')]"
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
                canUnfollow = True                
            else:
                print('tidak ada yang perlu di unfollow, saat ini: '+str(sum))
        except Exception as e:
            print('tidak bisa menemukan unfollow button')      
            return False   
    
    if canUnfollow==True:
        #click unfollow confirmation button [random]
        time.sleep(tool.randomNumber(4))
        elem = "//div[@data-testid='confirmationSheetDialog']//span[contains(text(),\'Unfollow')]"
        try:
            WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
        except:
            print('kesalahan web driver unfollow confirmation button')
        else:
            try:
                unfollowButton = driver.find_element(By.XPATH,elem)
                tool.customClick(driver,unfollowButton)
                return True
            except Exception as e:
                print('tidak bisa menemukan unfollow confirmation button'+str(e))   
                return False 
    #when we cannot unfollow due to small following amount just return true
    return True
    
def doFollow(driver):
    time.sleep(tool.randomNumber(4))
    #open status
    elem = "//a[contains(@href,\'/status/')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver open status')
        return False
    else:
        try:
            status = driver.find_elements(By.XPATH,elem)
            sum = len(status)-1
            rand = random.randint(0,sum)
            tool.customClick(driver,status[rand])
        except Exception as e:
            print('gagal klik open stastus')
            return False

    time.sleep(tool.randomNumber(4))
    #click photo
    elem = "//a[contains(@href,\'/likes')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver go to like')
        return False
    else:
        try:
            goToLike = driver.find_element(By.XPATH,elem)
            tool.customClick(driver,goToLike)
        except Exception as e:
            print('gagal klik go to like'+str(e))
            return False
    
    #click randomly follow button
    time.sleep(tool.randomNumber(4))
    elem = "//span[contains(text(),\'Follow')]"
    try:
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,elem)))
    except:
        print('kesalahan web driver follow button')
    else:
        try:
            followButton = driver.find_elements(By.XPATH,elem)
            sum = len(followButton)-1
            rand = random.randint(0,sum)
            tool.customClick(driver,followButton[rand])
            return True
        except Exception as e:
            print('gagal klik tombol follow'+str(e))
            return False