<#
Register-HRRoadmapPoll.ps1
============================
One-time registration: polls every 30 seconds, indefinitely, for an on-demand
HR Systems Roadmap pull request from the browser's "Pull roadmap now" button.
Replaces an earlier design (a single silent Thursday 07:00 run) that Kevin
explicitly rejected on 16 Sep 2026 -- he wants to trigger this himself, with
visible pass/fail feedback, not rely on an unattended fixed schedule with no
way to tell whether it silently failed overnight.

Idempotent: re-running replaces the existing task definition (/f) rather than
erroring if it already exists.

Prerequisite (not done by this script): MEETING_PREP_PENDING_SECRET must
already be set as a Windows User environment variable, matching the
PENDING_WRITE_SECRET Worker secret -- provisioned once by Drew, never
written to a file. Verify with:
    [Environment]::GetEnvironmentVariable('MEETING_PREP_PENDING_SECRET','User')
#>
$ErrorActionPreference = 'Stop'

$taskName = 'MeetingPrep-HRRoadmap-Poll'
$scriptPath = 'C:\Users\admin\Desktop\Run-HRRoadmapPoll.ps1'

if (-not (Test-Path $scriptPath)) {
    throw "Expected wrapper script not found at $scriptPath -- copy it there first."
}
if (-not [Environment]::GetEnvironmentVariable('MEETING_PREP_PENDING_SECRET', 'User')) {
    throw "MEETING_PREP_PENDING_SECRET is not set as a User environment variable. Set it before registering this task."
}

# Fires every 30 seconds, indefinitely, from creation -- this is the
# "frequently-polling local task" this feature depends on, not a once-daily
# trigger. Registered via the ScheduledTasks PowerShell module, not
# schtasks.exe directly -- schtasks.exe's /tr argument-quoting through
# PowerShell's native-exe marshalling silently mis-split a path argument
# during testing (16 Sep 2026), producing a false "Registered" success
# message while the task was never actually created. This module-based path
# avoids that whole class of quoting bug. No -RunLevel Highest: this task
# only reads a local file and makes outbound HTTPS calls, needs no elevated
# privilege, and this account isn't a local admin on this box (elevation was
# attempted and denied, Access 0x80070005 -- this is standard user rights).
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Seconds 30) -RepetitionDuration (New-TimeSpan -Days 3650)
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Force | Out-Null

Write-Host "Registered '$taskName' -- polls every 30 seconds."
Write-Host "Run it once manually now to verify it does nothing harmful when idle: Start-ScheduledTask -TaskName `"$taskName`""
