Write-Host "*** This will remove all users accounts besides yours and built-in accounts ***"
Write-Host "*** Please logout all other users before running this script! ***"
Write-Host "*** This will take time depending on the number of accounts, please let the script finish ***"

Start-Sleep -s 10

#Get the username of the logged-in user
$currentUser = Get-WmiObject -Class Win32_ComputerSystem | Select-Object -ExpandProperty UserName
#Clean up text
$currentUser = $currentUser -replace "TFHD_DOMAIN\\", ""

#Set Vars
$numAccounts = 0
[double]$freeStart = '{0:F2}' -f ((Get-PSDrive C).Free / 1GB)

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

#Get space saved
[double]$freeEnd = '{0:F2}' -f ((Get-PSDrive C).Free / 1GB)
$spaceSaved = $freeEnd - $freeStart

#Log when the cleaner was run
"Account Pruning was preformed $(Get-Date)" | out-file C:\cleaner-log.txt -Append
("Accounts Removed: " + $numAccounts) | out-file C:\cleaner-log.txt -Append
("Free space before operation: " + $freeStart + " GiB") | out-file C:\cleaner-log.txt -Append
("Free space after operation: " + $freeEnd) + " GiB"| out-file C:\cleaner-log.txt -Append
("Space Saved: " + $spaceSaved) + " GiB"| out-file C:\cleaner-log.txt -Append
" " | out-file C:\cleaner-log.txt -Append

Write-Host "*** Done! ***"
Write-Host "Removed $numAccounts accounts from the system. Saved $spaceSaved GiB" -Fore blue -Back white

Start-Sleep -s 15
