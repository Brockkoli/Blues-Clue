'''
Course: ICT2202 Digital Forensics
Lab: P5
Team: zero1
Anti-forensics tool name: Blue's Clue
'''

import time
import datetime
import os
from os import urandom
import shutil
import random
from random import randrange
import filedate
import ctypes
from pathlib import Path
from hashlib import md5
from Cryptodome.Cipher import AES
import wmi
from faker import Faker

#Variables
driveList=[]
encExtList = ['.rst','.txt','.md','.docx','.odt','.html','.ppt','.doc']# random file ext to use
encNameList = ['secret', 'darkweb', 'db-dump', 'blackmail', 'target', 'golddust', 'accounts', 'keys', 'finance',
'do-not-touch', 'cats', 'dogs', 'normal-things', 'important', 'not-important'] # random file name to use

srcPath = r'C:\Docuemnts\secret.txt' #CHANGE TO YOUR RESPECTTIVE PATH WHERE YOUR FILE IS
password = '31337'

newPath=Path(r'C:\Docuemnts') #NEW PATH, MAKE SURE THERE ARE MULTIPLE FOLDER TO ENSURE NEW FILE GO TO MULTIPLE DIRECTORY

ntdll = ctypes.windll.ntdll
setShutDownPriviledge = 19

def BSOD():#Literally just BSOD your device
    enabled = ctypes.c_bool()
    res = ntdll.RtlAdjustPrivilege(setShutDownPriviledge, True, False, ctypes.pointer(enabled))
    response = ctypes.c_ulong()
    res = ntdll.NtRaiseHardError(0xDEADDEAD, 0, 0, 0, 6, ctypes.byref(response))

'''
Function to get key and initialisation vector from the password + salt
    password is chosen by user
    salt is added to password for additional complication
    keyLength is length of the encryption key in bytes
    ivLength is the length of the initialisation vector in bytes
2 values will be return: key and iv
'''
def getKeyAndIv(password, salt, keyLength, ivLength): 
    d = d_i = b''
    while len(d) < keyLength + ivLength:
        d_i = md5(d_i + str.encode(password) + salt).digest() # get md5 hash value
        d += d_i
    return d[:keyLength], d[keyLength:keyLength+ivLength]

'''
inputFile is the plaintext file
outputFile is the encrypted file
call getKeyAndIv to create key and iv for cipher creation
'''
def encrypt(inputFile, outputFile, password, key_length=32):
    bs = AES.block_size # 16 bytes
    salt = urandom(bs) # return a string of random bytes
    key, iv = getKeyAndIv(password, salt, key_length, bs)

    # MODE_CBC or Ciphertext Block Chaining
    # each block of plaintext XOR with previous ciphertext block before encryption
    cipher = AES.new(key, AES.MODE_CBC, iv)
    outputFile.write(salt)
    complete = False

    while not complete:
        chunk = inputFile.read(1024 * bs) 
        if len(chunk) == 0 or len(chunk) % bs != 0:# add padding before encryption
            paddingSize = (bs - len(chunk) % bs) or bs
            chunk += str.encode(paddingSize * chr(paddingSize))
            complete = True
        outputFile.write(cipher.encrypt(chunk))

'''
Function to create and encrypt file in new directory
'''
def fileManip():
    subdirectories = [x for x in newPath.iterdir() if x.is_dir()]
    dstPathLen =len(subdirectories)
    pathSeed=random.sample(range(0,dstPathLen),int(dstPathLen/2))
    isExist= os.path.exists(srcPath)
    if isExist == True:
        pass
    else:
        fle = Path(srcPath)
        fle.touch(exist_ok=True)
        f = open(fle,"a")
        f.write(fake.name()+"\n\n"+fake.address()+"\n\n"+fake.text())
        f.close()

    with open(srcPath, 'rb') as inputFile, open(srcPath, 'wb') as outputFile: # encry file first, follow by making copy of it.
            encrypt(inputFile, outputFile, password)
 
    for x in pathSeed:
        dstPath=str(subdirectories[x])

        newDstPath = dstPath+"\\"+random.choice(encNameList)+random.choice(encExtList)
        shutil.copyfile(srcPath,newDstPath)

        a_file = filedate.File(newDstPath)
        newCreationMetaDate=meta_modification("creation")
        newMetadate=meta_modification("modified_accessed")
        a_file.set(
            created=newCreationMetaDate,
            modified=newMetadate,
            accessed=newMetadate
        )
    chngSrcName = newPath.__str__()+"\\"+random.choice(encNameList)+random.choice(encExtList)
    os.rename(srcPath,chngSrcName)
    src_file = filedate.File(chngSrcName)
    newCreationMetaDate=meta_modification("creation")
    newMetadate=meta_modification("modified_accessed")
    src_file.set(
        created=newCreationMetaDate,
        modified=newMetadate,
        accessed=newMetadate
    )
'''
Function to modify Metadate of files
'''
def meta_modification(metaDateType):
    if metaDateType == "creation":
        generatedYear = generateNumber(2020, 2021)
    else:
        generatedYear = generateNumber(2020, 2022)
    
    generatedMonth = generateNumber(1, 12)
    generatedDay = generateDay(generatedMonth)
    generatedHour = generateNumber(00, 23)
    generatedMinute = generateNumber(00, 59)
    generatedSecond = generateNumber(0, 60)
    generatedMicrosecond = generateNumber(000000, 999999)

    newModDateString = "{}.{}.{} {}:{}:{}.{}".format(generatedYear, generatedMonth, generatedDay, generatedHour, generatedMinute, generatedSecond,
    generatedSecond, generatedMicrosecond)

    return newModDateString

# To generate a number from range
def generateNumber(rangeStart, rangeEnd):
    return randrange(rangeStart, rangeEnd)

def generateDay(month):
    if month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
        return generateNumber(1, 31)
    elif month == 2:
        return generateNumber(1, 28)
    else:
        return generateNumber(1, 30)


'''
Function to retrive current plugged in drives seial number
'''
def list_driveID(): #get the drive ID
    """
    get all drive serial number 
    """
    c = wmi.WMI()
    serialID=[]
    for item in c.Win32_PhysicalMedia():
        serialID.append(item.SerialNumber)
    return serialID

'''
Function to check for changes in drive that are plugged in
'''
def watch_drives():#watch for drive change
    runCon=True
    while runCon:

        drives = list_driveID()
        if(drives==driveList): #if the changes was made because user was taking out and putting back in their usb drive, nothing happen
            pass
        
        elif(len(drives)<len(driveList)): #detect usb drive was was originally part of the machine 
            if (all(x in driveList for x in drives )):
                pass

        else: #if there was changes and it is an entirely new drive
            runCon=False
            fileManip() #file copying and manipulation function
            time.sleep(6)
            # BSOD() #BSOD function, Please comment it unless using it live

        time.sleep(1)

if __name__ == '__main__':
    
    driveList=list_driveID()
    fake = Faker() 
    watch_drives()
    
