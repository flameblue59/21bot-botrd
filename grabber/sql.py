import mysql.connector
import json
import requests
import os
import random

userEmail = ''
urlList = []

session = requests.Session()

mydb = mysql.connector.connect(
    host="localhost",
    username="root",
    password="",
    database="bot_number"
)

#To delete account from banned server
def sendDelete(account):
    mycursor = mydb.cursor()
    sql = "DELETE FROM banned_account WHERE email=%s"
    val = [account]
    mycursor.execute(sql,val)
    mydb.commit()
    
def updateLastSync(account):
    mycursor = mydb.cursor()
    sql = "UPDATE account_data SET lastSync=NOW() WHERE email=%s"
    val = [account]
    mycursor.execute(sql,val)
    mydb.commit()
    
#To send banned if the account permanently banned
def sendBanned(account):
    mycursor = mydb.cursor()
    sql = "UPDATE banned_account SET banned=true,bannedTime=CURRENT_TIMESTAMP() WHERE email=%s"
    val = [account]
    mycursor.execute(sql,val)
    mydb.commit()
    
#To send number
def sendNumber(source,uid,name,number):
    mycursor = mydb.cursor()
    sql = "INSERT INTO number_vault(category,subCategory,source,uid,name,number) VALUES ('general','general',%s,%s,%s,%s)"
    val = [source,uid,name,number]
    mycursor.execute(sql,val)
    mydb.commit()

def getBanned():

    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT email FROM banned_account")
    result = mycursor.fetchall()

    bannedAccount = []
    for row in result:
        bannedAccount.append(row['email'])
        
    return bannedAccount

def getExisting():
    global userEmail,urlList
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT email FROM account_data ORDER BY lastSync ASC"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    path = 'C://temp'
    accountFolder = os.listdir(path)    
    listAccount = []
    for row in result:
        if row['email'] in accountFolder:
            listAccount.append(row['email'])
    #get banned account
    listBanned = getBanned()
    for account in listAccount:
        if account in listBanned:
            listAccount.remove(account)        
    userEmail = random.choice(listAccount)
    
# To sync account data from /temp folder to sql
def syncAccount():
    path = "C://temp"
    listAccount = os.listdir(path)
    mycursor = mydb.cursor()
    for account in listAccount:
        sql = "INSERT INTO account_data(email,password) VALUES(%s,%s) ON DUPLICATE KEY UPDATE email=VALUES(email)"
        val = [account,"@bobby123@"]
        mycursor.execute(sql,val)
        mydb.commit()
        
#To get new account from server
def getAccount():
    
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT email FROM account_data")
    result = mycursor.fetchall()
    listAccount = []
    for row in result:
        listAccount.append(row['email'])
    
    #Get new account data
    url = "https://beyondlimit.co/api.php?f=olxMass"
    headers = {"accept": "application/json", 
            "content-type": "application/json", 
            }

    response = session.get(url, headers=headers)
    obj = response.json()
    accountNew = []
    for account in obj:
        #check if its already added
        state = account not in listAccount
        if state==True:
            accountNew.append(account)
            
def getUID():
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT id,start,end FROM olx_pool WHERE done=false ORDER BY rendered ASC"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    mycursor = mydb.cursor()
    sql = "UPDATE olx_pool SET rendered=CURRENT_TIMESTAMP() WHERE id=%s"
    val = [result[0]['id']]
    mycursor.execute(sql,val)
    mydb.commit()
    return result[0]

def updateUID(uid,poolId):
    mycursor = mydb.cursor()
    sql = "UPDATE olx_pool SET start=%s WHERE id=%s"
    val = [uid,poolId]
    mycursor.execute(sql,val)
    mydb.commit()
    mycursor = mydb.cursor()
    sql = "UPDATE olx_pool SET done=true WHERE start >= end and id=%s"
    val = [poolId]
    mycursor.execute(sql,val)
    mydb.commit()


    
getExisting()
#To sync account from folder to sql
syncAccount()
#To get new account
#getAccount()
#sendDelete('coba@gmail.com')
#To update last sync
#updateLastSync('adiraamanda@outlook.com')
#sendBanned('neilajulia@outlook.com')
currentUID = getUID()
print(currentUID)
updateUID('100010000','1')