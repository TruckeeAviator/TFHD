echo off
cls

echo **Removing ImprivataAgent Shared**
MsiExec.exe /I{747840DC-0E27-476E-8279-34A8CC5DF3C0} /qn
MsiExec.exe /X{562B7F33-EA0E-4C2E-A270-23CAA72C1480} /qn REBOOT=ReallySuppress /norestart
echo **Installing ImprivataAgent Unique**
cd "C:\sharedconvert"
msiexec.exe /i “ImprivataAgent_x64.msi" IPTXPRIMSERVER="HTTPS://TFHD-IMPRIV01.TFHD.AD/sso/servlet/messagerouter" AGENTTYPE=1 /qn /norestart
echo **Wait for ImprivataAgent to install**
timeout /t 120
start /D C:\ powershell -ExecutionPolicy Bypass C:\sharedconvert\shareconvert.ps1
