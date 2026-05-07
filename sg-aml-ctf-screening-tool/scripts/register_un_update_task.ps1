# Registers a Windows Scheduled Task to refresh UN sanctions lists on a schedule.
param(
    [ValidateSet("Daily","Weekly")]
    [string]$Frequency = "Daily",
    [string]$Time = "02:15",              # HH:MM 24h
    [ValidateSet("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")]
    [string[]]$DaysOfWeek = @("Monday"),  # used when -Frequency Weekly
    [string]$TaskName = "SG_AML_UN_Lists_Update",
    [string]$Description = "Refresh UN sanctions XML for SG AML/CTF skill",
    [string]$User = "$env:USERNAME"
)

$skillRoot = Split-Path $PSScriptRoot
$updateScript = Join-Path $skillRoot "update_un_lists.ps1"
$logDir = Join-Path $skillRoot "..\\logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }
$logFile = Join-Path $logDir "un_lists_update.log"

$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$updateScript`" *>> `"$logFile`""

if ($Frequency -eq "Weekly") {
    $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $DaysOfWeek -At $Time
} else {
    $trigger = New-ScheduledTaskTrigger -Daily -At $Time
}

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Description $Description -User $User -Force | Out-Null

Write-Host "Scheduled task '$TaskName' registered."
Write-Host "Action: powershell -File `"$updateScript`""
Write-Host "Logs will append to: $logFile"
Write-Host "Trigger: $Frequency at $Time (DaysOfWeek: $($DaysOfWeek -join ','))"
