[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidatePattern('^\d{4}-\d{2}-\d{2}$')]
    [string]$MeetingDate,

    [ValidateSet('Draft', 'Revise')]
    [string]$Mode = 'Draft',

    [string]$AdditionalContext = '',

    [string]$ExistingDraftPath = '',

    [string]$PriorSourceManifestPath = '',

    [string]$RevisionInstruction = '',

    [string]$ManualRoadmapRecapPath = '',

    [string]$FixturePath = '',

    [switch]$DryRun,

    [switch]$KeepWorkspace
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Repository = 'begb0037admin/meeting-records'
$WorkflowId = 'managers-meeting-draft'
$RunId = '{0}_{1}' -f (
    Get-Date
).ToUniversalTime().ToString('yyyyMMddTHHmmssZ'), (
    [guid]::NewGuid().ToString('N').Substring(0, 8)
)
$TaskName = "Managers Meeting draft - $MeetingDate"
$RuntimeRoot = Join-Path ([IO.Path]::GetTempPath()) 'claude-meeting-voice'
$Workspace = Join-Path $RuntimeRoot $RunId
$ClonePath = Join-Path $Workspace 'meeting-records'
$WorkspaceState = 'not-created'

$GenericSkillRoot = [IO.Path]::GetFullPath(
    (Join-Path $PSScriptRoot '..\..\chatGPT-meeting-prep-voice')
)
$ProfilePath = Join-Path $GenericSkillRoot 'profiles\managers-meeting.json'
$SchemaPath = Join-Path $GenericSkillRoot 'schemas\meeting-result.schema.json'
$ValidatorPath = Join-Path $GenericSkillRoot 'scripts\validate-meeting-result.py'
$ClaudeAdapterPath = Join-Path $PSScriptRoot 'invoke-claude.py'
$RepositoryRoot = [IO.Path]::GetFullPath(
    (Join-Path $PSScriptRoot '..\..\..\..')
)
$McpRoot = Join-Path $RepositoryRoot 'mcp\meeting-connector'
$FormatPath = Join-Path $RepositoryRoot (
    'Meeting Reviews\docs\reference\managers-meeting-format.md'
)

function Write-ProgressEvent {
    param(
        [Parameter(Mandatory)][string]$Stage,
        [Parameter(Mandatory)][string]$Message
    )
    $event = @{
        type = 'progress'
        runId = $RunId
        taskName = $TaskName
        stage = $Stage
        message = $Message
    } | ConvertTo-Json -Compress
    [Console]::Error.WriteLine($event)
}

function Write-Result {
    param([Parameter(Mandatory)][hashtable]$Data)
    [Console]::Out.WriteLine(($Data | ConvertTo-Json -Depth 30 -Compress))
}

function Require-Command {
    param([Parameter(Mandatory)][string]$Name)
    $command = Get-Command $Name -ErrorAction SilentlyContinue
    if ($null -eq $command) {
        throw "Required command '$Name' was not found on PATH."
    }
    return $command.Source
}

function ConvertFrom-ClaudeEnvelope {
    param([Parameter(Mandatory)][object]$Envelope)

    $candidate = $null
    if ($null -ne $Envelope.PSObject.Properties['structured_output']) {
        $candidate = $Envelope.structured_output
    }
    elseif ($null -ne $Envelope.PSObject.Properties['result']) {
        $candidate = $Envelope.result
    }
    elseif ($null -ne $Envelope.PSObject.Properties['status']) {
        $candidate = $Envelope
    }
    else {
        throw 'Claude envelope does not contain a structured result.'
    }

    if ($candidate -is [string]) {
        $text = $candidate.Trim()
        $text = $text -replace '^```(?:json)?\s*', ''
        $text = $text -replace '\s*```$', ''
        try {
            return $text | ConvertFrom-Json
        }
        catch {
            $firstBrace = $text.IndexOf('{')
            $lastBrace = $text.LastIndexOf('}')
            if ($firstBrace -ge 0 -and $lastBrace -gt $firstBrace) {
                $jsonSlice = $text.Substring(
                    $firstBrace, ($lastBrace - $firstBrace + 1)
                )
                try {
                    return $jsonSlice | ConvertFrom-Json
                }
                catch {
                    # Fall through to the stable public error below.
                }
            }
            throw 'Claude result field is not valid JSON.'
        }
    }
    return $candidate
}

