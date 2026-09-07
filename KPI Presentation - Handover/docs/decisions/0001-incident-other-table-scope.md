# ADR-0001: Slide 5 "Incident – Other Type" table — total, percentage base, and cross-slide reconciliation

**Status:** Accepted
**Date:** 2026-09-07
**Deciders:** Kevin Lelitte (directed the fix; deck goes to senior management, this class of error must not ship again); Lauren (content owner — defines "correct and reconciled"); Codex (found the internal arithmetic defect); Michael O'Sullivan (raised the cross-slide discrepancy in his 13 Aug 2026 reply on the July deck); Drew (implements the code + gate)
**Related:** ADR supersedes an earlier draft of this file that proposed a "trim to FA categories" rule — that is rejected here because it does not reconcile Slide 5 to Slide 7. See `docs/reference/incident-other-reconciliation.md` for the full source-query comparison and the reconciliation registry. `tools/speaking-briefs/build_kpi_presentation.py`.

---

## Context
Slide 5's first table ("Incident – Other Type", `Table 4`, fixed 12 rows = header + 10 category rows + Total) had two faults:

1. **Internal arithmetic (Codex, 7 Sep 2026):** the displayed Total and every percentage were computed on *all source rows minus a hardcoded blacklist* (`INCIDENT_OTHER_EXCLUDE`), but only a **fixed 10-row `io_order`** list was written. New tail categories that were neither template rows nor blacklisted ("Payroll Costing Report" Aug 1; "X5 - Costing Maintenance", "Odyssey", "HESA", "CONNECT - Account management" Jul) were counted in the Total/percentage base but had no visible row. Result: visible rows summed to less than the Total (Aug 59 vs 60; Jul 58 vs 62), and the percentage base appeared on no row.

