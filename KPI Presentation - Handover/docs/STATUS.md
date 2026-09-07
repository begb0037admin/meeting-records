# STATUS — KPI Presentation
**Last updated:** 7 Sep 2026 (Lauren rebuilt August 2026 clean on `b9826fd`; `validate_deck()` passed inline; self-test `ALL PASS`; 11 slides rendered + verified. Awaiting Codex final pass, then Kevin's approval, then canonical save.)
**Current phase:** Active — standing monthly responsibility. August 2026 run: rebuilt + self-validated + verified; not yet approved or saved.

## Confirmed
- SOP current: `docs/KPI_RUN_SOP.md`. Canonical naming: `KPI presentation - <Month> <Year>.pptx`.
- Last confirmed KPI run: May 2026. July 2026 deck was built and sent to Michael O'Sullivan (carries the Slide 5 defect below — see follow-up).
- **7 Sep 2026 — August source data verified live** (`...\2026\08 Aug\Source Data\`, 1 Sep 2026 export). Base deck: `...\07 Jul\KPI presentation - July 2026.pptx`.
- **7 Sep 2026 — pipeline picture-swap idempotency bug fixed by Drew** (`b13afe5`). Clean `build_month(2026, 8)` works; June self-test `ALL PASS` on the fixed script.
- **7 Sep 2026 — Slide 5 fix + captions + hardened gate implemented by Drew** (`b9826fd`) — Parts A + B + C below.
- **7 Sep 2026 — August 2026 rebuilt CLEAN on `b9826fd` by Lauren, verified** (scratchpad, evidence only — `Lauren Rebuilt Tests August 2026 (NOT canonical - pending Codex+Kevin review).pptx` + `aug_png\Slide1–11.PNG`). `validate_deck()` ran inline during the build with no exception. Slide 5 `Table 4`: 10 rows sum to Total 61, "Other" = 2 (3.28%), percentages equal the source sheet. Slide 5 scope caption + Slide 4 pointer present, within bounds, understated grey footnotes. R1 (Slide 5 Table 4 Total 61 == Slide 7 band total 61) ✓; R2 (Slide 5 Table 6 Total 368 == Slide 4 Service Request 368) ✓; D1 (Slide 4 Incident–Other 66 vs 61) registered differ-by-design. All month headers correct. Layout parity vs July: only the two intended caption boxes added; slides 8/9/10 chart-image shape name normalised to `Picture 2` (Drew's `b13afe5`) with identical geometry — no drift.

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
1. **DONE (Drew):** HANDOVER Parts A + B + C in `build_kpi_presentation.py` (`b9826fd`); self-test `ALL PASS`; gate proven to block a broken figure.
2. **DONE (Lauren, 7 Sep 2026):** rebuilt August 2026 clean on `b9826fd` to a non-canonical scratch path; `validate_deck()` passed inline; self-test `ALL PASS`; all 11 slides rendered and verified (Slide 5 Table 4 Total 61 / Other 2 / caption; Slide 4 pointer; R1/R2 reconcile; headers; layout parity).
3. **Codex (next):** final review pass on the rebuilt August deck **and** the `validate_deck()` logic in `build_kpi_presentation.py`.
4. On Codex clean + **Kevin's explicit approval of the visual:** Lauren saves canonical `KPI presentation - August 2026.pptx` into `...\2026\08 Aug\`; logs `docs/sessions/2026-08-KPI-run.md`; confirms distribution to Michael O'Sullivan.
5. Kevin decides the July-deck reissue vs written-reply question (Michael raised it 13 Aug — a reply is owed).
