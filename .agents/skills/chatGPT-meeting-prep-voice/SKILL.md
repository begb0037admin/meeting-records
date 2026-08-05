---
name: chatGPT-meeting-prep-voice
description: Use Claude Code as the established reasoning engine for meeting-records while Codex acts as the Voice interface. Use when Kevin asks by voice or text to prepare, draft, start, or review an HR Systems meeting brief on Windows, including Managers Meeting, FA Team Catch-up, HR Systems Roadmap, H&S Roadmap, Simon 1-1, team 1-1, or KPI Monthly Standing Agenda.
---

# Voice Meeting Prep

Use Codex as the conversational interface and Claude Code as the meeting-prep worker. Do not replace Claude's established `meeting-records` reasoning or rewrite its draft in Codex.

## Prototype boundary

- Produce a draft only.
- Never write, commit, or push a meeting document.
- Never schedule the workflow.
- Preserve the repository's show → approve → push gate.
- Treat GitHub as the sole source of truth. The launcher uses a fresh disposable checkout.

## Start a draft

1. Resolve the meeting type and intended date from the user's request.
2. If either materially affects the requested output and is unclear, ask one concise question.
3. Run `scripts/start-meeting-prep.ps1` from this skill directory:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill-dir>\scripts\start-meeting-prep.ps1" -MeetingType "<meeting type>" -MeetingDate "<YYYY-MM-DD>" -AdditionalContext "<optional user instruction>"
```

4. Allow the command to finish. It may take several minutes while Claude reads GitHub and connected sources.
5. Parse the single JSON object written to standard output. Treat standard error as progress or diagnostics, not as the result.

## Present the result

If the launcher returns `status: completed`:

1. State that Claude prepared the draft.
2. Summarize Claude's source coverage and any freshness warnings.
3. Read or summarize `spokenSummary` conversationally.
4. Display the complete `draftMarkdown` before seeking approval.
5. Ask what Kevin wants changed. Do not perform the change in Codex; explain that revision handoff is the next prototype stage if requested.

If the launcher or Claude returns a blocked or failed state:

1. Report the exact blocker.
2. Distinguish authentication, connector availability, stale source data, and Claude execution failures.
3. Do not substitute Codex-generated meeting content.

## Source and authority rules

- Claude must load the current `meeting-records` governance and workflow files from the fresh checkout.
- Claude owns source gathering, synthesis, and draft wording.
- Codex owns speech interaction, dispatch, progress explanation, and displaying results.
- Kevin owns every approval decision.
- A conversational acknowledgment such as "yes", "fine", or "looks good" never authorizes publication in this prototype.

## Diagnostics

Use `-DryRun` to verify the launcher, authentication discovery, dispatch contract, and output paths without cloning GitHub or invoking Claude:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill-dir>\scripts\start-meeting-prep.ps1" -MeetingType "HR Systems Managers Meeting" -MeetingDate "2026-08-05" -DryRun
```
