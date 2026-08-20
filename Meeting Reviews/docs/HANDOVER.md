# HANDOVER.md — Meeting Reviews

> Replace this file each session. Do not append.

**Session date:** 19-20 August 2026 (two sessions, same thread of work)
**Written by:** Drew (Kevin's dedicated engineering agent for Work Inbox, Command Centre, and the engineering side of meeting-records)
**Status:** Granola live-access blocker fixed and pushed to main, then a real live false-positive matching bug found and fixed same day. Managers Meeting Voice launcher now has a working, live-verified direct Granola REST tool. No meeting brief was published from either session — draft-only, as always.

---

## IF YOU ARE READING THIS COLD — START HERE

You have no memory of previous sessions. Do not guess context. This document is your complete brief for this thread of work. Read it in full before doing anything.

**Trigger:** Lauren ran the HR Systems Managers Meeting brief and found no live Granola access — she had to fall back on stale (24 June) captured docs. Per standing convention ("everything Lauren touches, Drew engineers"), this was Drew's engineering task, not Lauren's.

## Session 1 (19-20 Aug) — what was found and built

1. A Granola-capable path already existed: `.agents/skills/claude-meeting-voice/` (the launcher) + `mcp/meeting-connector/` (the MCP server), built and smoke-tested live on 1 August 2026, but depended on Granola being exposed as Claude's own **claude.ai account connector**. That was found live-broken 19 Aug: `ANTHROPIC_API_KEY` (the fleet's standing credential) disables claude.ai account connectors on this machine, even with a valid cached login — see `begb0037admin/agent-commons` `MEMORY.md`.
2. A separate, parallel Drew dispatch found that `work-inbox/fetch_inbox.py` already has a proven, production-hardened **direct Granola REST integration** (Phase 3.7b, closed since 4 Jul 2026) — a plain Bearer-token call against Granola's own public API (`GRANOLA_API_KEY`), independent of Claude's connector machinery. Kevin approved porting this pattern.
3. **Built and shipped** (commit `751b0efae21813d48b0007711faa8b4c5a0a7158`): `mcp/meeting-connector/meeting_context/granola_source.py` (new direct REST integration, independent of work-inbox's own untouched copy), a new MCP tool `get_latest_granola_meeting(title_pattern, lookback_days)` registered in both server modules, `start-managers-meeting.ps1` updated to use it instead of the broken connector, `CLAUDE.md` updated (claude.ai connector kept as a documented dormant fallback, not deleted). 44 tests, synthetic fixture (meeting-records is public — never commit real captured meeting content as a fixture).
4. Reviewed through **4 Codex passes** (the estate's standing hard cap that session) — every pass found real issues, all fixed. Also fixed two incidental pre-existing bugs found only because they blocked live verification: PowerShell's `2>` stderr redirect + `$ErrorActionPreference='Stop'` truncating real failures to one line, and `invoke-claude.py` never actually reconfiguring its own stdout to UTF-8 (crashed live on a real "→" character).
5. **Live-verified** against real production data: found the genuine latest "HR Systems Roadmap" Granola note (a real note titled "HR Systems Roadmpa 03/07" — Granola's own typo), correctly flagged it stale (47-day gap vs the weekly cadence), built a genuine 7-item draft from real Work Inbox/Command Centre data rather than fabricating anything.
6. **One separate, unrelated issue found, not fixed:** that live run's draft was rejected by `validate-meeting-result.py`'s own strict format check ("Only 2 exact speaker-note blocks found; minimum is 8") — a pre-existing content-formatting strictness issue, unrelated to Granola. Still open if anyone wants a full end-to-end launcher run to pass its own format gate.

## Session 2 (20 Aug, same day) — a real live bug, found and fixed under time pressure

Kevin's actual HR Systems Managers Meeting was scheduled 10:00 that morning. The coordinator asked for a fast, direct raw Granola query — not a full pipeline run — using the real title pattern for this meeting series, `"HR Systems Managers Meeting"` (not `"HR Systems Roadmap"`, which Session 1's testing used).

**A real bug surfaced immediately:** `get_latest_granola_meeting("HR Systems Managers Meeting")` wrongly returned the 3 July "HR Systems Roadmap" note instead of the real Managers Meeting note. Root cause: `select_latest_matching_note()`'s match threshold (`min(2, len(pattern_kw))`, a flat floor of 2 shared keywords) let "HR Systems Managers Meeting" (4 keywords: hr, systems, managers, meeting) match on just 2 shared tokens ("hr", "systems") against the Roadmap note — a false positive, since these are genuinely different, real, distinct Granola note series (confirmed live: "HR Systems Managers Meeting 24/06", "29/04", "15/04" all exist as their own real notes).

**This did NOT reach Kevin wrong** — the buggy tool's output was not trusted; the real answer (the 24 June Managers Meeting note, full content) was hand-verified by pulling the raw 91-note list directly and manually searching by title string, before the bug itself was even understood, and delivered to the coordinator for the 10:00 meeting.

**Fixed and shipped same day** (commit `487fda2ee10ca6150350538bb63ebca0f83c5bf2`): `required_overlap` changed from the flat `min(2, len(pattern_kw))` floor to `max(1, len(pattern_kw) - 1)` — a note's title may miss at most ONE of the pattern's words, scaling with how distinctive the pattern is. "HR Systems Roadmap" (3 keywords) still requires 2, surviving the real "Roadmpa" typo. "HR Systems Managers Meeting" (4 keywords) now requires 3, correctly rejecting the 2-keyword false match. 2 new regression tests added, full suite 46/46 passing. Live re-verified against the real API after the fix: both patterns now return the correct note.

**Codex was unavailable for this fix's review** — hit its usage limit mid-session (`retry Sep 13th 2026`), disclosed rather than skipped. Reviewed the fix directly instead, per the estate's Codex-scarcity fallback policy.

**A further, separate, pre-existing risk was found during that self-review — flagged here, deliberately NOT fixed, per Kevin's explicit instruction not to chase it today:** `"H&S Roadmap"` normalises to a single weak keyword (`{roadmap}`) because the "H&S" abbreviation is fully stripped by the short-token filter (the "&"→space rule splits it into bare "H" and "S", both too short to keep). That means a query for `"H&S Roadmap"` could in principle match ANY note containing the literal word "Roadmap", including a real "HR Systems Roadmap" note. Confirmed live: both series currently coexist and are both recently active (H&S Roadmap notes 17 Aug/6 Jul, HR Systems Roadmap notes 26 Jun/19 Jun). It happens to resolve correctly right now only because the most recent real "H&S Roadmap" note (17 Aug) is also the most recent "roadmap"-containing note overall — that's incidental to current data ordering, not a structural guarantee, and would misfire the moment that ordering flips. No live incident has hit this yet. Whoever picks this up next: the real fix needs care around how abbreviations like "H&S" are tokenised (a blanket single-character-token filter is what causes the degeneration) — don't just lower the threshold further, that would reopen the bug this session just closed.

## Next step for whoever picks this up

- The Granola blocker is fixed and both known-real patterns ("HR Systems Roadmap", "HR Systems Managers Meeting") are verified correct live.
- The `"H&S Roadmap"` cross-type ambiguity above is open, flagged, not urgent (no live incident yet) — pick up only if/when it actually misfires, or proactively if doing a broader pass on the matching logic.
- The unrelated speaker-note-block format-validation issue (Session 1) is still open too.
- Lauren's own everyday Fleet-dispatch workflow still does not have Granola wired in — separate, not-yet-made decision for Kevin.
- `voice-workflows/PROGRAMME_STATUS.md` Phase 5 remains stale since 1 Aug, not touched either session.

---

## Prior session context (28 July – 7 July 2026), preserved for reference

The original Voice meeting-prep prototype build (Codex Voice front end, later superseded by the Claude-native front door — see `voice-workflows/docs/decisions/2026-08-01-claude-voice-front-door.md`), Kevin's July leave handover, and the pre-leave action list from that period are archived in this repository's git history (see commit `d382674` and earlier on `main`) rather than repeated here, per this file's own "replace, do not append" convention.
