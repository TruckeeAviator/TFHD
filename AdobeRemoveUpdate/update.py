import os
import shutil
from datetime import datetime
import subprocess
import platform 

def ping(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]

    result = subprocess.run(command, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf8')
    if "Destination host unreachable" in output or "100% packet loss" in output:
        return 1
    return 0

#convert string into a list
def convertString(string):
    li = list(string.split("\n"))
    return li

#Download the installer, remove the wrong version, install the right version, cleanup
def removeUpdate(pcName):
    
    shutil.copyfile('C:\AcroRdrDC2300620320_en_US.exe', '\\\\%s\c$\AcroRdrDC2300620320_en_US.exe' % pcName)
    os.system('C:\windows\pstools\psexec \\\\%s wmic product where description="Adobe Acrobat (64-bit)" uninstall' % pcName)
    os.system('C:\windows\pstools\psexec \\\\%s C:\AcroRdrDC2300620320_en_US.exe -sfx_nu /sALL /msi EULA_ACCEPT=YES' % pcName)
    os.remove('\\\\%s\c$\AcroRdrDC2300620320_en_US.exe' % pcName)

#Read text file
file = open('list.txt', 'r')
data = file.read()
data = convertString(data)

#Loop through the list
for x in data:
    print("Running on: " + x.upper())

    if ping(x) != 0:
        print("Host " + x.upper() + " is off, skipping")
        outputFile = open("outputLog.txt", "a")
        outputFile.write(datetime.now().strftime("%D %H:%M") + ": " "Skipped " + x.upper() + "\n")
        outputFile.close()
        continue

    removeUpdate(x)
    print("*** Finished install on: " + x.upper() + " ***")

    #Write to log file
    outputFile = open("outputLog.txt", "a")
    outputFile.write(datetime.now().strftime("%D %H:%M") + ": " "Installed on " + x.upper() + "\n")
    outputFile.close()

file.close()
