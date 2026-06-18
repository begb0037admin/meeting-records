# CLAUDE.md — meeting-records
> AI bootstrap entry point. Read this first.
> Keep this file under 200 lines. Push details to linked docs.

## Identity
- **Project:** Meeting Records — container repo for Kevin's recurring meeting prep and records
- **Purpose:** Stores prep documents, agendas, notes, and handover materials for Kevin's recurring meetings and team management activities.
- **Owner:** Kevin Lelitte, Manager/Director HR Systems, University of Oxford
- **Status:** Active
- **Repo:** https://github.com/begb0037admin/meeting-records
- **Last updated:** 2026-06-18

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

| Meeting | File name format | Example |
|---|---|---|
| FA Team morning catch-up | `FA Team Catch-up — DD-MM.md` | `FA Team Catch-up — 19-06.md` |
| HR Systems Roadmap meeting | `HR Systems Roadmap — DD-MM.md` | `HR Systems Roadmap — 19-06.md` |
| KPI Monthly Standing Agenda | `KPI Standing Agenda — MMM YYYY.md` | `KPI Standing Agenda — Jun 2026.md` |
| Team 1-1 | `1-1 [Name] — DD-MM.md` | `1-1 Michael — 15-06.md` |

This matches how Kevin names meetings in Granola — files and Granola meetings are always in sync and easy to cross-reference.

## Meeting Prep Workflow (Roadmap Fridays)
Every Friday before the 10:00 HR Systems Roadmap meeting:
1. Read live roadmap from `begb0037admin/hr-projects/HR Systems Roadmap/HR Systems Roadmap MASTER.xlsm` (read-only, openpyxl via base64 decode)
2. Check Granola for recent FA team catch-ups (Kevin, Michael, Asta, James)
3. Check `begb0037admin/work-inbox/data/briefing.json` for inbox updates
4. Check `begb0037admin/command-centre/data/tasks.json` for active tasks
5. Produce two documents in `Meeting Reviews/`:
   - `FA Team Catch-up — DD-MM.md` — morning catch-up agenda before the roadmap meeting
   - `HR Systems Roadmap — DD-MM.md` — speaking brief for 10:00 roadmap meeting

## Hard Rules
- Never modify the HR Systems Roadmap — read only
- Never commit personal email content verbatim
- Always push prep documents directly to main
- Always update relevant HANDOVER.md at end of session
- File names MUST follow the Granola naming convention above

## Branch and Merge Protocol
Every time files are pushed to a branch, immediately ask Kevin:
> "I've pushed to a branch — are you happy with this? Shall I merge to main now?"

Recurring triggers throughout every session:
- **On every push** — ask immediately, without waiting
- **When Kevin signals satisfaction** — phrases like "good", "happy with that", "that's great", "okay", "done", "let's move on" — check if anything is on a branch and ask to merge
- **When the topic shifts** — before starting a new subject, check if anything is on a branch

Never leave files on a branch without Kevin's explicit sign-off.
