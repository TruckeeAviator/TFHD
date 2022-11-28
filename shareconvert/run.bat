echo off


MsiExec.exe /I{747840DC-0E27-476E-8279-34A8CC5DF3C0} /qn
MsiExec.exe /X{562B7F33-EA0E-4C2E-A270-23CAA72C1480} /qn
start /D C:\ powershell -ExecutionPolicy Bypass C:\sharedconvert\shareconvert.ps1cmd
