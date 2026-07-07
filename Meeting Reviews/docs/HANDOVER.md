# HANDOVER.md — Meeting Reviews

> Replace this file each session. Do not append.

**Session date:** 7 July 2026
**Written by:** Outgoing session
**Status:** Leave handover document created, iterated, approved by Kevin, and pushed to main. Kevin is now on pre-surgery leave prep. Surgery is Friday 10 July; he returns Monday 27 July.

---

## IF YOU ARE READING THIS COLD — START HERE

You have no memory of previous sessions. Do not guess context. Do not ask Kevin to recap. This document is your complete brief. Read it in full before doing anything.

You are working for **Kevin Lelitte**, Manager/Director HR Systems, University of Oxford. Kevin manages a team called the FA team (Kevin, Michael, Asta, James) and oversees all HR systems for the university. He operates through a network of GitHub repos that serve as his operational system — meeting prep, project tracking, dashboards, and tooling.

The governance model is defined in `CONSTITUTION.md` (in this repo, root level). Key principles:
- **Section 2:** A dispatch must be complete — the executor never makes architectural decisions. If you encounter something that requires a decision not covered here, stop and ask Kevin.
- **Section 5:** Conversation is temporary. Documentation is permanent. Update HANDOVER.md before this session ends.
- **Section 6:** Source of truth hierarchy: Kevin's current preferences > CONSTITUTION.md > AGENT_MODEL.md > CLAUDE.md > HANDOVER.md.
- **Section 10:** Effort level is Kevin's to set. Signal before beginning any high-effort task. Wait for Kevin to raise it.

**Approval gate (from `meeting-records/CLAUDE.md`):** Never push any meeting document without first showing it to Kevin in chat and receiving explicit approval. Show → approve → push. No exceptions. HANDOVER.md updates do not require approval before pushing.

**Branch rule:** Always push directly to main. Never leave work on a branch.

---

## Bootstrap order — do this before anything else

1. Read this file in full
2. Read `meeting-records/CLAUDE.md` — project identity, workflows, naming conventions, people, hard rules
3. Read `meeting-records/CONSTITUTION.md` — governing principles
4. Read `Meeting Reviews/docs/reference/meeting-prep-formats.md` — exact format for every meeting document type
5. Then read the CLAUDE.md of whichever repo the active task requires

Do not begin any task until steps 1–4 are complete.

---

## Kevin's leave status

| | |
|---|---|
| **Surgery date** | Friday 10 July 2026 |
| **Return date** | Monday 27 July 2026 |
| **Leave duration** | 10 Jul – 26 Jul inclusive (13 working days absent) |
| **Escalation chain** | Simon → Renu → Sarah |
| **Handover audience** | Athena, Marie, Simon, Sarah |

**Note for the first session after 27 July:** Kevin will be back. Begin by checking Granola for any meetings Kevin may have had or that his team attended during his absence. Check command-centre tasks.json for any updates. Check work-inbox briefing.json for inbox state. Then ask Kevin what he wants to pick up first.

---

## What was done in the session ending 7 July 2026

### Leave handover document — created, approved, pushed

**File:** `Meeting Reviews/Leave Handover — Jul 2026.md`
**Commit SHA:** e6c556831d01125b29f2035cd67715db1a93f1a6
**Status:** Pushed to main. Kevin approved before push.

The document contains:
1. **Team absence table** — 10 people (Kevin, Michael, Asta, James, Marie, Emma, Athena, Simon, Sarah, Julie Kimber), July dates, key overlap weeks identified
2. **8 active workstreams** in first-person voice (Kevin is the author):

| Workstream | Key coverage point |
|---|---|
| DTP1092 — Company 90 / College Staff in PXD | Crispin Poole leads; Nathan to raise OSM service request for Anna and Nick; test window TBC before 10 Jul |
| DTP1334 — H&S System (Cority, IRIS, DSE) | Revised deadline Sep/Oct agreed in principle; evaluation panel session 14 Jul (James and Chris attending); Rachel Midgley is Cority supplier contact |
| WFM / GLAM Rostering | Response from Cathy Hamer awaited (email sent 28 Jun); Michael to perform testing; no decisions needed during Kevin's absence |
| Non-Clinical Pay Uplift | Live; Michael and Michelle owners; Michael back 21 Jul — no action needed |
| Volunteering Absence Type | Oct/Nov rollout confirmed (option 2); email to Marie sent pre-leave; no action needed during absence |
| REF Attributes ESS | Nathan to raise ISM request; Kevin to test on return; no decisions needed |
| PFST / Sopra Steria | Kevin named SME; 8-week window from PFST meeting 9 Jul; Kevin picks up on return 27 Jul |
| Julie Training Checks | Wed 22 Jul is uncovered (Asta on leave, Julie on leave, Chris on leave); flagged to Marie to confirm cover |

### Absence calendar — produced and delivered

An HTML Gantt-style absence calendar was produced covering 6–31 July 2026 (20 working days, 10 people). Colour-coded per person, with a daily count row and heat scale. Delivered to Kevin as a file. Not committed to the repo (visual design — per CLAUDE.md hard rule, all mockups and visual designs are produced as Claude Artifacts or local files, never committed).

---

## Pre-leave actions — status as of 7 July 2026

These are Kevin's outstanding actions before surgery on Friday 10 July. They were identified during the leave prep session but may not all be complete. Check with Kevin if picking this up before 10 Jul.

