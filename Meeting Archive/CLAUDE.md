# Meeting Archive — Claude Bootstrap
## Identity
- **Project:** Meeting Archive
- **Purpose:** Historical archive of past meeting notes and Granola exports. Read-only reference. Active meeting prep lives in Meeting Reviews.
- **Owner:** Kevin Lelitte — HR Systems Manager/Director
- **Status:** Active (ongoing archive)
- **Repository:** https://github.com/begb0037admin/meeting-records/tree/main/Meeting%20Archive
## Bootstrap Order
1. This file
2. docs/STATUS.md
3. docs/HANDOVER.md
## Where Things Live
| What | Where |
|---|---|
| Archived meeting notes | docs/sessions/ (YYYY-MM-DD-meeting-name.md) |
| Active meeting reviews | `Meeting Reviews/` (sibling folder) |
| Current state | docs/STATUS.md |
| Latest handover | docs/HANDOVER.md |
| Framework reference | PROJECT_OS.md |
| Agent roles | AGENT_MODEL.md |
| Rollover procedure | ROLLOVER_SOP.md |
## Hard Rules
- Append only — do not delete or overwrite archived entries
- Active meeting prep belongs in Meeting Reviews, not here
## Out of Scope
- Active meeting preparation (see Meeting Reviews/)
- Project decisions (see individual project folders)
## Failover Chain
Kevin -> Hope -> Adam -> Work -> Admin
## Last updated
2026-06-18

## Branch and Merge Protocol
Every time files are pushed to a branch, immediately ask Kevin:
> "I've pushed to a branch — are you happy with this? Shall I merge to main now?"

Recurring triggers throughout every session:
- **On every push** — ask immediately, without waiting
- **When Kevin signals satisfaction** — phrases like "good", "happy with that", "that's great", "okay", "done", "let's move on" — check if anything is on a branch and ask to merge
- **When the topic shifts** — before starting a new subject, check if anything is on a branch

Never leave files on a branch without Kevin's explicit sign-off.
