# HANDOVER.md — Meeting Reviews

> Replace this file each session. Do not append.

**Session:** 3 July 2026 (continued — context compacted mid-session)
**Status:** Friday prep complete. Dashboard roadmap task approved, blocked on repo access. New session required.

---

## What was done this session

### 1. FA Team Catch-up — 03-07.md — pushed to main ✓

7 items. Key focus areas:
- Asta: SSO Migration (179) VS2022 decision TODAY
- James: DTP1334 follow-up debrief (meeting was 2 July)
- James: PACS org structure H&S impact (Colleges L2→L3)
- James: H&S Dashboards (174_b) — Brian still blocking
- Michael: WFM handover before leave (Monday 6 July)
- Asta: REF/HESA UDF — Nathan ISM request and Kevin's test window
- All: Emergency cover Loops by end of today

Note: Michael won't be in the Friday meeting — his items are for a separate check-in, not the 10:00 roadmap.

### 2. HR Systems Roadmap — 03-07.md — pushed to main ✓

Full roadmap brief for 10:00 meeting. Genuinely updated items:
- **ITS1004 WFM**: Resolution meeting 30 June — root cause established, GLAM stakeholders call planned
- **DTP1092 REF via ESS**: Approach confirmed 1 July (person-level UDF, 3 fields per appointment, ISM request)
- **Evo/PeopleXD**: Purchase confirmed 1 July — new item not yet on roadmap
- **PACS org structure**: Simon's ask from 29 June
- **July cover**: Emergency planning meeting 1 July

Unchanged since 26 June (noted explicitly in the document):
- **136 DPIA**: Stage 7 still with Marie Cooksey; deadline PASSED 30 June
- **174_b H&S Dashboards**: Brian still blocking; no movement
- **179 SSO Migration**: Decision point today; outcome from morning catch-up

Note: Kevin confirmed the roadmap Excel has not been updated since 26 June. The 03-07 document reflects Granola-sourced updates.

---

## Open task: Dashboard Roadmap — APPROVED, BLOCKED ON REPO ACCESS

### What this is

`dashboard-roadmap.json` is the **central roadmap for all active work across all ten dashboard repos**. It is not limited to meeting automation or any single workstream. Every ongoing item, planned feature, open fix, blocked task, or in-progress work across any of the ten repos belongs here. It is the cross-repo equivalent of what `HR Systems Roadmap MASTER.xlsm` is for the HR Systems team.

This was approved by Kevin on 3 July 2026. No effort level signal required — Kevin explicitly authorised it this session.

### Repos — full confirmed list

| Repo name | Dashboard name |
|---|---|
| `begb0037admin/command-centre` | Command Centre Dashboard |
| `begb0037admin/work-inbox` | Work Inbox Dashboard |
| `begb0037admin/meeting-records` | Meeting Dashboard |
| `begb0037admin/hr-projects` | HR Projects Dashboard |
| `begb0037admin/hris-dashboard` | HRIS Team Dashboard |
| `begb0037admin/hr-fa-knowledge-base` | Knowledge Base Dashboard |
| `begb0037admin/AG-FlexPoints` | AG FlexPoint Dashboard |
| `begb0037admin/clockify` | Clockify Dashboard |
| `begb0037admin/hris-change-requests` | Change Request Dashboard |
| `begb0037admin/hris-launcher` | HRIS Launcher Dashboard |

### Why it is blocked

Session scoped to `meeting-records` and `hr-projects` only. The remaining eight repos cannot be accessed mid-session. Kevin confirmed all repo names above. A new session with all ten repos added at launch is required.

### Exact steps for next session

**Step 1 — Bootstrap.**
Read in order:
1. This HANDOVER.md
2. `meeting-records/CLAUDE.md`
3. `meeting-records/CONSTITUTION.md`
4. `command-centre/CLAUDE.md` (if present)
5. `work-inbox/CLAUDE.md` (if present)

Do not begin work until bootstrap is complete.

**Step 2 — Scan all ten repos for existing tracked work.**

For each repo, check:
- `CLAUDE.md` — any roadmap sections, open items, or tracked work already present
- `HANDOVER.md` or `STATUS.md` — any open items or in-progress state
- Root directory — any file named `roadmap`, `tasks`, `backlog`, or similar
- `data/` directory (if present) — read `tasks.json`, `briefing.json`, or any JSON files that track work items
- Any other docs folder for open action lists

Record every find in full before writing anything. Do not skip any repo.

**Step 3 — Read schema references.**

Before designing the JSON structure, read:
- `command-centre/data/tasks.json`
- `work-inbox/data/briefing.json`

Match the style and structure conventions already in use. The schema for each entry in `dashboard-roadmap.json` must include at minimum:

```json
{
  "id": "string — short unique identifier e.g. DASH-001",
  "dashboard": "string — dashboard name from the table above",
  "repo": "string — repo name e.g. begb0037admin/hris-dashboard",
  "title": "string — brief title",
  "status": "string — blocked / in-progress / planned / complete",
  "description": "string — what this is and why it matters",
  "blockers": ["array of strings — current blockers, empty array if none"],
  "next_action": "string — the next concrete step",
  "owner": "string — Kevin or a team member",
  "last_updated": "YYYY-MM-DD"
}
```

