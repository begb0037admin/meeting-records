---
name: managers-meeting-voice
description: Prepare or revise Kevin's draft-only HR Systems Managers Meeting speaker's brief through Claude Code, with mandatory Roadmap assessment, source freshness, strict validation, and no publication or Outlook refresh.
---

# Managers Meeting Voice

Use this skill for:

> Prepare my Managers Meeting draft.

## Resolve

1. Resolve the intended Managers Meeting date from Kevin's request and current
   calendar context.
2. If the date is materially unclear, ask one concise question.
3. Name the visible task `Managers Meeting draft — YYYY-MM-DD`.

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
3. Display `draftMarkdown` in full without replacing it with a Codex summary.
4. Ask what Kevin wants changed.

For a blocked or failed result, report the exact source, validation,
authentication or execution blocker. Do not generate a substitute brief.

## Revise

Preserve the current draft and source manifest in temporary files, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill-dir>\scripts\start-managers-meeting.ps1" `
  -MeetingDate "<YYYY-MM-DD>" `
  -Mode Revise `
  -ExistingDraftPath "<temporary-draft-path>" `
  -PriorSourceManifestPath "<temporary-source-manifest-path>" `
  -RevisionInstruction "<Kevin's spoken instruction>"
```

Return the revised draft to the same conversation. The launcher revalidates it
and keeps the state `draft`.

## Safety

- This skill has no Outlook-refresh option.
- It exposes no repository or source-system write tool.
- It cannot publish, send, distribute or schedule.
- Any dirty checkout is a failed run.
- “Yes”, “fine”, “looks good” and “perfect” do not authorise publication.
