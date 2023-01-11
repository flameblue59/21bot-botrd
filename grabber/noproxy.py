from  selenium import webdriver
import undetected_chromedriver.v2 as uc
from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random
import sys
import json
#print(sys.argv[1])
def get_url():
    after_json = sys.argv[1].replace("[","").replace("]","").replace("\\","")
    count = sys.argv[2]
    url =[]
    for i in range(len(after_json.split(","))):
        url.append(after_json.split(",")[i])
    return url 
def login(url):
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(5)
    p = driver.find_element_by_xpath('//*[@id="container"]/header/div/div/div[3]/button/span')
    p.click()
    time.sleep(2)
    try:
        go = driver.find_element_by_xpath('/html/body/div[3]/div/div/div/button[3]')
        go.click()
        email = driver.find_element_by_id('email_input_field')
        email.send_keys(sys.argv[3])
        time.sleep(2)
        em = driver.find_element_by_xpath('/html/body/div[3]/div/div/form/div/button')
        em.click()
        driver.implicitly_wait(10)
        time.sleep(3)
        password = driver.find_element_by_id('password')
        password.send_keys(sys.argv[4])
        em = driver.find_element_by_xpath('/html/body/div[3]/div/div/form/div/button')
        em.click()
        time.sleep(3)
        verify =""
    except:
        go = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/button[3]')
        go.click()
        email = driver.find_element_by_id('email_input_field')
        email.send_keys(sys.argv[3])
        time.sleep(2)
        em = driver.find_element_by_xpath('/html/body/div[4]/div/div/form/div/button')
        em.click()
        driver.implicitly_wait(10)
        time.sleep(3)
        password = driver.find_element_by_id('password')
        password.send_keys(sys.argv[4])
        em = driver.find_element_by_xpath('/html/body/div[4]/div/div/form/div/button')
        em.click()
        time.sleep(3)
        verify =""
    try:
        pas =driver.find_element_by_class_name("_2AC5E")
        if pas!=None:
            verify ="invalid"
    except:
        pass
    return verify
def get_number(url):
    driver.implicitly_wait(10)
    time.sleep(3)
    driver.get(url)
    tel_num=""
    try:    
        tel_clic = driver.find_element_by_xpath('//*[@id="container"]/main/div/div/div/div[5]/div[2]/div/div/div[3]/div[2]')
        if tel_clic !=None:
            tel_clic.click()
            time.sleep(2)
            tel_num = driver.find_element_by_xpath('//*[@id="container"]/main/div/div/div/div[5]/div[2]/div/div/div[3]/div').text
            
    except:
        pass
    if tel_num!="":
        return url,tel_num

if __name__=="__main__":
    try:
            #user agent list
        userAgent = [
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9",
"Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4",
"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
        ]
        
        options = uc.ChromeOptions()

        # setting profile
        options.user_data_dir = "c:\\temp\\profile"

        # another way to set profile is the below (which takes precedence if both variants are used
        randProfile = random.randint(0,10000000);
        options.add_argument("--window-position=2000,0")
        options.add_argument('--start-maximized')
        options.add_argument('--user-data-dir=c:\\temp\\profile'+str(randProfile))
        #options.add_argument("user-agent="+random.choice(userAgent))

        # just some options passing in to skip annoying popups
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        driver = uc.Chrome(options=options)
        driver.set_page_load_timeout(10)
        
        driver.maximize_window()
        url_s = get_url()    
        tel_number =[]     
        pas_site = login(url_s[0])
#        print(pas_site)
        if pas_site != "invalid":
            for i in range(len(url_s)):
                #print('---------',i,'----------')
                tel= get_number(url_s[i])
                if tel !=None:
                    tel_number.append(tel)

            #print(tel_number)
            data=[]
            for ur in tel_number:
                we_ur,we_tenu = ur
                data.append({
                    "website":we_ur,
                    "telnumber":we_tenu
                })
            jsonName = 'data'+str(random.randint(1000,9999))+'.json'
            with open(jsonName, 'w') as outfile:
                json.dump(data, outfile)
            print(jsonName)
            driver.quit()
        else:
            print("banned")
            driver.quit()
    except:
        print("banned")
        driver.close()
