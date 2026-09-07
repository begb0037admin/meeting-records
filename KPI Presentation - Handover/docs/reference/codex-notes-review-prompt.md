# Codex prompt — mandatory monthly speaker-notes numeric verification

This is **checklist step 3** of the monthly KPI run (see `KPI_RUN_SOP.md`). It is
required every month, not optional QA. The automated `validate_deck()` gate
proves the speaker notes were *changed and reference the right month* — it
explicitly **cannot** verify the prose is factually correct. This step does.

## How to invoke

From the `meeting-records` repo root:

```
codex exec -s read-only --skip-git-repo-check "$(cat 'KPI Presentation - Handover/docs/reference/codex-notes-review-prompt.md')"
```

(or paste the PROMPT block below, with the four `<...>` placeholders filled in).
READ-ONLY: Codex must not rebuild, edit, or save anything. Save its report and
record the verdict line in `docs/sessions/YYYY-MM-KPI-run.md`.

If the verdict is `NOTES NOT CLEAR` → back to Lauren (wording / figure) or Drew
(pipeline). Do **not** work around it and do **not** send the deck to Kevin.

---

## PROMPT — fill the placeholders, then run

```
TASK: Independent numeric verification of the <MONTH YEAR> KPI Presentation
SPEAKER NOTES. READ-ONLY. Do not rebuild, edit, or save anything. Terse output,
findings only.

You are the mandatory monthly notes-accuracy pass. A Claude agent (Lauren)
authored these notes; do NOT trust her figures — re-derive every one yourself.

## Artefacts
- Speaker notes: KPI Presentation - Handover/notes/speaker-notes-<YYYY>-<MM>.md
  (## Slide N sections, 1-based, Slides 2-10)
- Built deck: <ABSOLUTE PATH TO THE .pptx>  (read its per-slide tables + the
  Slides 4/5 scope-note text + the Slide 1 title)
- Source data folder: <ABSOLUTE PATH TO ...\Source Data\>
    - HR_Systems_Functional_Team_Monthly_Report_Excel*.xlsx  (PXD volumes,
      SR/incident completion %, acceptance/completion times, created/completed)
    - Health and Safety Systems Support Statistics*.docx  (H&S volumes,
      time-to-resolve bands)
- Reconciliation reference: KPI Presentation - Handover/docs/reference/incident-other-reconciliation.md

## What to check — for EVERY `## Slide N` section
1. List every number, percentage, month name, year, MoM/YoY direction word
   ("up", "down", "flat", "improved", "fell"), and KPI band colour ("green",
   "amber", "red") the note asserts.
2. For each: re-derive it from (a) that slide's own table in the built deck AND
   (b) the underlying source file. Mark PASS / FAIL with: note's value, your
   value, and the source cell / sheet / paragraph it came from.
3. Cross-check the standing/context lines that carry figures (e.g. Slide 9's
   "peak was 8.3 days in February 2025 … 6.5 in October … 4.1 in January 2026"
   — confirm those anchors are stated correctly and not silently changed).
4. Confirm the reporting month/year is right everywhere and no prior month
   ("July", "June", "August 2025" used as if current) is left in by mistake.
5. Slide 5 note must reflect the ADR-0001 Incident-Other picture (Total = source
   month total, the "Other" row, the Slide 4-vs-5 scope difference) — NOT the
   pre-ADR-0001 "trimmed total" framing.
6. Confirm the note's framing of D1/D2 differences (Slide 4 vs Slide 5/7
   Incident-Other; Slide 4 total vs Slide 10 completed) matches the
   reconciliation reference — a note must not claim two differ-by-design figures
   should be equal.

## Method
- python + openpyxl / python-pptx / python-docx (available). If a package is
  missing, report it, don't skip the check.
- Do NOT run build_kpi_presentation.py or build_month().

## Output
- One block per slide (2-10): PASS / FAIL / PASS WITH NOTES, then each checked
  claim on its own line with note-value vs your-value vs source location.
- A summary table of every FAIL / material discrepancy.
- Final line exactly one of:
    NOTES CLEAR
    NOTES NOT CLEAR — <n> issues: <one line each>
```
