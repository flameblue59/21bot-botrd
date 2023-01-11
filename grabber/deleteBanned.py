import mysql.connector
import json
import requests
import os
import shutil
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
def deleteBanned():
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT email FROM banned_account WHERE banned=true"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    if len(result)==0:
        print('tidak ada akun untuk dihapus')
        return
    #get account list from folder
    accountInFolder = os.listdir('C:\\temp\\')
    accountList = []
    for row in result:
        account = row['email']
        #when account exists in folder then delete it
        if account in accountInFolder:
            accountList.append(account)
            shutil.rmtree('C:\\temp\\'+account)
    #define total account which folder deleted!
    total = len(accountList)
    print(str(total)+' account folder deleted')

deleteBanned()