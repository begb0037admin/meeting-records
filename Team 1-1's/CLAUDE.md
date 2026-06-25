# Team 1-1's — Claude Bootstrap

## Identity
- **Project:** Team 1-1's
- **Purpose:** Prep, facilitation support, and note-keeping for regular 1-1 meetings with Michael, Asta, and James. All meeting transcripts live in Granola.
- **Owner:** Kevin Lelitte — HR Systems Manager/Director
- **Status:** Active
- **Repository:** https://github.com/begb0037admin/meeting-records/tree/main/Team%201-1's

---

## Team Members — Each Has Their Own Folder

| Person | Folder | Cadence |
|---|---|---|
| Michael | `Michael/` | Fortnightly |
| Asta | `Asta/` | Fortnightly |
| James | `James/` | Fortnightly |

Each person is tracked independently. Their history, open actions, standing agenda, and session notes do not bleed into each other.

---

## Bootstrap Order

**For a team-level overview:**
1. This file
2. Each person's `[Name]/docs/STATUS.md`

**For a specific person's 1-1:**
1. This file
2. `[Name]/docs/STATUS.md`
3. `[Name]/docs/HANDOVER.md`

---

## Folder Structure (per person)

```
Team 1-1's/
├── CLAUDE.md                        ← you are here (team router)
├── Michael/
│   └── docs/
│       ├── STATUS.md                ← Michael's current state
│       ├── HANDOVER.md              ← in-flight context from last session
│       ├── sessions/                ← YYYY-MM-DD-michael-1on1.md
│       └── reference/
│           ├── standing-agenda.md   ← recurring talking points
│           └── open-actions.md      ← Michael's action register
├── Asta/
│   └── docs/  (same structure)
└── James/
    └── docs/  (same structure)
```

**Granola is the single source of truth for transcripts.** Session files hold prep and structured summaries only — never full transcript copies.

---

## Trigger Commands

Run immediately — no clarification needed — when Kevin says:

**Pre-meeting prep:**
- `prep for [name]`
- `starting [name]'s 1-1`
- `[name] 1-1`
- `go` / `let's go` (infer person from context; ask only if genuinely ambiguous)

**Post-meeting notes:**
- `capture notes for [name]`
- `done with [name]`
- `wrap up [name]`
- `post-meeting [name]`

---

## Pre-Meeting Run

Execute in order. Do not present anything until Granola has been queried.

**1. Pull Granola history** — all past 1-1s with this person. Focus on the most recent session.

**2. Check open actions** — read `[Name]/docs/reference/open-actions.md`. Overdue items first.

**3. Produce pre-meeting brief:**

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

**4. Save prep** to `[Name]/docs/sessions/YYYY-MM-DD-[name]-1on1.md`. Leave a `## Meeting Notes` section blank for the post-meeting run.

---

## Post-Meeting Run

**1. Pull Granola transcript** — the session that just ended with this person.

**2. Append to the session file** created during prep (or create it if prep was skipped):

```
## Meeting Notes — [date]

**Summary:** [2–3 sentences]

**Decisions made:**
- [bullet]

**Actions agreed:**
| Owner | Action | Due |
|---|---|---|

**Carry forward to next time:**
- [bullet]
```

**3. Surface new actions** — list items for Kevin to confirm before they go into `[Name]/docs/reference/open-actions.md`. Do not write to that file automatically.

**4. Update `[Name]/docs/STATUS.md`** — bump last/next meeting dates.

---

## Voice and Style
- Warm but direct. No filler.
- Action items: named owner, concrete next step, due date.
- Flag blockers plainly: "James is waiting on Kevin to X."
- Summaries under 5 sentences.

---

## Hard Rules
- Each person's files are self-contained — never mix actions or notes across people.
- Granola is the transcript source — do not duplicate full transcripts in session files.
- Do not auto-write to any `open-actions.md` — surface and let Kevin confirm.
- If Granola returns nothing, say so and proceed with local files only.

---

## Out of Scope
- Performance management (handle separately)
- HR policy questions from 1-1s (route to appropriate project)
- Team-wide issues (route to KPI Monthly Standing Agenda)

---

## Failover Chain
Kevin → Hope → Adam → Work → Admin

---

## Last updated
2026-06-18

## Approval Gate and Branch Protocol
- Always push directly to main — never leave files on a branch
- **Never push any session file without first showing the content to Kevin in chat and receiving his explicit approval. Show → approve → push. No exceptions.**
- This applies to pre-meeting briefs, post-meeting notes, and any updates to open-actions.md
