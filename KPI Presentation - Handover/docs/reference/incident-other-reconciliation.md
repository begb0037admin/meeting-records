# "Incident – Other" across Slides 4, 5, 7 — why the numbers differ, and what must reconcile

**Created:** 2026-09-07 · **Owner:** Lauren (content) · **Enforced by:** `build_kpi_presentation.py` self-test gate (Drew)
**Trigger:** Michael O'Sullivan's 13 Aug 2026 reply on the July 2026 deck — Slide 4 Incident–Other = 100, Slide 5 table total = 62. See ADR-0001.

This is the durable "why" reference. HANDOVER.md carries the implementation spec (which gets replaced each rollover); this file does not.

---

## The three figures and their Ivanti source queries

| Slide | Table / chart | Source sheet | Grouping field | Date filter | Incident scoping | Excludes HR Self-Service via |
|---|---|---|---|---|---|---|
| **4** | `Table 5` "Incident – Other" row + pie | `Tasks Completed by HRIS Analy2` | `Parent Ticket Type HRIS` | Created Date **and** Completed Date both in rolling **15 months** | grouped as `Parent Ticket Type HRIS = "Incident - Other"` | a **separate row** (`Incident - HR Self-Service`), not a filter |
| **5** | `Table 4` "Incident – Other Type" + pie | `Non-HR Self Service Incident T` | `Service Category` | Completed Date in **last month** | `Parent Object Name = Incident` | `Service Category != HR Self-Service` |
| **7** | `Table 5` + pie ("Time To Complete Other Incident Tasks") | `Time To Complete Other Incide1` | Time-to-complete band | Completed Date in rolling 15 months (current-month column used) | `Parent Ticket Type = Incident` | `Service Category != HR Self-Service` |

All three also filter `Owner Team = HRIS Analysis or HRIS Sys Admin` and `Status = Completed`.

## Observed figures (from source data)

| Month | Slide 4 Incident–Other | Slide 5 source total | Slide 7 band-count total |
|---|--:|--:|--:|
| Jun 2026 | 101 | 77 | 77 |
| Jul 2026 | 100 | 65 | 65 |
| Aug 2026 | 66 | 61 | 61 |

## What this means

- **Slide 5 and Slide 7 measure the same population** — "non-self-service Incident tasks completed last month" — one split by service category, the other by time to complete. Their totals are **identical every month** and **must** stay identical. This is a hard reconciliation.
- **Slide 4 is a different query.** It groups by `Parent Ticket Type HRIS` (a derived HRIS classification, not the raw `Service Category` / `Parent Object Name`), and it applies a rolling **15-month created-date** window. It runs higher than Slide 5/7 and is **not expected to match**. For Service Requests the equivalent Slide 4 figure *does* reconcile with the Slide 5 `Table 6` breakdown (150 / 246 / 368 across the three months), because for SRs the grouping fields align; for Incidents they do not.
- Making Slide 4 reconcile would require changing the upstream Ivanti report definition, which is out of scope (owned outside this project) and would break Slide 4's 15-month trend continuity.
- Resolution for the reader: Slide 5 and Slide 7 tie out exactly; a run-time caption on Slide 5 (and a short pointer on Slide 4) states that Slide 4's Incident–Other uses a different grouping and window. See ADR-0001 §4.

---

## Cross-slide reconciliation registry

The self-test gate checks each group below against the **freshly built month** (not just the June reference). A failure of a "must equal" group, or any mismatch of a repeated metric not listed here, **fails the build and writes no deck**.

### MUST BE EQUAL (exact; build fails otherwise)

| ID | Relationship | Verified Jun/Jul/Aug |
|---|---|---|
| R1 | Slide 5 `Table 4` Total  ==  Slide 7 current-month band-count total (`sum(slide7_bands[cur])`) | 77=77, 65=65, 61=61 |
| R2 | Slide 5 `Table 6` Total  ==  Slide 4 `Table 5` "Service Request" (cur)  ==  `Service Request Tasks complete` source total | 150=150=150, 246=246=246, 368=368=368 |
| R3 | Slide 4 `Table 5`: sum of the 4 category rows  ==  the "Total" row, **for each of the yr / prev / cur columns** | holds by construction; assert anyway |
| R4 | Slide 5 `Table 4`: sum of the 10 category rows (incl. "Other")  ==  the "Total" row  ==  source month total | after ADR-0001 fix: 77, 65, 61 |
| R5 | Slide 5 `Table 6`: sum of the 6 category rows  ==  the "Total" row | 150, 246, 368 |
| R6 | Every single-category percentage cell  ==  `round(count / displayed_total * 100, 2)` (abs diff ≤ 0.001) | — |
| R7 | Every percentage column sum  ==  100  (abs diff ≤ **0.10 pp**; the literal "100%" Total cell is accepted as-is) | — |
| R8 | Every pie/bar chart series value  ==  the matching table cell value (`round(chart_value, 2)` vs table cell, abs diff ≤ 0.001) | — |
| R9 | Slide 10 `Table 3` "Variance" row  ==  "Completed" − "Created", for each column; MoM/YoY delta cells arithmetically correct | — |
| R10 | Slide 2 / Slide 3 H&S "Total" rows  ==  sum of their category rows; MoM delta cells  ==  cur − prev | — |
| R11 | Slides 6 & 7 `Table 5`: "SAME OR NEXT DAY" cell  ==  `round((SameDay + NextDay counts) / month_total * 100, 2)`; "LESS THAN 5 DAYS"  ==  `round((SameDay + NextDay + 3–5 days) / month_total * 100, 2)` (abs diff ≤ 0.001, except the one entry in the "differ by design" table below) | — |

