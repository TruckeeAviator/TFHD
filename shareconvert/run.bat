echo off


MsiExec.exe /I{747840DC-0E27-476E-8279-34A8CC5DF3C0}
start /D C:\ powershell -ExecutionPolicy Bypass C:\sharedconvert\shareconvert.ps1cmd
