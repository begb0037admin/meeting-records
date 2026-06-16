# Standing Agenda — Monthly Prep SOP

> Trigger phrase: **"prep standing agenda"**
> Run this the day before the meeting.

## Steps

### 1. Check KPI run is done
- Confirm this month's KPI run session file exists in `docs/sessions/`
- If not done, flag to Kevin before proceeding — KPI run must precede the standing agenda

### 2. Pull Command Centre tasks
- Fetch `begb0037admin/command-centre` → `data/tasks.json`
- Filter: `done != true`, exclude purely parked items unless relevant
- Identify Kevin's active items (these go in the left column of Slide 3)
- Identify H&S / BAU standing items (right column of Slide 3)

### 3. Draft session file
- Create `docs/sessions/YYYY-MM-DD-standing-agenda.md`
- Kevin's items: each gets **What it is**, **Status**, **Progress** from tasks.json actions log
- H&S section: Cority, IRIS, DSE, Odyssey, HWP standing items from Command Centre + H&S Excel backlog
- Team section: blank table (Michael, James, Asta fill their own)
- Standing verbal items: KPI review, flex points, any gates on Marie/James return
- Post-meeting actions log: blank table to fill in after

### 4. Generate PowerPoint
- Base template: `Monthly Standing Agenda April 2026.pptx` (same folder)
- Slide 1: Update month/year
- Slide 2 (Wins): Placeholder if no wins confirmed yet
- Slide 3 (Projects / Items in Progress):
  - Left column (Table 2): Kevin's items — title bold + description
  - Right column (Table 7): H&S + BAU items — title bold + description
  - Leave `[Team] — to be added` slots for Michael, James, Asta
- Save as `Monthly Standing Agenda [Month] [Year].pptx`
- Deliver file to Kevin for review

### 5. Kevin reviews + hands to team
- Kevin confirms items, adds anything missing
- Hands deck to team — they fill their own slots
- Team fill Slide 2 (Wins) and their Slide 3 rows

### 6. Post-meeting
- Return to session file, fill in **Post-Meeting Actions Log**
- Update any Command Centre tasks affected by decisions/actions
- Update `docs/HANDOVER.md` and `docs/STATUS.md`

## File naming
- Session file: `docs/sessions/YYYY-MM-DD-standing-agenda.md` (date = meeting date)
- Deck: `Monthly Standing Agenda [Month YYYY].pptx`

## Slide structure reference (April 2026 template)
| Slide | Content |
|-------|---------|
| 1 | Title + Month Year |
| 2 | Wins / Items Delivered |
| 3 | Projects / Items in Progress (left = Kevin's, right = H&S/BAU) |

## Data sources
| Source | What it feeds |
|--------|---------------|
| `begb0037admin/command-centre` → `data/tasks.json` | Kevin's In Progress items, H&S items |
| `KPI Monthly Standing Agenda/docs/sessions/` | Confirm KPI run done |
| H&S Workflow Overview Excel (local) | H&S backlog must-haves for awareness |
| April `.pptx` template | Slide layout, colours, fonts |
