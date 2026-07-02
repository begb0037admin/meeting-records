# HANDOVER.md — Meeting Reviews

> Replace this file each session. Do not append.

**Session date:** 3 July 2026
**Written by:** Outgoing session — context compacted, this is the handover for the next session
**Status:** Friday meeting prep complete and pushed. One major task approved and ready to execute: Dashboard Roadmap creation. Blocked on repo access — requires a new session with all repos added at launch.

---

## IF YOU ARE READING THIS COLD — START HERE

You have no memory of previous sessions. Do not guess context. Do not ask Kevin to recap. This document is your complete brief. Read it in full before doing anything.

You are working for **Kevin Lelitte**, Manager/Director HR Systems, University of Oxford. Kevin manages a team called the FA team (Kevin, Michael, Asta, James) and oversees all HR systems for the university. He operates through a network of GitHub repos that serve as his operational system — meeting prep, project tracking, dashboards, and tooling.

The governance model is defined in `CONSTITUTION.md` (in this repo, root level). Read it. Key principles:
- **Section 2:** A dispatch must be complete — the executor never makes architectural decisions. If you encounter something that requires a decision not covered here, stop and ask Kevin.
- **Section 4:** Before any change, a restore point must be recorded. For file pushes to GitHub, the previous commit SHA is the restore point — note it before pushing.
- **Section 5:** Conversation is temporary. Documentation is permanent. Update HANDOVER.md before this session ends.
- **Section 6:** Source of truth hierarchy: Kevin's current preferences > CONSTITUTION.md > AGENT_MODEL.md > CLAUDE.md > HANDOVER.md. When documents conflict, the higher one wins.
- **Section 10:** Effort level is Kevin's to set. Signal before beginning any high-effort task. Wait. Do not proceed until Kevin raises the effort level. Exception: if this HANDOVER.md explicitly states Kevin already approved a task, proceed — the signal was given in the previous session.

**Approval gate (from `meeting-records/CLAUDE.md`):** Never push any meeting document without first showing it to Kevin in chat and receiving explicit approval. Show → approve → push. No exceptions. HANDOVER.md and CLAUDE.md updates are not meeting documents and do not require approval before pushing.

**Branch rule:** Always push directly to main. Never leave work on a branch.

---

## Bootstrap order — do this before anything else

1. Read this file in full
2. Read `meeting-records/CLAUDE.md` — project identity, workflows, naming conventions, people, hard rules
3. Read `meeting-records/CONSTITUTION.md` — governing principles
4. Read `Meeting Reviews/docs/reference/meeting-prep-formats.md` — exact format for every meeting document type
5. Then read the CLAUDE.md of whichever repo the active task requires (see task section below)

Do not begin any task until steps 1–4 are complete.

---

## The repo ecosystem

All repos are under the GitHub organisation `begb0037admin`. Kevin's operational system spans the following repos:

### Core repos (governance, projects, meetings)

| Repo | Purpose |
|---|---|
| `meeting-records` | Meeting prep documents — FA catch-ups, roadmap briefs, 1-1s, H&S roadmap, KPI agenda |
| `hr-projects` | HR Systems project workspaces + the live HR Systems Roadmap MASTER.xlsm (read-only, OneDrive-synced) |

### Dashboard repos (ten dashboards, all under active development)

| Repo | Dashboard name | Purpose |
|---|---|---|
| `command-centre` | Command Centre Dashboard | Central hub — also stores shared data files (tasks.json, briefing.json, dashboard-roadmap.json will live here) |
| `work-inbox` | Work Inbox Dashboard | Kevin's incoming work items and briefing data |
| `meeting-records` | Meeting Dashboard | Meeting prep automation and records |
| `hr-projects` | HR Projects Dashboard | HR Systems project tracking |
| `hris-dashboard` | HRIS Team Dashboard | HRIS team operations view |
| `hr-fa-knowledge-base` | Knowledge Base Dashboard | FA team knowledge base |
| `AG-FlexPoints` | AG FlexPoint Dashboard | AG FlexPoints data and tooling |
| `clockify` | Clockify Dashboard | Time tracking integration |
| `hris-change-requests` | Change Request Dashboard | HR systems change request tracking |
| `hris-launcher` | HRIS Launcher Dashboard | Launch hub for HRIS tools |

Note: `meeting-records` and `hr-projects` serve dual roles — they are both functional repos and dashboard repos.

