# STATUS — Meeting Pipeline Review
**Last updated:** 21 Aug 2026
**Current phase:** Open — review session with Kevin not yet booked

## Confirmed
- Triggering event: Kevin went into the 21 Aug 2026 HR Systems Roadmap meeting under-prepared. Concrete example: "Organisational Structure Update — August 2026" item was fully drafted 18 Aug, verified live in work-inbox/command-centre/agent-commons, but never made it into any brief.
- Second gap found same night while refreshing DTP1092 on the Roadmap brief: an ORCID-onboarding thread inside the Roadmap Master's own history (back to Oct 2024, last touched 27 Feb 2026) was never carried into the brief's overlay, and isn't tracked in command-centre/work-inbox either — no cross-reference source would have caught it.
- Root cause (Drew's diagnosis, `tools/speaking-briefs/PIPELINE_RELIABILITY_REVIEW.md`, commit `a28ac0d`): every brief is a hand-authored, per-session snapshot — no persistent cross-brief registry, no staleness mechanism. `roadmap-items.json`/`hs-items.json` (data both Roadmap and H&S Roadmap depend on) are session-local scratch extracts, not committed to the repo. 3 fix options sketched, none built.
- Structural fix already done (carve-out from the "no ad hoc changes" rule — organisational, not content): every active meeting now has its own dedicated handover area, no exceptions:
  - `HR Systems Roadmap - Handover`
  - `Health and Safety Roadmap - Handover` (renamed from "H&S Roadmap - Handover" per naming-convention fix)
  - `HR Systems Managers Meeting - Handover`
  - `SK - Handover` (pre-existing)
  - `Team 1-1's/{Asta,James,Michael}` (pre-existing)
  - `KPI Presentation - Handover` and `Standing Agenda - Handover` (split out of the former combined "KPI Monthly Standing Agenda" area, 21 Aug — format/pipeline kept intact, docs area only)

## Unconfirmed / needs Kevin
- When the review session itself will happen.
- Whether/when to build the FA Team Catch-up brief (no real brief exists yet — the "FA Catch-up Companion - 18-08-2026.html" file on Kevin's Desktop is mislabeled; its actual content is Standing Agenda companion material, not an FA Catch-up brief).
- Whether to extend the "H&S" → "Health and Safety" naming fix into `build_hs_roadmap.py`'s own output filename (`"H&S Roadmap - DD-MM-YYYY.html"`) and the older `Meeting Reviews/H&S Roadmap — *.md` dated notes — flagged, not yet done, since it touches committed code/output not just a folder name.

## Resolved (21 Aug 2026, same night)
- SK 1-1 commit-message misattribution (`c4a56b9`) — content was always accurate, only the "approved live during the SK 1-1" framing was wrong. Corrected via durable addendum in `SK - Handover/docs/HANDOVER.md` (commit `b26cb18`), not a history rewrite. Closed.

## Related, separate initiative: begb0037admin/kevin-work-hub
Same night, Kevin escalated this into a bigger ask: a standing, cross-repo "issues and improvements" dashboard — not a meeting brief, a living backlog of what's broken/needs fixing/could be improved across meetings, work-inbox, command-centre, knowledge base, and HRIS, fed by any agent noticing something while doing other work. Repo: renamed from the dormant `clockify` (legacy content archived intact under `Archive/clockify-project-2026-08-21/`). Live at https://begb0037admin.github.io/kevin-work-hub/, built and owned by Drew, content-fed by Lauren/Adam. As of this update: v1 was rejected twice (too much on one page, needed tabs; used the wrong visual style instead of `command-centre/BRANDING.md`; then the whole data model was wrong — it mirrored live counts instead of being an issues/improvements backlog) — v2 rework in progress. This is a distinct, ongoing initiative from the meeting-pipeline review above, though they share root findings (e.g. the "no persistent registry" problem is exactly the kind of item that belongs on kevin-work-hub's own backlog once it's built correctly).

## Known Gaps
- `build_roadmap.py` has not been refactored to use the shared `write_brief_output()` (unlike `build_sk_1on1.py`, `build_hs_roadmap.py`, `build_managers_meeting.py`, refactored 20 Aug) — tonight's Roadmap Desktop output was written by an ad hoc one-off script. Flagged to Drew, not yet actioned.
- `roadmap-items.json` reused in tonight's rebuild was a prior session's extract, not freshly re-pulled from the Roadmap Master `.xlsm` this session — if the Master has moved since, the brief's underlying facts (not just the hand-authored overlay) may themselves be stale.

## Up Next
1. Kevin books the review session.
2. Going in with: the two concrete gap examples above, Drew's 3 options doc, and the "which meetings still need code-level naming/output fixes" list.
3. Decide the actual reliability fix (from Drew's options or a variant) and get it built.
4. Resolve the SK 1-1 commit-message correction and the FA Catch-up build as part of or alongside the same session.
