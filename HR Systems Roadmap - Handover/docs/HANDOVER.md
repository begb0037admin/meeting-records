# HANDOVER — 2026-08-27 (latest)

## TL;DR — 27 Aug 2026 alignment pass
No meeting this cycle, no speaking brief. Marie asked Kevin to update the live HR Systems Roadmap master **directly**, ready for **Friday 28 Aug**. Kevin hand-enters every change himself. Lauren produced a verified, source-cited change proposal — **nothing written to the roadmap or `hr-projects`**. Deliverable: **`HR Systems Roadmap - Handover/docs/ALIGNMENT-2026-08-27.md`**. **The primary artefact is the consolidated change table at §1** (one row per item: Row ID · Title · Owner · Last update verbatim · Proposed update · Action for Kevin — sorted by owner). §2–§8 are the working detail; §9–§12 are the 27 Aug follow-ups. This §1 table layout is the standard for every future roadmap alignment pass.

**Verified live:** the authoritative master is the **local OneDrive copy** (`C:\Users\admin\OneDrive - Nexus365\HR Systems Roadmap Master\HR Systems Roadmap MASTER.xlsm`, modified 27 Aug 16:24, actively maintained). The `hr-projects` repo copy is **~12 weeks stale** (commit `f16a11a`, 6 Jun) — do not use it. Cross-referenced against `work-inbox` (briefing.json / inbox_suggestions.json, 27 Aug refresh), `command-centre` tasks.json (83 tasks), and 10 Granola notes since 10 Aug (Granola API reachable this session).

**Headline proposals (priority order):**
1. Empty **CA104_2526 "August update"** (Hierarchy Restructuring, deadline 9 Sept) — populate from Granola SK/Michael 1-1s + command-centre task-1787072363309: PACS level 2→3 college move + three new PACS management units via the Portal. *This is the "Organisational Structure Update" gap the 21 Aug handover raised — now has a clear home.*
2. Empty **Row 208** (38-day balances) — populate from the 19 Aug planning meeting + Michael 1-1 + Chemistry's 131 work groups (Michael, 27 Aug). Kevin updates holiday scheme per work group from 5 Oct.
3. **Row 179** (SSO migration, Lead: Kevin) — add 3 Aug Entra ID groups milestone + 25 Aug OSM auth issue; confirm the VS2022-licence blocker still holds.
4. **Row 136** (DPIA, Lead: Kevin) — add 27 Aug v0.5 share; deadline 31 Aug at risk.
5. **DTP1334** (H&S Management System, Lead: Kevin) — roll stale 27 Aug checkpoint forward.
6. **DTP1092** — ORCID sub-action ("Kevin to take forward") has no progress since 30 Jul; invalid deadline text `31/09/2026`.
7. New "New"-status rows **198 / 199** (WFM remaining depts; Botanic Gardens rostering) — decision needed on scope/ownership.

**Follow-ups added later on 27 Aug (now §9–§12 of the deliverable, after §1 was inserted):**
- **§9 — when the roadmap was genuinely last updated:** it is a *rolling* document (per-row `Date last reviewed`, no sheet-wide date). Last worked on **27 Aug** — a ~10-row batch of dashboard/HESA/REF/FA items (file saved 16:24). Last full cycle before that: **21 Aug meeting** (14 rows). **The Friday 22 Aug cycle was skipped** — nothing in the sheet is dated 22–24 Aug. ~25 active rows still carry a blank/pre-July review date. Data-entry errors flagged: row 180 review date `2026-12-18` (future), CA120_2526 progress line `29/05/2029`, DTP1092 deadline `31/09/2026` (invalid).
- **§10 — full before/after table:** verbatim current cell content vs proposed, for every proposed row.
- **§11 — owner-coverage sweep of all 268 rows** for Kevin/Simon/Marie/Michael/James/Asta. Findings: **Kevin leads 3 active rows, all in the proposal. Michael and Asta lead ZERO active rows** — their live work sits under 208/CA102_2526/CA104_2526/CA138_a/179 (all already proposed) — not a filtering error, structural. Simon/Marie C carry most other-owner active load; overlooked ones now flagged: **181, UOX008** (Simon), **202, 149, 193** (Marie C), **94** (James), **191** (Nathan).
- **§12 — 3 rows added from the sweep:** **204** (REF Appeal ESS — deadline 28 Aug tomorrow; REF2029 UDF promotion to UOXP), **183** (Sickness Absence Dashboard — data-model blocker, reviewed 3 Jul), **ITS960** (DSE — Granola *James 1-1 21/08* says "delivered and closed"; confirm, don't close unilaterally).
- Data-entry error rows also in the §1 table: **180**, **CA120_2526**, **DTP1092** (date fixes).

**Next concrete action:** Kevin works down the **§1 consolidated change table** in `ALIGNMENT-2026-08-27.md` and hand-enters approved rows into the OneDrive master for Friday.

**Gaps flagged:** Sarah Rowles' HESA-timing question and the H&S-dashboard org-mapping risk (both named in the 21 Aug handover) are **not corroborated** in this cycle's sources — Kevin to confirm if real.

**Pipeline freeze unchanged:** `tools/speaking-briefs/build_roadmap.py` and `roadmap-items.json` were **not** used or touched — the 21 Aug freeze still stands. This pass read the master directly.

---

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

## Engineering scoping — Drew, 21 Aug 2026 (later same night)
Per Kevin's instruction above, no code changes were made. Drew read `README.md`, `brief_chrome.py`, and all five `build_*.py` scripts, root-caused both gaps above, and wrote them up with 2-3 sketched (not built) reliability options: `tools/speaking-briefs/PIPELINE_RELIABILITY_REVIEW.md`. Confirmed via direct repo read: `roadmap-items.json` and `hs-items.json` are both session-local, uncommitted extracts (not in the repo tree at all); every `build_*.py` script's item content is a hand-authored per-session snapshot with no persistent cross-brief registry and no staleness flag anywhere. Also flagged there, as a related but separate fragility: `brief_chrome.py`'s `SCRATCH` constant is hardcoded to a specific prior session's scratchpad path, so a fresh session silently can't find `roadmap-items.json`/`hs-items.json` at all unless someone edits it first — same class of silent-staleness problem as the two gaps above. This is ready for the Kevin/Lauren review session; SendMessage sent to Lauren summarizing it the same night. The separate `build_roadmap.py` / `write_brief_output()` gap noted above (18) is captured in that document too, not raised as a standalone fix — it's in scope for the same review, not something to act on ad hoc.

## Docs Updated This Session
- [x] HANDOVER.md (new — first for this area)
- [ ] STATUS.md — not yet created
- [ ] Session log — not yet created
- [x] `tools/speaking-briefs/PIPELINE_RELIABILITY_REVIEW.md` (new, engineering scoping doc, Drew)
