# HANDOVER.md — Meeting Reviews

> Replace this file each session. Do not append.

**Session:** 3 July 2026
**Status:** Friday prep delivered. Both documents pushed to main.

---

## What was done this session

### 1. FA Team Catch-up — 03-07.md — pushed to main

7 items. Key focus areas:
- Asta: SSO Migration (179) VS2022 decision TODAY
- James: DTP1334 follow-up debrief (meeting was 2 July)
- James: PACS org structure H&S impact (Colleges L2→L3)
- James: H&S Dashboards (174_b) — Brian still blocking
- Michael: WFM handover before leave (Monday 6 July)
- Asta: REF/HESA UDF — Nathan ISM request and Kevin's test window
- All: Emergency cover Loops by end of today

Note: Michael won't be in the Friday meeting — the FA catch-up items for him are for the separate check-in, not the meeting itself.

### 2. HR Systems Roadmap — 03-07.md — pushed to main

Full roadmap brief for 10:00 meeting. Genuinely updated items:
- **ITS1004 WFM**: Resolution meeting 30 June — root cause established, GLAM stakeholders call planned
- **DTP1092 REF via ESS**: Approach confirmed 1 July (person-level UDF, 3 fields, ISM request)
- **Evo/PeopleXD**: Purchase confirmed 1 July — new item not yet on roadmap
- **PACS org structure**: Simon's ask from 29 June
- **July cover**: Emergency planning meeting 1 July

Unchanged since 26 June (noted explicitly in document):
- **136 DPIA**: Stage 7 still with Marie; deadline now PASSED
- **174_b H&S Dashboards**: Brian still blocking; no movement
- **179 SSO Migration**: Today is decision day; outcome from morning catch-up

Note on roadmap Excel: Kevin confirmed it has not been updated since the 26 June meeting. The document reflects Granola-sourced updates rather than roadmap changes.

---

## Automation status — STILL BROKEN

Six triggers were created on 1 July 2026 and all failed silently. Root cause: triggered sessions lack `mcp__github__*` and `mcp__Granola__*` tool access. The Claude_Code_Remote MCP server also needs re-authorisation (OAuth). Full detail in the previous HANDOVER.md (session 30 Jun – 1 Jul).

This session was triggered manually. The triggers are still enabled but still broken. Kevin asked about this during the session — it was not fixed this session.

**Steps still required (unchanged from previous HANDOVER):**
1. Re-authorise Claude_Code_Remote MCP (prerequisite)
2. Disable all six triggers while broken
3. Investigate MCP tool availability in triggered sessions
4. Fix trigger prompts
5. Test before re-enabling
6. Add verification/notification mechanism

Trigger IDs (from previous HANDOVER):
- FA Catch-up: `trig_01QZYRrgfaUBgxPpuhVP719x`
- HR Roadmap: `trig_01QUr1UThQjgsA8SC32LRUnC`
- H&S Roadmap: `trig_01Qj16eCt3czyZGMTKrqeGAw`
- SK 1-1: `trig_01MahTwTm6YU8mE8RKyEFcT9`
- HR Managers Meeting: `trig_013GXDAQs5QUUkAhRgExjmm5`
- KPI Monthly: `trig_01JDNnv6ag6NzUVsoPA9L5fH`

---

## Repo access issue this session

`begb0037admin/work-inbox` and `begb0037admin/command-centre` were not accessible — session scoped to `meeting-records` and `hr-projects` only. Kevin attempted to add them mid-session but this does not update live session permissions. Both documents note this in their sources footer. briefing.json and tasks.json were not used.

---

## Next session context

- Next Friday prep: 10 July (but Kevin is in surgery that day — no meeting)
- Next Wednesday FA catch-up: 8 July
- Kevin's surgery: 10 July. Two weeks recovery. Reduced/no availability from 10 July.
- Michael and Emma: absent w/c 6 July
- Marie: off 7–17 July
- From 13 July: Sarah is last manager standing
- **Key open items for next session:**
  - Chase outcome of SSO Migration decision (today's meeting)
  - Chase DPIA Stage 7 sign-off from Marie Cooksey
  - DTP1334: revised deadline and resourcing position — outcome from today's roadmap
  - REF/HESA UDF: has Nathan raised ISM request? Kevin to test before 10 July.
  - GLAM stakeholders call: set up after Kevin speaks with Simon and Marie
  - Evo: formal roadmap proposal for next roadmap meeting
  - Volunteering absence email to Marie (Oct/Nov timeline)
  - Loop handover docs: embedded in team chat today?

---

*Prepared: 3 July 2026 | Session: Manual prep (automation triggers broken)*
