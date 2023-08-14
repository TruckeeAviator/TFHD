#Get User List
Get-ChildItem "HKLM:\Software\Microsoft\Windows NT\CurrentVersion\ProfileList" |
    ForEach-Object{

        #Get path from reg
        $profileName=$_.GetValue('ProfileImagePath')

        if( ($profileName -notmatch 'administrator|Ctx_StreamingSvc|NetworkService|Localservice|systemprofile') )
        {
            Remove-Item $profileName"\AppData\Roaming\Zoom" -Recurse
            Remove-Item $profileName"\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Zoom" -Recurse
        }
    }
