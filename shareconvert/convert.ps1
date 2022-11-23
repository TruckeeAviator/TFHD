#Who is doing this?
$Credentials = Get-Credential

#Set vars
$shareduser=$env:COMPUTERNAME

#Set Regedit path
$RegPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"

#Delete shared keys for autologin
Remove-ItemProperty -Path $RegPath -Name "AutoAdminLogon"
Remove-ItemProperty -Path $RegPath -Name "DefaultUsername"
Remove-ItemProperty -Path $RegPath -Name "DefaultPassword"
Remove-ItemProperty -Path $RegPath -Name "ForceAutoLogon"

#Remove user from AD
#Remove-ADUser -Identity $shareduser

#Log to origianl build file
"Share to Uni convert" |Out-File C:\Build\Build.txt -Append
("Configured by " + $Credentials.UserName + " on: " + (Get-Date).ToString()) | Out-File C:\Build\Build.txt -Append

restart-computer
