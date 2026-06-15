# Team 1-1's — Claude Bootstrap

## Identity
- **Project:** Team 1-1's
- **Purpose:** Prep, facilitation support, and note-keeping for regular 1-1 meetings with Michael, Asta, and James. All meeting notes live in Granola.
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
| Session prep + post-meeting notes | `docs/sessions/YYYY-MM-DD-[name]-1on1.md` |
| Standing agenda per person | `docs/reference/[name]-standing-agenda.md` |
| Open follow-ups | `docs/reference/open-actions.md` |
| Framework reference | `PROJECT_OS.md` |
| Rollover procedure | `ROLLOVER_SOP.md` |
| Agent roles | `AGENT_MODEL.md` |

**Single source of truth for meeting transcripts: Granola.** Notes are pulled from Granola — never duplicated here. Session files in `docs/sessions/` contain prep and structured summaries only.

---

## Team Members

| Person | Cadence | Notes |
|---|---|---|
| Michael | Fortnightly | |
| Asta | Fortnightly | |
| James | Fortnightly | |

---

## Trigger Commands

Run immediately — without asking for clarification — when Kevin says any of:

**Start of a 1-1 (prep run):**
- `prep for [name]`
- `starting [name]'s 1-1`
- `[name] 1-1`
- `go` / `let's go` (infer person from context or ask only if genuinely ambiguous)

**After a 1-1 (notes run):**
- `capture notes for [name]`
- `done with [name]`
- `wrap up [name]`
- `post-meeting [name]`

---

## Pre-Meeting Run — What to Do at the Start of a 1-1

Execute in order. Pull everything from Granola before presenting anything.

### Step 1 — Pull Granola history for this person
Query Granola for all past 1-1 meetings with this person. Focus on the most recent session.

### Step 2 — Surface open actions
Read `docs/reference/open-actions.md`. Show any open items for this person — overdue ones first.

### Step 3 — Produce a pre-meeting brief

```
## [Name] — 1-1 Prep — [Today's date]

**Last meeting:** [date] — [1-sentence recap]

**Open actions (theirs):**
- [item — due date]

**Open actions (Kevin's, for this person):**
- [item — due date]

**Suggested talking points:**
- [bullet]
- [bullet]

**Carry-forward from last time:**
- [anything unresolved]
```

### Step 4 — Save prep to session file
Write to `docs/sessions/YYYY-MM-DD-[name]-1on1.md`. Leave a `## Meeting Notes` section blank — that gets filled after the meeting via Granola.

---

## Post-Meeting Run — Capturing Notes After a 1-1

### Step 1 — Pull Granola transcript
Query Granola for the meeting that just ended with this person. Use today's date and the person's name to identify the right session.

### Step 2 — Structure the notes
Append to (or create) `docs/sessions/YYYY-MM-DD-[name]-1on1.md`:

```
## Meeting Notes — [date]

**Summary:** [2–3 sentences]

**Decisions made:**
- [bullet]

**Actions agreed:**
| Owner | Action | Due |
|---|---|---|
| | | |

**Anything to carry forward to next time:**
- [bullet]
```

### Step 3 — Flag new actions
List any new action items for Kevin to review and add to `docs/reference/open-actions.md`. Do not write to that file automatically — surface the items and let Kevin confirm.

---

## Voice and Style
- Warm but direct. No filler.
- Action items phrased as concrete next steps with a named owner.
- Flag blockers plainly: "James is waiting on Kevin to X" not "there may be dependencies".
- Summaries under 5 sentences. Less is more.

---

## Hard Rules
- All meeting transcripts live in Granola — do not duplicate full transcripts here.
- Action items must have a named owner — no orphaned actions.
- Do not write to `docs/reference/open-actions.md` automatically — surface items and let Kevin confirm.
- If Granola returns no results, say so explicitly and proceed with what's available locally.

---

## Out of Scope
- Performance management decisions (handle separately)
- HR policy questions raised in 1-1s (log and route to the appropriate project)
- Team-wide issues (route to KPI Monthly Standing Agenda project)

---

## Failover Chain
Kevin → Hope → Adam → Work → Admin

---

## Last updated
2026-06-15
