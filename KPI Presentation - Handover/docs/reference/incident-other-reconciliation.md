# "Incident – Other" across Slides 4, 5, 7 — why the numbers differ

**Owner:** Lauren (content) · **Enforced by:** `build_kpi_presentation.py`'s `validate_deck()` (Drew)

"Incident – Other" appears on three slides. Each comes from a **different Ivanti query**, so the same-named metric legitimately shows different numbers. Without an on-slide note a reader is left with two unexplained figures — hence the scope captions on Slides 4 and 5 (ADR-0001 §4).

## The three figures and their source queries

| Slide | Table / chart | Source sheet | Grouping | Date filter | Incident scoping |
|---|---|---|---|---|---|
| **4** | `Table 5` "Incident – Other" row + pie | `Tasks Completed by HRIS Analy2` | `Parent Ticket Type HRIS` | Created **and** Completed Date both in rolling **15 months** | `Parent Ticket Type HRIS = "Incident - Other"`; HR Self-Service split off as a separate row |
| **5** | `Table 4` "Incident – Other Type" + pie | `Non-HR Self Service Incident T` | `Service Category` | Completed Date in **last month** | `Parent Object Name = Incident`, `Service Category != HR Self-Service` |
| **7** | `Table 5` + pie ("Time To Complete Other Incident Tasks") | `Time To Complete Other Incide1` | Time-to-complete band | Completed Date, rolling 15 months (current-month column) | `Parent Ticket Type = Incident`, `Service Category != HR Self-Service` |

All three also filter `Owner Team = HRIS Analysis or HRIS Sys Admin` and `Status = Completed`.

## What reconciles and what doesn't (August 2026)

- **Slide 5 `Table 4` Total (61) == Slide 7 current-month band-count total (61).** Same population — non-self-service Incident tasks completed last month — shown by service category vs by time to complete. This must be equal every month.
- **Slide 4 "Incident – Other" (66) is a different query and is not expected to match Slide 5/7.** Making it match would mean changing the upstream Ivanti report (owned outside this project) and breaking Slide 4's 15-month trend continuity. The captions state the difference.
- For Service Requests the equivalent figures *do* line up: Slide 5 `Table 6` Total == Slide 4 "Service Request" (cur) == the Service-Request source total (368 in August), because for SRs the grouping fields align.

## Checks `validate_deck()` enforces

**Must be equal (build fails otherwise):** Slide 5 `Table 4` Total == Slide 7 current-month band total · Slide 5 `Table 6` Total == Slide 4 "Service Request" (cur) == Service-Request source total · Slide 4 `Table 5` "Total" (cur) == `Tasks Completed by HRIS Analy3` "Completed Tasks" (cur). Plus generic internal consistency on every table (rows sum to Total; single-category % == count/Total; % column sums to 100 ± 0.10 pp; chart series == table cell).

**Differ by design (not asserted equal):**
- Slide 4 "Incident – Other" (cur) vs Slide 5/7 total — different Ivanti queries (above).
- Slide 4 `Table 5` "Total" (cur) vs Slide 10 `Table 3` "Completed" (cur) — Slide 10's figure is "Completed / Cancelled / Rejected", a broader disposition set.
- Slide 4 `Table 5` "Total" (yr / prev columns) vs `Analy3` for those months — the two Ivanti reports can disagree by ±1 on historical columns (export timing / late reclassification); only the current month is asserted exact.
- Slide 7 `Table 5` "LESS THAN 5 DAYS" (cur) — a sub-0.01 pp rounding-methodology ambiguity in the source; deviation ≤ 0.01 pp permitted on that cell only.

Any repeated figure across slides that isn't covered above and doesn't match fails the build.
