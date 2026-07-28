# CLAUDE.md — meeting-records
> AI bootstrap entry point. Read this first.
> Keep this file under 200 lines. Push details to linked docs.

## Identity
- **Project:** Meeting Records — container repo for Kevin's recurring meeting prep and records
- **Purpose:** Stores prep documents, agendas, notes, and handover materials for Kevin's recurring meetings and team management activities.
- **Owner:** Kevin Lelitte, Manager/Director HR Systems, University of Oxford
- **Status:** Active
- **Repo:** https://github.com/begb0037admin/meeting-records
- **Last updated:** 2026-06-26

## Bootstrap Order
1. This file (orientation)
2. Navigate to the relevant subfolder and read its CLAUDE.md
3. For meeting prep documents: read `Meeting Reviews/docs/reference/meeting-prep-formats.md` — this defines the exact format for every prep document type
4. Then check `Meeting Reviews/` for the most recent prep file of the same type as context

Do NOT ask Kevin for a recap. Navigate to the relevant subfolder.

## Codex Voice Front End (Prototype)
- Shared skill: `.agents/skills/meeting-prep-voice/`
- Purpose: let Kevin ask Codex Voice to start the existing Claude meeting-prep workflow on Windows.
- Codex is the conversational interface and dispatcher. Claude remains the reasoning engine and meeting-brief author.
- The prototype is draft-only. It has no authority to write, commit, push, schedule, publish, send, rename, or delete anything.
- Runtime checkouts are fresh and disposable. GitHub remains the sole source of truth.
- `ANTHROPIC_API_KEY` is removed only from the child Claude process when Claude.ai authentication is active, so configured Claude.ai connectors such as Granola can load. The parent shell and persisted environment are not changed.
- The normal show → approve → push gate remains unchanged. Revision and publication handoffs are deliberately deferred until the draft-only flow has been proven.

## Structure
| Folder | Purpose |
|---|---|
| `Meeting Reviews/` | One-off meeting prep docs. See naming convention below. |
| `KPI Monthly Standing Agenda/` | Monthly standing agenda meeting + monthly KPI run |
| `SK - Handover/` | Stephen Kirker handover materials |
| `Meeting Archive/` | Archived meeting records |
| `Team 1-1's/` | Team 1-1 records (Michael, Asta, James) |

## File Naming Convention
All meeting prep documents in `Meeting Reviews/` follow the Granola naming standard so files and meetings match:

| Meeting | File name format | Example | Granola title |
|---|---|---|---|
| FA Team morning catch-up | `FA Team Catch-up — DD-MM.md` | `FA Team Catch-up — 19-06.md` | `FA Team Catch-up — DD/MM` |
| HR Systems Roadmap meeting | `HR Systems Roadmap — DD-MM.md` | `HR Systems Roadmap — 19-06.md` | `HR Systems Roadmap — DD/MM` |
| H&S Roadmap meeting | `H&S Roadmap — DD-MM.md` | `H&S Roadmap — 22-06.md` | `H&S Roadmap DD/MM` |
| KPI Monthly Standing Agenda | `KPI Standing Agenda — MMM YYYY.md` | `KPI Standing Agenda — Jun 2026.md` | |
| Team 1-1 | `1-1 [Name] — DD-MM.md` | `1-1 Michael — 15-06.md` | |
| Simon 1-1 | `1-1 Simon — DD-MM.md` | `1-1 Simon — 26-06.md` | Granola title: `SK 1-1 DD/MM` |

