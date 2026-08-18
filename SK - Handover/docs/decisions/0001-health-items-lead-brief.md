# ADR-0001: Occupational Health / personal health items always lead the brief

**Status:** Accepted
**Date:** 2026-08-18
**Deciders:** Kevin Lelitte
**Related:** Simon 1-1 (19 Aug 2026) prep session

---

## Context
While preparing four new prep/discussion items for Kevin's 19 Aug 2026 1-1 with Simon Burford (P1 Occupational Health report, P2 Organisational Structure Update, P3 Cority Applicant Data Import file, P4 Volunteering Leave/TIMDEP04), Kevin gave an explicit standing instruction on card ordering: OH/health content is always placed first, ahead of any work item, regardless of urgency or deadline pressure elsewhere in the brief. His own words: "we will always start with my health - this is a 1-1 so the format is standard."

This session's brief had P2 (Org Structure) and P3 (Cority) each individually more time-critical by deadline (19 Aug and an open support ticket respectively) than P1 (OH). Kevin's instruction makes clear that deadline pressure does not override this ordering — health leads regardless.

## Decision
For this 1-1 (Kevin / Simon Burford) — and, per Kevin's own framing ("this is a 1-1 so the format is standard"), presumptively for other 1-1-style briefs Lauren builds (e.g. the future FA Team Catch-up, Team 1-1's with James/Michael/Asta) — any Occupational Health or personal-health prep item is always the first card in the Prep/Discussion Items section, ahead of every other item, irrespective of that other item's own deadline or urgency tier.

Health items are also held to the existing "kept deliberately bare" rule (see work-inbox/command-centre cross-reference discipline): no report content, only a one-line "say this" — this ADR governs ordering, not content depth, which remains separately Kevin's explicit instruction each time.

## Consequences
**Positive:**
- Consistent, predictable brief structure across sessions — no re-litigating card order each time a health item coexists with an urgent work item.
- Matches Kevin's own stated priority for how he wants to open these meetings.

**Negative / Trade-offs:**
- A more time-critical work item (e.g. a same-day deadline) is not visually first, even though it may need to be raised earliest in the actual conversation. This is a deliberate trade-off Kevin has accepted — brief *ordering* is not the same as conversational *sequencing*, and Kevin can still choose to raise a lower-card item first in the room.

**Follow-up work:**
- When `PREP_ITEMS` is implemented in `tools/speaking-briefs/build_sk_1on1.py` (pending Kevin's approval of tonight's four drafted items), the section's default sort/insertion order must place any `pill: note` / health-tagged item first, not rely on manual list ordering alone, so this doesn't regress on a future session.
- If/when this pattern is extended to other 1-1-style briefs (FA Team Catch-up, Team 1-1's), carry this same rule forward rather than re-deciding it — treat as durable, not a one-off for this meeting only, per Kevin's own framing.

## Alternatives Considered
- **Order strictly by deadline/urgency tier** — rejected; this is what tonight's draft would have produced by default (P2/P3 ahead of P1), and Kevin explicitly overrode it.
- **Order health items last, as a closing personal note** — not raised by Kevin, rejected implicitly by his instruction to lead with health.

## Notes
Captured from the 18 Aug 2026 Simon 1-1 prep session. See `docs/sessions/2026-08-18-simon-1on1-prep.md` and `docs/HANDOVER.md` (same date) for the full session record this decision came out of.
