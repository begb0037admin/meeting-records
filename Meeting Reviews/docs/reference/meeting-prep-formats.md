# Meeting Prep Formats — Reference

> Read this before writing any meeting prep document — scheduled or ad hoc.
> Defined formats are fixed. For a meeting type not listed here, use the closest format as a base,
> note the adaptation in the document footer, and add the new format here after Kevin approves it.

---

## FA Team Catch-up — DD-MM.md

```
# FA Team Catch-up — DD/MM

**Date:** [Weekday DD Month YYYY]
**Purpose:** [e.g. Morning FA team check-in before HR Systems Roadmap 10:00]
**Time needed:** ~25 minutes

---

## Items to raise

---

### 1. [Title — person responsible or topic]
**Ask:** [One or two sentences: what Kevin needs to know or confirm in this meeting.]

**Background:** [2–5 sentences: what is this, why it matters, current state, any blockers or dependencies.]

---

[Repeat for each item, numbered sequentially]

---

## Note for Kevin

Priority actions after this call:
- [Action 1]
- [Action 2]

---

*Prepared: DD Month YYYY | Sources: [Granola references, briefing.json, tasks.json]*
```

**Rules:**
- Numbered items, each with **Ask:** and **Background:** exactly as shown
- Ask is what Kevin needs to raise or confirm in the meeting
- Background is context for Kevin — he runs the conversation himself
- Note for Kevin lists Kevin's own post-meeting actions, not team actions
- Time needed is always ~25 minutes unless Kevin specifies otherwise

---

## HR Systems Roadmap — DD-MM.md

```
# HR Systems Roadmap — DD/MM

**Date:** [Weekday DD Month YYYY, HH:MM]
**Follow-on from:** [Previous meeting date]
**Prepared from:** [Data sources]

---

## 1. Headline position

[2–3 sentence paragraph: key themes, deadlines landing today, new items.]

---

## 2. Team items — status by item

---

**[ID] — [Project Name]**
Lead: [Name] | Team: [Names] | Deadline: [Date — flag PASSED or TODAY with ⚠️]

**Current position:** [2–4 sentences on where things actually stand.]

**What to say:** *"[Scripted text Kevin can read verbatim. First person. Includes any asks or proposed decisions.]"*

---

[Repeat for each roadmap item]

## 3. New this week

**[Item title]**
[Short paragraph.]

**What to say:** *"[Scripted text.]"*

---

## 4. Concerns and watching brief

| Item | Concern | Action |
|---|---|---|
| **[ID Name]** | [Risk] | [Kevin's action] |

---

## 5. Items complete — no update needed

- [ID] — [Name]: [Brief status and date]

---

*Prepared: DD Month YYYY | Sources: [List]*
```

**Rules:**
- What to say text is always italicised and in quotes — it is a speaking script
- Deadlines that have passed get ⚠️ PASSED; deadlines falling today get TODAY ⚠️
- Section 4 is always a table, never prose
- Section 5 is a bullet list — no elaboration needed

---

## 1-1 Simon — DD-MM.md

```
# 1-1 Simon — DD/MM

**Date:** [Weekday DD Month YYYY]
**Meeting:** Kevin / Simon fortnightly 1-1
**Last 1-1:** [DD Month YYYY]

---

## Kevin's health and working pattern

[Only include when Kevin has a current health/availability situation relevant to Simon.
Remove entirely when Kevin is at full capacity.]

---

## Priority items for Simon

### 1. [Item title]

[2–3 sentences of context.]

- **Ask of Simon:** [Specific ask or decision needed from Simon.]

---

[Repeat, numbered sequentially]

---

## Items Kevin owes Simon

- **[Item]** — [Context and current position]

---

## For Simon's awareness — [period]

| Item | Risk | Date |
|---|---|---|
| [Item] | [Risk] | [When] |

---

*Prepared: DD Month YYYY | Sources: [List]*
```

**Rules:**
- Every priority item must have a clear **Ask of Simon** — specific, not just context
- Items Kevin owes Simon = commitments Kevin has not yet delivered
- The awareness table is forward-looking risks Simon should know about
- Health section only included when relevant

---

## Team 1-1 — Michael, Asta, James

Session files live in `Team 1-1's/[Name]/docs/sessions/YYYY-MM-DD-[name]-1on1.md`.

**Pre-meeting brief (written before the 1-1):**

```
# [Name] — 1-1 — [DD Month YYYY]

## Pre-Meeting Prep

**Last formal 1-1:** [date] — [1-sentence recap, or "No recent session in Granola"]

---

### 1. [Topic]

**Background:** [2–4 sentences: context, history, current state.]

**What to raise:** [What Kevin wants to say or surface in this meeting.]

**Suggested words:**
> "[Suggested script — first person, conversational.]"

---

[Repeat for each topic]

---

### Tone Notes
[Short note on style/dynamic for this person and this meeting. Optional but encouraged.]

---

## Meeting Notes — [DD Month YYYY]

[Leave blank — completed post-meeting]
```

**Post-meeting notes (appended to the same file after the 1-1):**

```
## Meeting Notes — [DD Month YYYY]

**Summary:** [2–3 sentences covering what was discussed and outcome.]

**Decisions made:**
- [bullet]

**Actions agreed:**

| Owner | Action | Due |
|---|---|---|
| [Name] | [Action] | [Date] |

**Carry forward to next time:**
- [bullet]
```

**Rules:**
- Pre and post-meeting notes live in the same session file
- Open actions are surfaced to Kevin but NOT auto-written to `open-actions.md` — Kevin confirms first
- Pull Granola before writing — check most recent session and open actions first
- If Granola returns nothing, say so and work from local files only
- Each person's files are self-contained — never mix actions across people

---

## KPI Monthly Standing Agenda

Two distinct document types — keep them as separate session files.

**1. Standing Agenda meeting prep (before the monthly meeting):**

```
# Monthly Standing Agenda — [Month YYYY]

**Date:** [Weekday DD Month YYYY]
**Attendees:** [Names]

---

## Actions from last meeting

| # | Action | Owner | Status |
|---|---|---|---|
| 1 | [Action] | [Owner] | [Done / In progress / Overdue] |

---

## Standing agenda items

### 1. [Standing item]
[Brief context on current position. Any update since last month.]

### 2. [Standing item]
[...]

---

## New items this month

### [Item title]
[What it is and why it's on this month's agenda.]

---

*Prepared: DD Month YYYY | Sources: [Granola, tasks.json, briefing.json, prior session file]*
```

**2. KPI run output (when producing the monthly KPI figures):**

```
# KPI Run — [Month YYYY]

**Run date:** [DD Month YYYY]
**Produced by:** Kevin

---

## KPI outputs

| KPI | Value | Source | Notes |
|---|---|---|---|
| [KPI name] | [Figure] | [Data source] | [Any anomaly or caveat] |

---

## Commentary

[2–4 sentences: notable movements, anything that needs flagging to the group.]

---

## Distribution

[Who receives this output and how.]
```

**Rules:**
- KPI run output and meeting prep are always separate files — name them clearly: `YYYY-MM-standing-agenda.md` and `YYYY-MM-KPI-run.md`
- Every KPI figure must reference its data source — no undocumented numbers
- Action items from the meeting must have a named owner and due date

---

*Last updated: 26 June 2026*
