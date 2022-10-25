# ICT2202- Anti-forensic tool

- PC detect usb drive and encrpyt file + Generate false evidence
- Must be able to detect Usb drive
- Must be able to identify unique ID of drive
- Perform action when detected unauthorized drive (false evidence planting/corrupt or encrypt file)
- Processes must perform on background without being notice
- Code will be written in Python 

## User Instruction Manual
There are some pre-requistite before this script will work with your machine. Do follow the instruction to make sure that process goes through smoothly
1. PC must be installed with Windows operating system (e.g. Windows 10, 11)
2. Ensure machine is installed with Python version 3.0 onward and also with the following library using pip installer
   - filedate (pip intall filedate)
   - WMI (pip intall WMI)
   - pycryptomex (pip intall pycryptomex)
3. Open the script in a code editor tool(even notepad can work if you want to) and change the file directory to ensure the script to look for the right directory and perform its function.
4. Save it as a .pyw file to ensure that no console windows would prompt when the script is running in the background (or compile it to an executable file if you like)
5. Press `Win + R` , and you will see the Run prompt. Enter the following `shell:startup`![image](https://user-images.githubusercontent.com/24997390/197673717-8905ad4c-fb5f-4118-ac91-7dee69204a8f.png)
6. Press `OK` and a new winow will be open, just drag the .pyw script into it.![image](https://user-images.githubusercontent.com/24997390/197674255-8bd3ddf4-fc8b-4738-bf0a-81111499476a.png)
7. Restart your PC and it should running in the background
