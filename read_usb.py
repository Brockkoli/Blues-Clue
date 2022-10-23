from ast import Pass
import json
import subprocess
import time
import os
from os import urandom
import shutil
import random
import ctypes
from pathlib import Path
from dataclasses import dataclass
from hashlib import md5
from Cryptodome.Cipher import AES

#step 1
#detect USB drive
#step 2
#get a file, duplicate it and encrypt it?
#step 3
#change MetaData (maybe)
#step 4
#cause more disruptuion
#step 5
#profit

#change the variable accordingly, aUsb = authorised USB ID, pDrive = no. physical drive in machine (e.g. OS drive)
aUsb='4C530001230807115581'
pDrive = 2
dlist=[]

rootDir = 'D:\documents'

fileToSearch = 'Acad Calendar_SIT JDP 2022.pdf'
fileRenamed = 'copi.pdf'
# fileToSearch = 'iprep.xlsx'  # kian test doc
# fileRenamed = 'copi.xlsx'  # kian test doc
encNameList = ['secret.xlsx', 'darkweb.xlsx', 'db-dump.xlsx', 'blackmail.xlsx', 'target.xlsx', 'golddust.xlsx'] # list of names for the encrypted file 
encrpytedFile = random.choice(encNameList)
password = '31337'

newPath=Path('D:\documents')
# newPath=Path('C:\documents')  # kian test directory

ntdll = ctypes.windll.ntdll
setShutDownPriviledge = 19

def BSOD():
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

def fileManip(): #manipulate file by copy and to other directory
    subdirectories = [x for x in newPath.iterdir() if x.is_dir()]
    print("\nSubdirectories: ")
    print(subdirectories)
    dstPathLen =len(subdirectories)-1
    pathSeed=random.sample(range(0,dstPathLen),int(dstPathLen/2))
    print("\nPathseed: ")
    print(pathSeed)
    for roots, dirs, files in os.walk(rootDir):
        if(fileToSearch in files):
            filePath= os.path.join(rootDir,roots,fileToSearch)    

    for x in pathSeed:
        print(subdirectories[x])## to know which folder it goes
        dstPath=str(subdirectories[x])
        shutil.copyfile(filePath,dstPath+"\\"+fileRenamed)
        openCpFile = open(dstPath+"\\"+fileRenamed, 'rb')
        with openCpFile as inputFile, open(dstPath+"\\"+encrpytedFile, 'wb') as outputFile:    # encrypted file open as seperate file
            encrypt(inputFile, outputFile, password)
            openCpFile.close() # close copied file before deletion
            os.remove(dstPath+"\\"+fileRenamed) # delete unencrypted copied file


@dataclass
class Drive:
    serialId: str

def list_driveID(): #get the drive ID
    """
    get all drive serial number 
    """
    proc = subprocess.run(
        args=[
            'powershell',
            '-noprofile',
            '-command',
            'Get-WmiObject -Class Win32_PhysicalMedia | Select-Object serialnumber | ConvertTo-Json'
        ],
        text=True,
        stdout=subprocess.PIPE
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        print('Failed to enumerate drives')
        return []
    devices = json.loads(proc.stdout)

    return [Drive(serialId=d['serialnumber']) for d in devices]

def watch_drives():#watch for drive change
    prev = None
    runCon=True
    while runCon:

        drives = list_driveID()

        if prev != drives:
            prev = drives
        
        if(drives==dlist): #if the changes was made because user was taking out and putting back in their usb drive, nothing happen
            pass
        
        elif(len(drives)<len(dlist)): #detect usb drive was was originally part of the machine 
            if (all(x in dlist for x in drives )):
                pass

        else: #if there was changes and it is an entirely new drive
            # print("original drive:"+str(dlist))
            # print("updated drive:"+ str(drives))
            newDriveList= [item for item in drives if item not in dlist]
            print(newDriveList)
            for i in range(len(newDriveList)):
                if(newDriveList[i].serialId!=aUsb): #check if the new drive insert has the right ID
                    print("Foreign drive detected")
                    runCon=False
                    #fileManip() #file copying and manipulation function, WIP
                    # time.sleep(10)
                    #BSOD() #BSOD function, Please comment it no to get it trigger accidently
                    # break
                elif (newDriveList[i].serialId==aUsb):
                    pass

        time.sleep(1)


if __name__ == '__main__':
    dlist=list_driveID() 
    print(dlist)
    watch_drives()