Adjust the schema to match existing conventions if `tasks.json` or `briefing.json` use a different structure — consistency matters more than this template.

**Step 4 — Show Kevin the proposed schema and seed entries before pushing.**

Before writing any file:
1. Show Kevin the schema (confirm it matches existing conventions or propose adjustments)
2. Show Kevin the full list of seed entries derived from Step 2
3. Include the automation trigger entry below as the first Meeting Dashboard entry
4. Wait for Kevin's approval

Approval gate applies here. Do not push `dashboard-roadmap.json` without Kevin's explicit sign-off.

**Step 5 — Push `dashboard-roadmap.json` to `command-centre` main.**
Path: `data/dashboard-roadmap.json`

**Step 6 — Update every repo's CLAUDE.md.**

Add the following two additions to every repo in the table. Find the most appropriate section (Hard Rules, or a new section). Do not change any other content.

*Addition 1 — Dashboard roadmap reference:*
```
## Dashboard Roadmap
All roadmap items for this dashboard are tracked centrally at:
`begb0037admin/command-centre` → `data/dashboard-roadmap.json`

Do not maintain a local roadmap in this repo. All roadmap entries go to the central file.
```

*Addition 2 — Mockup rule (add to Hard Rules or equivalent):*
```
- Mockups and visual prototypes always use Claude Artifacts. Never create HTML files for mockups. Everything visual is presented as a live Artifact so it can be iterated in-session.
```

CLAUDE.md additions are mechanical and do not require Kevin's approval before pushing, but surface any unexpected content found during Step 2 before writing.

**Step 7 — Update this HANDOVER.md** to reflect completion and remove the blocked task.

---

## Automation status — STILL BROKEN

Six CronCreate triggers were created 1 July 2026. All fail silently. Root cause: triggered sessions only have default tools — no `mcp__github__*` or `mcp__Granola__*`. The Claude_Code_Remote MCP server also needs re-authorisation (OAuth).

**Trigger IDs (preserve — do not delete):**
- FA Catch-up: `trig_01QZYRrgfaUBgxPpuhVP719x`
- HR Roadmap: `trig_01QUr1UThQjgsA8SC32LRUnC`
- H&S Roadmap: `trig_01Qj16eCt3czyZGMTKrqeGAw`
- SK 1-1: `trig_01MahTwTm6YU8mE8RKyEFcT9`
- HR Managers Meeting: `trig_013GXDAQs5QUUkAhRgExjmm5`
- KPI Monthly: `trig_01JDNnv6ag6NzUVsoPA9L5fH`

**Fix sequence (not yet actioned):**
1. Re-authorise Claude_Code_Remote MCP: claude.ai → Settings → Connectors
2. Disable all six triggers while broken (avoid silent failures accumulating)
3. Investigate MCP tool access in triggered sessions
4. Fix trigger prompts or establish a pathway to get MCP tools into triggered sessions
5. Test with a single trigger before re-enabling all six
6. Add a notification/verification step so failures are surfaced

This will be tracked as an entry in `dashboard-roadmap.json` (Meeting Dashboard, status: blocked).

---

## How to start the new session

1. Add all ten repos to the session before sending the first message (list above)
2. First message: *"Continue the dashboard roadmap task from the HANDOVER.md in meeting-records"*
3. The new session reads this file, bootstraps, and executes Steps 1–7
4. No recap needed — this HANDOVER.md is the complete brief

---

## Upcoming context — relevant to all sessions

| Date | Event |
|---|---|
| Fri 3 Jul | HR Roadmap 10:00 — today. SSO decision. DPIA chase. DTP1334 revised deadline. |
| Mon 6 Jul | Michael and Emma absent |
| Mon 7 Jul | Marie absent (until 17 Jul) |
| Fri 10 Jul | Kevin's surgery. Approximately two weeks recovery. |
| Sun 13 Jul | Sarah only manager remaining |

**Open items from today's roadmap meeting — check outcomes in next session:**
- SSO Migration (179): did VS2022 licensing come through? Proceed or park formally?
- DPIA Stage 7 (136): any response from Marie Cooksey?
- DTP1334: revised deadline agreed (Sep proposed)? Resourcing position formally noted?
- REF/HESA UDF (DTP1092): Nathan's ISM request raised? Kevin's test window confirmed?
- GLAM stakeholders call (ITS1004): date set?
- Evo: formal roadmap proposal agreed for next roadmap meeting?
- Volunteering absence email to Marie (Oct/Nov timeline) — sent?
- Loop handover docs — collected and embedded in HR Systems Management Team chat?

---

*Prepared: 3 July 2026 | Session: Manual prep (automation triggers broken) | Sources: HR Systems Roadmap MASTER.xlsm (read-only, hr-projects), Granola (FA Catch-up 01/07, WFM Rostering Internal Review 30/06, Michael 1-1 Handover 02/07, Evo Implementation 01/07, Emergency Planning 01/07, HESA REF 01/07, HR Roadmap 26/06, FA Catch-up 26/06), briefing.json and tasks.json unavailable this session*
