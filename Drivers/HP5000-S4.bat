Echo off
cls
rem v0.2, Kory Albert, This is modified to run as Domain Admin instead of Local!
echo Installing HP Software, Accept EULA, Click finish when done.
echo.
echo.
echo ****Press any key AFTER webpage displays!!*****
echo.
echo.
cd\"HP Mercy Scan Files\Drivers\HP Full Scanner Drivers CD"
setup.exe
timeout /t 600
rem Had to use timeout because the batch file would not wait for this install to finish
rem
rem Next Step is to Remove most of the HP drivers and put in the Mercy Stuff.  The Msiexec.exe command is just the command line way to remove a program.  the /qn flag means no user intervention, forced uninstall
echo uninstalling HP ScanJet Flow 5000 s4 Basic Device Software (Original)
MsiExec.exe /x{E01EEBAF-571F-4F2C-850E-DA56D2EDD9E3} /qn
Echo Done!
echo uninstalling HP ScanJet Flow 5000 s4 Basic Device Software (Mercy)
MsiExec.exe /x{A5AD9074-F19F-424B-9886-A3D8BB5BD161} /qn
echo **Removing HP Fluff**
echo uninstalling HP SharePoint Plugin
Echo Done!
MsiExec.exe /x{DDB31001-D2F4-4B8B-AF8C-D69C862665E9} /qn
echo uninstalling HP OneDrive Plugin 
Echo Done!
MsiExec.exe /x{B643358B-B8EB-4E60-8CC8-C8310F1338BB} /qn
echo uninstalling HP Google Drive Plugin
Echo Done!
MsiExec.exe /x{AFAB3A91-C068-4E13-993B-4B92E22B9594} /qn
echo uninstalling HP FTP Plugin
Echo Done!
MsiExec.exe /x{5F3D8219-AE3D-41D4-8E7C-26ACA5872271} /qn
echo uninstalling HP Dropbox Plugin
Echo Done!
MsiExec.exe /x{D09E3CF2-4DD2-477C-825B-C69DEEEACCF0} /qn
Echo Done!
Echo Uninstall of Full HP Drivers Complete
Echo Done!
cls
cd\"HP Mercy Scan Files"
type "messages\mercy.txt"
copy "DeployHPScanINI.bat" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\DeployHPScanINI.bat"
Echo Copied Mercy INI to All Users startup.
Echo About to Install custom Mercy HP Driver.  Ctrl-C to abort
pause
cd\"HP Mercy Scan Files\Drivers"
SJ5000_U_Basicx64.exe
rem This file is from Mercy.  It is only the core driver for the scanner.  No interface with it.
Echo Done!
type "..\messages\firmware.txt"
echo If firmware update is NOT needed, press Ctrl-C to abort, otherwise
pause
Echo About to Install new Firmware
"HP ScanJet Enterprise Flow 5000 S4 UpdateFirmware(AutoOffDisable).exe"
rem This firmware update is from Mercy.  It does not exit on its own.  You must hit a key for it to exit when it is done.
echo Firmware installation complete (or not).
cls
type "..\messages\scannerreboot.txt"
echo Please wait 10 seconds for the scanner to power back up, then
pause
echo Running Firmware setting Utility
CanyonlandApp\DriverTest\drivertest.exe
cls
type "..\messages\complete.txt"
echo To Exit....
Pause
exit
