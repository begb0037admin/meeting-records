# Meeting Prep Formats — Reference

> Read this before writing any meeting prep document — scheduled or ad hoc.
> Defined formats are fixed. For a meeting type not listed here, use the closest format as a base,
> note the adaptation in the document footer, and add the new format here after Kevin approves it.

---

## Spoken-word standard (applies to ALL formats)

Every prep document must include scripted spoken sections — **"Say this:"** — written in natural first-person conversational English. These are not summaries; they are words Kevin can read verbatim in the meeting without sounding like he's reading a document. Rules:

- Write in the first person as Kevin
- Use natural spoken contractions and rhythm — "I want us to" not "it is recommended that"
- Each major agenda item gets a **Say this:** block
- Opening and closing always get a **Say this:** block
- Background sections are for Kevin's eyes only (context before he speaks) — keep them brief
- If there is a decision to make or a question to ask, script the exact words

---

## HR Systems Managers Meeting — DD-MM.md

Use the mandatory full specification in
[`managers-meeting-format.md`](managers-meeting-format.md). It requires a source/freshness summary, scripted opening and closing, complete management-level agenda fields, an inclusion/exclusion decision for every active Roadmap item, explicit risks/decisions/conflicts, and draft-only safety controls.

---

## FA Team Catch-up — DD-MM.md

```
# FA Team Catch-up — DD/MM

**Date:** [Weekday DD Month YYYY]
**Purpose:** [e.g. Morning FA team check-in before HR Systems Roadmap 10:00]
**Time needed:** ~25 minutes

---

## Opening

**Say this:**
*"[Natural spoken intro — set the agenda for the catch-up.]"*

---

## Items to raise

---

### 1. [Title — person responsible or topic]

**Background:** [2–5 sentences: what is this, why it matters, current state, any blockers or dependencies.]

**Say this:**
*"[Natural spoken words — what Kevin actually says to raise or confirm this item.]"*

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
- Every item has **Background:** (Kevin's context) and **Say this:** (Kevin's spoken words)
- Background is brief — 2–5 sentences max
- Say this is natural spoken English, first person
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

**Say this:**
*"[Natural spoken words — how Kevin raises this with Simon.]"*

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
- Every priority item must have a clear **Ask of Simon** and a **Say this:** block
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

**Say this:**
*"[Suggested script — first person, conversational.]"*

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

**Say this:**
*"[How Kevin introduces or updates this item at the meeting.]"*

### 2. [Standing item]
[...]

---

## New items this month

### [Item title]
[What it is and why it's on this month's agenda.]

**Say this:**
*"[How Kevin introduces this.]"*

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

## Ad hoc internal resolution meeting

Used when Kevin needs to resolve an operational issue with internal stakeholders before responding externally. See `WFM Rostering — 30-06.md` as the reference example.

```
# [Meeting title] — DD/MM

**Date:** [Weekday DD Month YYYY]
**Meeting type:** Internal resolution — [topic]
**Attendees:** [Names]
**Time needed:** ~[N] minutes

---

## Purpose

[2–4 bullet points: what needs to be resolved and what the outputs are.]

---

## Background

[Short factual summary — what happened, what's outstanding, why this meeting is needed.]

---

## Opening — set the agenda

**Say this:**
*"[Natural spoken intro covering the two or three things to get through. Name who Kevin will turn to first.]"*

---

## [N]. [Agenda item title]

**Background:** [2–4 sentences: context Kevin needs before speaking.]

**Say this:**
*"[Kevin's exact spoken words for this item — question, position, or ask.]"*

---

[Repeat for each item]

---

## Closing — agree outputs

**Say this:**
*"[Kevin's closing script — run through the outputs one by one and confirm ownership before leaving the room.]"*

---

## Note for Kevin

Outputs needed by end of meeting:
- [Output 1]
- [Output 2]

---

*Prepared: DD Month YYYY | Sources: [List]*
*Format: Ad hoc internal resolution meeting — [first use reference]*
```

**Rules:**
- Always includes an Opening and Closing with Say this scripts
- Every agenda item has Background (context) and Say this (spoken words)
- Note for Kevin lists the concrete outputs — not actions, outputs
- If the meeting exists to pre-agree an external response, that response must be one of the listed outputs

---

*Last updated: 29 June 2026*
