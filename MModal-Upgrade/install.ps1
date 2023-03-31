#Delete Directory
function Delete-Path()
    {
        Remove-Item -Path C:\MModalUpgrade -Force -Recurse
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
        else {
            return $false
        }
    }

function Uninstall-Apps($apps)
    {
        Start-Process "C:\Windows\System32\msiexec.exe" -ArgumentList "/x $($apps) /quiet /noreboot" -Wait
    }

#If MModal is on the system begin the install, Exit if not and clean up
if ((Install-Check) -eq $false)
    {
        Delete-Path
        exit
    }

#Remove old version
Uninstall-Apps("{0ECEFF07-07E9-493A-B6A0-DBC8CFAE8738}")
Uninstall-Apps("{12FFC0ED-35BC-471F-9E49-588E3F3C39E4}")
Uninstall-Apps("{160DFB5E-E017-48BF-A2CA-29094A0FFF9B}")
Uninstall-Apps("{18BCE7EB-01A0-4058-9352-7261AB6E9482}")
Uninstall-Apps("{1F3AC9F3-B521-4F8C-BA13-1E198C8F7917}")
Uninstall-Apps("{25CA5840-97FC-435F-A4D2-0BDCAEA12315}")
Uninstall-Apps("{2CC03E2A-FDCE-4A3C-AE44-E5D44A8E1BC0}")
Uninstall-Apps("{32550603-2526-4A33-B55B-91621E5FC562}")
Uninstall-Apps("{40AB63AB-5BFB-4CF3-8618-9FC74CFE8EEA}")
Uninstall-Apps("{4E6EF200-6C54-41B2-80E9-F71D03579EF4}")
Uninstall-Apps("{566627BA-33EC-4779-A2D8-7F86F7D2EBE9}")
Uninstall-Apps("{6AD7DB31-E0A4-4E1C-B8E8-B5C3EF91B31C}")
Uninstall-Apps("{710937E7-5605-4085-9318-2A491EA7F48B}")
Uninstall-Apps("{714B029E-0A0B-41EF-8629-50DF5315F8CA}")
Uninstall-Apps("{780C9FB5-ECB9-4AB5-AEC0-26F7257D4087}")
Uninstall-Apps("{7EBA15E2-7745-4A44-B841-3B66013C96DF}")
Uninstall-Apps("{84CB216B-ED82-4226-8AC5-CCE7AD5F7FD6}")
Uninstall-Apps("{87625148-11AD-466C-94D9-313FC1497515}")
Uninstall-Apps("{8B21C9A1-2DEF-4C3E-B285-A8A54B5FD37D}")
Uninstall-Apps("{97800A75-A887-4E73-AA80-EF46EFDD6348}")
Uninstall-Apps("{A46E9DCC-AE34-4000-896D-F035C7373864}")
Uninstall-Apps("{A561F225-56AC-4858-80B5-99C99B4EB1B4}")
Uninstall-Apps("{A607D664-6633-45F3-AB27-20B3EA2980C0}")
Uninstall-Apps("{A6DD0692-37DD-4870-B333-583D1C109E58}")
Uninstall-Apps("{A84780DA-8C68-4511-85E6-7AE6ABBEF967}")
Uninstall-Apps("{B0F40B32-B2BD-4CDE-9BF8-4584DCF1D75D}")
Uninstall-Apps("{C09F67F8-9691-48DC-AA55-8D038C814C68}")
Uninstall-Apps("{C21424FA-95AD-4165-860F-CB8B169A9AFA}")
Uninstall-Apps("{D0CA6133-E546-40EB-ABD3-DAA88E0F6335}")
Uninstall-Apps("{D0F409CB-7D49-4417-9BA1-7CD58E9891A1}")
Uninstall-Apps("{E32A9DF4-79B1-4311-AF00-36E93C2127E6}")
Uninstall-Apps("{E85951A0-D3B5-4C03-B384-8D7CBD522931}")
Uninstall-Apps("{FC806A94-5FAB-422B-AB6D-97B32E0B2B8A}")

#Start the installer batch script
Start-Process "\\tfhd_app\IT\Dist\MModal\Prod\Fluency.Direct.10.0.690.1877\fd.client\install_silent.bat"
Start-Sleep -s 100

#Wait for MModal to install
if ((Install-Check) -eq $false)
    {
        Start-Sleep -s 15
    }

Copy-Item "\\tfhd_app\IT\Dist\MModal\Prod\MModal Fluency Direct.lnk" -Destination "C:\Users\Public\Desktop\MModal Fluency Direct.lnk"

#Clean up
Delete-Path

#Error Checking
if ((Install-Check) -eq $true)
    {
        return "0"
    }
    else {
        return "1"
    }
