# Speaking-briefs pipeline reliability — engineering scoping (21 Aug 2026)

**Status:** Diagnosis and options only. No code changes made to any `build_*.py` script — per Kevin's explicit instruction (21 Aug), nothing further changes on the Roadmap brief pipeline until his dedicated review session with Lauren. This document exists to make that session productive: it's the engineering-side half of prep, in parallel with Lauren's content-side review.

**Author:** Drew (`begb0037admin/drew`), engineering owner of `tools/speaking-briefs/`. Content/curation judgement stays Lauren's; this document stops at "why does the pipeline behave this way" and "what could change it," not "what should a brief say."

**Triggering incident:** Kevin went into the 21 Aug HR Systems Roadmap meeting under-prepared. The "Organisational Structure Update — August 2026" item (Simon Burford's 3-management-unit reorg proposal) was fully drafted and verified live on 18 Aug — command-centre `task-1787072363309`, work-inbox `HANDOVER.md` commit `91ce237b`, draft reply `lauren-draft-15-20260818` in `agent-commons/pending-email-drafts/drafts.json` — but never reached the Roadmap brief. It sat in `SK - Handover/docs/HANDOVER.md`, written for the *SK 1-1* brief, and nothing carried it across to the Roadmap brief it also belonged in. Same evening, refreshing DTP1092 in `build_roadmap.py` surfaced a second gap: an ORCID-onboarding thread inside DTP1092's own update history (Oct 2024 → 27 Feb 2026, explicit open next-step "Crispin to arrange plan for ORCID onboarding") that's tracked nowhere — not in `roadmap-items.json`'s consuming script, not command-centre, not work-inbox.

---

## 1. What each script actually pulls from

Read in full: `README.md`, `brief_chrome.py`, `build_roadmap.py`, `build_managers_meeting.py`, `build_hs_roadmap.py`, `build_sk_1on1.py`. (`build_kpi_presentation.py` is architecturally a different pipeline — see §1.6 — and isn't where either gap happened, so it's covered only briefly.)

| Script | Item data source | Committed to `meeting-records`? | "Say this" / narrative content |
|---|---|---|---|
| `build_roadmap.py` | `roadmap-items.json`, read from `{SCRATCH}\roadmap-items.json` — a session-local extract of `HR Systems Roadmap MASTER.xlsm` (local OneDrive, `hr-projects` repo per `roadmap_export.py`'s `SOURCES` dict) | **No.** Not in the repo tree at all (confirmed — `git/trees/main` search returns nothing for `roadmap-items.json` or `hs-items.json`) | Hand-authored `OVERLAY` dict, keyed by a **fixed, hardcoded `ITEM_ORDER` list** of 8 Roadmap Master IDs (`136`, `DTP1334`, `DTP1092`, `ITS1004`, `179`, `174_b`, `22_c`, `22_d`) |
| `build_hs_roadmap.py` | `hs-items.json`, same pattern — session-local extract of the H&S Systems Backlog workbook | **No.** | Hand-authored `PILL` + `SAY` dicts, also a **fixed `ITEM_ORDER` list** of 12 IDs, plus a `FORCE_INCLUDE` set for James/Kevin-owned items |
| `build_managers_meeting.py` | No tracked-items master at all — a hardcoded Python list `AGENDA` of 7 dicts, hand-carried forward from the last captured meeting note + manual cross-check | N/A — there's no extract step, the whole thing is hand-authored per build | Same list is both the data and the narrative — no separation |
| `build_sk_1on1.py` | Same shape as Managers Meeting: hardcoded `AGENDA` list, hand-carried from the last captured 1-1 outcome + leave handover + manual Work Inbox/Command Centre check | N/A | Same — data and narrative are one hand-written list |
| `build_kpi_presentation.py` | Structurally different: edits a `.pptx` directly from a month's raw Excel/Word export (local OneDrive, never committed), gated by a bundled self-test that diffs every cell against a known-correct prior deck | N/A (own runbook, own gate) | N/A — numeric/table data, not narrative items |

**Nothing in any of these five scripts already resembles an automatic "refresh check."** The closest things that exist are all manual, textual, and per-build:
- A `flag_paragraphs` block at the top of each brief stating how many meeting cycles are missing and what date the brief's facts are "as of" (e.g. `build_roadmap.py`'s "3 July position... not a confirmed account of any July discussion").
- A `FOOTNOTE` block listing which sources were checked that session (Granola, Work Inbox, Command Centre) and when.
- A one-line disclosure when a source couldn't be reached (`build_sk_1on1.py`: "Granola was not reachable when this brief was built").

All three of those are **prose the builder wrote by hand that session** — not a mechanism. There is no field anywhere (script or data file) recording "this item was last verified on X" that a future session could check programmatically, and no step that says "before finishing this brief, check every other brief's item set for anything that should also appear here."

### 1.1 The `SCRATCH` path itself is a related fragility, not just the missing refresh check

`brief_chrome.py` line 15 hardcodes `SCRATCH` to a specific prior session's scratchpad UUID (`...75a25187-c549-45b9-ab8d-623015c16c47\scratchpad`). Every session's actual scratchpad directory is a fresh UUID. This means `roadmap-items.json`/`hs-items.json` — already session-local and un-versioned — are also sitting at a path that literally won't exist for a new session unless someone edits `SCRATCH` first or happens to still have that old directory around. This isn't the root cause of the two gaps Kevin raised, but it's the same class of problem (silent, un-signalled staleness) and worth flagging for the review session — a session could easily be re-reading a `roadmap-items.json` that's weeks old without any error, because there's no check that the file's age is recent, only that it exists.

---

## 2. Root cause, not symptom

**It is not a missing sync step from Granola/1-1-prep-drafts into the Roadmap Master or its extract.** The Roadmap Master workbook itself was never the problem in either gap:
- The Organisational Structure Update item was never a Roadmap Master row at all — Simon's reorg proposal doesn't have (and was never given) a Roadmap item ID. It exists only as a command-centre task, a work-inbox HANDOVER entry, and a drafted email reply. Even a perfect, always-fresh `roadmap-items.json` extract would not have surfaced it, because the extract only ever contains what's already a formal Roadmap Master row (`roadmap_export.py`'s own `selectionRequirement` field literally says "Assess every item and retain include/exclude reason" — it's scoped to *existing* Master rows, not to discovering new candidate items from other sources).
- The ORCID thread **is** inside the Roadmap Master's own DTP1092 history (it showed up in `roadmap-items.json`'s update log for that item) — so the extract mechanism did carry it. The gap there is downstream: `build_roadmap.py`'s `OVERLAY["DTP1092"]` is a hand-authored paragraph that each session's builder rewrites from scratch, cross-referencing Command Centre/Work Inbox for *what's changed*, but with no forcing function to also re-read that item's *entire* update history each time and check whether an old open thread is being silently dropped. A human (or an AI builder under time pressure) naturally focuses on "what's new since last time" and loses whatever isn't in the most recent update.

