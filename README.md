# ICT2202- Team Zero1's Anti-forensic tool

Blue's clue is a proof-of-concept anti-forensics tool to covertly delay the digital forensics investigation using various disruptive and manipulative features.
> **Note:** This is an assignment project for  **ICT 2202 Digital Forensics** 

> Singapore Institute of Technology Bachelor of Engineering with Honours in Information and Communications Technology majoring in Information Security
##  Usage

## Solution name: Blue's clue
- PC detect usb drive and encrpyt file + Generate false evidence
- Must be able to detect Usb drive
- Must be able to identify unique ID of drive
- Perform action when detected unauthorized drive (false evidence planting/corrupt or encrypt file)
- Processes must perform on background without being notice (do not have any prompt)
- Code will be written in Python 

---

## User Instruction Manual
There are some pre-requistite before this script will work with your machine. Do follow the instruction to make sure that process goes through smoothly
1. PC must be installed with Windows operating system 8 onward
2. Ensure machine is installed with Python version 3.0 onwards
3. Run "Requirements.bat" to install the dependencies by entering the following in cmd.exe: `Requirements.bat`
   - Which will install the following: 
      - filedate  
      - WMI
      - pycryptodomex
      - Faker
4. Open the script in a code editor tool (even notepad can work if you want to) and change the file directory to ensure the script to look for the right directory and perform its function.
5. Save it as a .pyw file to ensure that no console windows would prompt when the script is running in the background (or compile it to an executable file)
6. Press `Win + R` , and you will see the Run prompt. Enter the following `shell:startup`![image](https://user-images.githubusercontent.com/24997390/197673717-8905ad4c-fb5f-4118-ac91-7dee69204a8f.png)
7. Press `OK` and a new winow will be open, just drag the .pyw script into it.![image](https://user-images.githubusercontent.com/24997390/197674255-8bd3ddf4-fc8b-4738-bf0a-81111499476a.png)
8. Restart your PC and the program should be running in the background

---

### Upon Installation
Do **NOT** attempt to plug in any USB drives into the computer upon the installation of the program. Whitelisting of USB devices are done on startup of the program. As this is a program that is supposed to run in the background, hence there is no GUI for manual whitelisting of USB drives. 

---

### To whitelist USB 
#### Whitelist upon installation
1. Make sure that the program is added to run on startup
2. Shutdown the computer
3. Plug in the desired USB drive
4. Power on the computer
5. The USB device is now whitelisted, it can be removed and plugged backed into the computer for use!

#### Whitelist upon startup
1. Make sure that the USB device is plugged into the computer before powering on
2. Turn on the computer
3. The USB device is now whitelisted, it can be removed and plugged backed into the computer for use!

#### Set your file source and destination
1. Under `srcPath` varaible,  just change it to where your file is located. A text file will be created if the file you have stated doesn't exist!
2. For the destination, just chage `newPath` variable to a folder with multiple sub-folders, do have more than 4 sub-folder if possible!
