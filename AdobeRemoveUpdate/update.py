import os
import shutil

#convert string into a list
def convertString(string):
    li = list(string.split("\n"))
    return li

#Download the installer, remove the wrong version, install the right version, cleanup
def removeUpdate(pcName):
    
    shutil.copyfile('C:\AcroRdrDC2300620320_en_US.exe', '\\\\%s\c$\AcroRdrDC2300620320_en_US.exe' % pcName)
    os.system('C:\windows\pstools\psexec \\\\%s wmic product where description="Adobe Acrobat (64-bit)" uninstall')
    os.system('C:\windows\pstools\psexec \\\\%s C:\AcroRdrDC2300620320_en_US.exe -sfx_nu /sALL /msi EULA_ACCEPT=YES')
    os.remove('\\\\%s\c$\AcroRdrDC2300620320_en_US.exe' % pcName)

#Read text file
file = open('list.txt', 'r')
data = file.read()
data = convertString(data)

#Loop through the list
for x in data:
    removeUpdate(x)
    print("*** Finished install on: " + x.upper())
