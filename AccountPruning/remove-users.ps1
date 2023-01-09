# Get the username of the logged-in user
$currentUser = Get-WmiObject -Class Win32_ComputerSystem | Select-Object -ExpandProperty UserName

# Get a list of all local user accounts
$users = Get-LocalUser

# Filter the list to exclude the current user and the administrator account
$users = $users | Where-Object {$_.Name -ne $currentUser -and $_.Name -ne 'Administrator'}

# Delete each user account
foreach ($user in $users) {
    Remove-LocalUser -Name $user.Name
}
