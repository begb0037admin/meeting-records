<#
Register-HRRoadmapPendingDraft.ps1
===================================
One-time registration: weekly HR Systems Roadmap pending-draft extraction,
every Thursday morning (the day before the Friday meeting), on this desktop
(same host/pattern as work-inbox's WorkInbox-* scheduled tasks -- see
create_inbox_tasks.bat). Idempotent: re-running replaces the existing task
definition (/f) rather than erroring if it already exists.

Prerequisite (not done by this script): MEETING_PREP_PENDING_SECRET must
already be set as a Windows User environment variable, matching the
PENDING_WRITE_SECRET Worker secret -- provisioned once by Drew, never
written to a file. Verify with:
    [Environment]::GetEnvironmentVariable('MEETING_PREP_PENDING_SECRET','User')
#>
$ErrorActionPreference = 'Stop'

$taskName = 'MeetingPrep-HRRoadmap-WeeklyPrepop'
$scriptPath = 'C:\Users\admin\Desktop\Run HR Roadmap Pending Draft.ps1'

if (-not (Test-Path $scriptPath)) {
    throw "Expected wrapper script not found at $scriptPath -- copy it there first."
}
if (-not [Environment]::GetEnvironmentVariable('MEETING_PREP_PENDING_SECRET', 'User')) {
    throw "MEETING_PREP_PENDING_SECRET is not set as a User environment variable. Set it before registering this task."
}

schtasks /create /tn $taskName `
    /tr "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`"" `
    /sc weekly /d THU /st 07:00 /rl highest /f

Write-Host "Registered '$taskName' -- runs every Thursday 07:00."
Write-Host "Run it once manually now to verify: schtasks /run /tn `"$taskName`""
