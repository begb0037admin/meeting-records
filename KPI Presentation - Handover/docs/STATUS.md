# STATUS — KPI Presentation
**Last updated:** 7 Sep 2026 (August 2026 build attempt — blocked on a pipeline bug, see HANDOVER.md)
**Current phase:** Active — standing monthly responsibility (Lauren's `AGENT.md`, 7 Aug 2026). August 2026 run in progress, blocked.

## Confirmed
- SOP current: `docs/KPI_RUN_SOP.md`
- Last confirmed KPI run: May 2026 (sent to Michael O'Sullivan 9 Jun 2026; presented 10 Jun 2026).
- July 2026 KPI Presentation independently verified end-to-end, 7 Aug 2026 — zero divergence. Drew's `KPI presentation - July 2026.pptx` is the official July deck.
- Canonical naming: `KPI presentation - <Month> <Year>.pptx`.
- **7 Sep 2026 — August 2026 source data present and verified.** Local OneDrive `...\Functional Analysis Team Monthly Statistics\2026\08 Aug\Source Data\`, landed 7 Sep 2026 from the 1 Sep 2026 export (= August month-end): Excel `HR_Systems_Functional_Team_Monthly_Report_Excel - 202609010715.xlsx`, H&S `Health and Safety Systems Support Statistics - 202609010600.docx`. Not a GitHub file.
- **7 Sep 2026 — self-test gate PASS.** `python build_kpi_presentation.py` → `ALL PASS` (9/9 extraction vs known June, every table cell across 11 slides matches real June deck, 9/9 chart-value checks). The one known disclosed 0.01pp rounding NOTE on slide 7 "LESS THAN 5 DAYS" prints as expected — not a failure.

## Blocked — needs Drew
- **`build_month(2026, 8)` fails at the slides 8/9/10 picture-swap:** `RuntimeError: slide 8: Picture 2 not found - layout may have changed`. Root cause: the large chart-image shape is looked up by hardcoded `sh.name == "Picture 2"`, which only exists in hand-made real decks. Drew's July pipeline output renamed those shapes (`Picture 13` slide 8, `Picture 11` slides 9/10) — `python-pptx.add_picture()` auto-assigns a new name. August is the first month built on a pipeline-generated base deck, so the first to hit it. The pipeline is not idempotent month-over-month. This is a pipeline bug, not a content/data issue — belongs to Drew per the Lauren/Drew split.

## Unconfirmed — needs Kevin
- Whether a June and/or July 2026 KPI run was actually done/circulated during Kevin's Jul/Aug absence (carried forward, still open).

## Known Gaps
- `docs/reference/kpi-definitions.md` still a stub — no KPI names/sources/methods documented.
- Everything upstream of the picture-swap builds correctly for August (all tables slides 2–10, all native pie charts, slide 1 title, all three regenerated chart images) — confirmed via a diagnostic build with a local uncommitted workaround, rendered and visually checked. But no clean, unpatched August deck exists yet.

## Up Next
1. Drew fixes the `Picture 2` naming/idempotency bug in `tools/speaking-briefs/build_kpi_presentation.py`; re-runs the bundled self-test (must still be `ALL PASS`).
2. Lauren re-runs `build_month(2026, 8)` clean with no local patch, to a clearly non-canonical file; renders it; shows Kevin for approval.
3. On Kevin's explicit go-ahead only: save as canonical `KPI presentation - August 2026.pptx` in `...\2026\08 Aug\`. Then log `docs/sessions/2026-08-KPI-run.md` and confirm distribution to Michael O'Sullivan.
