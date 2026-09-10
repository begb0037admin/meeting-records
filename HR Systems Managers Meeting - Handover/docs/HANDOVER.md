# HANDOVER — HR Systems Managers Meeting voice prototype

## Checkpoint — 10 September 2026

### Current state

The implementation is still present in `begb0037admin/meeting-records`, but it
has been reorganised into separate responsibilities rather than removed:

- `.agents/skills/chatGPT-meeting-prep-voice/` is the retained Codex/ChatGPT
  Voice front-end proof of concept. It dispatches a draft-only request to the
  established Claude workflow in a fresh disposable checkout.
- `.agents/skills/claude-meeting-voice/` is the current Claude-native front
  door and direct launcher for the Managers Meeting workflow.
- `mcp/meeting-connector/` is the focused meeting-context MCP. Its normal tools
  read GitHub-published Work Inbox, Command Centre, HR roadmap and previous
  meeting material. Outlook refresh is a separate explicit action, never an
  automatic or background action.

The repository's current governance record treats the direct Claude workflow
as the approved route. The Codex/ChatGPT route remains useful as a historical
Windows prototype, but it must not be described as a verified production
Voice-to-background-work integration.

The current `main` checkpoint is commit `aa2e2ef` (10 September 2026). No
current Managers Meeting run is expected for this checkpoint; the last
archived Managers Meeting material available for proof-of-concept validation is
the 24 June 2026 record.

### Evidence checked in this session

- The repository layout and both voice skills were read from a fresh shallow
  GitHub checkout.
- The MCP unit suite passed: 46 tests, including read-only source handling,
  roadmap filtering, Granola-source handling, result validation, and the exact
  Outlook-refresh confirmation gate.
- The historical stdio validator exists and exposes the six expected tools,
  including the separately guarded Outlook action. In this Windows run it
  reached MCP initialisation, tool listing, source health, briefing, tasks and
  roadmap calls, but did not emit its final summary. The earlier sandbox run
  failed before starting the child process with `WinError 5`. Treat the
  historical end-to-end validator as **incomplete in this checkpoint**, not as
  a new pass claim.

### Safety boundary

- No Outlook refresh was run.
- No current meeting information was used or implied.
- No meeting brief, task, source repository or live record was published or
  changed.
- The repository's show → approve → push gate remains in force.

### Exact next safe action

1. If Kevin wants to continue the Codex-as-Voice-front-end experiment, run a
   no-write Windows smoke test from ChatGPT Voice and verify that a visible
   background handoff and returned draft actually appear. Use archived material
   or harmless placeholder data only.
2. Separately rerun the 24 June stdio validation until it either completes with
   its JSON summary or produces a captured diagnostic. Do not use that run to
   refresh Outlook, publish a brief, or change a live record.
3. Only after Kevin approves the user experience should the team decide whether
   the Codex route should be restored as a supported front end; until then,
   Claude direct remains the documented production route.

### Resume instruction

Start with this file, then read `STATUS.md` and the 10 September session log.
For a live meeting-prep request, use `.agents/skills/claude-meeting-voice/`.
For the Windows Voice prototype only, use
`.agents/skills/chatGPT-meeting-prep-voice/` and keep the run draft-only.
