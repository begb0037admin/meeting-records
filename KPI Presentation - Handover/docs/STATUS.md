# STATUS — KPI Presentation
**Last updated:** 7 Sep 2026 (August 2026 build complete — awaiting Kevin's approval of the visual before the canonical save)
**Current phase:** Active — standing monthly responsibility (Lauren's `AGENT.md`, 7 Aug 2026). August 2026 run: built, self-tested, rendered; pending sign-off.

## Confirmed
- SOP current: `docs/KPI_RUN_SOP.md`
- Last confirmed KPI run: May 2026 (sent to Michael O'Sullivan 9 Jun 2026; presented 10 Jun 2026).
- July 2026 KPI Presentation independently verified end-to-end, 7 Aug 2026. Drew's `KPI presentation - July 2026.pptx` is the official July deck.
- Canonical naming: `KPI presentation - <Month> <Year>.pptx`.
- **7 Sep 2026 — August 2026 source data present and verified.** Local OneDrive `...\Functional Analysis Team Monthly Statistics\2026\08 Aug\Source Data\`, landed 7 Sep 2026 from the 1 Sep 2026 export (= August month-end): Excel `HR_Systems_Functional_Team_Monthly_Report_Excel - 202609010715.xlsx`, H&S `Health and Safety Systems Support Statistics - 202609010600.docx`. Not a GitHub file. Base deck: `...\07 Jul\KPI presentation - July 2026.pptx`.
- **7 Sep 2026 — pipeline picture-swap idempotency bug fixed by Drew** (`build_kpi_presentation.py`, commit `b13afe5`): slides 8/9/10 chart-image lookup is now name-independent (falls back to largest-area Picture) and normalises the shape name to `Picture 2` on write, so it is idempotent month-over-month.
- **7 Sep 2026 — self-test gate PASS on the fixed script.** `python build_kpi_presentation.py` → `ALL PASS` (9/9 extraction vs known June, every table cell across all 11 slides matches the real June deck, 9/9 chart-value checks). The known disclosed 0.01pp rounding NOTE on slide 7 "LESS THAN 5 DAYS" prints as expected — not a failure.
- **7 Sep 2026 — August 2026 deck built CLEAN** (no local patch) via `build_month(2026, 8)` to a non-canonical scratchpad file. 11 slides; slide 1 title → "AUGUST 2026 KPI STATISTICS |"; 134 table cells across slides 2–10 updated vs July; all native pie charts recomputed; all three chart images regenerated at the carried-forward positions; slides 8/9/10 pictures correctly re-normalised to `Picture 2`. All 11 slides rendered to PNG and visually confirmed — Oxford / People Department chrome intact, crest untouched.

## Awaiting Kevin
- Approval of the rendered August visual. On his explicit go-ahead only: save canonical `KPI presentation - August 2026.pptx` into `...\2026\08 Aug\`, then log `docs/sessions/2026-08-KPI-run.md` and confirm distribution to Michael O'Sullivan.
- Still open (carried forward): whether a June and/or July 2026 KPI run was actually circulated during Kevin's Jul/Aug absence.

## Known Gaps
- `docs/reference/kpi-definitions.md` still a stub — no KPI names/sources/methods documented.
- Minor pre-existing cosmetic (not a regression, present in prior months): slides 8 & 9's matplotlib "Total:" annotation slightly overlaps the final bar's data label.
- Self-test still builds only single months on hand-made base decks. Worth strengthening to chain two consecutive months (build N, then N+1 on that output) now that idempotency matters — flagged to Drew.

## Up Next
1. Kevin reviews the visual and approves (or requests changes).
2. On approval: Lauren saves canonical `KPI presentation - August 2026.pptx` into `...\2026\08 Aug\`, logs the session file, confirms the deck goes to Michael O'Sullivan.
