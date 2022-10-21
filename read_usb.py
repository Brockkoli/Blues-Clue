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

rootDir = 'D:\documents'

# fileToSearch = 'Acad Calendar_SIT JDP 2022.pdf'
# fileRenamed = 'copi.pdf'
fileToSearch = 'iprep.xlsx'
fileRenamed = 'copi.xlsx'
encrpytedFile = 'enc.xlsx'
password = '31337'

#newPath=Path('D:\documents')
newPath=Path('C:\documents')

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
    cipher = AES.new(key, AES.MODE_CBC, iv)  # MODE_CBC or Ciphertext Block Chaining
    outputFile.write(salt)
    finished = False

    while not finished:
        chunk = inputFile.read(1024 * bs) 
        if len(chunk) == 0 or len(chunk) % bs != 0:# add padding before encryption
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += str.encode(padding_length * chr(padding_length))
            finished = True
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
        with open(dstPath+"\\"+fileRenamed, 'rb') as inputFile, open(dstPath+"\\"+encrpytedFile, 'wb') as outputFile:    # encrypted file open as seperate file currently for testing purposes
            encrypt(inputFile, outputFile, password)


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

#with annotation
def watch_drives():#watch for drive change
    prev = None
    while True:
        drives = list_driveID()
        if prev != drives:
            prev = drives
            print(drives)
        if (len(drives)>pDrive):
            if(drives[-1].serialId!=aUsb): #check if the new drive insert has the right ID
                print("Foreign drive detected")
                fileManip()
                time.sleep(10)
                # BSOD() #BSOD function, Please comment it no to get it trigger accidently
                break
            elif (drives[-1].serialId==aUsb):
                print("Authorised drive detected") #remove all print when not trouble shooting
                break

        time.sleep(1)


if __name__ == '__main__':
    watch_drives()