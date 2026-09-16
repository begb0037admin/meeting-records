<#
Run HR Roadmap Pending Draft.ps1
================================
Weekly, unattended (Windows Task Scheduler, Thursdays): pulls the latest
extract_hr_roadmap_pending.py from GitHub (cache-busted, same pattern as
work-inbox's Run_Inbox_Briefing.ps1) and runs it. Reads the local HR Systems
Roadmap Master.xlsm directly -- no Outlook/Graph/connector involved. Posts a
draft agenda for the next HR Systems Roadmap Meeting occurrence to
meeting.lelitte.co.uk; never touches GitHub, never submits a locked intake.

Requires the MEETING_PREP_PENDING_SECRET Windows User environment variable
to already be set (provisioned once by Drew alongside the matching Worker
secret -- see CHECKPOINT.md's Phase 5 entry). This script does not set,
read aloud, or log that value anywhere.
#>
$ErrorActionPreference = 'Stop'

$scriptPath = Join-Path $PSScriptRoot 'extract_hr_roadmap_pending.py'
Write-Host "[$(Get-Date -Format s)] Downloading latest script from GitHub..."
$t = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
Invoke-WebRequest -UseBasicParsing `
    "https://raw.githubusercontent.com/begb0037admin/meeting-records/main/meeting-prep-intake/automation/extract_hr_roadmap_pending.py?t=$t" `
    -OutFile $scriptPath

Write-Host "[$(Get-Date -Format s)] Running HR Roadmap pending-draft extraction..."
python $scriptPath

if ($LASTEXITCODE -eq 0) {
    Write-Host "[$(Get-Date -Format s)] Done."
} else {
    Write-Host "[$(Get-Date -Format s)] ERROR - exit code $LASTEXITCODE, see output above."
}
exit $LASTEXITCODE