## People & Abbreviations
| Abbreviation | Person | Role |
|---|---|---|
| SK | Simon (Kevin's manager) | Director-level; Kevin's 1-1 is with Simon. Granola titles: `SK 1-1 DD/MM`. File names: `1-1 Simon — DD-MM.md` in `Meeting Reviews/`. |
| FA team | Kevin, Michael, Asta, James | Functional Analysis team |

## Meeting Cadence
| Meeting | Day | Frequency |
|---|---|---|
| FA Team Catch-up | Wednesday + Friday | Twice weekly |
| HR Systems Roadmap | Friday | Weekly |
| H&S Roadmap | Monday | Weekly |
| Simon 1-1 (SK) | Wednesday | Fortnightly |
| Team 1-1 — Michael / Asta / James | Varies | Rotating weekly (one per week) |
| KPI Monthly Standing Agenda | 2nd–3rd week | Monthly |

## Meeting Prep Workflow (FA Catch-up Wednesdays)
Every Wednesday FA team check-in (Kevin, Michael, Asta, James):
1. Check Granola for the most recent FA catch-up and any relevant meetings since
2. Check `begb0037admin/work-inbox/data/briefing.json` for inbox updates
3. Check `begb0037admin/command-centre/data/tasks.json` for active tasks
4. Produce one document in `Meeting Reviews/`: `FA Team Catch-up — DD-MM.md`

## Meeting Prep Workflow (Roadmap Fridays)
Every Friday before the 10:00 HR Systems Roadmap meeting:
1. Read live roadmap from `begb0037admin/hr-projects/HR Systems Roadmap/HR Systems Roadmap MASTER.xlsm` (read-only, openpyxl via base64 decode)
2. Check Granola for recent FA team catch-ups (Kevin, Michael, Asta, James)
3. Check `begb0037admin/work-inbox/data/briefing.json` for inbox updates
4. Check `begb0037admin/command-centre/data/tasks.json` for active tasks
5. Produce two documents in `Meeting Reviews/`:
   - `FA Team Catch-up — DD-MM.md` — morning catch-up agenda before the roadmap meeting
   - `HR Systems Roadmap — DD-MM.md` — speaking brief for 10:00 roadmap meeting

## Meeting Prep Workflow (H&S Roadmap Mondays)
Every Monday before the H&S Roadmap meeting (attendees: Kevin, James, Chris):
1. Check Granola for the most recent H&S Roadmap meeting (previous Monday) — pull open actions and carry-forwards
2. Check Granola for any H&S-adjacent meetings during the week (e.g. evaluation sessions, PUG, supplier calls)
3. Produce one document in `Meeting Reviews/`: `H&S Roadmap — DD-MM.md`

Document structure:
- Actions from last meeting — status check table
- Standing items by system (Cority, IRIS/Eco Online, DSE, Odyssey, Risk Base)
- Any active projects (e.g. H&S Management System evaluation)
- Funding and blockers
- Source footer

## Meeting Prep Workflow (Simon 1-1)
Fortnightly, every Wednesday. Granola title: `SK 1-1 DD/MM`. File: `1-1 Simon — DD-MM.md` in `Meeting Reviews/`.
1. Pull Granola — most recent SK 1-1 and any relevant meetings since
2. Check `begb0037admin/work-inbox/data/briefing.json` and `begb0037admin/command-centre/data/tasks.json`
3. Produce `1-1 Simon — DD-MM.md` — show to Kevin, get approval, then push to main

## Meeting Prep Workflow (Team 1-1s — Michael, Asta, James)
Rotating weekly — one person per week, cycling through Michael, Asta, James. Detailed workflow in `Team 1-1's/CLAUDE.md`.
1. Pull Granola — most recent 1-1 with this person
2. Read `Team 1-1's/[Name]/docs/reference/open-actions.md` — overdue items first
3. Read `Team 1-1's/[Name]/docs/HANDOVER.md`
4. Produce pre-meeting brief — show to Kevin, get approval, then save to `Team 1-1's/[Name]/docs/sessions/`
5. Post-meeting: pull Granola transcript, append notes to same session file — show to Kevin, get approval, then push
6. Surface new actions for Kevin to confirm — do NOT auto-write to open-actions.md

## Meeting Prep Workflow (KPI Monthly Standing Agenda)
Monthly — typically 2nd or 3rd week. Detailed context in `KPI Monthly Standing Agenda/CLAUDE.md`.
1. Read `KPI Monthly Standing Agenda/docs/HANDOVER.md` and most recent session file
2. Pull Granola for any relevant discussions since last meeting
3. Check `begb0037admin/command-centre/data/tasks.json` for relevant actions
4. Produce meeting prep document — show to Kevin, get approval, then save to `KPI Monthly Standing Agenda/docs/sessions/`
5. KPI run output is a separate file from meeting prep — same approval gate applies

## Meeting Prep Workflow (Ad Hoc)
Any meeting Kevin asks to prepare for — one-off reviews, supplier meetings, evaluation sessions, escalation meetings, or any meeting not covered by the scheduled workflows above.
1. Ask Kevin what data sources are relevant (Granola, inbox, tasks, roadmap, emails, prior notes)
2. Gather those sources
3. Produce one document in `Meeting Reviews/` following the naming convention
4. For meeting types not yet in `docs/reference/meeting-prep-formats.md`: use the closest existing format as a base, note the adaptation, and add the new format to the reference doc after Kevin approves it

The approval gate applies equally to ad hoc documents. Show → approve → push. No exceptions.

## Effort Level Governance
Before any task where higher effort is warranted, signal to Kevin: what the task is, why higher effort is needed, and an explicit request to raise the effort level. Wait — do not proceed until Kevin raises it. Signal when the high-effort phase is done; Kevin decides when to return to normal. Never change effort level unilaterally. See CONSTITUTION.md Section 10 (v2.0, 2026-06-27).

## Hard Rules
- Never modify the HR Systems Roadmap — read only
- Never commit personal email content verbatim
- Always push prep documents directly to main
- Always update `Meeting Reviews/docs/HANDOVER.md` at end of session
- File names MUST follow the Granola naming convention above
- **Approval gate:** Never push any meeting document — scheduled or ad hoc — without first showing the full content to Kevin in chat and receiving his explicit approval. Show → approve → push. No exceptions.
- All mockups and visual designs are produced as Claude Artifacts — never committed to the repository (see CONSTITUTION.md Section 11)

## Branch and Merge Protocol
Always push directly to main. If a branch must be used, merge it to main immediately upon completion — never leave files on a branch.
