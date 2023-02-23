Write-Host "*** This will remove all users accounts besides yours and built-in accounts ***"
Write-Host "*** Please logout all other users before running this script! ***"
Write-Host "*** This will take time depending on the number of accounts, please let the script finish ***"

#Log when the cleaner was run
"Account Pruning was preformed $(Get-Date)" | out-file C:\cleaner-log.txt -Append
Start-Sleep -s 10

#Get the username of the logged-in user
$currentUser = Get-WmiObject -Class Win32_ComputerSystem | Select-Object -ExpandProperty UserName
#Clean up text
$currentUser = $currentUser -replace "TFHD_DOMAIN\\", ""
$numAccounts = 0

#Get User List
Get-ChildItem "HKLM:\Software\Microsoft\Windows NT\CurrentVersion\ProfileList" |
    ForEach-Object{

        #Get path from reg to convert into username string
        $profileName=$_.GetValue('ProfileImagePath')

        #Current user checking doesnt work via RDP. Current users dont seem to be affected as the system brings an error. Removing if/and check
        if( ($profileName -notmatch 'administrator|Ctx_StreamingSvc|NetworkService|Localservice|systemprofile') )
        {

            #Clean up string for removal command
            $profileName= $profileName -replace "C:\\Users\\", ""
            write-host "Removing profile: $profileName" -Fore green

            #Remove Account from computer
            Get-CimInstance -Class Win32_UserProfile | Where-Object { $_.LocalPath.split('\')[-1] -eq $profileName } 2>$null | Remove-CimInstance
            Write-Host "Removed!" -Fore red
            $numAccounts++
        }
        else
        {
            Write-Host "Skipping: $profileName" -Fore blue -Back white
        }
        
    }

Write-Host "*** Done! ***"
Write-Host "Removed $numAccounts accounts from the system." -Fore blue -Back white

Start-Sleep -s 5
