<#
Register-HRRoadmapPoll.ps1
============================
One-time registration: polls every 2 minutes, indefinitely, for an on-demand
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
$scriptPath = 'C:\Users\admin\Desktop\Run HR Roadmap Poll.ps1'

if (-not (Test-Path $scriptPath)) {
    throw "Expected wrapper script not found at $scriptPath -- copy it there first."
}
if (-not [Environment]::GetEnvironmentVariable('MEETING_PREP_PENDING_SECRET', 'User')) {
    throw "MEETING_PREP_PENDING_SECRET is not set as a User environment variable. Set it before registering this task."
}

# /sc MINUTE /mo 2: fires every 2 minutes, indefinitely, from creation -- this is
# the "frequently-polling local task" this feature depends on, not a once-daily
# trigger. /rl highest keeps behaviour consistent with work-inbox's own tasks.
schtasks /create /tn $taskName `
    /tr "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`"" `
    /sc minute /mo 2 /rl highest /f

Write-Host "Registered '$taskName' -- polls every 2 minutes."
Write-Host "Run it once manually now to verify it does nothing harmful when idle: schtasks /run /tn `"$taskName`""
