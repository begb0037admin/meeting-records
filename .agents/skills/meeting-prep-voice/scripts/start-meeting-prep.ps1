[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateNotNullOrEmpty()]
    [string]$MeetingType,

    [Parameter(Mandatory)]
    [ValidatePattern('^\d{4}-\d{2}-\d{2}$')]
    [string]$MeetingDate,

    [string]$AdditionalContext = '',

    [switch]$RefreshOutlook,

    [string]$RefreshConfirmation = '',

    [switch]$DryRun,

    [switch]$KeepWorkspace
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Repository = 'begb0037admin/meeting-records'
$RunId = '{0}_{1}' -f (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ'), ([guid]::NewGuid().ToString('N').Substring(0, 8))
$RuntimeRoot = Join-Path ([IO.Path]::GetTempPath()) 'meeting-prep-voice'
$Workspace = Join-Path $RuntimeRoot $RunId
$ClonePath = Join-Path $Workspace 'meeting-records'
$WorkspaceState = 'not-created'

function Write-Diagnostic {
    param([Parameter(Mandatory)][string]$Message)
    [Console]::Error.WriteLine("meeting-prep-voice: $Message")
}

function Write-Result {
    param([Parameter(Mandatory)][hashtable]$Data)
    [Console]::Out.WriteLine(($Data | ConvertTo-Json -Depth 20 -Compress))
}

function Require-Command {
    param([Parameter(Mandatory)][string]$Name)
    $command = Get-Command $Name -ErrorAction SilentlyContinue
    if ($null -eq $command) {
        throw "Required command '$Name' was not found on PATH."
    }
    return $command.Source
}

function Get-ClaudeAuthentication {
    param([Parameter(Mandatory)][string]$ClaudePath)
    $raw = & $ClaudePath auth status 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Claude authentication probe failed: $($raw -join ' ')"
    }
    try {
        $auth = ($raw -join [Environment]::NewLine) | ConvertFrom-Json
    }
    catch {
        throw 'Claude authentication probe did not return valid JSON.'
    }
    if (-not $auth.loggedIn) {
        throw 'Claude Code is not logged in.'
    }
    return $auth
}

function New-DispatchPrompt {
    param(
        [Parameter(Mandatory)][string]$RequestedMeetingType,
        [Parameter(Mandatory)][string]$RequestedMeetingDate,
        [string]$UserContext,
        [bool]$OutlookRefreshRequested,
        [string]$OutlookRefreshConfirmation
    )

    return @"
You are Claude Code, the established Reasoning Seat for Kevin Lelitte's meeting-records workflow.

Prepare a DRAFT ONLY for:
- Meeting type: $RequestedMeetingType
- Meeting date: $RequestedMeetingDate
- Additional instruction from Kevin: $UserContext
- Explicit Outlook refresh requested for this invocation: $OutlookRefreshRequested

Authority and workflow:
1. Read CLAUDE.md, CONSTITUTION.md, AGENT_MODEL.md, Meeting Reviews/docs/HANDOVER.md, and Meeting Reviews/docs/reference/meeting-prep-formats.md before drafting.
2. Follow the existing bootstrap order and meeting-specific workflow. Do not ask Kevin for a recap.
3. Read the most recent prep document of the same meeting type.
4. Use the existing configured connectors and sources required by CLAUDE.md, including Granola where the workflow calls for it.
5. Check source dates and report stale, unavailable, empty, or contradictory inputs explicitly.
6. Do not call refresh_outlook_work_inbox unless "Explicit Outlook refresh requested" above is True. If True, pass this user-supplied confirmation exactly: $OutlookRefreshConfirmation
7. Do not edit any file. Do not commit, push, schedule, publish, send, rename, or delete anything.
8. Do not turn this into an implementation plan. Produce the actual meeting-prep draft in the repository's approved style.
9. If critical source coverage is missing, return status "blocked" instead of inventing content.

Return only the structured result required by the supplied JSON schema.
"@
}