| Action | Status | Notes |
|---|---|---|
| Email to James and Chris, cc Simon — PACS org structure | **Not yet sent (as of 7 Jul)** | Task them to complete H&S system impact assessment and report to Simon during Kevin's absence. Simon requested this on 29 Jun. |
| Email to Marie (cc Simon) — volunteering absence type | **Not yet sent (as of 7 Jul)** | Confirm Oct/Nov timeline, option 2, POG backlog. |
| Email to Rob (cc James) — task-per-incident requirement | **Not yet sent (as of 7 Jul)** | |
| Chase Nathan — REF ISM request raised? | **Not confirmed** | Kevin to confirm before 10 Jul |
| Julie training checks — Wed 22 Jul cover | **Flagged in handover** | Marie to confirm; Kevin to flag to Simon if unresolved |
| Job description — October start | **Noted** | Needs posting by end of July; Kevin back 27 Jul is tight — may need Simon to act if deadline can't move |

---

## Active task from previous session — Dashboard Roadmap (NOT YET DONE)

This task was approved on 3 July 2026 and was not executed before this session ran out of context. It is still outstanding and should be picked up when Kevin returns on 27 July.

### What this is

Create `command-centre/data/dashboard-roadmap.json` — a central JSON file tracking all active work across all ten dashboard repos. Full spec is reproduced below.

**Kevin approved this task on 3 July 2026. No effort level signal is required. Proceed directly to execution.**

### Execution steps

**Step 1** — Read every repo's CLAUDE.md (all ten dashboard repos) before touching any files.
Also read:
- `command-centre/data/tasks.json` — to match existing JSON schema conventions
- `work-inbox/data/briefing.json` — same reason

**Step 2** — Scan all ten repos for existing tracked work: HANDOVER.md, STATUS.md, any roadmap/backlog/tasks files, roadmap sections in CLAUDE.md, data/*.json tracking files. Record all finds before writing anything.

**Step 3** — Propose the schema to Kevin before writing. Show: proposed schema, full list of seed entries, automation trigger entry. Wait for explicit approval.

**Step 4** — Push `data/dashboard-roadmap.json` to `command-centre` main.

Minimum schema per entry:
```json
{
  "id": "DASH-001",
  "dashboard": "Meeting Dashboard",
  "repo": "begb0037admin/meeting-records",
  "title": "Brief title",
  "status": "blocked | in-progress | planned | complete",
  "description": "What this is and why it matters.",
  "blockers": ["Blocker 1"],
  "next_action": "The next concrete step.",
  "owner": "Kevin",
  "last_updated": "2026-07-07"
}
```

**First entry — always include this (DASH-001):**
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

**Step 5** — Update every repo's CLAUDE.md with the Dashboard Roadmap reference block and mockup rule (see 3 July HANDOVER.md for exact text). These additions do not require Kevin's approval before pushing.

**Step 6** — Update HANDOVER.md to mark this task complete.

**Automation trigger IDs (preserve — do not delete):**
- FA Catch-up: `trig_01QZYRrgfaUBgxPpuhVP719x`
- HR Roadmap: `trig_01QUr1UThQjgsA8SC32LRUnC`
- H&S Roadmap: `trig_01Qj16eCt3czyZGMTKrqeGAw`
- SK 1-1: `trig_01MahTwTm6YU8mE8RKyEFcT9`
- HR Managers Meeting: `trig_013GXDAQs5QUUkAhRgExjmm5`
- KPI Monthly: `trig_01JDNnv6ag6NzUVsoPA9L5fH`

---

## How to start the new session (post-27 July return)

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
   > Kevin is back from surgery. Read HANDOVER.md in meeting-records and brief me on what needs picking up.

3. The new session reads this file, completes the bootstrap order, then presents Kevin with a prioritised list: (a) any urgent items from his absence, (b) the dashboard roadmap task, (c) pre-leave actions that may still be open.

---

## Calendar context — July 2026

| Date | Event |
|---|---|
| Mon 7 Jul | Marie absent (until 17 Jul) |
| Thu 9 Jul | PFST meeting — Kevin attending |
| Fri 10 Jul | Kevin's surgery — absent from here until 27 Jul |
| Week 13–18 Jul | Most exposed week — 6 people absent simultaneously |
| Wed 22 Jul | Julie training checks gap day — Asta on leave, Julie on leave, Chris on leave |
| Thu 24 Jul | Julie returns |
| Mon 27 Jul | Kevin returns |

---

## Repo ecosystem reference

| Repo | Purpose |
|---|---|
| `meeting-records` | Meeting prep documents — FA catch-ups, roadmap briefs, 1-1s, H&S roadmap, KPI agenda |
| `hr-projects` | HR Systems project workspaces + live HR Systems Roadmap MASTER.xlsm (read-only) |
| `command-centre` | Central hub — tasks.json, dashboard-roadmap.json (pending creation) |
| `work-inbox` | Inbox dashboard and briefing.json |
| `hris-dashboard` | HRIS team operations view |
| `hr-fa-knowledge-base` | FA team knowledge base |
| `AG-FlexPoints` | AG FlexPoints data and tooling |
| `clockify` | Time tracking integration |
| `hris-change-requests` | Change request tracking |
| `hris-launcher` | Launch hub for HRIS tools |

---

*Prepared: 7 July 2026 | Sources used this session: Granola (multiple meetings), work-inbox/data/briefing.json, command-centre/data/tasks.json, hr-projects HR Systems Roadmap MASTER.xlsm (read-only), email screenshots provided by Kevin (PFST/Marie Cooksey, Simon Teams message re PACS, Simon email re volunteering, Marie email re Julie training checks)*
