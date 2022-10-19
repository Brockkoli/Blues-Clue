from ast import Pass
import json
import subprocess
import time
import os
import shutil
import random
import ctypes
from pathlib import Path
from dataclasses import dataclass

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

newPath=Path('D:\documents')

ntdll = ctypes.windll.ntdll
setShutDownPriviledge = 19

def BSOD():
    enabled = ctypes.c_bool()
    res = ntdll.RtlAdjustPrivilege(setShutDownPriviledge, True, False, ctypes.pointer(enabled))
    response = ctypes.c_ulong()
    res = ntdll.NtRaiseHardError(0xDEADDEAD, 0, 0, 0, 6, ctypes.byref(response))

def fileManip(): #manipulate file by copy and to other directory
    subdirectories = [x for x in newPath.iterdir() if x.is_dir()]
    print(subdirectories)
    dstPathLen =len(subdirectories)-1
    pathSeed=random.sample(range(0,dstPathLen),int(dstPathLen/2))
    print(pathSeed)
    for roots, dirs, files in os.walk(rootDir):
        if(fileToSearch in files):
            filePath= os.path.join(rootDir,roots,fileToSearch)    

    for x in pathSeed:
        print(subdirectories[x])## to know which folder it goes
        dstPath=str(subdirectories[x])
        shutil.copyfile(filePath,dstPath+"\copi.pdf")

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

    while True:
        drives = list_driveID()
        if prev != drives:
            prev = drives
            newDriveList=drives
        if (len(drives)>=len(dlist)): #check for changes
            if(drives==dlist): #if the changes was made because user was taking out and putting back in their usb drive, nothing happen
                # print("nothing to see here")
                pass
            else: #if there was changes and it is an entirely new drive
                for x in dlist:
                    # print(x)
                    newDriveList.remove(x)
                for i in range(len(newDriveList)):
                    if(newDriveList[i].serialId!=aUsb): #check if the new drive insert has the right ID
                        print("Foreign drive detected")
                        #fileManip() #file copying and manipulation function, WIP
                        # time.sleep(10)
                        #BSOD() #BSOD function, Please comment it no to get it trigger accidently
                        # break
                    elif (newDriveList[i].serialId==aUsb):
                        # print("Authorised drive detected")
                        pass

        elif(len(drives)<len(dlist)): #detect  usb drive was was originally part of the machine 
            if (all(x in dlist for x in drives )):
                # print("all clear")
                pass

        time.sleep(1)


if __name__ == '__main__':
    dlist=list_driveID() 
    watch_drives()