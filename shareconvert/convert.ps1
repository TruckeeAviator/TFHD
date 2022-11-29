#Who is doing this?
$Credentials = Get-Credential

#Install Pre requirments, Admin tools
Add-WindowsCapability -Online -Name "Rsat.ServerManager.Tools~~~~0.0.1.0"
Add-WindowsCapability -Online -Name "Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0"

#Set vars
$shareduser = $env:COMPUTERNAME
$regprofile = "HKLM:SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
$RegPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
$ImprivataShared = "{562B7F33-EA0E-4C2E-A270-23CAA72C1480}"
$ImprivataSharedupdated = "{FF1756D4-D776-4F8D-86E1-638C4B42F44A}"
$Uniflow = "{747840DC-0E27-476E-8279-34A8CC5DF3C0}"
$PathImprivada = "C:\sharedconvert\ImprivataAgent_x64.msi"

# Retrieve DN of local computer.
$SysInfo = New-Object -ComObject "ADSystemInfo"
$ComputerDN = $SysInfo.GetType().InvokeMember("ComputerName", "GetProperty", $Null, $SysInfo, $Null)

#Delete shared keys for autologin. Some of these are legacy and will guive error.
Remove-ItemProperty -Path $RegPath -Name "AutoAdminLogon"
Remove-ItemProperty -Path $RegPath -Name "DefaultUsername"
Remove-ItemProperty -Path $RegPath -Name "DefaultPassword"
Remove-ItemProperty -Path $RegPath -Name "ForceAutoLogon"

#Remove user from AD
Remove-ADUser -Identity $shareduser -Confirm:$False

#Delete AD memberships
Remove-ADGroupMember -Identity "Shared" -Members $ComputerDN -Confirm:$False
Remove-ADGroupMember -Identity "App-Imprivata Shared (Logout)" -Members $ComputerDN -Confirm:$False

#Remove local user from Reg and C:
Get-CimInstance -Class Win32_UserProfile | Where-Object { $_.LocalPath.split('\')[-1] -eq $shareduser } | Remove-CimInstance

#Remove Uniflow if possible
Start-Process "C:\Windows\System32\msiexec.exe" -ArgumentList "/x $($Uniflow) /quiet /noreboot" -Wait

#Remove Imprivada shared
Start-Process "C:\Windows\System32\msiexec.exe" -ArgumentList "/x $($ImprivataShared) /quiet REBOOT=ReallySuppress /noreboot" -Wait
Start-Process "C:\Windows\System32\msiexec.exe" -ArgumentList "/x $($ImprivataSharedupdated) /quiet REBOOT=ReallySuppress /noreboot" -Wait

Start-Sleep -s 10

#Reinstall imprivada as unique
Start-Process "C:\Windows\System32\msiexec.exe" -ArgumentList "/i $($PathImprivada) IPTXPRIMSERVER=HTTPS://TFHD-IMPRIV01.TFHD.AD/sso/servlet/messagerouter AGENTTYPE=1 /qn /norestart" -Wait

#Add new AD memberships
$App = @(
    "Unique"
)
Start-Job -Credential $Credentials -ArgumentList $App -ScriptBlock {
    
    Param($App)

    [int] $ADS_PROPERTY_APPEND = 3
    #Get the computer DN
    $SysInfo = New-Object -ComObject "ADSystemInfo"
    $UserDN = $SysInfo.GetType().InvokeMember("ComputerName", "GetProperty", $Null, $SysInfo, $Null)
    $ComputerDN = "LDAP://$UserDN"
    #Get the Domain DN
    $ORoot = [ADSI]"LDAP://rootDSE"
    $strDomainPath = $ORoot.Get("defaultNamingContext")
    #Create ADODB connection
    $oConnection = New-Object -ComObject "ADODB.Connection"
    $oConnection.Provider= "ADsDSOObject"
    $oConnection.Open("Active Directory Provider")

    foreach($App in $App)
    {
        #Get the specefied group
        $oRs = $oConnection.Execute("SELECT adspath FROM 'LDAP://$strDomainPath' WHERE objectCategory='group' AND  Name='$App'")
        If (!$oRs.EOF)
        {
            $strAdsPath = ($oRs.Fields |  Select value ).value
        }
        If($strAdsPath)
        {
            $objGroup = [ADSI]$strAdsPath
            $objComputer = [ADSI]$ComputerDN
            #verify if the computer is a member of the Group
            If ($objGroup.ismember($objComputer.adspath) -eq $false) 
            {
                #Add the the computer to the specefied group
                $objGroup.PutEx($ADS_PROPERTY_APPEND,"member",@("$UserDN"))
                $objGroup.setinfo()
            }
        }
    }
}
Start-Sleep -s 10
$App = @(
    "App-Imprivata Unique"
)
Start-Job -Credential $Credentials -ArgumentList $App -ScriptBlock {
    
    Param($App)

    [int] $ADS_PROPERTY_APPEND = 3
    #Get the computer DN
    $SysInfo = New-Object -ComObject "ADSystemInfo"
    $UserDN = $SysInfo.GetType().InvokeMember("ComputerName", "GetProperty", $Null, $SysInfo, $Null)
    $ComputerDN = "LDAP://$UserDN"
    #Get the Domain DN
    $ORoot = [ADSI]"LDAP://rootDSE"
    $strDomainPath = $ORoot.Get("defaultNamingContext")
    #Create ADODB connection
    $oConnection = New-Object -ComObject "ADODB.Connection"
    $oConnection.Provider= "ADsDSOObject"
    $oConnection.Open("Active Directory Provider")

    foreach($App in $App)
    {
        #Get the specefied group
        $oRs = $oConnection.Execute("SELECT adspath FROM 'LDAP://$strDomainPath' WHERE objectCategory='group' AND  Name='$App'")
        If (!$oRs.EOF)
        {
            $strAdsPath = ($oRs.Fields |  Select value ).value
        }
        If($strAdsPath)
        {
            $objGroup = [ADSI]$strAdsPath
            $objComputer = [ADSI]$ComputerDN
            #verify if the computer is a member of the Group
            If ($objGroup.ismember($objComputer.adspath) -eq $false) 
            {
                #Add the the computer to the specefied group
                $objGroup.PutEx($ADS_PROPERTY_APPEND,"member",@("$UserDN"))
                $objGroup.setinfo()
            }
        }
    }
}

#Log to origianl build file
"Shared to Unique convert" |Out-File C:\Build\Build.txt -Append
("Configured by " + $Credentials.UserName + " on: " + (Get-Date).ToString()) | Out-File C:\Build\Build.txt -Append

Start-Sleep -s 10

#Remove extra admin tools
Remove-WindowsCapability -Online -Name "Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0"
Remove-WindowsCapability -Online -Name "Rsat.ServerManager.Tools~~~~0.0.1.0"

restart-computer
