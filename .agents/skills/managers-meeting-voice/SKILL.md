---
name: managers-meeting-voice
description: Prepare, revise, or historically test Kevin's draft-only HR Systems Managers Meeting speaker's brief. This IS the front door — Kevin talks or types directly into this Claude session, and this skill runs the workflow itself. Mandatory Roadmap assessment, source freshness, strict validation, no publication or Outlook refresh.
---

# Managers Meeting Voice

As of 1 August 2026 Claude is the approved voice/chat front door for this
workflow (see `begb0037admin/voice-workflows`
`docs/decisions/2026-08-01-claude-voice-front-door.md`). There is no separate
dispatcher and no job/poll wrapper — this session runs the launcher directly
and waits for it to finish. The two-minute-command-window constraints in the
retired ChatGPT Work plugin do not apply here.

Use this skill for:

> Prepare my Managers Meeting draft.
> Run the historical Managers Meeting check.
> Revise my Managers Meeting draft.

## Resolve

1. Resolve the intended Managers Meeting date from Kevin's request and current
   calendar context.
2. If the date is materially unclear, ask one concise question.
3. Use historical mode only when Kevin explicitly asks for the historical or
   archived integration check — see Historical mode below. Do not treat a dry
   run or a backend run as a genuine user smoke test.
4. Name the visible task `Managers Meeting draft — YYYY-MM-DD`.

## Get the launcher

The launcher (`scripts/start-managers-meeting.ps1`) is a PowerShell script and
must exist as a local file to run. GitHub remains the sole source of truth —
do not treat any local copy as a standing working checkout. Before each run,
sync the read-only reference checkout at `C:\Users\admin\meeting-records` to
`main` (`git -C C:\Users\admin\meeting-records pull --ff-only`; if that path
does not exist, fetch the script fresh from
`raw.githubusercontent.com/begb0037admin/meeting-records/main/.agents/skills/managers-meeting-voice/scripts/start-managers-meeting.ps1`
into scratchpad instead) and run it from there. Never commit or push through
this checkout — it is read-only reference.

## Draft

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill-dir>\scripts\start-managers-meeting.ps1" -MeetingDate "<YYYY-MM-DD>"
```

If Granola confirms the latest Roadmap outcome was not captured, keep the run
blocked unless Kevin supplies a manual recap. Store an explicit recap as UTF-8 JSON:

```json
{
  "meetingTitle": "HR Systems Roadmap — DD/MM",
  "meetingDate": "YYYY-MM-DD",
  "suppliedBy": "Kevin",
  "recap": "Kevin's substantive account of decisions, actions and changes."
}
```

Pass it with `-ManualRoadmapRecapPath`. The result must retain Granola as
`unavailable` and list `manual-roadmap-recap` separately as `used`. Never infer
or reconstruct the recap.

The command emits progress events on standard error and one result object on
standard output. Surface the task name and current stage while it runs.

For a completed result:

1. Report source coverage and freshness warnings.
2. Present `spokenSummary`.
3. Display `draftMarkdown` in full.
4. Ask what Kevin wants changed.

For a blocked or failed result, report the exact source, validation,
authentication or execution blocker. Do not generate a substitute brief.

## Historical mode

The approved archived integration check uses the fixture dated 24 June 2026.
The launcher itself takes `-FixturePath` (there is no `-HistoricalFixture`
convenience switch here — that lived only in the retired ChatGPT plugin):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill-dir>\scripts\start-managers-meeting.ps1" `
  -MeetingDate "2026-06-24" `
  -FixturePath "<meeting-records-checkout>\mcp\meeting-context\fixtures\managers-meeting-2026-06-24.json"
```

The fixture deliberately withholds the benchmark and pins `-MeetingDate` to
`2026-06-24` — the launcher rejects any other date paired with this fixture.
Report the result the same way as a live Draft run; do not present a
historical-mode result as a genuine live smoke test.

## Revise

Preserve the current draft and source manifest in temporary files, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill-dir>\scripts\start-managers-meeting.ps1" `
  -MeetingDate "<YYYY-MM-DD>" `
  -Mode Revise `
  -ExistingDraftPath "<temporary-draft-path>" `
  -PriorSourceManifestPath "<temporary-source-manifest-path>" `
  -RevisionInstruction "<Kevin's spoken or typed instruction>"
```

Return the revised draft to the same conversation. The launcher revalidates it
and keeps the state `draft`.

## Safety

- This skill has no Outlook-refresh option.
- It exposes no repository or source-system write tool.
- It cannot publish, send, distribute or schedule.
- Any dirty checkout is a failed run.
- “Yes”, “fine”, “looks good” and “perfect” do not authorise publication.
