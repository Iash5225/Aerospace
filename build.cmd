@echo off
rem Step 1: Show hidden items in File Explorer (if not already enabled)
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v Hidden /t REG_DWORD /d 1 /f
taskkill /f /im explorer.exe
start explorer.exe
timeout /t 3 /nobreak >nul

rem Step 2: Determine the username based on the directories in C:\Users
powershell -Command ^
"$usersDirectory = 'C:\Users'; ^
$userDirectories = Get-ChildItem -Path $usersDirectory | Where-Object { $_.PSIsContainer -and $_.Name -ne 'Public' -and $_.Name -ne 'Default' -and $_.Name -ne 'Default User' }; ^
if ($userDirectories.Count -eq 1) { ^
    $username = $userDirectories[0].Name; ^
    Write-Host 'Username determined: ' $username; ^
} else { ^
    Write-Host 'Unable to determine the username automatically. Please specify the username.'; ^
    exit 1; ^
}"

rem Step 3: Open File Explorer at the desired directory
start /e "C:\Users\%username%\AppData\Roaming\OpenRocket\Plugins"
