<#
Run HR Roadmap Poll.ps1
========================
Runs frequently (every 1-2 minutes, via Task Scheduler -- see
Register-HRRoadmapPoll.ps1), not on a fixed daily schedule. Pulls the latest
poll_hr_roadmap_pull.py and extract_hr_roadmap_pending.py from GitHub
(cache-busted, same pattern as work-inbox's Run_Inbox_Briefing.ps1), then
runs the poller once. Most invocations do nothing (no pull was requested from
the browser this tick) and exit quickly -- that's expected, not a fault.

Kevin explicitly rejected a silent once-a-week unattended run for this
feature (16 Sep 2026) -- this frequent-poll design exists so the button click
in the browser gets picked up and processed within roughly a minute or two,
with a visible status indicator, rather than him waiting for a fixed
schedule or wondering whether an overnight run silently failed.

Requires the MEETING_PREP_PENDING_SECRET Windows User environment variable
to already be set (provisioned once by Drew alongside the matching
PENDING_WRITE_SECRET Worker secret -- see CHECKPOINT.md's Phase 5 entry).
This script does not set, read aloud, or log that value anywhere.
#>
$ErrorActionPreference = 'Stop'

$pollerPath = Join-Path $PSScriptRoot 'poll_hr_roadmap_pull.py'
$extractorPath = Join-Path $PSScriptRoot 'extract_hr_roadmap_pending.py'
$t = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()

Invoke-WebRequest -UseBasicParsing `
    "https://raw.githubusercontent.com/begb0037admin/meeting-records/main/meeting-prep-intake/automation/poll_hr_roadmap_pull.py?t=$t" `
    -OutFile $pollerPath
Invoke-WebRequest -UseBasicParsing `
    "https://raw.githubusercontent.com/begb0037admin/meeting-records/main/meeting-prep-intake/automation/extract_hr_roadmap_pending.py?t=$t" `
    -OutFile $extractorPath

python $pollerPath
$code = $LASTEXITCODE
if ($code -ne 0) {
    Write-Host "[$(Get-Date -Format s)] Poll exited with code $code (0 = nothing requested or handled cleanly; non-zero on a real failure -- check output above)."
}
exit $code
