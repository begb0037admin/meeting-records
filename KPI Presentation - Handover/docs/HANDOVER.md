# HANDOVER — 2026-09-07 (Slide 5 defect + cross-slide reconciliation + hardened gate)

## TL;DR
The August 2026 KPI deck built clean (Drew's `b13afe5` picture-swap fix) and rendered, then two problems surfaced and **must be fixed before the deck goes to Kevin / senior management**:
1. **Internal arithmetic bug on Slide 5 `Table 4`** (Codex) — visible rows don't sum to the Total; percentage base appears on no row.
2. **Cross-slide "Incident – Other" mismatch** (Michael O'Sullivan, 13 Aug 2026 email on the July deck) — Slide 4 = 100, Slide 5 = 62, Slide 7 = 65 for July, unexplained.
Plus a **directive from Kevin**: the self-test gate returned `ALL PASS` with bug #1 live (it only diffs against a reference deck carrying the same bug). The gate must be hardened so this class of error cannot ship.

Decision + rationale: **ADR-0001** (`docs/decisions/0001-incident-other-table-scope.md`). Reconciliation reference + registry: **`docs/reference/incident-other-reconciliation.md`**. This file is the implementation spec for Drew. **Do not rebuild / do not put the current deck to Kevin until all three parts below are done.** Nothing is saved to the OneDrive archive.

---

## IMPLEMENTATION STATUS — Parts A + B + C DONE (Drew, 7 Sep 2026)

All three parts landed as one change to `tools/speaking-briefs/build_kpi_presentation.py` (+ its `.gitignore`). No canonical deck built; nothing written to OneDrive.

- **A** — `INCIDENT_OTHER_EXCLUDE` deleted. `extract_pxd` now reads the sheet's own month-total row (shape `(<int>, 0, None)`), asserts the source's own category rows sum to it, builds 9 whitelist rows (`INCIDENT_OTHER_NAMED`) + a computed `Other` = `io_total − sum(named)` (asserts `>= 0`), and emits `slide5_incident_other` / `slide5_incident_other_total`. `populate_deck` writes rows 1–10 + Total (`str(io_total)`) + Total-% cell `"100%"`. Row 10 label is "Other" (Kevin confirmed "fold into Other", no 11th row).
- **B** — `_upsert_textbox()` helper; `IncidentOtherScopeCaption` on Slide 5 below `Table 4`, `IncidentOtherPointer` on Slide 4 below `Table 5`. 9 pt, deck grey `#595959`, wrapped, positioned from the table shape's geometry at run time, idempotent by shape name. Text is ADR-0001 §4 verbatim with `{N}` = `io_total`.
- **C** — `validate_deck(prs, pxd, hs_current, hs_prev, year, month)` + `DeckValidationError`. Called by `build_month` after `populate_deck`, before save. Failure ⇒ prints all failures, raises, **no deck at `out_path`** (`.REJECTED` copy only), `__main__` exits non-zero. Implements every C1 check, the C2 registry (`RECONCILIATION_MUST_EQUAL` R1/R2/R-cur exact; `RECONCILIATION_DIFFER_BY_DESIGN` D1–D4; un-registered repeated-metric backstop), and C3 (June extraction oracle 68 → 77; June-reference diff skips `Table 4` and checks it against `IO_ORACLE[(2026,6)]`; fresh August build + gate; `IO_ORACLE[(2026,8)]` = Total 61 as the second known-good month).

**Self-test:** `python build_kpi_presentation.py` → `ALL PASS`, exit 0. June (updated `Table 4` oracle) and a fresh August build both green; R1/R2/R-cur exact on both. Gate proven to block: one injected wrong figure ⇒ `DeckValidationError`, no deck written.

**One deliberate deviation from the literal spec (A2/C1.2):** percentages are computed with `Decimal` + `ROUND_HALF_UP` (helper `pct2`), not Python's `f"{x:.2f}"` / `round(x, 2)`. Python uses round-half-to-even and hits float-repr edge cases (`round(40.625, 2) == 40.62`), which would make the new gate reject percentages that are actually correct against the source. ROUND_HALF_UP is what the Ivanti / H&S reports use, so Slide 5's percentages now equal the source sheet's own "Category %" column exactly (verified Jun/Jul/Aug) — this is what ADR-0001 §1 asks for. The emitter and the gate use the same function, so they stay self-consistent.

**Next step is Lauren's** (see "Next concrete action" below): clean `build_month(2026, 8)` → render → Kevin approval. Parts A/B/C spec text is kept below unchanged for the audit trail.

---

## State of play
- Data source verified live (7 Sep 2026): `...\2026\08 Aug\Source Data\` — `HR_Systems_Functional_Team_Monthly_Report_Excel - 202609010715.xlsx`, `Health and Safety Systems Support Statistics - 202609010600.docx`. Base deck `...\07 Jul\KPI presentation - July 2026.pptx`.
- Picture-swap idempotency bug: fixed, `b13afe5`. Clean `build_month(2026, 8)` works.
- Clean August render exists in scratchpad (evidence only) — carries the Slide 5 defect, so NOT for Kevin.
- All other slides verified accurate vs source (Codex); design/layout parity vs July is clean.

---

## PART A — Slide 5 `Table 4` "Incident – Other Type": total, base, and row set

**Owner of the decision:** Lauren (ADR-0001). **Drew implements.** Do **not** edit anything else about the table's look.

### A1. Remove the blacklist
Delete `INCIDENT_OTHER_EXCLUDE` (const near line 56) and every reference to it.

### A2. New extraction logic — `extract_pxd`, the `Non-HR Self Service Incident T` block (~lines 214–225)
- Read the sheet's own **total row** — the row shaped `(<int>, 0, None)` (values seen: 77 Jun, 65 Jul, 61 Aug). Call it `io_total`.
- Sanity-assert `io_total == sum of all category-row counts` in that sheet (fail the build if the source itself doesn't add up).
- Define an ordered map of the **9 named rows** → source category name:

  ```
  INCIDENT_OTHER_NAMED = [
      ("People Management",        "People Management"),
      ("Time and Attendance",      "Time and Attendance"),
      ("Payroll",                  "Payroll"),            # exact — NOT "Payroll Costing Report", NOT "X5 - Costing Maintenance"
      ("HR Reporting",             "HR Reporting"),
      ("Data Protection Request",  "Data Protection Request"),
      ("Staff Requests",           "Staff Requests"),
      ("Work Groups & Managers",   "Work Groups and Managers"),
      ("Recruitment",              "Recruitment"),
      ("Roster (WFM)",             "Roster (WFM)"),
  ]
  ```
- For each named row: `count = source count for its mapped category, else 0`.
- `other_count = io_total - sum(named counts)`; assert `other_count >= 0`.
- Emit:
  - `out["slide5_incident_other"]` = ordered `{display_label: (count, f"{count/io_total*100:.2f}%")}` for the 9 named rows **plus** `("Other", (other_count, f"{other_count/io_total*100:.2f}%"))`.
  - `out["slide5_incident_other_total"] = io_total`.

### A3. Display — `populate_deck`, the `io_order` loop (~lines 587–595)
- Replace the hardcoded `io_order` with the 10 labels from `INCIDENT_OTHER_NAMED` + `"Other"` (row 10 was "Interfaces" — it becomes "Other").
- Write rows 1–10 from `slide5_incident_other`; write the Total row (`t4_5.rows[11].cells[1]`) = `str(pxd["slide5_incident_other_total"])`, and set the Total percentage cell to `"100%"` (match existing style).
- No other change to the table.

### A4. Expected values after A1–A3 (test oracle)

| Row | Jun | Jul | Aug |
|---|--:|--:|--:|
| People Management | 28 | 22 | 31 |
| Time and Attendance | 18 | 21 | 18 |
| Payroll | 1 | 3 | 2 |
| HR Reporting | 5 | 3 | 0 |
| Data Protection Request | 7 | 1 | 3 |
| Staff Requests | 2 | 5 | 1 |
| Work Groups & Managers | 3 | 1 | 3 |
| Recruitment | 2 | 1 | 0 |
| Roster (WFM) | 0 | 1 | 1 |
| **Other** | **11** | **7** | **2** |
| **Total** | **77** | **65** | **61** |

Percentages = each count / Total, 2 dp (these now equal the source sheet's own "Category %" column). **The June self-test oracle changes** — update the June-reference `Table 4` expected cells to the Jun column above (Total 77, Other 11), not the real June deck's 68/no-Other. Note in the self-test why (circulated June deck carried the same defect).

---

## PART B — Scope captions (run-time text boxes)

### B1. Slide 5 — new text box below `Table 4`
Body font, ~9 pt, deck body colour, left-aligned under the table. Text, with `{N}` = `io_total`:
> Incident – Other (this table): non-self-service Incident tasks completed last month, by service category — total {N}. Slide 4's Incident – Other trend groups by HRIS parent ticket type over a rolling 15-month window and will not match this total. Slide 7 breaks down this same {N}-task population by time to complete.

### B2. Slide 4 — new short text box near `Table 5`
> Incident – Other = tasks completed by HRIS parent ticket type (rolling 15-month window). Slide 5 shows last month's service-category breakdown.

Text boxes only (`slide.shapes.add_textbox`) — no table/row/layout changes. If a box already exists from a prior run (name-match), update it in place rather than stacking.

---

## PART C — Harden the self-test gate (BLOCKING, runs against the freshly built month)

Add `validate_deck(prs, pxd, hs_current, hs_prev, year, month)` called by `build_month` **after `populate_deck` builds the Presentation but before the final save**. On any failure: collect **all** failures, print them, raise `DeckValidationError`. `build_month` must not leave a usable deck at `out_path` when validation fails (write to `out_path + ".REJECTED"` or don't write at all, and exit non-zero from `__main__`). The existing June-reference cell diff stays, as an **additional** gate, not the only one.

### C1. Internal-consistency checks — every data table, every month
For every table that has a "Total" row (Slides 2, 3, 4, 5×2, 8, 9, 10 — enumerate by slide+table name):
1. **Row sum == Total**, exact integer, for every value column (yr/prev/cur where applicable). (registry R3, R4, R5, R10)
2. **Single-category % cell == `round(count / displayed_total * 100, 2)`**, `abs diff ≤ 0.001`. (R6)
3. **% column sum == 100**, `abs diff ≤ 0.10` pp; accept a literal `"100%"` Total cell. Document the 0.10 pp tolerance in a comment (worst-case rounding error for ≤11 rows ≈ 0.055 pp). (R7)
4. **Combined-band cells (Slides 6 & 7 `Table 5`)**: "SAME OR NEXT DAY" == `round((SameDay+NextDay)/month_total*100,2)`; "LESS THAN 5 DAYS" == `round((SameDay+NextDay+3–5days)/month_total*100,2)`; `abs diff ≤ 0.001`, **except** Slide 7 "LESS THAN 5 DAYS" cur cell → allowed `≤ 0.01` pp (registry D4). (R11)
5. **Delta cells**: Slide 4 MoM == `cur − prev`, YoY == `cur − yr` (fmt_delta form); Slide 10 Variance row == Completed − Created per column, and its MoM/YoY cells arithmetically consistent; Slide 2/3 MoM == cur − prev. (R9, R10)
6. **Chart series == table cells**: for each pie, series value for a category == `round(that category's table % cell, 2)` (`abs diff ≤ 0.001`); for Slide 8/9 trend charts, the last 3 bars == the table's yr/prev/cur cells; for Slide 10 combo chart, the Created/Completed series == `slide10_created`/`slide10_completed`. (R8)

### C2. Cross-slide reconciliation — from the registry in `docs/reference/incident-other-reconciliation.md`
Encode the registry as an in-code structure (`RECONCILIATION_MUST_EQUAL`, `RECONCILIATION_DIFFER_BY_DESIGN`).

**Must be equal (exact; fail otherwise):**
- **R1** `slide5_incident_other_total` == `sum(slide7_bands current-month counts)` — i.e. Slide 5 `Table 4` Total == Slide 7 current-month band total.
- **R2** Slide 5 `Table 6` Total == Slide 4 `Table 5` "Service Request" (cur) == Service-Request source total (`Service Request Tasks complete` total row).
- **R-cur** Slide 4 `Table 5` "Total" (cur) == `Tasks Completed by HRIS Analy3` "Completed Tasks" for the current month.

**Differ by design (must NOT be asserted equal; presence in the registry is what allows them):**
- **D1** Slide 4 "Incident – Other" (cur) vs Slide 5 `Table 4` Total vs Slide 7 band total — different Ivanti queries (see reference doc).
- **D2** Slide 4 "Total" (cur) vs Slide 10 "Completed" (cur) — latter includes Cancelled/Rejected.
- **D3** Slide 4 "Total" (yr/prev) vs Analy3 for those months — ±1 tolerance (export timing); only cur is exact (that's R-cur).
- **D4** Slide 7 "LESS THAN 5 DAYS" (cur) vs exact division — ≤ 0.01 pp.

**Rule:** if the code identifies a repeated metric across slides that is **not** in either registry list and the values mismatch → **fail the build** with a message naming the slides and asking for a registry decision. (This is the "never ship this class of error again" backstop.)

### C3. Run the whole gate against BOTH months in `__main__`
1. Existing extraction checks vs known June figures — keep.
2. Existing June-reference full-deck cell diff — keep, with the `Table 4` oracle updated per A4.
3. **New:** `validate_deck` against the freshly built June deck.
4. **New:** build August 2026 and run `validate_deck` against it (August's source data is present). Add the A4 August column as a second known-good cell oracle once Kevin approves the corrected figures.
5. Any failure anywhere → print all, final line `SOME FAILED - do not trust this script on real data yet`, exit non-zero.

---

## Next concrete action
Parts A / B / C are implemented and self-test-green (see "IMPLEMENTATION STATUS" above; `build_kpi_presentation.py`, commit on `main`). **Lauren:** re-run `build_month(2026, 8)` clean to the canonical location, re-render all 11 slides, check Slide 5 `Table 4` (Total 61, Other 2, scope caption present), the Slide 4 pointer, and layout parity vs July, then put the visual to Kevin. The build now self-validates before it writes — a `validate_deck` failure produces no deck (only an `out_path + ".REJECTED"` copy), so a green build is a passed gate. Canonical `KPI presentation - August 2026.pptx` saved into `...\2026\08 Aug\` only on Kevin's explicit go-ahead.

**Separate, Kevin's call:** July 2026 deck already sent to Michael O'Sullivan has the old Slide 5 numbers (Total 62, no Other row, no caption). Corrected would be Total 65 / Other 7 / caption. Decide: reissue the July deck, or send Michael a written explanation citing ADR-0001 + the reconciliation reference. A reply is owed — he raised it on 13 Aug.

## Watch out for
- Do NOT put the current rendered deck to Kevin — Slide 5 `Table 4` is still wrong.
- Do NOT fold "Payroll Costing Report" / "X5 - Costing Maintenance" into Payroll (ADR-0001 §3) — they go to "Other".
- Row 10 "Interfaces" → "Other" is intentional (ADR-0001 §2). If Kevin wants Interfaces kept as its own row, that's an 11th row = a layout change = Drew, separate.
- June self-test oracle for `Table 4` **changes** (Total 68 → 77, add Other 11) — that is the fix, not a regression.
- Slide 4 vs Slide 5/7 still differ by design (D1) — do not try to force them equal; the captions (Part B) are the resolution.
- Do NOT "fix" the Slide 7 "LESS THAN 5 DAYS" 0.01 pp cell — registered (D4).
- Nothing saved to OneDrive; scratchpad artifacts are evidence only.
- KPI run is not complete until Parts A–C land, the deck is rebuilt, and Kevin approves.
