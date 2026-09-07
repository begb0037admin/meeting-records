# STATUS — KPI Presentation
**Last updated:** 7 Sep 2026 (August 2026 build: two content defects found post-render — fix spec issued for Drew, deck NOT going to Kevin yet)
**Current phase:** Active — standing monthly responsibility. August 2026 run blocked on the Slide 5 fix + hardened gate.

## Confirmed
- SOP current: `docs/KPI_RUN_SOP.md`. Canonical naming: `KPI presentation - <Month> <Year>.pptx`.
- Last confirmed KPI run: May 2026. July 2026 deck was built and sent to Michael O'Sullivan (carries the Slide 5 defect below — see follow-up).
- **7 Sep 2026 — August source data verified live** (`...\2026\08 Aug\Source Data\`, 1 Sep 2026 export). Base deck: `...\07 Jul\KPI presentation - July 2026.pptx`.
- **7 Sep 2026 — pipeline picture-swap idempotency bug fixed by Drew** (`b13afe5`). Clean `build_month(2026, 8)` works; June self-test `ALL PASS` on the fixed script.
- **7 Sep 2026 — clean August deck built + all 11 slides rendered** (scratchpad, evidence only). Design/layout parity vs July clean; all slides except Slide 5 `Table 4` verify accurate vs source (Codex).

## Blocked — fix spec issued, awaiting Drew
Independent review (Codex) + Michael O'Sullivan's 13 Aug email found two defects on the "Incident – Other" figures, and Kevin directed the self-test gate be hardened. All three are specced for Drew in `docs/HANDOVER.md` (Parts A/B/C), with the decision in **ADR-0001** and the reconciliation registry in **`docs/reference/incident-other-reconciliation.md`**:
- **A — Slide 5 `Table 4` arithmetic:** displayed rows didn't sum to the Total; % base appeared on no row (new tail category "Payroll Costing Report" counted but not shown). Fix: 9 named FA rows + an "Other" row; Total & % base = the full source month total (Jun 77 / Jul 65 / Aug 61), which also makes Slide 5 reconcile exactly to Slide 7. Row 10 "Interfaces" → "Other".
- **B — Scope captions:** run-time text boxes on Slide 5 and Slide 4 explaining that Slide 4's Incident–Other trend uses a different Ivanti grouping/window and won't match Slide 5/7 (which do match each other).
- **C — Hardened gate:** `validate_deck()` run against the *freshly built* month (not just the June reference) — row-sum == Total, % == count/Total, % column sums to 100 (±0.10 pp), chart series == table cells, and the cross-slide reconciliation registry (R1 Slide 5↔Slide 7 exact; R2 Slide 4 SR ↔ Slide 5 `Table 6` exact; D1–D4 registered as differ-by-design). Build exits non-zero and writes no deck on any failure. Also add August as a second known-good self-test month.

## Awaiting Kevin (after Drew's fix + rebuild)
- Approval of the corrected August visual before the canonical OneDrive save.
- **Separate decision:** July 2026 deck already sent to Michael has the old Slide 5 numbers (Total 62). Corrected = Total 65 / add "Other 7" / caption. Reissue the deck, or send Michael a written explanation citing ADR-0001. A reply is owed (he raised it 13 Aug).
- Optional: keep "Interfaces" as its own named row (needs an 11th row = layout change, Drew) instead of folding it into "Other".
- Still open: whether a June/July 2026 KPI run was circulated during Kevin's absence (now partly answered — July deck exists and went to Michael).

## Known Gaps
- `docs/reference/kpi-definitions.md` still a stub — populate using ADR-0001 + the reconciliation reference.
- Minor pre-existing cosmetic (not a regression): Slides 8 & 9 matplotlib "Total:" annotation slightly overlaps the last bar label.

## Up Next
1. Drew implements HANDOVER Parts A + B + C as one change; hardened gate green on June (updated `Table 4` oracle) and a fresh August build.
2. Lauren re-runs `build_month(2026, 8)` clean, re-renders, checks Slide 5 (Total 61 / Other 2 / caption) + Slide 4 pointer, puts visual to Kevin.
3. On approval: save canonical `KPI presentation - August 2026.pptx` into `...\2026\08 Aug\`; log `docs/sessions/2026-08-KPI-run.md`; confirm distribution to Michael O'Sullivan.
4. Kevin decides the July-deck reissue vs written-reply question.