$ClaudePath = $null
$GitPath = $null
$GhPath = $null
$ClaudeAuth = $null
$ClaudeRaw = $null
$ChildHadAnthropicApiKey = Test-Path Env:ANTHROPIC_API_KEY
$SavedAnthropicApiKey = if ($ChildHadAnthropicApiKey) { $env:ANTHROPIC_API_KEY } else { $null }

try {
    $ClaudePath = Require-Command 'claude'
    $GitPath = Require-Command 'git'
    $GhPath = Require-Command 'gh'
    $ClaudeAuth = Get-ClaudeAuthentication -ClaudePath $ClaudePath

    if ($RefreshOutlook -and $RefreshConfirmation -cne 'REFRESH OUTLOOK AND PUBLISH WORK INBOX') {
        throw 'Explicit Outlook refresh requires the exact confirmation: REFRESH OUTLOOK AND PUBLISH WORK INBOX'
    }
    if (-not $RefreshOutlook -and $RefreshConfirmation) {
        throw 'RefreshConfirmation was supplied without -RefreshOutlook.'
    }

    $Prompt = New-DispatchPrompt `
        -RequestedMeetingType $MeetingType `
        -RequestedMeetingDate $MeetingDate `
        -UserContext $AdditionalContext `
        -OutlookRefreshRequested ([bool]$RefreshOutlook) `
        -OutlookRefreshConfirmation $RefreshConfirmation

    if ($DryRun) {
        Write-Result @{
            schemaVersion = 1
            status = 'dry-run'
            runId = $RunId
            repository = $Repository
            meetingType = $MeetingType
            meetingDate = $MeetingDate
            claudePath = $ClaudePath
            gitPath = $GitPath
            ghPath = $GhPath
            claudeLoggedIn = [bool]$ClaudeAuth.loggedIn
            claudeAuthMethod = [string]$ClaudeAuth.authMethod
            stripsAnthropicApiKeyForChild = [bool]($ClaudeAuth.authMethod -eq 'claude.ai' -and $ChildHadAnthropicApiKey)
            workspacePolicy = 'fresh-disposable-checkout'
            publicationAuthority = 'none'
            outlookRefreshRequested = [bool]$RefreshOutlook
        }
        exit 0
    }

    New-Item -ItemType Directory -Path $Workspace -Force | Out-Null
    $WorkspaceState = 'created'

    Write-Diagnostic "cloning $Repository into a disposable workspace"
    $SavedErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $CloneOutput = & $GhPath repo clone $Repository $ClonePath -- --depth 1 2>&1
        $CloneExitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $SavedErrorActionPreference
    }
    foreach ($Line in $CloneOutput) {
        Write-Diagnostic ([string]$Line)
    }
    if ($CloneExitCode -ne 0) {
        throw "GitHub clone failed with exit code $CloneExitCode."
    }

    $Schema = @{
        type = 'object'
        additionalProperties = $false
        properties = @{
            status = @{ type = 'string'; enum = @('completed', 'blocked') }
            meetingType = @{ type = 'string' }
            meetingDate = @{ type = 'string' }
            sourceManifest = @{
                type = 'array'
                items = @{
                    type = 'object'
                    additionalProperties = $false
                    properties = @{
                        source = @{ type = 'string' }
                        status = @{ type = 'string'; enum = @('used', 'stale', 'unavailable', 'empty', 'contradictory', 'not-required') }
                        freshnessDate = @{ type = @('string', 'null') }
                        notes = @{ type = 'string' }
                    }
                    required = @('source', 'status', 'freshnessDate', 'notes')
                }
            }
            spokenSummary = @{ type = 'string' }
            draftMarkdown = @{ type = 'string' }
            blockers = @{ type = 'array'; items = @{ type = 'string' } }
            nextStep = @{ type = 'string' }
        }
        required = @('status', 'meetingType', 'meetingDate', 'sourceManifest', 'spokenSummary', 'draftMarkdown', 'blockers', 'nextStep')
    } | ConvertTo-Json -Depth 20 -Compress

    $McpRoot = Join-Path $ClonePath 'mcp\meeting-context'
    $McpConfig = @{
        mcpServers = @{
            'meeting-context' = @{
                type = 'stdio'
                command = 'python'
                args = @('-m', 'meeting_context.server')
                env = @{
                    PYTHONPATH = $McpRoot
                    MEETING_CONTEXT_ALLOW_OUTLOOK_REFRESH = if ($RefreshOutlook) { '1' } else { '0' }
                }
            }
        }
    } | ConvertTo-Json -Depth 10 -Compress
    $McpConfigPath = Join-Path $Workspace 'mcp-config.json'
    [IO.File]::WriteAllText($McpConfigPath, $McpConfig, [Text.UTF8Encoding]::new($false))

    Push-Location $ClonePath
    try {
        if ($ClaudeAuth.authMethod -eq 'claude.ai' -and $ChildHadAnthropicApiKey) {
            Write-Diagnostic 'removing ANTHROPIC_API_KEY from the child Claude process so Claude.ai connectors can load'
            Remove-Item Env:ANTHROPIC_API_KEY
        }

        Write-Diagnostic 'starting Claude in non-interactive, draft-only mode'
        $ClaudeArgs = @(
            '--print',
            '--output-format', 'json',
            '--json-schema', $Schema,
            '--permission-mode', 'dontAsk',
            '--setting-sources', 'user,project,local',
            '--mcp-config', $McpConfigPath,
            '--effort', 'medium',
            '--name', "meeting-prep-$RunId",
            $Prompt
        )
        $SavedErrorActionPreference = $ErrorActionPreference
        $ErrorActionPreference = 'Continue'
        try {
            $ClaudeRaw = & $ClaudePath @ClaudeArgs
            $ClaudeExitCode = $LASTEXITCODE
        }
        finally {
            $ErrorActionPreference = $SavedErrorActionPreference
        }
        if ($ClaudeExitCode -ne 0) {
            throw "Claude exited with code $ClaudeExitCode."
        }
    }
    finally {
        if ($ChildHadAnthropicApiKey) {
            $env:ANTHROPIC_API_KEY = $SavedAnthropicApiKey
        }
        Pop-Location
    }

    try {
        $ClaudeEnvelope = ($ClaudeRaw -join [Environment]::NewLine) | ConvertFrom-Json
    }
    catch {
        throw 'Claude completed but did not return valid JSON.'
    }

    $Dirty = & $GitPath -C $ClonePath status --porcelain
    if ($LASTEXITCODE -ne 0) {
        throw 'Unable to verify the disposable checkout state.'
    }
    if ($Dirty) {
        $WorkspaceState = 'preserved-dirty'
        Write-Diagnostic "Claude changed the draft-only checkout; preserving it for inspection at $Workspace"
    }
    elseif ($KeepWorkspace) {
        $WorkspaceState = 'preserved-by-request'
    }
    else {
        Remove-Item -LiteralPath $Workspace -Recurse -Force
        $WorkspaceState = 'removed-clean'
    }

    Write-Result @{
        schemaVersion = 1
        status = 'completed'
        runId = $RunId
        repository = $Repository
        meetingType = $MeetingType
        meetingDate = $MeetingDate
        workspaceState = $WorkspaceState
        workspacePath = if ($WorkspaceState -like 'preserved-*') { $Workspace } else { $null }
        claude = $ClaudeEnvelope
    }
    exit 0
}
catch {
    if ($ChildHadAnthropicApiKey) {
        $env:ANTHROPIC_API_KEY = $SavedAnthropicApiKey
    }
    if ($WorkspaceState -eq 'created' -and (Test-Path -LiteralPath $Workspace)) {
        $WorkspaceState = 'preserved-after-failure'
    }
    Write-Result @{
        schemaVersion = 1
        status = 'failed'
        runId = $RunId
        repository = $Repository
        meetingType = $MeetingType
        meetingDate = $MeetingDate
        error = $_.Exception.Message
        workspaceState = $WorkspaceState
        workspacePath = if (Test-Path -LiteralPath $Workspace) { $Workspace } else { $null }
    }
    exit 1
}
