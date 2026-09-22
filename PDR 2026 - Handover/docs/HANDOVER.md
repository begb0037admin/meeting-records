# HANDOVER — PDR 2026 prep pack — 2026-09-14

## TL;DR
First-ever PDR (Performance Development Review) prep pack, built across two sessions (13–14 Sep 2026): four briefs, one each for Kevin Lelitte, Michael O'Sullivan, James Salas Guillen, and Asta Palmer, all in the same `brief_chrome.py` template style as every other meeting brief. All four dates are now confirmed. Michael's meeting has already happened (14 Sep) and his brief has real 2025-vs-2026 content — his own dedicated handover is `Team 1-1's/Michael/docs/HANDOVER.md` in this repo, read that for his specifics. James's and Kevin's content is thinner (built earlier in the process, before it matured) and worth a quality pass before their real meetings. Three genuine gaps remain open: Kevin's/Asta's 2025 PDR docs unreadable, James's 2025 doc never attempted, and the HR Systems PDR Completion 2026 SharePoint tracker never successfully read. None of this was glossed over — see "Open Gaps" below.

## Standing pattern established this workstream — carry forward
Kevin now uses a `PDR 2026/<Person Name>/` folder structure in his Meetings folder (`C:\Users\admin\OneDrive - Nexus365\Meetings\Meetings\PDR 2026\`; moved there from `D:\OneDrive - lelitte.com\Desktop\PDR 2026\` and `C:\Users\admin\Documents\PDR 2026\` on 21 Sep 2026 -- files merged, the newest copy of each is live and any older copy sits in an `_older versions` folder inside that person's folder; a `Template\` folder and last year's 2025 forms live alongside), one subfolder per person, each containing that person's brief HTML(s). **This is the new standing convention for PDR files going forward** — any future PDR build (this cycle's remaining meetings, or next year's cycle) should write into this structure, not a flat drop into the Meetings folder root (`brief_chrome.write_brief_output` routes `PDR 2026 - <Person>` briefs into `PDR 2026\<Person>\` once the routing change on branch `lauren/meetings-output-routing` is merged). As with every other brief type, the generated HTML itself is never committed to GitHub (ephemeral-output rule) — only this durable handover and the generator script are.

## State of Play, by person

| Person | PDR date | Brief status | 2025 doc | Notes |
|---|---|---|---|---|
| Kevin Lelitte | Confirmed, Thu 30 Sep 2026, with Simon Burford (moved from stale 16 Sep field, confirmed 22 Sep) | Rebuilt 22 Sep with real 2026 content — see 22 Sep update at the end of this file | Confirmed to exist, content blocked (download layer) | Complete and correct on disk; ready for Kevin's review ahead of the 30 Sep meeting |
| Michael O'Sullivan | Already happened, 14 Sep 2026 | Done, real 2025-vs-2026 content | Extracted in full (Kevin dropped the file manually) | Manager Summary still pending — see dedicated handover |
| James Salas Guillen | Confirmed, Mon 21 Sep 2026, 12:00–1:00pm | Built, comparatively thin | Never attempted this cycle | Clears before his 25–28 Sep annual leave |
| Asta Palmer | Thu 1 Oct 2026, 12:00–1:00pm (moved again 22 Sep from Thu 24 Sep, which itself was moved 21 Sep from Fri 25) | Rebuilt 22 Sep | Now in her local folder; read in full 21 Sep | See 22 Sep Asta update at the end of this file |

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

---

## Update — 14 Sep 2026 (later, same day): meeting-flow format extended to all four people

Kevin asked for the same PDR **meeting-flow** format used for Michael's `PDR Review Form - 14-SEP-2026.md` (a single flowing script-style markdown document structured around Oxford's real 6-stage PDR Conversation Guide, weaving in each person's real content as context then giving natural bolded sayable questions, live checkboxes in Section 6, and a one-line Granola pointer at the end — not a reference doc, not blank fields to fill in later) to be applied to James Salas Guillen, Asta Palmer, and Kevin Lelitte himself.

**Source verified directly, not paraphrased from memory:** `PDR Conversation Guide - PDR Refresh - 22.05.2024 v1.docx` (Kevin's Downloads folder) was extracted via its raw `word/document.xml` (python-docx's own paragraph API returned nothing — the guide's content lives in a form that only surfaces through raw XML `w:t` runs, worth remembering for any future Oxford `.docx` extraction). Exact 6-stage question wording confirmed: Check in on workload and wellbeing; Performance/progress; Values; Personal development & career aspirations; Working together; Agree actions and close.

**Built:**
- `PDR 2026/James Salas Guillen/PDR Review Form - 21-SEP-2026.md`
- `PDR 2026/Asta Palmer/PDR Review Form - 25-SEP-2026.md`
- `PDR 2026/Kevin Lelitte/PDR Review Form - 16-SEP-2026.md`

All three saved to their respective Desktop folders and, unlike this repo's usual ephemeral-output rule for generated HTML briefs/decks, **deliberately also committed here** (Kevin's explicit instruction this session: "Commit all three to meeting-records with clear messages") — this is a considered exception for this artifact type (a small, durable, hand-authored-style conversation guide, not a large generated HTML/pptx output), not a silent reversal of the ephemeral-output convention for briefs generally.

**Genuine content gaps found and left honest, not papered over** (per Kevin's explicit instruction not to invent content):
- **James and Asta:** neither brief has any real 2026 self-review content pulled from either of them directly — both HTML briefs' only real material is dated command-centre/work-inbox activity ("Themes to cover for 2026"), which was used for Section 2 (Performance/progress) only. Sections 1 (Workload & wellbeing), 3 (Values), 4 (Personal development), and 5 (Working together) have **no real material to draw on** for either person — each of those sections is flagged plainly in-file ("No 2026 self-review content confirmed for this section yet — check with [name] directly or via Granola before the meeting") and kept to the plain standard guide questions only, not padded with invented personalised detail.
- **James's 2025 doc:** never attempted this cycle (connector-pacing rule) — no 2025 continuity/contrast possible.
- **Asta's 2025 doc:** confirmed to exist (`Asta Palmer - PDR Review.docx`) but content still blocked at the download layer — same result, flagged.
- **Kevin's own brief:** framed as reviewee prep (not questions to ask someone else), per his instruction and the guide's own "whether you are a manager or a colleague" language. Real material exists for Sections 1 and 2 (absence-coverage gaps overlapping his own July leave; the SHSMS resourcing case and his 3 active roadmap rows) — used directly. Sections 3 and 4 have no real material (his 2025 doc is confirmed to exist but content-blocked, same as Asta's) and are flagged the same way. **Reviewer identity is presumed Simon Burford but unconfirmed by any source checked** — flagged explicitly in Section 5 and at the top of the file; worth confirming before or at the start of the meeting.

**Not done / still open:** none of this content-gap work changes the three still-open items from the previous update (Kevin's/Asta's 2025 docs blocked until Oxford's Edu identity is back in use post-1 Oct 2026; James's 2025 doc never attempted; the HR Systems PDR Completion 2026 SharePoint tracker never successfully read). Once any of those unblock, these three new meeting-flow docs should be revisited for real self-review content in Sections 1/3/4/5, not just Section 2.

Commits: `17765933` (James), `903d1d58` (Asta), `bc2c46eb` (Kevin), this file (`PDR 2026 - Handover/docs/HANDOVER.md`) at the commit immediately following.

---

## Update — 14 Sep 2026 (later still, same day): Sections 1/3/4/5 filled from real 2025 transcripts; PDR SOP + canonical guide reference added

The gaps flagged in the previous update above — no 2025 continuity for James, Asta, or Kevin in Sections 1/3/4/5 — are now closed for these three people, **not via the Oxford connector (still blocked, Issue B above), but via Kevin pointing directly at the real recorded meeting transcripts already sitting locally**: `C:\Users\admin\OneDrive - Nexus365\Kevin Lelitte - Transcribed Files\` — `2025__0912_james_PDR.docx`, `2025__0917_Kevin_PDR.docx`, `2025__0922_Asta_PDR.docx`, plus `2025__0930_Micharl_PDR.docx` for Michael (read-only, see below). These are meeting recordings/transcripts, not the written review-form docx files that are SharePoint-blocked — a genuinely different, unblocked source. Unlike the canonical guide (see prior update), `python-docx`'s normal paragraph API worked fine on all four — these aren't Oxford template documents.

**Sections 1, 3, 4, 5 updated with real last-year content, framed explicitly as "last year's discussion" for comparison, in:**
- `PDR 2026/James Salas Guillen/PDR Review Form - 21-SEP-2026.md`
- `PDR 2026/Asta Palmer/PDR Review Form - 25-SEP-2026.md`
- `PDR 2026/Kevin Lelitte/PDR Review Form - 16-SEP-2026.md`

(Section 2 untouched in all three — it already had real 2026 content from the prior pass.)

**Genuine gaps found even with the transcripts as a source — left flagged in-file, not papered over:**
- James: no real depth on the People/Quality values beyond naming them (only Collaboration was elaborated).
- Asta: no Oxford/Professional-Services values-framework discussion at all in her 2025 transcript — Section 3 stays a flagged gap.
- Kevin: same as Asta for Section 3 — no directly-named values discussion; reviewer identity still unconfirmed (the transcript opens mid-conversation, doesn't name them).
- All three: still no 2026 self-review content for Sections 1/3/4/5 — the transcripts only ever supply last-year comparison material, not this year's actual answers. Ask directly in the room.

**Michael O'Sullivan — read-only, per Kevin's explicit instruction not to touch his already-closed docs.** `2025__0930_Micharl_PDR.docx` was read and compared against his finished `PDR Review Form - 14-SEP-2026.md`/`.docx`. Two things worth relaying to Kevin, not actioned:
1. The finished doc's Section 4 line "positive feedback from his Head of Department" and "agreed to explore leadership development" reads a little stronger than the transcript supports — the actual 2025 feedback on the team-lead role was attributed to Marie specifically (not explicitly "Head of Department"), and Michael's own words on leadership/mentoring were tentative ("I wouldn't say no... I'll definitely consider it," "not actively looking," "if something presents itself, I might take it up") rather than an agreed plan. Similarly, "a SQL-training/peer-learning commitment was also agreed" reads as more settled than the transcript shows — Michael has basic SQL from sessions with Simon (also attended by Helen), described himself as "definitely less confident" and open to more, but no firm training commitment was actually agreed in the conversation, just an open discussion.
2. Not in the finished doc, worth having as background even though not actioned: Michael led the mobile app project largely solo last year ("felt like a bit of a one-man band on that one," started as Simon's project then passed to him) — a real achievement not currently referenced anywhere in his 2026 write-up. Also, Michael raised that recorded catch-ups make people more guarded about what they say — a team-culture point, not specific to his own PDR.

**Nothing in Michael's closed files was edited.**

**New process docs added (Job 3/4 of this session):**
- `PDR 2026 - Handover/docs/PDR_SOP.md` — the repeatable PDR prep/run SOP: check the person's real prior-year transcript first (new step, see below), the folder-per-person convention (now under the Meetings folder), building the single six-stage flow doc with real content and never-invented questions, running the meeting from that one file, the post-meeting Granola-to-Manager-Summary step, and a "don't reopen a closed PDR" rule. Matches the existing SOP pattern (`STANDING_AGENDA_SOP.md`, `KPI_RUN_SOP.md`) used elsewhere in this repo.
- `PDR 2026 - Handover/docs/reference/PDR Conversation Guide - PDR Refresh - 22.05.2024 v1.docx` — the canonical Oxford guide itself, copied in from Kevin's Downloads folder (previously only read locally, never placed in the repo). `docs/reference/README.md` added alongside it documenting what it is and the `python-docx`-paragraph-API-returns-nothing extraction gotcha already recorded in the prior update above.
- **New standing step captured in the SOP:** before building any future PDR flow doc, always check `Kevin Lelitte - Transcribed Files` for that person's real prior-year transcript first — richer than the review-form docx summary, and (as this session showed) can be genuinely available even when the review-form docx itself is SharePoint-blocked. Filename pattern is roughly `YYYY__MMDD_<name>_PDR.docx` but isn't perfectly consistent (Michael's real file has a typo, "Micharl").

**Not done / still open:** Kevin's and Asta's *written* 2025 review-form docx files remain genuinely SharePoint-blocked (Issue B above, unchanged) — this session's transcript-based fill is a different, working path around that gap, not a fix for it. The HR Systems PDR Completion 2026 SharePoint tracker (Open Gap #4 above) is still never successfully read. 2026 self-review content for Sections 1/3/4/5 across James, Asta, and Kevin is still genuinely absent — worth asking directly in each real meeting rather than assuming the transcript fill covers it.

Commits: `f2aeb81`/`635b310` (canonical guide docx), `13676eb` (`PDR_SOP.md`), `b56a6ca` (`docs/reference/README.md`), plus updates to the three flow docs above (James, Asta, Kevin) with new commit SHAs on `main`.

---

## Update — 21 Sep 2026: James Salas Guillen brief rebuilt for the real 2026 form; meeting moved to Tue 22 Sep 13:30

**What changed since the 14 Sep entries above:** James's completed 2026 form arrived (saved by him and emailed to Kevin 18 Sep). The PDR meeting itself moved: live calendar data (work-inbox briefing, 21 Sep) shows **Tue 22 Sep 2026, 13:30**, not Mon 21 Sep 12:00 as the earlier briefs said. End time is not in the data; James's email subject still carries the old date. James is off Fri 25–Mon 28 Sep, back Tue 29; Kevin is off Fri 25 Sep. PDRs are due by end of September.

**Built (local Meetings folder only, deliberately not committed — the content names an individual's performance review and this repo is public):**
- `PDR 2026\James Salas Guillen\PDR 2026 - James Salas Guillen - 21-09-2026.html` — standing-format brief on `brief_chrome.py`, replaces the 13 and 14 Sep briefs.
- `PDR 2026\James Salas Guillen\PDR Review Form - 22-SEP-2026.md` — matching meeting-flow note, named for the new meeting date.
- Superseded files (both old HTML briefs and the 14 Sep flow note) are in that person's `_older versions` folder. James's `.docx` forms were not touched.
- The generator was a one-off scratchpad script over `brief_chrome.write_brief_output` (no change to any committed `build_*.py`). `build_pdr_prep.py` regenerates all four people in one run and would overwrite finished briefs, so it was not used.

**Method gotchas worth keeping:** (1) Check the live calendar before trusting any PDR date recorded in an earlier brief. (2) Oxford `.docx` forms: python-docx and lxml tree walks lose content-control text; extracting `w:t` runs per `w:p` with a regex on `word/document.xml` works. (3) Verify the person's own claims against the H&S backlog workbook and the monthly incident statistics (KPI source data) before they go into a Manager Summary. (4) Granola's API history starts 13 Apr 2026; earlier 2026 meetings can't be checked there.

**Open — Kevin's call:** `PDR 2026/James Salas Guillen/PDR Review Form - 21-SEP-2026.md`, `PDR 2026/Asta Palmer/...` and `PDR 2026/Kevin Lelitte/...` are already committed in this public repo and contain personal workload and development detail from the 2025 recordings. The James copy is now superseded and out of date. Not removed or changed here; needs a decision on whether to take these out of the public repo.

**Next concrete action:** Kevin runs the meeting Tue 22 Sep 13:30 from the brief; afterwards the Manager Summary is drafted from the Granola recording (windows: Wed 23–Thu 24 Sep or Tue 29–Wed 30 Sep) and Kevin logs completion in the HR Systems PDR Completion 2026 tracker himself (still unreadable from here). Then Kevin's own PDR folder is the next task. Asta's PDR is booked Fri 25 Sep 12:00, which is Kevin's leave day — flag to Kevin.

---

## Update — 21 Sep 2026 (later): Asta Palmer PDR moved to Thu 24 Sep 12:00

- **Moved** from Fri 25 Sep 12:00-1:00pm to **Thu 24 Sep 2026, 12:00-1:00pm** because Kevin is on annual leave Fri 25 (back Mon 28). Kevin moves the calendar entry himself; the live calendar (work-inbox briefing refreshed 21 Sep 12:25) still showed Fri 25 when the brief was built.
- **Rebuilt (local Meetings folder only, not committed):** `PDR 2026\Asta Palmer\PDR 2026 - Asta Palmer - 21-09-2026.html` and `PDR Review Form - 24-SEP-2026.md`. Superseded versions are in that folder's `_older versions`. Same one-off scratchpad generator pattern as James's; `build_pdr_prep.py` still hard-codes 25 Sep for Asta and regenerates all four briefs, so do not run it.
- **Decision closed (Kevin, 21 Sep):** the PDR `.md` files already in this public repo stay exactly as they are. This supersedes the "Open — Kevin's call" item in the James entry above; do not raise it again. No new PDR personal detail has been pushed here.
- **Not seen:** Asta's 2026 form (nothing in her folder, work-inbox or command-centre as of 21 Sep).
- **Next concrete action:** Kevin moves the calendar entry and confirms Thu 24 12:00 with Asta; James's meeting is first (Tue 22 Sep 13:30); Asta's Manager Summary from the Granola recording on Thu 24 after the meeting or Mon 28-Wed 30 Sep (PDRs due by end of September); Kevin's own PDR folder after that. Full detail is in Lauren's private memory (`memory/pdr-asta-24sep-move.md`).

---

## Update — 22 Sep 2026: Asta Palmer PDR moved again, to Thu 1 Oct 12:00 — flags now open on the deadline and a possible 24 Sep calendar clash

- **Moved again:** Thu 24 Sep 2026, 12:00-1:00pm -> **Thu 1 Oct 2026, 12:00-1:00pm**. Same 12:00 time kept, per Kevin's instruction, since no conflict was found in the sources checked (see caveat below). This is the second move for Asta this cycle (originally Fri 25 Sep). Same day, James Salas Guillen's PDR also moved, to Thu 24 Sep — the date Asta is moving away from — handled as a separate brief by a different agent. Kevin moves the calendar himself; not touched here.
- **Rebuilt (local Meetings folder only, not committed):** `PDR 2026\Asta Palmer\PDR 2026 - Asta Palmer - 22-09-2026.html` and `PDR Review Form - 01-OCT-2026.md`. Superseded versions (21 Sep HTML, 24 Sep flow note) moved into that folder's `_older versions`. Screenshotted at four scroll positions with Playwright's bundled Chromium and visually checked — layout matches the standard `brief_chrome.py` template, banned-string scan clean. Generator is a one-off scratchpad script (`build_pdr_asta_2026_1oct.py`), not committed — same pattern as the 21 Sep rebuild. `build_pdr_prep.py` still hard-codes an earlier date for Asta and regenerates all four briefs; do not run it for one person.
- **New flag, not present before, genuinely material:** command-centre's own tracker task records PDR sessions as due "by end of September 2026." A meeting on Thu 1 Oct now falls **after** that stated deadline. Flagged in the brief (top flag box, at-a-glance table, risks section, to-verify list) — this needs Kevin's decision on whether/how to escalate against the HR Systems PDR Completion 2026 tracker, not resolved here.
- **Calendar conflict check — genuinely could not verify live, said so rather than guessing.** The only calendar source available (work-inbox `data/briefing.json`) was refreshed 21 Sep 12:25, predates this move, only covers a 5-day window through 25 Sep, and does not extend to 1 Oct at all. Also checked work-inbox's `needs_reply.json`/`inbox_suggestions.json`/`triage_ledger.json` and command-centre's `tasks.json` for anything fresher — nothing found. **Kept 12:00 per instruction (no conflict found in what's available), but this is not the same as a confirmed-clear live check** — flagged plainly in the brief rather than asserted either way. Also could not confirm whether James's newly-moved Thu 24 Sep slot collides with Asta's outgoing Thu 24 Sep 12:00 entry until Kevin completes both moves.
- Date-dependent facts that genuinely flipped with the new date (not just cosmetic swaps): the Holiday Records build (started w/c 28 Sep) is now underway by the meeting rather than pending; the ~29 Sep flex-point grace date referenced against that item has now passed; Kevin's Fri 25-Mon 28 Sep annual leave now falls entirely before the meeting rather than after, changing the realistic Manager Summary drafting windows.
- **Not seen:** Asta's 2026 form (nothing in her folder, work-inbox or command-centre as of this rebuild).
- **Next concrete action:** Kevin moves the calendar entry to Thu 1 Oct 12:00 and confirms with Asta; checks whether James's Thu 24 Sep slot and Asta's outgoing Thu 24 Sep entry actually clash once both moves are applied; decides whether the now-after-deadline meeting date needs flagging on the PDR Completion 2026 tracker. Full detail in Lauren's private memory (`memory/pdr-asta-1oct-move.md`).

---

## Update — 22 Sep 2026 (later): Kevin's own PDR — meeting date confirmed 30 Sep 2026; Tableau/SSO removed; Michael O'Sullivan BAU + Emma Fitz-Gibbon evidence added

Direct continuation of the 22 Sep rebuild recorded above ("real 2026 draft replaces blank template"), which had left the meeting date genuinely TBC and flagged two of Simon's three named 2025 Manager-Summary priorities for Kevin as not visibly addressed in the new form. Both are now closed.

- **Meeting date confirmed: Thu 30 Sep 2026, Kevin's PDR with Simon Burford.** No longer TBC. The docx (renamed from the stale `16-SEP-2026` filename to `PDR Review Form - 30-SEP-2026.docx`), the matching `.md` flow note, and the HTML brief's date fields are all aligned to this.
- **Tableau/SSO content removed from the brief**, at Kevin's explicit instruction, reason recorded verbatim: **"I do not administer Tableau."** This was a misattribution correction, not a data gap — the underlying stalled Tableau/SSO item (t033) may still be real, just wrongly attributed to Kevin; don't reintroduce it into his PDR content without checking with him first.
- **Michael O'Sullivan BAU-support evidence added**, sourced from Granola — closes the "supporting Michael's BAU return... uncredited" gap flagged in the prior update.
- **Emma Fitz-Gibbon evidence added**, sourced via the Codex-connector email search — closes the "Emma isn't named anywhere in the 2026 form" gap flagged in the prior update.
- **Standing lesson, recorded because it cost Kevin real frustration:** the first evidence-search pass this session was not scoped to named people up front — Kevin had to ask twice before it was narrowed. Once scoped, it worked. **Future evidence searches for this kind of task (PDR priorities/relationships evidence-gathering) should scope to the relevant named people as the first pass, without being asked** — for this task that list is Simon Burford, Marie Cooksey, Emma Fitz-Gibbon, Athena, Sarah Rowles, Michael O'Sullivan.

**Output files confirmed complete and correct on disk** (local OneDrive, per the ephemeral-output rule — the `.md` flow note is the standing committed exception noted earlier in this handover, though the committed copy in this repo, `PDR 2026/Kevin Lelitte/PDR Review Form - 16-SEP-2026.md`, still carries the old date and was not touched in this checkpoint — see Watch Out For below):
- `PDR 2026\Kevin Lelitte\PDR Review Form - 30-SEP-2026.docx`
- `PDR 2026\Kevin Lelitte\PDR Review Form - 30-SEP-2026.md`
- `PDR 2026\Kevin Lelitte\PDR 2026 - Kevin Lelitte - 22-09-2026.html`
- Old versions (blank-template docx, prior transcript-only/16-SEP-dated md, earlier HTML briefs) archived to that folder's `_older versions`, renamed with clear `superseded-*` naming.

**Watch Out For (new):** the committed `.md` copy in this GitHub repo (`PDR 2026/Kevin Lelitte/PDR Review Form - 16-SEP-2026.md`, committed 14 Sep per the exception above) still carries the old 16-Sep filename/date and has not been re-synced to the 30-Sep content in this checkpoint — this repo's copy is a snapshot from the meeting-flow-format work, not a live mirror of the local OneDrive file, so treat it as stale until someone deliberately re-commits it.

Full session detail: Lauren's own memory, `begb0037admin/lauren` `memory/pdr-kevin-2026-30sep-confirmed-and-evidence-22sep.md`.

**Next concrete action:** Kevin reviews the brief and review form, then attends his 30 Sep PDR meeting with Simon Burford. Post-meeting: Manager Summary drafted from the Granola recording, same pattern as the other PDRs this cycle.
