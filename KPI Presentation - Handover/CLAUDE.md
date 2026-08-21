# KPI Presentation — Claude Bootstrap
## Identity
- **Project:** KPI Presentation (monthly KPI run)
- **Purpose:** Producing, reviewing, and distributing HR KPI outputs for the monthly team meeting to Michael O'Sullivan. Split out from the former combined "KPI Monthly Standing Agenda" area, 21 Aug 2026, per Kevin's instruction that these are two separate meetings — format and pipeline kept intact, area split only.
- **Owner:** Kevin Lelitte — HR Systems Manager/Director
- **Status:** Active
- **Repository:** https://github.com/begb0037admin/meeting-records/tree/main/KPI%20Presentation%20-%20Handover

## Bootstrap Order
1. This file
2. `docs/STATUS.md`
3. `docs/HANDOVER.md`

## Trigger Phrases
| Phrase | Action |
|--------|--------|
| "prep KPI run" / "run KPIs" | Follow `docs/KPI_RUN_SOP.md` exactly |

## Where Things Live
| What | Where |
|---|---|
| Current state | `docs/STATUS.md` |
| Latest handover | `docs/HANDOVER.md` |
| KPI run SOP | `docs/KPI_RUN_SOP.md` |
| KPI definitions + sources | `docs/reference/kpi-definitions.md` |
| Generator script | `tools/speaking-briefs/build_kpi_presentation.py` (engineered by Drew) |
| Real source data | Local OneDrive, `Functional Analysis Team Monthly Statistics\<YYYY>\<MM Mon>\Source Data\` — NOT this repo |

## Monthly Rhythm
| Activity | When | Owner |
|---|---|---|
| KPI run | Before standing agenda | Kevin + Lauren (co-work) |

## Data Sources for Prep
| Source | Used for |
|--------|----------|
| Local OneDrive `Functional Analysis Team Monthly Statistics\` | Real KPI source Excel + H&S Word doc, per month |
| `begb0037admin/command-centre` → `data/tasks.json` | Cross-reference only |

## Hard Rules
- KPI run must be complete before standing agenda prep (this is a real cross-area dependency — see `Standing Agenda - Handover`)
- Self-test gate is mandatory before any monthly build is trusted — see Lauren's `AGENT.md`, "Standing responsibility: Monthly KPI Presentation build"
- Never automate/schedule this build — Kevin explicitly declined a cron trigger, 7 Aug 2026
- KPI definitions not yet documented — populate `docs/reference/kpi-definitions.md` with Kevin
- **Never push any KPI output without first showing the content to Kevin in chat and receiving his explicit approval. Show → approve → push. No exceptions.**

## Last updated
2026-08-21 (area split from combined KPI Monthly Standing Agenda)
