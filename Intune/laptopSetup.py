import os

#List of software to remove
removeSoftwareList = ["Google Chrome", "Adobe Acrobat Reader", "Microsoft Office Professional Plus 2013", "Microsoft Office Professional Plus 2016", "Configuration Manager Client"]

#Remove software loop
print("Removing Software\n")
for removeSoftware in removeSoftwareList:
    os.system(f'wmic product where description="{removeSoftware}" uninstall')

#Remove SCCM
os.system('C:\Windows\ccmsetup\ccmsetup.exe /uninstall')

#Install software
installSoftwareList = ['"C:\Intune\Zoom VDI\ZoomVDIUniversalPluginx64.msi"', '"C:\Intune\Zoom\ZoomInstallerFull.msi"']

#Install software loop
print("Installing Software\n")
for installSoftware in installSoftwareList:
    os.system(f'msiexec /i {installSoftware} /qn')

#Install Cisco Umbrella
os.system('msiexec /i "C:\Intune\Cisco Umbrella\Setup.msi" /qn ORG_ID=*** USER_ID=***')

#Install Intune
os.system('winget install "Company Portal" --source msstore --accept-package-agreements --accept-source-agreements')
