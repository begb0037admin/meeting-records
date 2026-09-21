# HANDOVER — Michael — 2026-09-14

## TL;DR
Michael O'Sullivan's PDR 2026 happened TODAY (14 Sep), earlier than the original 18 Sep booking. His prep brief is finished with real 2025-vs-2026 comparison content and is filed in `C:\Users\admin\OneDrive - Nexus365\Meetings\Meetings\PDR 2026\Michael O'Sullivan\` (moved there from the Desktop on 21 Sep 2026). **The one thing still outstanding — and the single most important next action on this whole thread — is Kevin completing the Manager Summary section of the real PDR form himself, after he reviews the Granola recording of today's meeting.** That has not happened yet. Granola was unavailable in this session (connector dropped mid-session), so it could not be pulled here.

This file replaces a stale 15 June 2026 scaffold that had nothing to do with PDR — see "Note on this folder's other files" below before assuming `STATUS.md`/`open-actions.md` in this same folder are current or relevant to PDR.

## State of Play
- **Date confirmed:** Michael's PDR ran today, 14 Sep 2026 — confirmed two ways: his own email reply this morning, and the dated current-year form Kevin dropped onto the Desktop (`PDR Review Form - 14-SEP-2026.docx` -- now in `PDR 2026\Michael O'Sullivan\` in the Meetings folder; the older Desktop version is kept in its `_older versions` folder). The original booking was for 18 Sep; it moved earlier, and 14 Sep is the real date, not a typo or conflict to resolve further.
- **Brief status: done.** `PDR 2026 - Michael O'Sullivan - 14-09-2026.html`, in `C:\Users\admin\OneDrive - Nexus365\Meetings\Meetings\PDR 2026\Michael O'Sullivan\` (moved from the Desktop 21 Sep 2026) (per the new standing PDR 2026 folder pattern — see the PDR-2026-wide handover below). Built by `tools/speaking-briefs/build_pdr_prep.py` (`begb0037admin/meeting-records`), same `brief_chrome.py` chrome as every other brief.
- **Real 2025-vs-2026 comparison content, already in the brief:**
  - 2025 achieved: WFM Leave & Absence, Roster, Mobile App, Rolled-Up Holiday Pay all delivered; Staff Request Restructure (CoreHR → PeopleXD Portal); sustained BAU/incident work through the WFM secondment; an Award for Excellence noted by Kevin.
  - 2025 self-review explicitly asked to move into a manager/team-lead role, cited positive Head-of-Department feedback, and Kevin's own matching 2025 agreed action was to explore leadership-development/mentoring opportunities for him.
  - 2025 agreed action also included a SQL-training/peer-learning commitment.
  - 2026 self-review says "happy in current role" — no development ask, no leadership aspiration mentioned, and the SQL-training commitment is never referenced at all. This is a real reversal/apparently-dropped commitment, not just an unanswered box, and both points are flagged as discussion points in the brief (a dedicated cross-reference/risk block plus the "Happy in current role" flag card).
  - Michael's full 2026 self-review (Annual Personal Development Review Form, ~900 words, all sections) was extracted verbatim from a real Oxford mailbox message via the Codex M365 connector's mail domain (which was healthy that morning even while SharePoint was not — see the SharePoint note below).
  - Full detail and the extraction method: `begb0037admin/lauren` `memory/pdr-michael-2025-recap-14sept.md`.
- **2025 review docx source:** Kevin unblocked this himself by dropping `Michael - PDR Review Form 29SEP2025.docx` directly onto the Desktop — not pulled via any connector. This was the right call, and per the SharePoint note below it may be the only reliable path for the other three people's 2025 docs too.
- **Manager Summary — NOT done.** Kevin's own explicit plan is to complete the Manager Summary section of the actual PDR form himself, once he has reviewed the Granola recording of today's meeting. This has not happened as of this write-up. The Granola connector was unavailable this session (dropped mid-session) — it could not be pulled live here, so no attempt was made to draft the Manager Summary content in Michael's brief or anywhere else.

## Note on this folder's other files (found stale, out of scope to fix here)
`docs/STATUS.md` and `docs/reference/open-actions.md` in this same `Team 1-1's/Michael/` folder are still dated 15 June 2026 — they track Michael's regular fortnightly 1-1, a separate thread from PDR, and were not touched this session. They are genuinely stale (last real update predates several months of subsequent work) but updating them is a different task from this PDR handover and was left alone rather than silently rewritten. Flagging so a future session doesn't assume they're current.

## Next Concrete Action
1. Pull the Granola recording/transcript of today's (14 Sep) PDR meeting once the connector is available again.
2. From that, draft the four Manager Summary fields (performance comments, development/support priority comments, agreed actions, final comments) grounded in what was actually discussed — not inferred from the 2025/2026 self-review contrast alone.
3. Drop the drafted Manager Summary into Michael's brief for Kevin to review, before he finalizes the real PDR form docx himself.

## Watch Out For
- Do not draft or guess Manager Summary content from the self-review contrast alone — it must come from the actual 14 Sep meeting (Granola), once available.
- The Granola connector was unavailable this session for reasons unrelated to the Codex M365/SharePoint OAuth issues below — don't conflate the two when picking this back up.
- Michael's own 2025 doc is already fully extracted and in the brief — no further connector work is needed for his 2025 content specifically.
- **Oxford SharePoint / Codex M365 connector — genuine, not-yet-fixed limitation, separate from the (closed) 13–14 Sep token-rotation bug:** a Codex M365 connector call for an Oxford SharePoint file returning `403` then `404` in sequence (or a mail-attachment download hitting `WinError 10061`/`403`/a retry-policy refusal) is a real permission gap, not a transient glitch. 403 = the parked Edu identity (`begb0037@ox.ac.uk`, deliberately out of use until 1 Oct 2026); 404/download-failure = the personal-identity failover genuinely has no access to that specific Oxford resource. This will keep happening for any Oxford SharePoint/attachment resource that needs Edu access until 1 Oct 2026 — it is not something to keep re-attempting. Kevin manually dropping the file (as he did here for Michael's 2025 doc) is the only reliable path before then. Full record: `begb0037admin/agent-commons` `memory/candidate_sharepoint_edu_permission_gap.md`; adjacent: `memory/candidate_codex_edu_connector_deferred_until_1oct.md`; underlying evidence: `begb0037admin/drew` `memory/codex-m365-connector-still-broken-after-cross-machine-fix-14sept.md` and sibling 14 Sep files. This is unrelated to the cross-machine refresh-token-rotation bug (`codex_connector_reauth.ps1`), which is genuinely fixed and closed — see the PDR-2026-wide handover for that distinction.

## Docs Updated This Session
- [x] HANDOVER.md (replaced, this file)
- [ ] STATUS.md / open-actions.md — left untouched, flagged stale above, not in scope for this update
