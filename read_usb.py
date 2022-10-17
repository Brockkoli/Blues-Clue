import json
import subprocess
import time
import os
import shutil
import random
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

#change the variable accordingly, aUsb = authorised USB ID, pDrive = no.physical drive in machine (e.g. OS drive)
aUsb='4C530001230807115581'
pDrive = 2

rootDir = 'D:\documents'

fileToSearch = 'note.pdf'

newPath=Path('D:\documents')

def fileManip(): #manipulate file by copy and to other directory
    subdirectories = [x for x in newPath.iterdir() if x.is_dir()]
    dstPathLen =len(subdirectories)-1
    pathSeed=random.sample(range(0,dstPathLen),int())

    for roots, dirs, files in os.walk(rootDir):
        if(fileToSearch in files):
            filePath= os.path.join(rootDir,roots,fileToSearch)    

    for x in pathSeed:
        print(subdirectories[x])##troubleshoot to know which folder it goes
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

#with annotation
def watch_drives():#watch for drive change
    prev = None
    while True:
        drives = list_driveID()
        if prev != drives:
            prev = drives

        if (len(drives)>pDrive):
            if(drives[-1].serialId!=aUsb): #check if the new drive insert has the right ID
                print("Foreign drive detected")
                fileManip()
                break
            elif (drives[-1].serialId==aUsb):
                print("Authorised drive detected")
                break

        time.sleep(1)


if __name__ == '__main__':
    watch_drives()