**Root cause, stated plainly:** every brief is a **hand-authored snapshot, rebuilt from scratch each session**, not a data-driven pipeline with a persistent, cross-referenced item registry. Two consequences follow directly, and both fired here:

1. **No propagation mechanism between briefs.** An item captured while preparing one brief (SK 1-1, 18 Aug) has no path to also land in a different brief that covers the same territory (Roadmap) except a person remembering to do it by hand. `SK - Handover/docs/HANDOVER.md`'s own 18 Aug entry says as much: "none of it has been pushed into `build_sk_1on1.py` yet," and there was never a step that asked "does this also belong in Roadmap." Confirmed nothing in `agent-commons`, `command-centre`, or `work-inbox` cross-references items *by which briefs they should appear in* — that concept doesn't exist as data anywhere.
2. **No staleness/completeness check on existing items.** Even for an item that's already correctly inside the pipeline (DTP1092, tracked from the start), there's no mechanism forcing a full re-read of everything on record for it — only "what changed since I last touched this." A multi-year-old open thread inside a still-active item's own history has no flag distinguishing it from noise; it just silently doesn't get re-surfaced unless a human happens to scroll the whole history that session (which is what happened 21 Aug, by chance, while doing something else).

This is exactly the pattern Kevin named: "there is enough information in Granola, Outlook, work-inbox and command-centre" — the *source data exists* in essentially every case. What's missing is a reliable, repeatable step that (a) pulls it fresh rather than reusing whatever a scratchpad happens to hold, and (b) checks it against every brief it's relevant to, not just the one it was captured for.

---

## 3. Options (sketch only — not built, not chosen)

