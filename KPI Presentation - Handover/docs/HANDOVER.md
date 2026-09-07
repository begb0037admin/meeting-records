# HANDOVER — 2026-09-07 (August 2026 rebuilt on the hardened pipeline — awaiting Codex final pass, then Kevin)

## TL;DR
Drew shipped Parts A + B + C (`meeting-records` `b9826fd`): Slide 5 `Table 4` fix (9 named rows + "Other", total = full source month total), run-time scope captions on Slides 5 & 4, and a blocking `validate_deck()` gate. Lauren re-ran `build_month(2026, 8)` clean — `validate_deck()` ran inline and passed, the bundled self-test is `ALL PASS` (June + fresh August), and the 11 rendered slides verify correct. **Next gate: Codex final pass on the rebuilt deck + the `validate_deck` logic, then Kevin approves, then Lauren saves the canonical file.** Nothing is in the OneDrive `08 Aug` archive.

## State of Play
- **Pipeline:** `tools/speaking-briefs/build_kpi_presentation.py` at `b9826fd` (picture-swap fix `b13afe5` + Slide 5 / captions / gate `b9826fd`). Percentages now use `ROUND_HALF_UP` (matches the Ivanti source sheets).
- **Self-test:** `python build_kpi_presentation.py` → `ALL PASS`. Includes: extraction vs known June; ADR-0001 June `Table 4` oracle (PM 28 … Other 11, Total 77); full June-reference cell diff; `validate_deck()` against the freshly built June deck; a fresh `build_month(2026, 8)` + `validate_deck()` against it; explicit Aug `Table 4` value checks + caption-presence checks. The Slide 7 "LESS THAN 5 DAYS" 0.01 pp NOTE prints as expected (registry D4).
- **`validate_deck()`** proven to block on tampered figures (Drew) and ran inline on Lauren's clean August build with no exception. Covers: row-sum == Total; single-category % == count/Total; % column sums to 100 (±0.10 pp); combined-band cells; delta cells; chart series == table cells; cross-slide registry R1 / R2 / R-cur exact, D1–D4 registered.
- **Clean August build:** `Lauren Rebuilt Tests August 2026 (NOT canonical - pending Codex+Kevin review).pptx` + `aug_png\Slide1–11.PNG` in session scratchpad. Not canonical.

## Verification of the rebuilt August deck (Lauren, direct)
- **Slide 5 `Table 4`:** People Management 31 (50.82%), Time and Attendance 18 (29.51%), Payroll 2 (3.28%), HR Reporting 0 (0.00%), Data Protection Request 3 (4.92%), Staff Requests 1 (1.64%), Work Groups & Managers 3 (4.92%), Recruitment 0 (0.00%), Roster (WFM) 1 (1.64%), **Other 2 (3.28%)**, **Total 61 (100%)**. The 10 category rows sum to 61. Percentages equal the source sheet's own "Category %" column.
- **Slide 5 `Table 6`:** Manager Self Service 177, WG-HR Self-Service 86, Add New Shift Type 64, HR Systems User Access 38, People Data Dashboards 3, Enhancement & Changes 0 → Total 368. Rows sum to 368.
- **Captions present and within slide bounds:** Slide 5 `IncidentOtherScopeCaption` ("… by service category — total 61 … Slide 7 breaks down this same 61-task population …"); Slide 4 `IncidentOtherPointer` ("… by HRIS parent ticket type (rolling 15-month window). Slide 5 shows last month's service-category breakdown."). Both render as understated grey footnotes below their tables, no overlap.
- **Cross-slide reconciliation on the built deck:** R1 Slide 5 `Table 4` Total (61) == Slide 7 "Other Incident" band-count total (61) ✓. R2 Slide 5 `Table 6` Total (368) == Slide 4 "Service Request" cur (368) ✓. D1 Slide 4 "Incident – Other" cur (66) vs Slide 5/7 (61) — registered differ-by-design, not asserted equal, explained by the captions.
- **Month headers:** Slide 1 "AUGUST 2026 KPI STATISTICS |"; Slide 2/3 "Jul 26 / Aug 26"; Slide 4 "Aug 25 / Jul 26 / Aug 26"; Slide 6/7 "Jul 26 / Aug 26"; Slide 8/9 row-2 "Aug 25 / Jul 26 / Aug 26"; Slide 10 "Aug 25 / Jul 26 / Aug 26". All correct.
- **Layout parity vs July base deck:** slides 1/2/3/6/7/11 identical shape sets. Slide 4 +1 shape (`IncidentOtherPointer`), Slide 5 +1 shape (`IncidentOtherScopeCaption`) — the two intended captions. Slides 8/9/10: the large chart image's shape name normalised `Picture 13`/`Picture 11` → `Picture 2` (Drew's `b13afe5`) with **identical left/top/width/height** — name change only, no positional drift. No other differences.
- **Other August figures:** Slide 4 PXD categories Aug25/Jul26/Aug26 — Service Request 140/246/368, Incident – Other 77/100/66, HR Self Service 46/56/53, Change 25/16/17, Total 288/418/504. Slide 2 H&S Jul26/Aug26 — Cority 17/11, Odyssey 5/7, IRIS 9/5, DSE 0/0, Total 31/23. Slide 8 avg acceptance 1.7/1.0/0.2; Slide 9 avg completion 3.7/1.9/1.8; Slide 10 created 314/462/491, completed 298/440/518.

## Next Concrete Action
Codex does a final review pass on (a) the rebuilt August deck and (b) the `validate_deck()` logic in `build_kpi_presentation.py`. If clean → Kevin reviews the visual and approves → Lauren copies the scratchpad deck to `C:\Users\admin\OneDrive - Nexus365\Functional Analysis Team Monthly Statistics\2026\08 Aug\KPI presentation - August 2026.pptx`, creates `docs/sessions/2026-08-KPI-run.md`, and confirms distribution to Michael O'Sullivan. If Codex finds an issue → back to Drew (script) or Lauren (content), do not work around it.

## Watch Out For
- Do not save to the OneDrive canonical path before Codex's pass **and** Kevin's approval.
- July 2026 deck already sent to Michael O'Sullivan still has the old Slide 5 numbers (Total 62). Corrected = Total 65 / add "Other 7" / caption. **Kevin's call:** reissue the July deck or send Michael a written explanation citing ADR-0001 + `docs/reference/incident-other-reconciliation.md`. He raised it 13 Aug — a reply is owed.
- "Interfaces" is folded into "Other" (ADR-0001 §2). If Kevin wants it kept as its own row → 11th row = layout change = Drew, separate.
- Do not "fix" the Slide 7 "LESS THAN 5 DAYS" 0.01 pp cell — registered D4.
- Minor pre-existing cosmetic (not a regression): Slides 8 & 9 matplotlib "Total:" annotation slightly overlaps the last bar label — same in every prior month.
- KPI run is not complete until Codex passes, Kevin approves, the canonical file is saved, and Michael's July query is answered.
