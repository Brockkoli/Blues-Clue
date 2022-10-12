import json
import subprocess
import time
from dataclasses import dataclass
from typing import Callable, List

#change this accordingly, aUsb = authorised USB ID, pDrive = physical drive in machine (e.g. OS drive)
aUsb='4C530001230807115581'
pDrive = 2

@dataclass
class Drive:
    serialId: str

def list_driveID() -> List[Drive]:
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

    return [Drive(
        serialId=d['serialnumber']
    ) for d in devices]

def watch_drives(on_change: Callable[[List[Drive]], None], poll_interval: int = 1):
    prev = None
    while True:
        drives = list_driveID()
        if prev != drives:
            on_change(drives)
            prev = drives

        if (len(drives)>pDrive):
            if(drives[-1].serialId==aUsb): #check if the new drive insert has the right ID
                print("USB detected")
            else:
                print("unauthorise")

        time.sleep(poll_interval)


if __name__ == '__main__':
    watch_drives(on_change=print)