function New-DispatchPrompt {
    param(
        [Parameter(Mandatory)][string]$ProfileJson,
        [string]$FixtureJson,
        [string]$ManualRecapJson,
        [string]$RevisionInputPath
    )

    $modeInstruction = if ($Mode -eq 'Revise') {
@"
Revision mode:
- Read the revision instruction and the absolute paths of the prior draft and
  prior source manifest from: $RevisionInputPath
- Read both referenced files in full before revising.
- Change only the requested sections where possible.
- Retain all supported evidence and re-check any claim affected by the revision.
- Return a complete replacement draft, still marked draft.
"@
    }
    else {
        'Draft mode: produce a new complete speaker''s brief.'
    }

    return @"
You are Claude Code preparing Kevin Lelitte's HR Systems Managers Meeting brief.

Task:
- Workflow: $WorkflowId
- Meeting type: HR Systems Managers Meeting
- Meeting date: $MeetingDate
- Mode: $Mode
- Additional context: $AdditionalContext
- Task name: $TaskName

Workflow profile:
$ProfileJson

Historical fixture, if supplied:
$FixtureJson

Kevin-provided manual Roadmap outcome recap, if supplied:
$ManualRecapJson

$modeInstruction

Mandatory process:
1. Read the repository governance available in the checkout.
2. Follow the Managers format requirements embedded in the workflow profile.
3. Use every Managers Meeting read tool supplied by the
   managers-meeting-context MCP as applicable.
4. Call Granola for the actual latest HR Systems Roadmap meeting outcome.
   If it is absent, a completed result is allowed only when the launcher supplied
   a substantive Kevin-provided manual recap. Record Granola as unavailable and
   the manual recap separately as sourceId manual-roadmap-recap with status used.
5. Assess every active Roadmap item returned by the MCP and record every
   inclusion/exclusion decision in roadmapAssessment.
6. Transform selected Roadmap items into management-level content.
7. Report source record dates, retrieval dates, freshness and conflicts.
8. Do not read the benchmark named in the profile when generating the draft.
   In historical mode it is deliberately absent from the checkout and is
   comparison-only.
9. Do not refresh Outlook. No refresh tool is supplied.
10. Do not edit any file, source system or repository. Do not commit, push,
    publish, send, distribute or schedule.
11. If a critical source is missing, return status blocked with blockers.
12. Return only one JSON object matching the required result schema at:
    $SchemaPath
"@
}

$ClaudePath = $null
$GitPath = $null
$GhPath = $null
$PythonPath = $null
$Fixture = $null
$ManualRoadmapRecap = $null
$MeetingRecordsRef = 'main'
$RoadmapRef = 'main'
$ClaudeRaw = $null
$Validation = $null
$SavedAnthropicApiKey = $null
$ChildHadAnthropicApiKey = Test-Path Env:ANTHROPIC_API_KEY