### Option A — Shared item registry + explicit "which briefs" tagging
Introduce one committed (not session-local) data file — e.g. `tools/speaking-briefs/item_registry.json` — as the single place an item is captured once, tagged with which brief(s) it belongs to (`roadmap`, `sk_1on1`, `managers_meeting`, `hs_roadmap`), a `last_verified` date, and a `source` pointer (command-centre task id / work-inbox HANDOVER commit / Granola note id). Each `build_*.py` script reads its own filtered view from this one registry instead of hand-authoring `AGENDA`/`OVERLAY` dicts per session.
- **Effort:** Medium-high. Needs a schema, a migration of all four briefs' existing hardcoded items into it, and rewriting each script's rendering to read from the registry rather than inline dicts (the narrative "current position"/"say this" text still needs human judgement, but the item *existence and tagging* becomes structural).
- **Reliability gain:** High for the propagation gap specifically — an item tagged `["roadmap", "sk_1on1"]` physically cannot be built into one brief and silently skip the other. Doesn't by itself fix the staleness-within-an-item problem (§2, point 2) unless paired with something like Option C.
- **Dependency on Kevin:** Low ongoing — once seeded, new items get tagged at capture time (by whoever's drafting that session, Lauren or an agent), not something Kevin has to remember to feed in himself. Initial migration effort is one-time, not recurring.

### Option B — Scheduled/on-demand cross-brief propagation check
Keep every brief's authoring exactly as it is today (hand-authored, per-session), but add one lightweight step, run before any brief is considered finished: pull every open/live item currently sitting in command-centre + work-inbox + the most recent HANDOVER.md files across all four brief areas, and diff that set against what's actually rendered in the brief being built. Anything open-and-relevant but absent from the brief gets flagged as a question, not silently included or excluded.
- **Effort:** Low-medium. No schema migration — it's a checklist/script that reads existing sources (all already read individually by each brief today) and cross-references, rather than a new data model.
- **Reliability gain:** Medium — catches "item exists elsewhere but isn't in this brief" (would have caught the Org Structure gap directly), but relies on the check itself being run every time, and on command-centre/work-inbox tasks being tagged well enough to search reliably. Doesn't fix the "old thread buried inside an item's own history" class of gap (ORCID) unless it also does a full-history re-read per item, not just a "what's new" pull.
- **Dependency on Kevin:** Very low — this is closer to Drew building a real script (not just a documented convention) that Lauren or an agent runs as a gate before publishing. Least dependent on anyone remembering to do it by hand, if it's wired into `write_brief_output()` as a mandatory pre-step rather than a suggestion in the README.

### Option C — Per-item "last verified" / full-history-required flag
Smaller, orthogonal fix: for items that DO have a persistent record (Roadmap Master rows, H&S Backlog rows), require that each brief-build session explicitly re-reads and re-confirms the item's **full** update history (not just "what's changed"), and stamps a `last_full_review` date next to it. If that date is older than some threshold (e.g. 60 days), the brief surfaces it as a forced "explicitly confirm or dismiss this old thread" line rather than letting it age out silently.
- **Effort:** Low. Doesn't need a new registry — could be a small addition to the existing `roadmap-items.json`/`hs-items.json` extract step (`roadmap_export.py` already has a `selectionRequirement` field pattern to extend) plus a check in `build_roadmap.py`/`build_hs_roadmap.py`.
- **Reliability gain:** Directly targets the ORCID-class gap (old-thread-inside-a-still-tracked-item). Doesn't help the Org Structure-class gap at all (item was never inside a tracked master in the first place) — needs pairing with A or B for full coverage.
- **Dependency on Kevin:** Low — mechanical, runs automatically as part of the existing extract step once built.

**Read across all three:** A and B are not mutually exclusive and address the two different gap classes from §2 directly (A → propagation, B → a cheaper partial version of the same, C → within-item staleness). A + C together would have caught both 18/21 Aug gaps; B alone would have caught the Org Structure gap but likely not the ORCID one, since ORCID isn't "elsewhere and missing," it's "here and buried." None of these fixes anything about `build_managers_meeting.py`/`build_sk_1on1.py`'s complete absence of a tracked-items master behind them at all — those two are hand-authored `AGENDA` lists with no underlying Master workbook, so any registry/propagation fix has to treat them as first-class citizens in the registry from the start, not bolt onto the two Master-workbook-backed scripts only.

---

## 4. Open questions for the Kevin/Lauren review session

1. Is a committed shared registry (Option A) worth the migration effort, or is Option B's lighter-weight cross-check enough given how few briefs there are (4 active + KPI Presentation which is a different animal)?
2. Who tags/maintains the registry day to day if A is chosen — Lauren at capture time, or does this need an automated pull from command-centre/work-inbox task creation?
3. Does the Org Structure Update item need a real Roadmap Master row now (so it's inside the formal extract going forward), separately from whatever propagation fix gets built?
4. What's the right staleness threshold for Option C's `last_full_review` flag — 60 days, tied to the meeting's own cadence, something else?
5. Should `SCRATCH`'s hardcoded prior-session path (§1.1) be fixed regardless of which option is chosen, given it's an independent, currently-silent source of stale data?

---

## 5. What this document is not

Not a decision. Not an implementation. Not a change to `build_roadmap.py`, `build_managers_meeting.py`, `build_hs_roadmap.py`, `build_sk_1on1.py`, `build_kpi_presentation.py`, `brief_chrome.py`, `roadmap_export.py`, or any committed data file. Per Kevin's explicit 21 Aug instruction, no further ad hoc content changes go into the Roadmap brief (or, by the same logic, any other brief pipeline) until he and Lauren have had the dedicated review session this document is meant to prepare for.
