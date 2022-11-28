#Who is doing this?
$Credentials = Get-Credential

#Set Pre requirments
Add-WindowsCapability -Online -Name "Rsat.ServerManager.Tools~~~~0.0.1.0"
Add-WindowsCapability -Online -Name "Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0"

#Set vars
$shareduser=$env:COMPUTERNAME
$regprofile="HKLM:SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
$RegPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"

# Retrieve DN of local computer.
$SysInfo = New-Object -ComObject "ADSystemInfo"
$ComputerDN = $SysInfo.GetType().InvokeMember("ComputerName", "GetProperty", $Null, $SysInfo, $Null)

#Delete shared keys for autologin
Remove-ItemProperty -Path $RegPath -Name "AutoAdminLogon"
Remove-ItemProperty -Path $RegPath -Name "DefaultUsername"
Remove-ItemProperty -Path $RegPath -Name "DefaultPassword"
Remove-ItemProperty -Path $RegPath -Name "ForceAutoLogon"

#Remove user from AD
Remove-ADUser -Identity $shareduser -Confirm:$False

#Delete AD memberships
Remove-ADGroupMember -Identity "Shared" -Members $ComputerDN -Confirm:$False
Remove-ADGroupMember -Identity "App-Imprivata Shared (Logout)" -Members $ComputerDN -Confirm:$False

#Delete local shared user account
Remove-Item -LiteralPath "C:\Users\$shareduser" -Force -Recurse

#Reinstall imprivada as unique
#msiexec.exe /i “ImprivataAgent_x64.msi" IPTXPRIMSERVER="HTTPS://TFHD-IMPRIV01.TFHD.AD/sso/servlet/messagerouter" AGENTTYPE=1 /qn /norestart

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
"Share to Uni convert" |Out-File C:\Build\Build.txt -Append
("Configured by " + $Credentials.UserName + " on: " + (Get-Date).ToString()) | Out-File C:\Build\Build.txt -Append

Start-Sleep -s 10

#Remove extra admin tools
Remove-WindowsCapability -Online -Name "Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0"
Remove-WindowsCapability -Online -Name "Rsat.ServerManager.Tools~~~~0.0.1.0"

restart-computer
