#Delete Directory
function Delete-Path()
    {
        Remove-Item -LiteralPath "C:\MModalUpgrade" -Force -Recurse
    }
    
#Check if MModal is installed on system
function Install-Check()
    {
        $mmodalInstallPath = "C:\Program Files (x86)\MModal\MModal Fluency Direct\FluencyDirectLauncher.exe"
        $checkPath = Test-Path $mmodalInstallPath
        if ($checkPath -eq $true)
        {
            return $true
        }
        else 
        {
            return $false
        }
    }

#If MModal is on the system begin the install, Exit if not and clean up
if ((Install-Check) -eq $false)
    {
        Delete-Path
        exit
    }

#Start the installer batch script
Start-Process "\\tfhd_app\IT\Dist\MModal\Prod\Fluency.Direct.10.0.690.1877\fd.client\install_silent.bat"
Start-Sleep -s 30

#Wait for MModal to install
if ((Install-Check) -eq $false)
    {
        Start-Sleep -s 15
    }

Copy-Item "\\tfhd_app\IT\Dist\MModal\Prod\MModal Fluency Direct.lnk" -Destination "C:\Users\Public\Public Desktop"

#Cleanup
Delete-Path
return "0"
