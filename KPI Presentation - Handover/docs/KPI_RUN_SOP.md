# KPI Run — Monthly SOP

> Trigger phrase: **"prep KPI run"** or **"run KPIs"**
> Runs monthly, before the standing agenda meeting.

## Steps

### 1. Produce KPI output
- Co-work session with Kevin
- Pull KPI data from source systems (to be documented in `docs/reference/kpi-definitions.md`)
- Produce output in agreed format

### 2. Draft the month's speaker notes — mandatory, not optional
Speaker notes for Slides 2–10 (Slide 1 title card and Slide 11 "Thank you" carry
no notes, matching established practice since March 2026) are part of the
deliverable, not a nice-to-have — Kevin reads them aloud when presenting.
**Gap found 7 Sep 2026:** the pipeline never touched `notes_slide`, so the
July and then August decks both silently carried June's notes forward
verbatim (Kevin was reading June's figures aloud in July and August). This
step exists so it never happens silently again.

- **Author (Lauren, content):** draft `KPI Presentation - Handover/notes/speaker-notes-<YYYY>-<MM>.md`
  — `## Slide N` markdown sections (1-based slide number, 2–10 only). Match
  the established voice/length/per-slide structure from recent prior months
  (read at least 3–4 months back, not just the immediately preceding month —
  it may itself be stale), carry forward standing lines (e.g. H&S "still
  building the dataset", "not sitting idle with us — waiting on customer/
  third party", WFM-complete/settled-BAU-footprint, small-team/no-headroom,
  the fixed Slide 9 historical peak-trend anchors) updated only where the
  underlying fact has changed. Every number in the notes must be cross-checked
  against that month's own deck tables and source data before it's used — no
  invented context, no numbers carried from a prior month's notes without
  re-verifying them against the current month.
- **Place (Drew, pipeline):** `build_kpi_presentation.py` loads the notes file
  via `load_month_notes()` and refuses to build without it for the required
  slides — it places approved text, it never drafts or judges wording.
- Do not let this step slip because the tables/charts already validate — the
  hardened gate checks numbers, not notes; a stale-but-numerically-valid deck
  is still a build the SOP treats as incomplete.

### 3. Log session file
- Create `docs/sessions/YYYY-MM-KPI-run.md`
- Record: what was produced, figures, any anomalies, distribution list, and
  confirmation the month's speaker notes were drafted, cross-checked, and
  written into the canonical deck (or, if the deck was locked/in use when the
  run happened, the exact follow-up state — see HANDOVER.md).

### 4. Distribute
- Send KPI data to Michael O'Sullivan for team meeting presentation
- Michael presents at monthly team meeting (Simon Burford chairs)

### 5. Standing agenda
- KPI section at the standing agenda = questions on already-circulated figures only
- No need to re-present — flag any follow-up actions in the session file

## File naming
- Session file: `docs/sessions/YYYY-MM-KPI-run.md`

## Dependency
- KPI run must be complete before standing agenda prep begins
- If KPI run is not done, flag to Kevin — do not proceed with standing agenda prep

## Reference
- KPI definitions, sources, recipients: `docs/reference/kpi-definitions.md` (to be populated)
