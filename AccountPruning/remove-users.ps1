#Get the username of the logged-in user
$currentUser = Get-WmiObject -Class Win32_ComputerSystem | Select-Object -ExpandProperty UserName
#Clean up text
$currentUser = $currentUser -replace "TFHD_DOMAIN\\", ""

#Get User List
Get-ChildItem ’HKLM:\Software\Microsoft\Windows NT\CurrentVersion\ProfileList’ |
    ForEach-Object{

        #Location on C: Drive
        $profilepath=$_.GetValue('ProfileImagePath')

        #Delete accounts if not system related or logged in
        if( ($profilepath -notmatch 'administrator|Ctx_StreamingSvc|NetworkService|Localservice|systemprofile') -and ($profilepath -notmatch "$currentUser") )
        {

            #Remove User path
            Write-Host "Removing item: $profilepath" -ForegroundColor green
            Remove-Item -Path "$profilepath"

            #Remove Reg Value
            Write-Host $_.PSPath
            Remove-Item $_.PSPath -Whatif

        }
        else
        {
            Write-Host "Skipping item:$profilepath" -Fore blue -Back white
        }
    }

Start-Sleep -s 10
