# Monthly Standing Agenda — Claude Bootstrap
## Identity
- **Project:** Monthly Standing Agenda meeting
- **Purpose:** Prep, facilitation, and follow-up for the Monthly Standing Agenda meeting. Split out from the former combined "KPI Monthly Standing Agenda" area, 21 Aug 2026, per Kevin's instruction that these are two separate meetings — format and pipeline kept intact, area split only.
- **Owner:** Kevin Lelitte — HR Systems Manager/Director
- **Status:** Active
- **Repository:** https://github.com/begb0037admin/meeting-records/tree/main/Standing%20Agenda%20-%20Handover

## Bootstrap Order
1. This file
2. `docs/STATUS.md`
3. `docs/HANDOVER.md`

## Trigger Phrases
| Phrase | Action |
|--------|--------|
| "prep standing agenda" | Follow `docs/STANDING_AGENDA_SOP.md` exactly |

## Where Things Live
| What | Where |
|---|---|
| Current state | `docs/STATUS.md` |
| Latest handover | `docs/HANDOVER.md` |
| Standing agenda SOP | `docs/STANDING_AGENDA_SOP.md` |
| Meeting agendas + notes | `docs/sessions/` (YYYY-MM-DD-standing-agenda.md) |
| Slide template | `Monthly Standing Agenda April 2026.pptx` (style reference only — March/April 2026 are the true style templates per Lauren's `AGENT.md`; the real live deck is local OneDrive `People Department - HR Systems - Monthly Standing Agenda\`) |

## Monthly Rhythm
| Activity | When | Owner |
|---|---|---|
| Standing agenda prep | Day before meeting | Lauren (trigger: "prep standing agenda") |
| Standing agenda meeting | Monthly | Kevin chairs |
| Post-meeting follow-up | Same day | Kevin + Lauren |

## Data Sources for Prep
| Source | Used for |
|--------|----------|
| `begb0037admin/command-centre` → `data/tasks.json` | Kevin's In Progress items, H&S items |
| `begb0037admin/work-inbox` | Cross-reference, read-only |
| Granola meetings | Cross-reference — access gap open, see Known Gaps in STATUS.md |
| `Monthly Standing Agenda April 2026.pptx` | Slide template (layout, colours, fonts) |
| H&S Workflow Overview Excel | H&S backlog must-haves |

## Hard Rules
- KPI run must be complete before standing agenda prep (real cross-area dependency — see `KPI Presentation - Handover`)
- Always generate the `.pptx` from the April 2026 template — never start from scratch
- Style rule: short, bold, single-line titles only — never paragraph descriptions (March/April 2026 style, not May/June/July's drift)
- Kevin's items go in the left column (Slide 3), H&S/BAU in the right column
- Team fill their own slots — never pre-fill team items
- Post-meeting: always update the session file actions log and affected Command Centre tasks
- **Never push any meeting document without first showing the content to Kevin in chat and receiving his explicit approval. Show → approve → push. No exceptions.**

## Last updated
2026-08-21 (area split from combined KPI Monthly Standing Agenda)
