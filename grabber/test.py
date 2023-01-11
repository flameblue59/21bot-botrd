import random
import shutil
import os

path = 'C://temp'
listAccount = os.listdir(path)
account = random.choice(listAccount)
print(account)

shutil.rmtree(path+'//cobatest')