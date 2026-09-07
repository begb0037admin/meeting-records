# STATUS — KPI Presentation
**Last updated:** 7 Sep 2026 (Drew implemented HANDOVER Parts A + B + C in `build_kpi_presentation.py`; self-test green on June + a fresh August build; deck NOT yet rebuilt/rendered/approved — that is Lauren's next step)
**Current phase:** Active — standing monthly responsibility. August 2026 run: pipeline fix landed, awaiting Lauren's clean rebuild + render + Kevin's approval.

## Confirmed
- SOP current: `docs/KPI_RUN_SOP.md`. Canonical naming: `KPI presentation - <Month> <Year>.pptx`.
- Last confirmed KPI run: May 2026. July 2026 deck was built and sent to Michael O'Sullivan (carries the Slide 5 defect below — see follow-up).
- **7 Sep 2026 — August source data verified live** (`...\2026\08 Aug\Source Data\`, 1 Sep 2026 export). Base deck: `...\07 Jul\KPI presentation - July 2026.pptx`.
- **7 Sep 2026 — pipeline picture-swap idempotency bug fixed by Drew** (`b13afe5`). Clean `build_month(2026, 8)` works; June self-test `ALL PASS` on the fixed script.
- **7 Sep 2026 — clean August deck built + all 11 slides rendered** (scratchpad, evidence only). Design/layout parity vs July clean; all slides except Slide 5 `Table 4` verify accurate vs source (Codex).

## Done — HANDOVER Parts A + B + C implemented (Drew, 7 Sep 2026)
Landed as one change to `tools/speaking-briefs/build_kpi_presentation.py` (+ `.gitignore`). Decision in **ADR-0001**, registry in **`docs/reference/incident-other-reconciliation.md`**. Nothing saved to OneDrive; no canonical deck built.
- **A — Slide 5 `Table 4` arithmetic (done):** `INCIDENT_OTHER_EXCLUDE` blacklist deleted. Table now built from a 9-row whitelist (`INCIDENT_OTHER_NAMED`) + a computed `Other` row = source month total − sum(named); Total row and every % base = the sheet's own month total row (Jun 77 / Jul 65 / Aug 61). Row 10 "Interfaces" → "Other" (Kevin confirmed, no 11th row). Source-sanity assert added: build fails if the source sheet's own category rows don't sum to its own total. Percentages emitted round-half-up (Decimal) so they equal the source sheet's own "Category %" column exactly — small, deliberate deviation from the spec's literal `:.2f`, see HANDOVER note.
- **B — Scope captions (done):** run-time `add_textbox` boxes — `IncidentOtherScopeCaption` on Slide 5 below `Table 4`, `IncidentOtherPointer` on Slide 4 below `Table 5`. 9 pt, deck grey, wrapped, idempotent (found by name and updated in place on re-runs). Text per ADR-0001 §4 with `{N}` = source month total.
- **C — Hardened blocking gate (done):** new `validate_deck(prs, pxd, hs_current, hs_prev, year, month)`, called by `build_month` after `populate_deck` and **before save**. On any failure it prints every failure, raises `DeckValidationError`, writes **no** deck at `out_path` (a `.REJECTED` copy is saved for inspection) and `__main__` exits non-zero. Checks: row-sum == displayed Total (exact, every table); single-category % == count/Total (±0.001); % column sums to 100 (±0.10 pp, documented); combined-band cells on Slides 6 & 7 (exact except registered D4 ≤ 0.01 pp); delta cells (MoM/YoY/Variance) arithmetically correct; pie chart series == table cell values; trend/combo chart source arrays == table cells. Cross-slide registry encoded in code: **R1** Slide 5 `Table 4` Total == Slide 7 current-month band total (exact); **R2** Slide 5 `Table 6` Total == Slide 4 "Service Request" cur == SR source total (exact); **R-cur** Slide 4 Total cur == Analy3 Completed Tasks cur (exact); **D1–D4** registered differ-by-design; unregistered repeated metric that mismatches → fail. Self-test now also builds a fresh **August 2026** and runs the gate against it; `IO_ORACLE` carries both June (Total 77) and August (Total 61) known-good `Table 4` columns; the June-reference cell-diff skips `Table 4` and checks it against the corrected oracle instead (68 → 77).

**Self-test result (7 Sep 2026, `python build_kpi_presentation.py` → `ALL PASS`, exit 0):** Part 1 + 1b green (June extraction + full `Table 4` mapping vs oracle); Part 2 green (every table cell matches the real June deck, `Table 4` vs ADR-0001 oracle); Part 3 green (`validate_deck` on freshly built June); Part 4 green (fresh August build, gate passed inline, `Table 4` = Total 61 / Other 2, captions present). Gate proven to block: injecting one wrong figure → `DeckValidationError`, no deck written, `.REJECTED` copy only, non-zero exit.

## Awaiting Kevin (after Drew's fix + rebuild)
- Approval of the corrected August visual before the canonical OneDrive save.
- **Separate decision:** July 2026 deck already sent to Michael has the old Slide 5 numbers (Total 62). Corrected = Total 65 / add "Other 7" / caption. Reissue the deck, or send Michael a written explanation citing ADR-0001. A reply is owed (he raised it 13 Aug).
- Optional: keep "Interfaces" as its own named row (needs an 11th row = layout change, Drew) instead of folding it into "Other".
- Still open: whether a June/July 2026 KPI run was circulated during Kevin's absence (now partly answered — July deck exists and went to Michael).

## Known Gaps
- `docs/reference/kpi-definitions.md` still a stub — populate using ADR-0001 + the reconciliation reference.
- Minor pre-existing cosmetic (not a regression): Slides 8 & 9 matplotlib "Total:" annotation slightly overlaps the last bar label.

## Up Next
1. **DONE (Drew, 7 Sep 2026):** HANDOVER Parts A + B + C implemented in `build_kpi_presentation.py`; self-test `ALL PASS` on June (updated `Table 4` oracle 68 → 77) and a fresh August build; R1/R2/R-cur exact; gate proven to block a broken figure.
2. **Lauren (next):** re-run `build_month(2026, 8)` clean to the canonical location, re-render all 11 slides, check Slide 5 `Table 4` (Total 61 / Other 2 / scope caption present), the Slide 4 pointer, and overall layout parity vs July, then put the visual to Kevin. The build now self-validates before it writes — if `validate_deck` fails, no deck is produced.
3. On Kevin's explicit approval: save canonical `KPI presentation - August 2026.pptx` into `...\2026\08 Aug\`; log `docs/sessions/2026-08-KPI-run.md`; confirm distribution to Michael O'Sullivan.
4. Kevin decides the July-deck reissue vs written-reply question (Michael raised it 13 Aug — a reply is owed).
