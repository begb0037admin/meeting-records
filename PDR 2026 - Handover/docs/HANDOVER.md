# HANDOVER — PDR 2026 prep pack — 2026-09-14

## TL;DR
First-ever PDR (Performance Development Review) prep pack, built across two sessions (13–14 Sep 2026): four briefs, one each for Kevin Lelitte, Michael O'Sullivan, James Salas Guillen, and Asta Palmer, all in the same `brief_chrome.py` template style as every other meeting brief. All four dates are now confirmed. Michael's meeting has already happened (14 Sep) and his brief has real 2025-vs-2026 content — his own dedicated handover is `Team 1-1's/Michael/docs/HANDOVER.md` in this repo, read that for his specifics. James's and Kevin's content is thinner (built earlier in the process, before it matured) and worth a quality pass before their real meetings. Three genuine gaps remain open: Kevin's/Asta's 2025 PDR docs unreadable, James's 2025 doc never attempted, and the HR Systems PDR Completion 2026 SharePoint tracker never successfully read. None of this was glossed over — see "Open Gaps" below.

## Standing pattern established this workstream — carry forward
Kevin now uses a `PDR 2026/<Person Name>/` folder structure on his Desktop (`D:\OneDrive - lelitte.com\Desktop\PDR 2026\`), one subfolder per person, each containing that person's brief HTML(s). **This is the new standing convention for PDR files going forward** — any future PDR build (this cycle's remaining meetings, or next year's cycle) should write into this structure, not a flat Desktop drop. As with every other brief type, the generated HTML itself is never committed to GitHub (ephemeral-output rule) — only this durable handover and the generator script are.

## State of Play, by person

| Person | PDR date | Brief status | 2025 doc | Notes |
|---|---|---|---|---|
| Kevin Lelitte | Confirmed, 16 Sep 2026, 15:00–16:00 | Built, comparatively thin | Confirmed to exist, content blocked (download layer) | Closest upcoming meeting of the three still ahead — worth a quality pass first if time allows |
| Michael O'Sullivan | Already happened, 14 Sep 2026 | Done, real 2025-vs-2026 content | Extracted in full (Kevin dropped the file manually) | Manager Summary still pending — see dedicated handover |
| James Salas Guillen | Confirmed, Mon 21 Sep 2026, 12:00–1:00pm | Built, comparatively thin | Never attempted this cycle | Clears before his 25–28 Sep annual leave |
| Asta Palmer | Confirmed, 25 Sep 2026, 12:00–1:00pm | Built | Confirmed to exist, content blocked (download layer) | — |

## Build history
- `tools/speaking-briefs/build_pdr_prep.py` added — commit `928c816` (13 Sep 2026), README documented — commit `d2797c4`.
- Second-pass fill-in for Kevin/James/Asta (James's date found, Kevin's/Asta's 2025 docs confirmed-to-exist-but-blocked) — commit `2e913e6`, README updated — commit `8e76183`.
- Michael's 2025-vs-2026 real content added, after Kevin manually unblocked the source docx — commit not listed by short SHA in this handover's source brief but recorded as `4bc2c9c` in Lauren's own memory (`memory/pdr-michael-2025-recap-14sept.md`); README corrected same day (`5db9f9821963b7664dd9800dd8c5276fa23cfbe8`) to stop claiming the 2025 doc "was pulled for real via the connector" — it wasn't, Kevin's manual drop unblocked it.
- Full session-by-session detail lives in Lauren's own memory: `begb0037admin/lauren` `memory/pdr-2026-first-build.md`, `memory/pdr-2026-second-pass-14sept.md`, `memory/pdr-michael-2025-recap-14sept.md`.

## Open Gaps — genuine, not glossed over

1. **Michael's Manager Summary.** The single most important open item on this whole workstream. Kevin will complete it himself once he's reviewed the Granola recording of today's (14 Sep) meeting — not done yet, Granola was unavailable this session. Full detail and next steps: `Team 1-1's/Michael/docs/HANDOVER.md`.
2. **Kevin's and Asta's 2025 PDR docs.** Both confirmed to exist (found by name/date/size via mail search) but content extraction has failed every attempt at the download layer (`WinError 10061`, `HTTP 403`, a Codex retry-policy refusal). **This is now understood to be a genuine Oxford SharePoint/Edu-identity permission gap, not a transient glitch — see the dedicated section below.** James's 2025 doc was never attempted at all this cycle (one bounded connector pass per pacing rules) — worth trying, but expect the same wall.
3. **James's and Kevin's brief content is comparatively thin.** Both were built in the 13–14 Sep second pass, before the process/lessons that shaped Michael's much richer brief had landed. Worth a content quality pass before their actual meetings if there's time — Kevin's (16 Sep) is the more urgent of the two given it's soonest.
4. **HR Systems PDR Completion 2026 tracker (SharePoint).** Never successfully read this workstream — a separate, unresolved connector/permissions issue, distinct from both the SharePoint-permission gap below and the (closed) token-rotation bug. Not investigated further this session; flag to Drew if it's needed before the remaining three meetings.

## Oxford SharePoint / Codex M365 connector — two genuinely separate issues, do not conflate

**Issue A — cross-machine refresh-token rotation collision. CLOSED, fixed 14 Sep 2026.** Broke 13 Sep with `oauth_token_invalid_grant`/`TRIGGER_REAUTHENTICATION` on the personal identity (`kevin@lelitte.co.uk`). Root cause: the same refresh token was held independently by three live things at once (desktop CLI store, a long-running Codex Desktop Electron process, and the Oxford laptop's own failover profile) — whichever refreshed first invalidated the others via standard OAuth rotation. Fixed via `codex_connector_reauth.ps1` in `begb0037admin/work-inbox`: kills stale processes on both machines over SSH, does a single fresh login on the desktop, propagates the resulting `auth.json` to the Oxford laptop, verifies both independently. **Confirmed working live on both machines as of 14 Sep 2026.** Full root-cause writeup: `begb0037admin/drew/memory/codex-m365-connector-cross-machine-root-cause-13sept.md`; closure record: local session memory `codex-connector-cross-machine-fix-closed.md`.

**Issue B — Edu-identity permission gap on specific Oxford SharePoint libraries/attachments. NOT fixed, will not self-resolve before 1 Oct 2026.** Discovered the same day, initially mistaken for a continuation of Issue A. A Codex M365 connector call for an Oxford SharePoint file returning `403` then `404` in sequence (as hit pulling Michael's 2025 PDR docx before Kevin's manual drop unblocked it) — or a mail-attachment download hitting `WinError 10061`/`403`/a retry-policy refusal (as hit on Kevin's and Asta's 2025 docs this cycle) — is a genuine permission/entitlement issue, not a random or transient download glitch:
- `403` = the request hit the parked Edu identity (`begb0037@ox.ac.uk`), which is deliberately out of usage until 1 October 2026 per Kevin's own explicit decision (not a bug — see `begb0037admin/agent-commons/memory/candidate_codex_edu_connector_deferred_until_1oct.md`).
- `404` (or the mail-attachment download failure modes) = the personal-identity failover then picks up the request but genuinely has no permission to that specific Oxford resource at all — a real access-denied, not "file not found."
- **This will keep happening for any Oxford SharePoint file or attachment that needs Edu access, for as long as Edu stays parked (until 1 Oct 2026).** It is not something to keep re-attempting with new phrasing or retry loops — Codex's own risk-guard will in fact block a second raw download attempt after any failed one as "policy circumvention," so there is no in-session workaround either.
- **The only reliable path before 1 Oct 2026 is Kevin pulling the affected file himself and dropping it in manually** — exactly as he did for Michael's 2025 doc. This should be treated as the default plan for Kevin's, Asta's, and (if attempted) James's 2025 docs, and for the PDR Completion 2026 tracker if that turns out to be Edu-gated too.
- Full record, pushed to `agent-commons` this session so any agent hitting Oxford SharePoint knows about it (not just this repo): `begb0037admin/agent-commons/memory/candidate_sharepoint_edu_permission_gap.md`, cross-referenced from `agent-commons/MEMORY.md` and `memory/index.json`. Underlying technical evidence: `begb0037admin/drew/memory/codex-m365-connector-still-broken-after-cross-machine-fix-14sept.md`, `memory/codex-m365-mail-attachment-download-winerror-10061-14sept.md`, `memory/codex-m365-mail-domain-independently-healthy-plus-attachment-fetch-gotchas-14sept.md`.
- **Re-check after 1 October 2026** once the Edu identity is expected back in normal use — do not assume this is still blocked past that date without a fresh live check.

## Next Concrete Action
1. Michael's Manager Summary (see his own handover) — highest priority, blocks finalizing his real PDR form.
2. Content quality pass on Kevin's brief before 16 Sep, and James's before 21 Sep, if time allows.
3. Retry Kevin's/Asta's 2025 docs (and attempt James's for the first time) only via Kevin manually dropping the files — do not re-attempt the connector path before 1 Oct 2026 per the permission gap above.
4. Flag the HR Systems PDR Completion 2026 SharePoint tracker to Drew if it's needed before the remaining meetings — never successfully read this workstream, cause not yet diagnosed.

## Watch Out For
- Don't conflate Issue A (closed) and Issue B (open) above — a future session seeing "connector fixed 14 Sep" in passing must not assume SharePoint/attachment pulls for Oxford files are unblocked in general.
- Don't re-attempt the connector path for Kevin's/Asta's/James's 2025 docs before 1 Oct 2026 — it's expected to fail the same way every time until then.
- Michael's brief and Desktop file were verified byte-identical before/after the shared `build_pdr_prep.py` script was rerun for the other three people — the shared script running again does not silently touch an already-finished person's output, but always worth a diff-check after any future shared rerun.
- The `PDR 2026/<Person>/` Desktop folder structure is the standing convention now — don't drop a future PDR brief flat on the Desktop.

## Docs Updated This Session
- [x] `PDR 2026 - Handover/docs/HANDOVER.md` (this file, new)
- [x] `Team 1-1's/Michael/docs/HANDOVER.md` (replaced stale June scaffold)
- [x] `begb0037admin/lauren` `MEMORY.md` + new memory file (see below)
- [x] `begb0037admin/agent-commons` `MEMORY.md`, `memory/index.json`, new candidate file — SharePoint Edu-permission-gap finding pushed cross-agent
