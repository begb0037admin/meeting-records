# HANDOVER.md — Meeting Reviews

> Replace this file each session. Do not append.

**Session date:** 19-20 August 2026
**Written by:** Drew (Kevin's dedicated engineering agent for Work Inbox, Command Centre, and the engineering side of meeting-records)
**Status:** Granola live-access blocker fixed and pushed to main. Managers Meeting Voice launcher now has a working, live-verified direct Granola REST tool. No meeting brief was published from this session — draft-only, as always.

---

## IF YOU ARE READING THIS COLD — START HERE

You have no memory of previous sessions. Do not guess context. This document is your complete brief for this thread of work. Read it in full before doing anything.

**Trigger:** Lauren ran the HR Systems Managers Meeting brief and found no live Granola access — she had to fall back on stale (24 June) captured docs. Per standing convention ("everything Lauren touches, Drew engineers"), this was Drew's engineering task, not Lauren's.

## What was found

1. A Granola-capable path already existed: `.agents/skills/claude-meeting-voice/` (the launcher) + `mcp/meeting-connector/` (the MCP server), built and smoke-tested live on 1 August 2026. It depended on Granola being exposed as Claude's own **claude.ai account connector** inside a disposable child `claude --print` process.
2. That path was never formally accepted by Kevin (`voice-workflows/PROGRAMME_STATUS.md` Phase 5 sat at "Awaiting Kevin" since 1 Aug with zero further commits) and was never wired into Lauren's actual day-to-day dispatch — every real brief she's built went through ordinary Fleet dispatch, which never had Granola tooling by design.
3. Re-running the actual launcher live on 19 Aug reproduced the same "no Granola" failure Lauren hit — root-caused directly: `claude mcp list` on this machine states plainly that `ANTHROPIC_API_KEY` (the fleet's standing credential) disables claude.ai account connectors, even with a valid cached claude.ai login. This affects any agent session on this estate, not just this workflow — see `begb0037admin/agent-commons` `MEMORY.md`.
4. A separate, parallel Drew dispatch (working in Kevin's Outlook) found that `work-inbox/fetch_inbox.py` already has a proven, production-hardened **direct Granola REST integration** (Phase 3.7b, closed since 4 Jul 2026) — a plain Bearer-token call against Granola's own public API (`GRANOLA_API_KEY`), completely independent of Claude's connector machinery. Kevin approved porting this pattern into meeting-connector.

## What was built and shipped (commit `751b0efae21813d48b0007711faa8b4c5a0a7158`, pushed to `main` 19 Aug 2026)

- `mcp/meeting-connector/meeting_context/granola_source.py` (new) — the direct REST integration. Reuses work-inbox's proven fetch/auth/parsing plumbing as an independent implementation (work-inbox's own copy is untouched, still closed/do-not-modify). Genuinely new logic: given a recurring meeting-type title pattern (e.g. "HR Systems Roadmap"), paginate the live notes list back up to 120 days and return the single **latest** matching note by real date — not the first keyword-overlap hit, since Kevin has had real 7+ week meeting gaps and multiple same-pattern-titled notes can exist across that window.
- New MCP tool `get_latest_granola_meeting(title_pattern, lookback_days)`, registered in both `managers_server.py` and `managers_server_no_roadmap.py`.
- `start-managers-meeting.ps1`: swapped the broken `mcp__claude_ai_Granola__*` connector reference for the new tool in both the allow-list and the dispatch prompt; removed `GRANOLA_API_KEY` from the generated `mcp-config.json` (it reaches the child process via normal inheritance instead — avoids ever writing the key to a workspace file that a failed run could preserve).
- `CLAUDE.md` documents the new primary path; the claude.ai connector reference is kept as a **documented, dormant fallback**, not deleted, per Kevin's explicit instruction.
- `mcp/meeting-connector/fixtures/granola-notes-sample.json` (synthetic — meeting-records is a public repo, no real captured meeting content was committed) + `tests/test_granola_source.py`, 44 tests, all passing.
- Reviewed through **4 Codex passes** (the estate's standing hard cap) — every pass found real issues (missing type/error guards, an overly-permissive match threshold, a tool-registration asymmetry, a plaintext-credential-on-disk risk, unbounded input handling, a malformed-response false-negative, invalid-date handling, a found-with-no-summary ambiguity) — all fixed, all covered by new regression tests.
- Also fixed two **incidental pre-existing bugs**, unrelated to Granola, discovered only because they blocked live verification of this exact change: `start-managers-meeting.ps1`'s `2>` stderr redirect combined with the script's own `$ErrorActionPreference = 'Stop'` was truncating any real child-process failure to a 1-line fragment; `invoke-claude.py` never actually reconfigured its own stdout to UTF-8 despite its docstring promising "lossless ... UTF-8 handling", crashing on any real drafted content containing a character outside the Windows default code page (confirmed live: a plain "→" arrow).

## Live verification (the real proof, not just tests)

Ran the actual launcher for real (not a dry run) against real current data. It called `get_latest_granola_meeting("HR Systems Roadmap")`, scanned 79 real Granola notes across a live 120-day lookback, and found the genuine latest match — a real note titled **"HR Systems Roadmpa 03/07"** (a real typo on Granola's own side, not introduced by this code). It correctly flagged that note as `status=found, hasSummary=true` but **stale** — a 47-day gap against the weekly Friday cadence, matching the 1 August pilot's own independent finding exactly. It then built a genuine, current 7-item draft grounded in real live Work Inbox/Command Centre data (SHSMS tender deadline, WFM/GLAM resolution, DTP1092, the org-structure thread, a flagged PII issue in the Cority thread, DSE Online Assessment, HESA module status) rather than fabricating anything.

**One separate, unrelated issue was found and NOT fixed** — flagged here for whoever picks this thread up next: that same live run's output was rejected by `validate-meeting-result.py`'s own strict format check ("Only 2 exact speaker-note blocks found; minimum is 8"). This is a pre-existing content-formatting strictness issue in the drafting/validation layer, unrelated to Granola. If a full end-to-end launcher run with a passing format validation is wanted, this needs a separate look — likely either a dispatch-prompt formatting instruction tweak, or a validator adjustment, out of scope for this session.

## Next step for whoever picks this up

- The Granola blocker Lauren hit is now genuinely fixed and live on `main`. If Kevin wants Lauren's HELD Managers Meeting brief re-run through this exact launcher path, it will now reach live Granola data correctly — but the unrelated speaker-note-block format-validation issue above would still need addressing first for that specific launcher run to pass its own gate cleanly.
- Lauren's own everyday Fleet-dispatch workflow (how she's actually built every real brief so far) still does **not** have Granola wired in — this session only fixed the launcher path, not Lauren's ordinary dispatch. Whether to wire live Granola into her normal workflow too is a separate decision for Kevin, not yet made.
- `voice-workflows/PROGRAMME_STATUS.md` Phase 5 ("Q&A and acceptance") has been stale since 1 Aug 2026 and was not updated this session — worth a look if picking this programme back up formally.

---

## Prior session context (28 July – 7 July 2026), preserved for reference

The original Voice meeting-prep prototype build (Codex Voice front end, later superseded by the Claude-native front door — see `voice-workflows/docs/decisions/2026-08-01-claude-voice-front-door.md`), Kevin's July leave handover, and the pre-leave action list from that period are archived in this repository's git history (see commit `d382674` and earlier on `main`) rather than repeated here, per this file's own "replace, do not append" convention.
