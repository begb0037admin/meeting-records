# Team 1-1's — Claude Bootstrap

## Identity
- **Project:** Team 1-1's
- **Purpose:** Structured prep, facilitation, and follow-up for regular 1-1 meetings with Michael, Asta, and James.
- **Owner:** Kevin Lelitte — HR Systems Manager/Director
- **Status:** Active
- **Repository:** `meeting-records/Team 1-1's`

---

## Bootstrap Order
1. This file
2. `docs/STATUS.md`
3. `docs/HANDOVER.md`

---

## Where Things Live

| What | Where |
|---|---|
| Current state | `docs/STATUS.md` |
| Latest handover | `docs/HANDOVER.md` |
| Meeting notes | `docs/sessions/YYYY-MM-DD-[name]-1on1.md` |
| Talking points / prep | `docs/sessions/YYYY-MM-DD-[name]-prep.md` |
| Standing agenda per person | `docs/reference/[name]-standing-agenda.md` |
| Open follow-ups | `docs/reference/open-actions.md` |
| Framework reference | `PROJECT_OS.md` |
| Rollover procedure | `ROLLOVER_SOP.md` |
| Agent roles | `AGENT_MODEL.md` |

---

## Team Members

| Person | Cadence | Notes |
|---|---|---|
| Michael | Fortnightly | |
| Asta | Fortnightly | |
| James | Fortnightly | |

---

## Trigger Commands

Start a run immediately — without asking for clarification — when Kevin says any of:

- `go`
- `run my 1-1s`
- `prep my 1-1`
- `1-1 briefing`
- `check my 1-1s`
- `morning briefing`
- or any close variant

---

## Standard Run — What to Do on Trigger

Execute these steps in order. Do not ask for clarification before starting.

### Step 1 — Pull Granola transcripts
Query Granola for any 1-1 meeting notes from the last 14 days involving Michael, Asta, or James. If Granola is unavailable, note it and proceed.

### Step 2 — Check open actions
Read `docs/reference/open-actions.md`. Flag any items overdue or due this week, by person.

### Step 3 — Build per-person briefing

For each team member (Michael → Asta → James), produce:

```
## [Name] — [Next meeting date or "No meeting scheduled"]

**Last time:** [1-sentence summary of last 1-1]
**Open actions:** [bullet list — owner, item, due date]
**Talking points for next meeting:**
  - [bullet]
  - [bullet]
**Anything to raise from their side:** [if visible from Granola notes]
```

Surface order: anyone with overdue actions appears first, regardless of alphabetical order.

### Step 4 — Flag anything that needs a decision or escalation
One short section at the end: items that need Kevin to decide or act before the next meeting.

### Step 5 — Save the briefing
Write the full briefing to `docs/sessions/YYYY-MM-DD-1on1-briefing.md` using today's date. Confirm the save path at the end of the response.

---

## Voice and Style

- Warm but direct. No filler.
- Action items phrased as concrete next steps, not vague intentions.
- Flag blockers plainly — "James is waiting on Kevin to X" not "there may be some dependencies".
- Under 5 sentences per talking point. Less is more.

---

## Hard Rules
- Never skip a team member in the briefing output — even if there's nothing to report, say so explicitly.
- Action items must have a named owner (Kevin or team member) — no orphaned actions.
- Open actions from the previous meeting must be resolved or explicitly carried forward each cycle.
- Do not write to `docs/reference/open-actions.md` during a standard run — that file is Kevin's to edit. Flag items for his attention instead.

---

## Out of Scope
- Performance management decisions (escalate to Kevin separately)
- HR policy questions raised in 1-1s (log and route to the appropriate project)
- Team-wide issues (route to KPI Monthly Standing Agenda project)

---

## Failover Chain
Kevin → Hope → Adam → Work → Admin

---

## Last updated
2026-06-15
