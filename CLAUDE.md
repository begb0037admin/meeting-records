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
3. For meeting prep documents: check `Meeting Reviews/` for the most recent prep file

Do NOT ask Kevin for a recap. Navigate to the relevant subfolder.

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

## Hard Rules
- Never modify the HR Systems Roadmap — read only
- Never commit personal email content verbatim
- Always push prep documents directly to main
- Always update relevant HANDOVER.md at end of session
- File names MUST follow the Granola naming convention above

## Branch and Merge Protocol
Always push directly to main. If a branch must be used, merge it to main immediately upon completion — never leave files on a branch.