### DIFFER BY DESIGN (registered; NOT asserted equal — each has a one-line reason)

| ID | Figures | Reason they legitimately differ |
|---|---|---|
| D1 | Slide 4 `Table 5` "Incident – Other" (cur)  vs  Slide 5 `Table 4` Total  vs  Slide 7 band total | Slide 4 groups by `Parent Ticket Type HRIS` over a rolling 15-month created-date window; Slides 5/7 use `Parent Object/Ticket Type = Incident` + `Service Category != HR Self-Service`, last-month completed only. Different Ivanti report definitions. Caption on Slide 5 explains. |
| D2 | Slide 4 `Table 5` "Total" (cur)  vs  Slide 10 `Table 3` "Completed" (cur) | Slide 4 Total = tasks **completed** by parent type; Slide 10 "Completed" = "Completed / Cancelled / Rejected" from the `Tasks` sheet — a broader disposition set. |
| D3 | Slide 4 `Table 5` "Total" (yr / prev columns)  vs  `Tasks Completed by HRIS Analy3` for those months | The two Ivanti reports can disagree by ±1 for historical columns due to export-timing / late reclassification (e.g. Aug 25: Slide 4 sum 288 vs Analy3 289). Only the **current** month is asserted equal (R-cur below); historical columns tolerate ±1. |
| D4 | Slide 7 `Table 5` "LESS THAN 5 DAYS" (cur)  vs exact count division | Documented sub-0.01 pp rounding-methodology ambiguity in the source (e.g. deck 87.02% vs 67/77 = 87.01%). Permitted deviation: ≤ 0.01 pp on this cell only. |

### Current-month tie to the trend total

| ID | Relationship |
|---|---|
| R-cur | Slide 4 `Table 5` "Total" (cur)  ==  `Tasks Completed by HRIS Analy3` "Completed Tasks" for the current month (504 / 418 / 313 for Aug / Jul / Jun) — exact |

---

## Maintenance
When a new repeated metric is identified on the deck, add it here as a "must be equal" (R) or "differ by design" (D) entry **before** it can pass the build. The gate treats any un-registered repeated figure that mismatches as a build failure.

## Gate hardening pass — 7 Sep 2026 (Codex audit follow-up)
`validate_deck()` in `build_kpi_presentation.py` was extended after a Codex audit of the first version (`b9826fd`). Blocking wiring, `pct2` half-up, and the June oracle 68→77 were confirmed sound; five hardening gaps were closed. None of these change any figure in the verified June/August build (before/after cell diff empty):

1. **Structural manifest + Total-row sweep** — `EXPECTED_TABLES` / `EXPECTED_NATIVE_CHART_SLIDES` / `EXPECTED_CAPTIONS` / `EXPECTED_SLIDE_COUNT` / `COVERED_TOTAL_ROW_TABLES`. The gate now enumerates every slide's tables, native charts and run-time captions and fails if the inventory changes, and sweeps **every** table for a `Total`-labelled row (integer columns must sum to it, `%` column must sum to 100). A `Total` row in a table not in `COVERED_TOTAL_ROW_TABLES` fails the build — so a future added table/row cannot pass unchecked.
2. **Per-category source trace** — every displayed count on Slide 4 `Table 5` is asserted against `pxd["slide4_categories"]`, and every Slide 5 `Table 4` count is reconstructed from the raw source Service-Category map (`slide5_incident_other_source_counts`) — a coherently-wrong allocation (two categories swapped, totals/percentages still self-consistent) now fails.
3. **H&S source match** — Slide 2 and Slide 3 counts are compared to the H&S Word-doc figures (`hs_current` / `hs_prev`), not merely checked for internal consistency.
4. **Chart-image value chain** — `populate_deck` records the exact arrays handed to `make_trend_chart` / `make_combo_chart` on `prs._kpi_chart_series`; the gate asserts `source series == chart array == table cell` for Slides 8/9/10 (the PNG itself can't be read back, but it provably derives from verified numbers).
5. **Emitter/validator rounding parity** — `populate_deck`'s Slide 6/7 combined-band cells and pie now use `pct2` (Decimal ROUND_HALF_UP), the same helper the gate checks against, removing a future false-failure risk on a `.xx5` cell. Verified a no-op for Jun/Jul/Aug.
