# Meeting Connector MCP

Read-only source adapter for the Windows Managers Meeting Voice proof of concept.

It exposes five normal read tools:

- `get_source_health`
- `get_inbox_briefing`
- `get_command_centre_tasks`
- `get_roadmap_items`
- `get_previous_meeting_prep`

All normal repository reads use authenticated `gh api --method GET`.

It also exposes one deliberately separate consequential action:

- `refresh_outlook_work_inbox`

This action runs only when its MCP process was separately enabled for an
explicit refresh invocation and it is called with the exact confirmation
`REFRESH OUTLOOK AND PUBLISH WORK INBOX`. It invokes the established
`work-inbox/Run_Inbox_Briefing.ps1` process from a disposable checkout, so its
existing GitHub publication and Command Centre task-update behaviour still
applies. Normal meeting preparation must not call it. There is no schedule,
polling, automatic refresh, or background worker.

The Voice launcher keeps the action disabled in normal meeting preparation.
It enables it only when called with both `-RefreshOutlook` and the exact
`-RefreshConfirmation` value.

For historical validation, pass the Git refs that existed at the meeting date.
The 24 June 2026 proof of concept uses:

- Work Inbox: `1dded7a99ed3`
- Command Centre: `019dd2497c69`
- HR roadmap: `f16a11ac3377`
- Meeting record: `main`

Granola remains Claude's existing connector. `get_source_health` reports it as
external coverage so Claude must explicitly confirm whether that connector was
available; the MCP does not pretend to reproduce Granola.

Run from this directory:

```powershell
python -m pip install -e .
python -m meeting_context.server
```

Validate the real stdio MCP protocol against archived sources:

```powershell
python scripts/validate_historical.py
```

The Voice launcher supplies this server to Claude for that invocation while
retaining Claude's existing user-level connectors, including Granola.
