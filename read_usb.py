import json
import subprocess
import time
from dataclasses import dataclass
from typing import Callable, List

detect_usb = False


@dataclass
class Drive:
    letter: str
    label: str
    drive_type: str

def list_drives():
    """
    Get a list of drives using WMI
    :return: list of drives
    """
    proc = subprocess.run(
        args=[
            'powershell',
            '-noprofile',
            '-command',
            'Get-WmiObject -Class Win32_LogicalDisk | Select-Object deviceid,volumename,drivetype | ConvertTo-Json'
        ],
        text=True,
        stdout=subprocess.PIPE
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        print('Failed to enumerate drives')
        return []
    devices = json.loads(proc.stdout)

    return [Drive(
        letter=d['deviceid'],
        label=d['volumename'],
        drive_type=d['drivetype']
        # drive_type=drive_types[d['drivetype']]
    ) for d in devices]


def watch_drives(on_change: Callable[[List[Drive]], None], poll_interval: int = 1):
    prev = None
    while True:
        drives = list_drives()
        if prev != drives:
            on_change(drives)
            prev = drives
            for x in range(len(drives)):  # test-start
                if(drives[x].drive_type==2):
                    print("USB detected")#test-end
        time.sleep(poll_interval)


if __name__ == '__main__':
    watch_drives(on_change=print)


