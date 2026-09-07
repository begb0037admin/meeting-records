# STATUS — KPI Presentation

**Last updated:** 7 Sep 2026 — **August 2026 run complete, delivered, checkpointed.**
Final canonical `...\2026\08 Aug\KPI presentation - August 2026.pptx` — md5 `215162c9ccbd8a19bc76ddf5ef0b8e95` / 2,275,660 B, built on `7fe23f2`. `validate_deck()` PASS. Figures byte-identical across every verified build (`dcb3e67e` → `38d68fa2` → `215162c9`: 0 table/chart/image diff).
**Open:** AI-fingerprint scrub of the base template's slide-layout image alt-text + a permanent `validate_deck()` check for it; one PowerPoint round-trip visual confirmation of the placeholder captions. See HANDOVER.md "Next Concrete Action".

## STANDING RULE — no sign of AI on the deck
Kevin, 7 Sep 2026: *"do not leave any sign of AI on any decks — this is not an option, any notes/mentions must be removed, this is standing process."* Full rule + enforcement plan in `KPI_RUN_SOP.md` and `HANDOVER.md`. Applies to speaker notes, all slide/shape text, `docProps`, image alt-text on slides **and layouts/masters**, comments, embedded-object metadata.

## THE MONTHLY KPI RUN — MANDATORY ORDERED CHECKLIST
Hard-coded (Kevin, 7 Sep 2026). In order, every month; each step gates the next. Full detail: `KPI_RUN_SOP.md`.
1. **BUILD** — `build_month(YYYY, M)`. `validate_deck()` runs inline before write; failure ⇒ no deck (`.REJECTED` only), non-zero exit. Hard-stops if the speaker-notes file is missing.
2. **SPEAKER NOTES (Lauren)** — `notes/speaker-notes-YYYY-MM.md`, `## Slide N` for Slides 2–10. Automated notes check must pass (non-empty, not byte-identical to base deck, current month referenced).
3. **CODEX VERIFIES EVERY NOTE NUMBER — mandatory, every month, not optional QA.** `codex exec -s read-only --skip-git-repo-check` from repo root, prompt shape in `docs/reference/codex-notes-review-prompt.md`; re-derive every figure from slide table + source; log verdict in the session file. `NOTES NOT CLEAR` ⇒ back to Lauren/Drew.
4. **NO-AI-FINGERPRINT CHECK green** (standing rule above).
5. **ONLY THEN → KEVIN.** The deck is Kevin's to present — do not assert a recipient or auto-circulate.

## Done — August 2026
- **Source data verified live** (`...\2026\08 Aug\Source Data\`, 1 Sep 2026 export). Base deck: `...\07 Jul\KPI presentation - July 2026.pptx`.
- **ADR-0001 — Slide 5 `Table 4` methodology.** 9 named FA-category rows + an "Other" row (row 10, formerly "Interfaces"); Total and every % based on the full source month total (Aug 61), so the 10 rows sum to the Total, percentages equal the source sheet's own "Category %" column, and **Slide 5 `Table 4` Total (61) == Slide 7 band total (61)**. Costing categories go to "Other", not Payroll. Slide 4 "Incident – Other" (66) is a different Ivanti query, not expected to match — explained by on-slide scope captions (Slides 4 & 5).
- **Hardened `validate_deck()` gate** (runs inline before write; any failure ⇒ no deck, `.REJECTED` only, non-zero exit): structural manifest + Total-row sweep on every table; per-category source trace (Slides 4 & 5); H&S source match (Slides 2 & 3); row sums / single-category % == count/Total / % column sums to 100 ±0.10 pp / delta cells / chart series == table cells; cross-slide **R1** (Slide 5 `Table 4` Total == Slide 7 band total), **R2** (Slide 5 `Table 6` Total == Slide 4 SR == SR source total), **R-cur** (Slide 4 Total cur == `Analy3` Completed Tasks cur) exact; **D1–D4** registered differ-by-design; any un-registered repeated figure that mismatches fails the build. Self-test `ALL PASS` (June fixture + fresh August).
- **Speaker notes.** The pipeline had never touched `notes_slide`, so the deck's Slides 2–10 notes were June's, carried verbatim. Now: `notes/speaker-notes-2026-08.md` authored fresh (voice/structure from March–June decks), every figure cross-checked against the built deck + source; `build_month()` auto-loads it and hard-fails if missing; `validate_deck()` fails on empty / byte-identical-to-base / month-not-referenced notes. Written into the canonical deck, 0 figure diff, `validate_deck()` PASS.
- **Scope captions.** Re-homed from free `add_textbox` (which PowerPoint dropped on open/save) to an inherited layout placeholder — survives a PowerPoint round-trip. Gate hard-fails if the caption *text* is absent (rename/re-home tolerated).
- **AI-signature audit of the delivered canonical:** speaker notes CLEAN, visible slide text/titles CLEAN, `docProps` CLEAN (`dc:creator` "Dave Startup" = template author, `cp:lastModifiedBy` "Kevin Lelitte"). **FOUND, not yet scrubbed:** ~19 `ppt/slideLayouts/*.xml` carry `descr="A close-up of a sign  AI-generated content may be incorrect."` — inherited from the Oxford OU base template, not added by our build, invisible on the slides. Must be removed — see HANDOVER "Next Concrete Action" a.

## Open items
1. **Scrub the AI alt-text from the base template's slide layouts, rebuild the canonical August deck, re-verify** (0 figure diff, `validate_deck()` PASS, Codex notes still CLEAN). HANDOVER "Next Concrete Action" a.
2. **Add a permanent `validate_deck()` no-AI-fingerprint check** (notes + all text + `docProps` + every slide/layout/master image alt-text + comments; hard-fail on any hit; + tampering test). Drew. HANDOVER "Next Concrete Action" b.
3. **One PowerPoint open/close visual confirmation** that the Slide 4/5 placeholder captions survive the round-trip. Kevin. HANDOVER "Next Concrete Action" c.
4. **Backlog:** populate `docs/reference/kpi-definitions.md` (still a stub) using ADR-0001 + the reconciliation reference.

## Known Gaps / notes
- `docs/reference/kpi-definitions.md` still a stub.
- Do not "fix" the Slide 7 "LESS THAN 5 DAYS" 0.01 pp cell — documented source rounding-methodology ambiguity, ≤0.01 pp permitted on that cell only.
- Minor pre-existing cosmetic (not a regression): Slides 8 & 9 matplotlib "Total:" annotation slightly overlaps the last bar label — same every month.
- "Interfaces" folded into "Other" on Slide 5 (ADR-0001 §2); an 11th row to keep both named is a deferred layout change.
