# KPI Monthly Standing Agenda — Claude Bootstrap
## Identity
- **Project:** KPI Monthly Standing Agenda
- **Purpose:** Covers two linked monthly rhythms: (1) Monthly Standing Agenda meeting — prep, facilitation, follow-up; and (2) Monthly KPI run — producing, reviewing, and distributing HR KPI outputs.
- **Owner:** Kevin Lelitte — HR Systems Manager/Director
- **Status:** Active
- **Repository:** https://github.com/begb0037admin/meeting-records/tree/main/KPI%20Monthly%20Standing%20Agenda

## Bootstrap Order
1. This file
2. `docs/STATUS.md`
3. `docs/HANDOVER.md`

## Trigger Phrases
| Phrase | Action |
|--------|--------|
| "prep standing agenda" | Follow `docs/STANDING_AGENDA_SOP.md` exactly |
| "prep KPI run" / "run KPIs" | Follow `docs/KPI_RUN_SOP.md` exactly |

## Where Things Live
| What | Where |
|---|---|
| Current state | `docs/STATUS.md` |
| Latest handover | `docs/HANDOVER.md` |
| Standing agenda SOP | `docs/STANDING_AGENDA_SOP.md` |
| KPI run SOP | `docs/KPI_RUN_SOP.md` |
| Meeting agendas + notes | `docs/sessions/` (YYYY-MM-DD-standing-agenda.md) |
| KPI run session files | `docs/sessions/` (YYYY-MM-KPI-run.md) |
| KPI definitions + sources | `docs/reference/kpi-definitions.md` |
| Slide template | `Monthly Standing Agenda April 2026.pptx` |

## Monthly Rhythm
| Activity | When | Owner |
|---|---|---|
| KPI run | Before standing agenda | Kevin + Claude (co-work) |
| Standing agenda prep | Day before meeting | Claude (trigger: "prep standing agenda") |
| Standing agenda meeting | Monthly | Kevin chairs |
| Post-meeting follow-up | Same day | Kevin + Claude |

## Data Sources for Prep
| Source | Used for |
|--------|----------|
| `begb0037admin/command-centre` → `data/tasks.json` | Kevin's In Progress items, H&S items |
| `Monthly Standing Agenda April 2026.pptx` | Slide template (layout, colours, fonts) |
| H&S Workflow Overview Excel | H&S backlog must-haves |

## Hard Rules
- KPI run must be complete before standing agenda prep
- Always generate the `.pptx` from the April template — never start from scratch
- Kevin's items go in the left column (Slide 3), H&S/BAU in the right column
- Team fill their own slots — never pre-fill team items
- Post-meeting: always update the session file actions log and affected Command Centre tasks
- KPI definitions not yet documented — populate `docs/reference/kpi-definitions.md` with Kevin

## Approval Gate and Branch Protocol
- Always push directly to main — never leave files on a branch
- **Never push any meeting document or KPI output without first showing the content to Kevin in chat and receiving his explicit approval. Show → approve → push. No exceptions.**

## Last updated
2026-07-31