2. **Cross-slide (Michael O'Sullivan, 13 Aug 2026, on the July deck):** "Incident – Other" appears on three slides with three different numbers — Slide 4 trend (Jul 100), Slide 5 table total (Jul 62), Slide 7 time-to-complete total (Jul 65). A reader is left with no way to tell whether that is an error or a scope difference.

Verified facts (Jun/Jul/Aug 2026 source data):
- Slide 5's source sheet total and Slide 7's current-month band-count total are **identical every month** (77/77, 65/65, 61/61). They are the same population — "non-self-service Incident tasks completed last month" — shown two ways (by service category / by time to complete).
- Slide 4's "Incident – Other" is a **different Ivanti query** (`Parent Ticket Type HRIS` grouping, rolling 15-month created-date window) and runs consistently higher (101/100/66 vs 77/65/61). It is not expected to match, and never has — the hand-made June deck also showed Slide 5 = 68 against a Slide 7 total of 77.
- Slide 4's "Service Request" figure and Slide 5's `Table 6` (Service Request breakdown) total **do** reconcile every month (150/246/368), because for Service Requests the two queries' grouping fields align.

## Decision

### 1. Slide 5 `Table 4` total and percentage base = the full month source total
The Total row shows the source sheet's own month total for "Non-HR Self Service Incident T" (Jun 77 / Jul 65 / Aug 61). Every percentage = `count / that total`, 2 dp. This makes Slide 5's percentages equal the source sheet's own "Category %" column, and makes **Slide 5 `Table 4` Total == Slide 7 current-month band total** — a hard reconciliation that must hold every month.

### 2. Row set: 9 named FA categories + one "Other" row
`Table 4` keeps 12 rows (no layout change). Rows 1–9 are fixed named categories; **row 10 becomes "Other"** (replacing "Interfaces") and absorbs every source category not mapped to rows 1–9. Row 11 = Total.

| Row | Display label | Source category name it maps to |
|--:|---|---|
| 1 | People Management | `People Management` |
| 2 | Time and Attendance | `Time and Attendance` |
| 3 | Payroll | `Payroll` (exact — **not** `Payroll Costing Report`, **not** `X5 - Costing Maintenance`) |
| 4 | HR Reporting | `HR Reporting` |
| 5 | Data Protection Request | `Data Protection Request` |
| 6 | Staff Requests | `Staff Requests` |
| 7 | Work Groups & Managers | `Work Groups and Managers` (source spelling; displayed with `&`) |
| 8 | Recruitment | `Recruitment` |
| 9 | Roster (WFM) | `Roster (WFM)` |
| 10 | **Other** | every source category not in rows 1–9 (e.g. My Development, Applications/Software, Applicant, Pensions, Biztalk SSIS & Azure, Payroll Costing Report, X5 - Costing Maintenance, Odyssey, HESA, CONNECT - Account management, Interfaces, and any future unmapped name) |
| 11 | Total | source month total |

`other_count = source_month_total − sum(rows 1–9)`; assert `>= 0`. Nothing is dropped; nothing is silently added to a named row.

Expected results: **June** PM 28, T&A 18, Payroll 1, HR Reporting 5, DPR 7, Staff Requests 2, WG&M 3, Recruitment 2, Roster (WFM) 0, **Other 11**, Total **77**. **July** PM 22, T&A 21, Payroll 3, HR Reporting 3, DPR 1, Staff Requests 5, WG&M 1, Recruitment 1, Roster (WFM) 1, **Other 7**, Total **65** (deck currently shows 62). **August** PM 31, T&A 18, Payroll 2, HR Reporting 0, DPR 3, Staff Requests 1, WG&M 3, Recruitment 0, Roster (WFM) 1, **Other 2**, Total **61** (deck currently shows 60).

> Note: this changes June's self-test oracle — the real June deck shows a "trimmed" Total of 68 and no "Other" row. The June-reference cell diff for `Table 4` must be updated to the corrected values above (Total 77, Other 11) rather than treated as a regression. This is deliberate: the circulated June deck carried the same defect, just without an unmapped category large enough to expose it.

### 3. "Payroll Costing Report" / "X5 - Costing Maintenance" are NOT folded into Payroll
The source lists them separately from `Payroll` in the same month (Aug: Payroll 2 *and* Payroll Costing Report 1). Costing (CoreHR/X5 cost-allocation) is a distinct workstream. They go into "Other", not the Payroll row.

### 4. Scope caption on Slide 5 (and a short pointer on Slide 4)
A small text box on Slide 5, below `Table 4`, built at run time:
> "Incident – Other (this table): non-self-service Incident tasks completed last month, by service category — total {N}. Slide 4's Incident – Other trend groups by HRIS parent ticket type over a rolling 15-month window and will not match this total. Slide 7 breaks down this same {N}-task population by time to complete."

A short pointer on Slide 4 near `Table 5`:
> "Incident – Other = tasks completed by HRIS parent ticket type (rolling 15-month window). Slide 5 shows last month's service-category breakdown."

### 5. Cross-slide reconciliation is enforced by the build
See `docs/reference/incident-other-reconciliation.md` for the registry. In brief:
- **Must be equal (build fails otherwise):** Slide 5 `Table 4` Total == Slide 7 current-month band-count total. Slide 5 `Table 6` Total == Slide 4 "Service Request" (cur) == Service-Request source total. Every table's category rows sum to its Total row. Every single-category percentage == count / Total. Every percentage column sums to 100% ± 0.10 pp. Every pie/bar series value == its table cell.
- **Differ by design (registered, with reason):** Slide 4 "Incident – Other" (cur) vs Slide 5/7 total. Slide 4 "Total" (cur) vs Slide 10 "Completed" (cur — the latter includes Cancelled/Rejected). Slide 7 `Table 5` "LESS THAN 5 DAYS" (cur) may deviate ≤ 0.01 pp from exact count division (documented rounding-methodology ambiguity).
- Any mismatch **not** in the registry fails the build and writes no deck.

## Consequences
**Positive:**
- Slide 5 rows always sum to its Total, percentages always reconcile to a visible base, and Slide 5 ties exactly to Slide 7 — the numbers a reader (Michael) compares now agree or carry an on-slide explanation.
- Slide 5 percentages equal the source sheet's own percentages — independently checkable.
- Deterministic: any new source category name flows into "Other" with no code change and no per-month decision.
- The build refuses to produce a deck that fails an internal or registered cross-slide check.

**Negative / Trade-offs:**
- "Interfaces" loses its named row (folded into "Other"). Kevin's call: accept this (no layout change), or have Drew add an 11th row so both "Interfaces" and "Other" show (a layout change — deferred unless Kevin asks).
- The July 2026 deck already sent to Michael has the old (wrong) numbers. Separate decision below.
- Slide 4 still differs from Slide 5/7; that is inherent to the source reports and is now explained by caption rather than removed.

**Follow-up:**
- **Kevin to decide:** reissue the July 2026 deck (Slide 5 Total 62 → 65, plus row/percentage changes; add "Other 7"; add caption) to Michael O'Sullivan, or send him a short written explanation referencing this ADR. Michael has already raised it, so a reply of some kind is owed.
- Fill `docs/reference/kpi-definitions.md` for these tables using this ADR and the reconciliation reference.
- Drew: implement the mapping change, the caption, and the hardened self-test gate together (spec in `docs/HANDOVER.md`).

## Alternatives Considered
- **Trim `Table 4` to the FA categories only (Total = sum of named rows)** — rejected. It was the earlier draft of this ADR. It keeps Slide 5 ≠ Slide 7 (59 vs 61 in Aug) and makes Slide 5's percentages diverge from the source's own — i.e. it fixes the internal arithmetic but not Michael's actual complaint.
- **Fold unmapped categories into the nearest named row** — rejected. Mislabels data (e.g. costing tasks counted as "Payroll"); makes named rows match no single source figure.
- **Rewrite the upstream Ivanti reports so Slide 4 and Slide 5/7 use the same filter** — rejected / out of scope. The source workbook is a scheduled Ivanti export owned outside this project; changing it would break 15 months of Slide 4 trend continuity.
- **Extend the blacklist each month** — rejected. Inherently reactive: a wrong deck ships first, then the missing name is found. That is exactly how the July deck shipped wrong.
- **Add an 11th "Other" row (keep Interfaces named)** — viable, deferred. It is a genuine layout change; Codex confirmed current layout parity is clean and the instruction was not to introduce a layout change now. Offer to Kevin as an option.
- **Do nothing** — rejected. The numbers do not reconcile and the error is already in a circulated deck.