try {
    foreach ($requiredPath in @(
        $ProfilePath, $SchemaPath, $ValidatorPath, $ClaudeAdapterPath, $McpRoot, $FormatPath
    )) {
        if (-not (Test-Path -LiteralPath $requiredPath)) {
            throw "Required workflow component is missing: $requiredPath"
        }
    }

    if ($Mode -eq 'Revise') {
        if (-not $RevisionInstruction.Trim()) {
            throw 'Revision mode requires -RevisionInstruction.'
        }
        foreach ($path in @($ExistingDraftPath, $PriorSourceManifestPath)) {
            if (-not $path -or -not (Test-Path -LiteralPath $path)) {
                throw "Revision input is missing: $path"
            }
        }
    }

    if ($FixturePath) {
        if (-not (Test-Path -LiteralPath $FixturePath)) {
            throw "Fixture file not found: $FixturePath"
        }
        $Fixture = Get-Content -Raw -Encoding UTF8 -LiteralPath $FixturePath | ConvertFrom-Json
        if ($Fixture.meetingDate -ne $MeetingDate) {
            throw 'Fixture meetingDate does not match -MeetingDate.'
        }
        if (-not $Fixture.generationRestrictions.withholdBenchmark) {
            throw 'Historical fixture must withhold the benchmark.'
        }
        $MeetingRecordsRef = [string]$Fixture.refs.meetingRecordsRef
        $RoadmapRef = [string]$Fixture.refs.roadmapRef
    }

    if ($ManualRoadmapRecapPath) {
        if (-not (Test-Path -LiteralPath $ManualRoadmapRecapPath)) {
            throw "Manual Roadmap recap file not found: $ManualRoadmapRecapPath"
        }
        $ManualRoadmapRecap = Get-Content -Raw -Encoding UTF8
            -LiteralPath $ManualRoadmapRecapPath | ConvertFrom-Json
        foreach ($field in @("meetingTitle", "meetingDate", "suppliedBy", "recap")) {
            if (-not $ManualRoadmapRecap.PSObject.Properties[$field] -or
                -not ([string]$ManualRoadmapRecap.$field).Trim()) {
                throw "Manual Roadmap recap requires a non-empty $field field."
            }
        }
        if ([string]$ManualRoadmapRecap.suppliedBy -ne "Kevin") {
            throw "Manual Roadmap recap suppliedBy must be Kevin."
        }
        if ($Fixture -and
            [string]$ManualRoadmapRecap.meetingDate -ne
                [string]$Fixture.requiredGranolaMeeting.meetingDate) {
            throw "Manual Roadmap recap date does not match the fixture gap."
        }
    }

    Write-ProgressEvent -Stage 'preflight' -Message 'Checking runtime dependencies'
    $ClaudePath = Require-Command 'claude'
    $GitPath = Require-Command 'git'
    $GhPath = Require-Command 'gh'
    $PythonPath = Require-Command 'python'

    $authRaw = & $ClaudePath auth status 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Claude authentication probe failed: $($authRaw -join ' ')"
    }
    $ClaudeAuth = ($authRaw -join [Environment]::NewLine) | ConvertFrom-Json
    if (-not $ClaudeAuth.loggedIn) {
        throw 'Claude Code is not logged in.'
    }

    if ($DryRun) {
        Write-Result @{
            schemaVersion = 2
            status = 'dry-run'
            workflowId = $WorkflowId
            meetingType = 'HR Systems Managers Meeting'
            meetingDate = $MeetingDate
            taskName = $TaskName
            runId = $RunId
            mode = $Mode
            profilePath = $ProfilePath
            schemaPath = $SchemaPath
            fixtureId = if ($Fixture) { $Fixture.fixtureId } else { $null }
            meetingRecordsRef = $MeetingRecordsRef
            manualRoadmapRecapProvided = [bool]$ManualRoadmapRecap
            outlookRefreshAvailable = $false
            publicationAuthority = 'none'
            claudeLoggedIn = [bool]$ClaudeAuth.loggedIn
        }
        exit 0
    }

    New-Item -ItemType Directory -Path $Workspace -Force | Out-Null
    $WorkspaceState = 'created'

    Write-ProgressEvent -Stage 'checkout' -Message (
        "Cloning meeting-records at $MeetingRecordsRef"
    )
    $cloneOutput = & $GhPath repo clone $Repository $ClonePath -- --no-checkout --quiet 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "GitHub clone failed: $($cloneOutput -join ' ')"
    }
    & $GitPath -C $ClonePath checkout --quiet --detach $MeetingRecordsRef 2>&1 | ForEach-Object {
        Write-ProgressEvent -Stage 'checkout' -Message ([string]$_)
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to check out meeting-records ref $MeetingRecordsRef."
    }

    $McpConfigPath = Join-Path $Workspace 'mcp-config.json'
    $McpConfig = @{
        mcpServers = @{
            'managers-meeting-context' = @{
                type = 'stdio'
                command = $PythonPath
                args = @('-m', 'meeting_context.managers_server_no_roadmap')
                env = @{
                    PYTHONPATH = $McpRoot
                    MEETING_CONTEXT_GRANOLA_STATUS = 'external-must-be-checked'
                    MEETING_CONTEXT_INBOX_REF = if ($Fixture) {
                        [string]$Fixture.refs.workInboxRef
                    } else { 'main' }
                    MEETING_CONTEXT_TASKS_REF = if ($Fixture) {
                        [string]$Fixture.refs.commandCentreRef
                    } else { 'main' }
                    MEETING_CONTEXT_ROADMAP_REF = $RoadmapRef
                    MEETING_CONTEXT_MEETING_RECORDS_REF = $MeetingRecordsRef
                }
            }
        }
    } | ConvertTo-Json -Depth 10 -Compress
    [IO.File]::WriteAllText(
        $McpConfigPath, $McpConfig, [Text.UTF8Encoding]::new($false)
    )

    $RevisionInputPath = ''
    if ($Mode -eq 'Revise') {
        $RevisionInputPath = Join-Path $Workspace 'revision-input.json'
        $null = Get-Content -Raw -Encoding UTF8 -LiteralPath $PriorSourceManifestPath | ConvertFrom-Json
        $revisionInput = @{
            existingDraftPath = [IO.Path]::GetFullPath($ExistingDraftPath)
            priorSourceManifestPath = [IO.Path]::GetFullPath(
                $PriorSourceManifestPath
            )
            revisionInstruction = $RevisionInstruction
        } | ConvertTo-Json -Depth 3
        [IO.File]::WriteAllText(
            $RevisionInputPath, $revisionInput, [Text.UTF8Encoding]::new($false)
        )
    }

    $ProfileJson = Get-Content -Raw -Encoding UTF8 -LiteralPath $ProfilePath
    $FixtureJson = if ($Fixture) {
        $Fixture | ConvertTo-Json -Depth 20 -Compress
    }
    else {
        ''
    }
    $ManualRecapJson = if ($ManualRoadmapRecap) {
        $ManualRoadmapRecap | ConvertTo-Json -Depth 10 -Compress
    }
    else {
        ''
    }
    $RoadmapInputPath = Join-Path $Workspace 'active-roadmap.json'
    Write-ProgressEvent -Stage 'sources' -Message 'Exporting formal active Roadmap fields'
    $HadPythonPath = Test-Path Env:PYTHONPATH
    $SavedPythonPath = if ($HadPythonPath) { $env:PYTHONPATH } else { $null }
    try {
        $env:PYTHONPATH = $McpRoot
        $RoadmapRaw = & $PythonPath -m meeting_context.roadmap_export --ref $RoadmapRef
        if ($LASTEXITCODE -ne 0) {
            throw 'Formal Roadmap export failed.'
        }
    }
    finally {
        if ($HadPythonPath) { $env:PYTHONPATH = $SavedPythonPath }
        else { Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue }
    }
    [IO.File]::WriteAllText(
        $RoadmapInputPath,
        ($RoadmapRaw -join [Environment]::NewLine),
        [Text.UTF8Encoding]::new($false)
    )

    $Prompt = New-DispatchPrompt `
        -ProfileJson $ProfileJson `
        -FixtureJson $FixtureJson `
        -ManualRecapJson $ManualRecapJson `
        -RevisionInputPath $RevisionInputPath
    $Prompt += "`nMandatory formal active Roadmap evidence file: $RoadmapInputPath`nRead it in full and assess all activeItemCount items."

    $AllowedTools = @(
        'Read',
        'mcp__managers-meeting-context__get_source_health',
        'mcp__managers-meeting-context__get_inbox_briefing',
        'mcp__managers-meeting-context__get_command_centre_tasks',
        'mcp__managers-meeting-context__get_previous_managers_prep',
        'mcp__managers-meeting-context__get_latest_roadmap_prep',
        'mcp__claude_ai_Granola__*'
    )

    Write-ProgressEvent -Stage 'drafting' -Message 'Starting Claude Code'
    Push-Location $ClonePath
    try {
        if ($ClaudeAuth.authMethod -eq 'claude.ai' -and $ChildHadAnthropicApiKey) {
            $SavedAnthropicApiKey = $env:ANTHROPIC_API_KEY
            Remove-Item Env:ANTHROPIC_API_KEY
        }
        $PromptPath = Join-Path $Workspace 'dispatch-prompt.txt'
        $ClaudeStderrPath = Join-Path $Workspace 'claude-stderr.txt'
        [IO.File]::WriteAllText(
            $PromptPath, $Prompt, [Text.UTF8Encoding]::new($false)
        )
        $AdapterArgs = @(
            $ClaudeAdapterPath,
            '--claude', $ClaudePath,
            '--schema', $SchemaPath,
            '--mcp-config', $McpConfigPath,
            '--name', "managers-meeting-$RunId",
            '--prompt-file', $PromptPath,
            '--allowed-tools', ($AllowedTools -join ',')
        )
        $ClaudeRaw = & $PythonPath @AdapterArgs 2> $ClaudeStderrPath
        $ClaudeExitCode = $LASTEXITCODE
        if ($ClaudeExitCode -ne 0) {
            $ClaudeError = Get-Content -Raw -Encoding UTF8 -LiteralPath $ClaudeStderrPath
            throw "Claude exited with code $ClaudeExitCode. $ClaudeError"
        }
    }
    finally {
        if ($ChildHadAnthropicApiKey) {
            $env:ANTHROPIC_API_KEY = $SavedAnthropicApiKey
        }
        Pop-Location
    }

    Write-ProgressEvent -Stage 'validation' -Message 'Parsing Claude result'
    $ClaudeRawPath = Join-Path $Workspace 'claude-envelope.json'
    [IO.File]::WriteAllText(
        $ClaudeRawPath,
        ($ClaudeRaw -join [Environment]::NewLine),
        [Text.UTF8Encoding]::new($false)
    )
    $ClaudeEnvelope = ($ClaudeRaw -join [Environment]::NewLine) | ConvertFrom-Json
    $MeetingResult = ConvertFrom-ClaudeEnvelope -Envelope $ClaudeEnvelope
    $ResultPath = Join-Path $Workspace 'meeting-result.json'
    [IO.File]::WriteAllText(
        $ResultPath,
        ($MeetingResult | ConvertTo-Json -Depth 30),
        [Text.UTF8Encoding]::new($false)
    )

    $validationRaw = & $PythonPath $ValidatorPath `
        --result $ResultPath `
        --profile $ProfilePath
    $ValidationExitCode = $LASTEXITCODE
    $Validation = ($validationRaw -join [Environment]::NewLine) | ConvertFrom-Json
    if ($ValidationExitCode -ne 0 -or -not $Validation.valid) {
        throw "Meeting result validation failed: $($Validation.errors -join '; ')"
    }

    $Dirty = & $GitPath -C $ClonePath status --porcelain
    if ($LASTEXITCODE -ne 0) {
        throw 'Unable to verify checkout state.'
    }
    if ($Dirty) {
        $WorkspaceState = 'preserved-dirty'
        throw 'Claude changed the draft-only checkout.'
    }

    if ($KeepWorkspace) {
        $WorkspaceState = 'preserved-by-request'
    }
    else {
        Remove-Item -LiteralPath $Workspace -Recurse -Force
        $WorkspaceState = 'removed-clean'
    }

    Write-ProgressEvent -Stage 'return' -Message 'Returning validated draft'
    $RevisionReturn = if (
        $null -ne $MeetingResult.PSObject.Properties['revision']
    ) {
        $MeetingResult.revision
    }
    else {
        $null
    }
    Write-Result @{
        schemaVersion = 2
        status = [string]$MeetingResult.status
        workflowId = [string]$MeetingResult.workflowId
        meetingType = [string]$MeetingResult.meetingType
        meetingDate = [string]$MeetingResult.meetingDate
        draftState = [string]$MeetingResult.draftState
        taskName = $TaskName
        runId = $RunId
        mode = $Mode
        sourceManifest = $MeetingResult.sourceManifest
        roadmapAssessment = $MeetingResult.roadmapAssessment
        spokenSummary = [string]$MeetingResult.spokenSummary
        draftMarkdown = [string]$MeetingResult.draftMarkdown
        blockers = $MeetingResult.blockers
        warnings = $MeetingResult.warnings
        nextStep = [string]$MeetingResult.nextStep
        revision = $RevisionReturn
        validation = $Validation
        workspaceState = $WorkspaceState
        outlookRefreshed = $false
        publicationAuthority = 'none'
    }
    exit 0
}
catch {
    if ($ChildHadAnthropicApiKey -and $null -ne $SavedAnthropicApiKey) {
        $env:ANTHROPIC_API_KEY = $SavedAnthropicApiKey
    }
    if (
        $WorkspaceState -eq 'created' -and
        (Test-Path -LiteralPath $Workspace)
    ) {
        $WorkspaceState = 'preserved-after-failure'
    }
    Write-Result @{
        schemaVersion = 2
        status = 'failed'
        workflowId = $WorkflowId
        meetingType = 'HR Systems Managers Meeting'
        meetingDate = $MeetingDate
        draftState = 'draft'
        taskName = $TaskName
        runId = $RunId
        mode = $Mode
        error = $_.Exception.Message
        validation = $Validation
        workspaceState = $WorkspaceState
        workspacePath = if (Test-Path -LiteralPath $Workspace) {
            $Workspace
        }
        else {
            $null
        }
        outlookRefreshed = $false
        publicationAuthority = 'none'
    }
    exit 1
}
