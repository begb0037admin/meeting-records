# STATUS — KPI Presentation
**Last updated:** 7 Sep 2026 (August 2026 build — picture-swap idempotency bug fixed by Drew; unblocked, awaiting Lauren's clean build)
**Current phase:** Active — standing monthly responsibility (Lauren's `AGENT.md`, 7 Aug 2026). August 2026 run in progress, unblocked.

## Confirmed
- SOP current: `docs/KPI_RUN_SOP.md`
- Last confirmed KPI run: May 2026 (sent to Michael O'Sullivan 9 Jun 2026; presented 10 Jun 2026).
- July 2026 KPI Presentation independently verified end-to-end, 7 Aug 2026 — zero divergence. Drew's `KPI presentation - July 2026.pptx` is the official July deck.
- Canonical naming: `KPI presentation - <Month> <Year>.pptx`.
- **7 Sep 2026 — August 2026 source data present and verified.** Local OneDrive `...\Functional Analysis Team Monthly Statistics\2026\08 Aug\Source Data\`, landed 7 Sep 2026 from the 1 Sep 2026 export (= August month-end): Excel `HR_Systems_Functional_Team_Monthly_Report_Excel - 202609010715.xlsx`, H&S `Health and Safety Systems Support Statistics - 202609010600.docx`. Not a GitHub file.
- **7 Sep 2026 — self-test gate PASS.** `python build_kpi_presentation.py` → `ALL PASS` (9/9 extraction vs known June, every table cell across 11 slides matches real June deck, 9/9 chart-value checks). The one known disclosed 0.01pp rounding NOTE on slide 7 "LESS THAN 5 DAYS" prints as expected — not a failure.

## Resolved — Drew, 7 Sep 2026
- **`build_month(2026, 8)` picture-swap idempotency bug — FIXED** in `tools/speaking-briefs/build_kpi_presentation.py` (commit `b13afe5`). The slides 8/9/10 chart-image lookup no longer depends on the hardcoded name `"Picture 2"`: new `find_chart_picture(slide)` helper resolves the shape by name if present (unchanged behaviour on the hand-made May/June self-test bases), otherwise falls back to the largest-area Picture on the slide (the chart image dwarfs the small crest/header logo). After `add_picture()` the new shape's name is normalised back to `"Picture 2"`, so every deck this pipeline produces is a valid name-matched base for the next month — idempotent month-over-month.
  - Self-test gate: `python build_kpi_presentation.py` → `ALL PASS` (9/9 extraction, all 11-slide table cells vs real June deck, 9/9 chart checks; known 0.01pp slide-7 rounding NOTE printed as expected).
  - Diagnostic `build_month(2026, 8)` (built to scratch, not saved to OneDrive, scratch deleted): completes with no `RuntimeError`; slides 8/9/10 each end with the regenerated chart image named `Picture 2` alongside the untouched crest picture.

## Unconfirmed — needs Kevin
- Whether a June and/or July 2026 KPI run was actually done/circulated during Kevin's Jul/Aug absence (carried forward, still open).

## Known Gaps
- `docs/reference/kpi-definitions.md` still a stub — no KPI names/sources/methods documented.
- No clean, unpatched August deck exists yet — the fix is in, but Lauren still needs to run the real build (step 1 below).
- Self-test still only exercises hand-made bases (May→June). It does not yet chain two consecutive pipeline months (build N, then build N+1 on that output), so month-over-month idempotency is now correct-by-construction but not gated by a test. Drew's note: worth adding when the self-test is next touched.

## Up Next
1. Lauren re-runs `build_month(2026, 8)` clean with no local patch, to a clearly non-canonical file; renders it; shows Kevin for approval.
2. On Kevin's explicit go-ahead only: save as canonical `KPI presentation - August 2026.pptx` in `...\2026\08 Aug\`. Then log `docs/sessions/2026-08-KPI-run.md` and confirm distribution to Michael O'Sullivan.
