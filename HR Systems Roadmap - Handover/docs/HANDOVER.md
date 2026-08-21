# HANDOVER — 2026-08-21

## TL;DR
Kevin went into his 21 Aug HR Systems Roadmap meeting under-prepared — the brief was missing real, findable content. Concrete example he raised live: **"Organisational Structure Update — August 2026" (Simon's 3-management-unit reorg proposal) was not present in the Roadmap brief at all**, despite having been fully drafted 18 Aug as an SK 1-1 prep item and sitting, verified, in work-inbox/command-centre/agent-commons since. Kevin's explicit position: there is enough information in Granola, Outlook, work-inbox, and command-centre to keep the Roadmap current, and this must not happen again. **He has asked to book dedicated time to go through this in detail — nothing further should be changed on the Roadmap pipeline until that session.**

## State of Play
- `tools/speaking-briefs/build_roadmap.py` was refreshed live during tonight's meeting (commit `c737180`) — DTP1092's Company 90/UOXU/integration-testing status was added, after being surfaced live by Kevin correcting an earlier misattribution to the SK 1-1 brief (see Watch Out For).
- While refreshing DTP1092, a second, deeper gap surfaced: the item's own Roadmap Master update history (in `roadmap-items.json`, not committed to GitHub — session-local extract) contains an **ORCID onboarding-sequencing thread going back to Oct 2024**, last touched 27 Feb 2026, with an explicit open next-step ("Crispin to arrange plan for ORCID onboarding") never picked up in any rewrite of this card, and **not tracked anywhere in command-centre or work-inbox** — checked live, confirmed absent from both.
- The Organisational Structure Update item (Simon's reorg, the H&S dashboard mapping risk, Sarah Rowles' HESA-timing question) was drafted as `PREP_ITEMS` P1 for the SK 1-1 brief on 18 Aug (see `SK - Handover/docs/HANDOVER.md`, same date) but **never implemented in any brief** — SK 1-1 or Roadmap. It is a genuinely live, real item (command-centre `task-1787072363309`, work-inbox `HANDOVER.md` commit `91ce237b`) that simply fell into the gap between "drafted for one brief" and "actually belongs in / is also needed on another."
- Root pattern across both examples: items get captured and drafted in one place (a 1-1 prep session, a Roadmap Master row) but there is no reliable mechanism ensuring they propagate to every brief that should carry them, and no scheduled refresh cadence independent of "did someone happen to ask."

## Next Concrete Action
**Do not resume ad hoc content changes to `build_roadmap.py` or the Roadmap brief pipeline.** Wait for Kevin to set the dedicated review session. Going into that session with: (1) the ORCID gap above, (2) the Organisational Structure Update cross-brief gap above, (3) a fuller audit of what else in Granola/Outlook/work-inbox/command-centre isn't currently reaching the Roadmap brief.

## Watch Out For
- Earlier tonight, the DTP1092/Company 90/UOXU update was **mistakenly pushed into `build_sk_1on1.py`** (commit `c4a56b9`) on the wrong premise that the live discussion was happening in the SK 1-1 meeting. It was actually the Roadmap meeting throughout. The SK 1-1 commit's content is factually accurate (independently verified) but its commit message wrongly states it was "approved live during the SK 1-1" — **not corrected yet**, flagged to Kevin, no decision taken on whether to fix.
- Do not assume `roadmap-items.json` (the extracted Roadmap Master data feeding `build_roadmap.py`) is being freshly re-pulled each session — tonight's build reused a prior session's extract from local scratch storage since the Master `.xlsm` itself was not re-fetched. If the Master has moved since that extract was taken, this brief's underlying facts (not just the hand-authored overlay) may themselves be stale.
- `build_roadmap.py` has **not** been refactored to use the shared `write_brief_output()` (unlike `build_sk_1on1.py`, `build_hs_roadmap.py`, `build_managers_meeting.py`, refactored 20 Aug) — its Desktop output tonight was written by an ad hoc one-off script, not the standard pipeline. This is an engineering gap for Drew, not yet raised to him.

## Docs Updated This Session
- [x] HANDOVER.md (new — first for this area)
- [ ] STATUS.md — not yet created
- [ ] Session log — not yet created