---

## What was done in the session ending 3 July 2026

### Meeting prep — both documents pushed to main

**`Meeting Reviews/FA Team Catch-up — 03-07.md`** — pushed to main. Morning FA team catch-up agenda (before the 10:00 roadmap meeting). 7 items: SSO decision (Asta), DTP1334 debrief (James), PACS org structure (James), H&S Dashboards (James), WFM handover (Michael — note: Michael won't be in the Friday meeting, this is for a separate check-in), REF/HESA UDF (Asta), emergency Loop docs (all).

**`Meeting Reviews/HR Systems Roadmap — 03-07.md`** — pushed to main. Full speaking brief for 10:00 HR Systems Roadmap meeting. Genuine updates this week: WFM resolution meeting outcome, REF/HESA approach confirmed, Evo/PeopleXD purchase confirmed, PACS org structure impact request, July cover planning. Items unchanged since 26 June: DPIA Stage 7, H&S Dashboards, SSO Migration.

### Dashboard roadmap task — approved, not yet executed

Kevin approved the creation of a central `dashboard-roadmap.json` in `command-centre`. Full specification is in the task section below. The session was blocked on repo access (only `meeting-records` and `hr-projects` were accessible). A new session with all repos added is required to execute.

---

## ACTIVE TASK: Dashboard Roadmap — approved, ready to execute

### What this is and why it exists

Kevin's dashboard ecosystem has no central roadmap. Work items, planned features, open fixes, and blockers are scattered across repos or not tracked at all. `dashboard-roadmap.json` is the solution: a single JSON file in `command-centre/data/` that tracks all active work across all ten dashboard repos. It is the cross-repo equivalent of what `HR Systems Roadmap MASTER.xlsm` is for the HR Systems team.

This is not limited to any single workstream or topic. Every ongoing item, planned feature, open fix, blocked task, or in-progress work across any of the ten repos belongs in this file.

**Kevin approved this task on 3 July 2026. No effort level signal is required. Proceed directly to execution.**

### Step 1 — Read every repo's CLAUDE.md

Before touching any files, read the CLAUDE.md in each of the ten dashboard repos. This tells you what each repo is for, what conventions it follows, and whether there are any rules that affect how you write to it. If a repo has no CLAUDE.md, note that and proceed.

Also read:
- `command-centre/data/tasks.json` (if it exists) — to understand the existing JSON schema conventions
- `work-inbox/data/briefing.json` (if it exists) — same reason

You are matching the schema style already in use, not inventing a new one.

### Step 2 — Scan all ten repos for existing tracked work

For each repo, look for:
- Any HANDOVER.md or STATUS.md — open items and in-progress state
- Any file named `roadmap`, `backlog`, `tasks`, or similar in the root or `data/` directory
- Any roadmap or tracked-work sections inside CLAUDE.md
- Any `data/*.json` files that contain work tracking

Record every find in full before writing anything. This is a read-only phase.

### Step 3 — Propose the schema to Kevin before writing

Once you have read `tasks.json`, `briefing.json`, and all existing content, draft the JSON schema for `dashboard-roadmap.json`. Show Kevin:
1. The proposed schema (with field names, types, and a worked example)
2. The full list of seed entries you found in Step 2, formatted as JSON
3. The automation trigger entry (see below — this is always the first entry)

Wait for Kevin's explicit approval before writing any file. This is the approval gate for the data design.

### Step 4 — Push `data/dashboard-roadmap.json` to `command-centre` main

Path: `command-centre/data/dashboard-roadmap.json`

Minimum schema per entry (adjust to match existing conventions from Step 1):

```json
{
  "id": "DASH-001",
  "dashboard": "Meeting Dashboard",
  "repo": "begb0037admin/meeting-records",
  "title": "Brief title",
  "status": "blocked | in-progress | planned | complete",
  "description": "What this is and why it matters.",
  "blockers": ["Blocker 1", "Blocker 2"],
  "next_action": "The next concrete step.",
  "owner": "Kevin",
  "last_updated": "2026-07-03"
}
```

**First entry — always include this:**
```json
{
  "id": "DASH-001",
  "dashboard": "Meeting Dashboard",
  "repo": "begb0037admin/meeting-records",
  "title": "Automated meeting prep triggers — broken, awaiting fix",
  "status": "blocked",
  "description": "Six CronCreate triggers were created on 1 July 2026 to automatically run weekly meeting prep documents: FA Catch-up (Wednesday), HR Systems Roadmap (Friday), H&S Roadmap (Monday), SK 1-1 (Wednesday fortnightly), HR Managers Meeting, and KPI Monthly. All six fail silently on every run. Root cause: triggered sessions only receive default tool access and do not have mcp__github__* or mcp__Granola__* tools, which are required for meeting prep. The Claude_Code_Remote MCP server also requires OAuth re-authorisation before any fix can be tested.",
  "blockers": [
    "Claude_Code_Remote MCP server needs OAuth re-authorisation via claude.ai Settings > Connectors",
    "MCP tool availability in triggered sessions (mcp__github__*, mcp__Granola__*) not yet resolved"
  ],
  "next_action": "Re-authorise Claude_Code_Remote MCP, then investigate MCP tool availability in triggered sessions and fix or redesign trigger prompts to work within available tools.",
  "owner": "Kevin",
  "last_updated": "2026-07-03"
}
```

Trigger IDs (preserve — do not delete):
- FA Catch-up: `trig_01QZYRrgfaUBgxPpuhVP719x`
- HR Roadmap: `trig_01QUr1UThQjgsA8SC32LRUnC`
- H&S Roadmap: `trig_01Qj16eCt3czyZGMTKrqeGAw`
- SK 1-1: `trig_01MahTwTm6YU8mE8RKyEFcT9`
- HR Managers Meeting: `trig_013GXDAQs5QUUkAhRgExjmm5`
- KPI Monthly: `trig_01JDNnv6ag6NzUVsoPA9L5fH`

### Step 5 — Update every repo's CLAUDE.md

Add the following two blocks to the CLAUDE.md in each of the ten dashboard repos. Find the most appropriate section (Hard Rules, or create a new section called `## Dashboard Roadmap`). Do not change any other content. Do not reformat or reorganise existing content.

**Block 1 — Roadmap reference:**
```
## Dashboard Roadmap
All roadmap items for this dashboard are tracked centrally:
- Repo: `begb0037admin/command-centre`
- File: `data/dashboard-roadmap.json`

Do not maintain a local roadmap in this repo. All roadmap entries go to the central file.
```

**Block 2 — Mockup rule (add to Hard Rules or equivalent section):**
```
- Mockups and visual prototypes always use Claude Artifacts. Never create HTML files for mockups. All visual work is presented as a live Artifact so it can be iterated in-session.
```

If a repo has no CLAUDE.md, create a minimal one with these two blocks and the repo identity (name, purpose, owner). Surface it to Kevin before pushing.

These CLAUDE.md additions do not require Kevin's approval before pushing — they are mechanical and non-ambiguous. However, if Step 2 surfaced any unexpected existing roadmap content in a repo, surface that to Kevin before overwriting or migrating it.

### Step 6 — Update this HANDOVER.md

Before ending the session, replace this file with an updated version that:
- Marks the dashboard roadmap task as complete
- Records what was found in each repo during Step 2
- Updates the open items section with anything new
- Follows the same cold-session-proof standard as this document

---

## How to use the tools

### GitHub operations
All file reads and writes go through the GitHub MCP tools:
- **Read a file:** `mcp__github__get_file_contents` with `owner: begb0037admin`, `repo: <repo-name>`, `path: <file-path>`
- **Push one or more files:** `mcp__github__push_files` with `branch: main`. Always push to main directly.
- **Check what's in a repo:** `mcp__github__get_file_contents` with `path: /` to list root contents

If a push fails, check the error before retrying. Do not retry blind.

### HR Systems Roadmap Excel (hr-projects only — read-only)
The file `HR Systems Roadmap/HR Systems Roadmap MASTER.xlsm` is a binary Excel file. To read it:
1. Call `mcp__github__get_file_contents` — the API returns it as base64-encoded text
2. Extract the base64 content from the response
3. `import base64; data = base64.b64decode(content); open('/tmp/roadmap.xlsm', 'wb').write(data)`
4. `pip install openpyxl -q` then `import openpyxl; wb = openpyxl.load_workbook('/tmp/roadmap.xlsm', read_only=True)`
5. Key sheet: `Work Tracker`. Key columns: ID(0), Activity(1), Lead(6), Team(7), Deadline(19), Progress(22), Next steps(23), Date last reviewed(24), Status(26), Status Details(27)
6. FA team filter: Kevin, Michael, Asta, James

NEVER modify this file. It is a senior management document that Kevin updates manually.

### Granola (meeting transcripts)
Use `mcp__Granola__list_meetings` to find recent meetings, then `mcp__Granola__get_meeting_transcript` to pull content. Match meetings by title using the Granola naming standard defined in `meeting-records/CLAUDE.md`.

---

## Automation status — still broken

Six CronCreate triggers fire at 07:00 UTC each relevant day but all fail silently. The fix is tracked as DASH-001 in `dashboard-roadmap.json` (once that file exists). Until then, all meeting prep is manual.

Fix sequence (not yet actioned — do not attempt in the dashboard roadmap session unless Kevin explicitly asks):
1. Re-authorise Claude_Code_Remote MCP: claude.ai → Settings → Connectors
2. Disable all six triggers while broken
3. Investigate MCP tool access in triggered sessions
4. Fix or redesign trigger prompts
5. Test with one trigger before re-enabling all six
6. Add notification/verification so failures surface

---

## Calendar context — July 2026

| Date | Event |
|---|---|
| Fri 3 Jul | HR Roadmap 10:00 — SSO decision, DPIA chase, DTP1334 revised deadline |
| Mon 6 Jul | Michael and Emma absent (annual leave) |
| Mon 7 Jul | Marie absent (until 17 Jul) |
| Fri 10 Jul | Kevin's surgery — approximately two weeks recovery. Kevin absent from 10 Jul. |
| Sun 13 Jul | Sarah is the only remaining manager |

Escalation chain while Kevin is out: Simon → Renu → Sarah.

---

## Open items from 3 July roadmap meeting — check outcomes in next session

These were live issues going into the 10:00 meeting on 3 July. The next session should check Granola for the meeting transcript to confirm outcomes.

| Item | What was open | What to check |
|---|---|---|
| SSO Migration (179) | VS2022 licensing decision — proceed or park? | Did Asta confirm licensing? What was decided? |
| DPIA Stage 7 (136) | Sitting with Marie Cooksey; deadline passed 30 June | Any response from Marie or Information Compliance Team? |
| DTP1334 H&S System | 31 Jul deadline unachievable; Sep proposed | Did the group agree the revised deadline? Resourcing position formally noted? |
| REF/HESA UDF (DTP1092) | Nathan to raise ISM request; Kevin to test before surgery | ISM request raised? Test window confirmed? |
| WFM GLAM call (ITS1004) | Kevin to speak with Simon and Marie before setting date | Call date set? |
| Evo/PeopleXD | Purchase confirmed; not yet on roadmap | Formal proposal for next roadmap meeting agreed? |
| Volunteering absence email | Kevin to send to Marie — Oct/Nov timeline | Sent? |
| Loop handover docs | Everyone to share links with Kevin by end of 3 Jul | Collected and embedded in HR Systems Management Team chat? |

---

## How to start the new session

1. Add all ten repos to the session before sending the first message:
   - `begb0037admin/meeting-records`
   - `begb0037admin/hr-projects`
   - `begb0037admin/command-centre`
   - `begb0037admin/work-inbox`
   - `begb0037admin/hris-dashboard`
   - `begb0037admin/hr-fa-knowledge-base`
   - `begb0037admin/AG-FlexPoints`
   - `begb0037admin/clockify`
   - `begb0037admin/hris-change-requests`
   - `begb0037admin/hris-launcher`

2. Send this as the first message:
   > Continue the dashboard roadmap task from the HANDOVER.md in meeting-records

3. The new session reads this file, completes the bootstrap order, then executes Steps 1–6 above.

---

*Prepared: 3 July 2026 | Outgoing session: manual prep run (automation triggers broken) | Sources used this session: HR Systems Roadmap MASTER.xlsm (read-only, hr-projects, openpyxl via base64 decode), Granola (FA Catch-up 01/07, WFM Rostering Internal Review 30/06, Michael 1-1 Handover 02/07, Evo Implementation Meeting 01/07, Emergency Planning Meeting 01/07, HESA REF Meeting 01/07, HR Roadmap 26/06, FA Catch-up 26/06), briefing.json and tasks.json unavailable this session (work-inbox and command-centre not in session scope)*
