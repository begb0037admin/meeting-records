# HR Systems Roadmap — Alignment Pass — 27 August 2026

**Type:** Alignment / source-cited change proposal only. **No meeting this cycle, no speaking brief.**
Marie asked Kevin to update the live HR Systems Roadmap master directly, ready for **Friday 28 Aug 2026**.
Kevin hand-enters every approved change into the `.xlsm` himself. Nothing in this document has been written to the roadmap.

---

## 1. Source of truth — verified live

| | Detail |
|---|---|
| **Authoritative master used** | `C:\Users\admin\OneDrive - Nexus365\HR Systems Roadmap Master\HR Systems Roadmap MASTER.xlsm` |
| File modified (local OneDrive) | **2026-08-27 16:24** — actively maintained today |
| md5 (OneDrive copy) | `926b613b47379cc515da73afef7efa13` — read from a scratch copy, original untouched, opened read-only |
| Repo copy is **stale — do not use** | `begb0037admin/hr-projects` → `HR Systems Roadmap/HR Systems Roadmap MASTER.xlsm`, last touched by commit `f16a11a` (2026-06-06 "init: migrate HR project docs from local"), md5 `2a3249d289d8b551b06676596ef0f410`, ~29 KB smaller. It is ~12 weeks behind the OneDrive master. |
| Verdict | The **OneDrive copy is the live master**. A GitHub file existing is not proof it is authoritative — confirmed here it is not. |

**State of the master:** it is *not* stale. ~33 items are `In Progress`; a large number carry `Date last reviewed = 2026-08-21` (aligned to the 21 Aug Roadmap meeting) and several were touched **today, 27 Aug** (rows 133, 143_b, 172_a, 200, 207, 211, DTP1092, CA105_d, CA112, CA129). This is a *gap-filling* pass, not a rebuild.

Sheet read: **`Work Tracker`** (A1:AC269, 268 data rows). Column map: A ID · B Activity · C Phase · G Lead · H Team · M System · P Priority · R Start · S Closed · T Deadline · V Deadline type · W Progress updates (newest first) · X Next steps · Y Date last reviewed · Z Next checkpoint · AA Status · AB Status details · AC % complete.

---

## 2. What was cross-referenced (mandatory 1 Aug 2026 rule)

| Source | Read | Notes |
|---|---|---|
| `work-inbox/data/briefing.json` | Yes — "Thursday 27 August · 12:01" refresh | `needs` / `fyi` arrays scanned for roadmap keywords |
| `work-inbox/data/inbox_suggestions.json` | Yes — generated 2026-08-27 12:00 | `new_tasks` + `applied_updates` |
| `work-inbox/data/needs_reply.json` | Yes | no roadmap-relevant reply items |
| `command-centre/data/tasks.json` | Yes — 83 tasks, parsed open (`done != true`) | richest dated action log |
| Granola meeting notes (`created_after=2026-08-10`) | Yes — 10 notes, key ones pulled in full | **Granola access works this session** via `GRANOLA_API_KEY` |

Granola notes used: *HR Systems Roadmap 21/08*, *Planning for depts move to 38 day balance 19/08*, *SK 1-1 19/08*, *Michael 1-1 20/08*, *HR Systems Managers Meeting 20/08*, *James 1-1 21/08*, *FA Team Catch-up 19/08*, *Sickness Absence Data Catch-up 21/08*, *Sickness Absence Survey working group 25/08*.

**Verified directly:** the master's cell contents; the cross-reference source files above; Granola summaries.
**Taken from documentation (not primary email):** `command-centre` action-log wording (it paraphrases emails). Flagged inline where a proposal rests on it.
**Could not check:** the *original emails* behind command-centre entries (no mailbox access — Lauren never touches Outlook); some 21 Aug handover concerns (see §6).

---

## 3. Per-row change proposals

Format: **Current** = verbatim from the live master. **Proposed** = for Kevin to review, adapt to house phrasing, and hand-enter. Progress lines follow the master's own `DD/MM/YY - …` newest-first style.

### PRIORITY A — Kevin's own lead items

---

#### Row **179** — Migration of HR Reporting Users to SSO  · Lead: Kevin · Status: On Hold

| Field | Current | Proposed |
|---|---|---|
| Date last reviewed (Y) | `2026-07-03` | `2026-08-27` |
| Progress updates (W) — add newest lines | top line is `03/07/26 - Migration … placed on hold until Visual Studio 2022 licences become available …` | Prepend: `25/08/26 - IT Services (Louise Piper) notified OSM users of authentication issues affecting login; may affect migration testing.` and `03/08/26 - Nexus team confirmed the six PeopleXD data access groups populated in Entra ID with the user lists Asta provided on 16 July, advancing SSO migration work.` |
| Status (AA) | `On Hold` | **No change proposed** — but see flag |

**Sources:** `command-centre` t033 action log — `[03 Aug 2026]` (email: Simon Burford — "FW: Creation of your 6 PeopleXD data access groups in Entra ID") and `work-inbox/inbox_suggestions.json` applied_update on t033 — `[25 Aug 2026]` (email: Louise Piper — "OSM: Authentication Issues"). Both are command-centre/inbox-log wording, not primary email.
**FLAG for Kevin:** the "on hold pending Visual Studio 2022 licences" blocker (03/07) has no recorded resolution — confirm whether it still holds. Also two authentication-project call follow-ups are sitting in your inbox (Alex Manton-Jones, 11 Aug and 26 Aug) that may bear on this item.

---

#### Row **136** — PeopleXD Data Protection Impact Assessment  · Lead: Kevin · Status: In Progress · **Deadline 2026-08-31**

| Field | Current | Proposed |
|---|---|---|
| Date last reviewed (Y) | `2026-08-21` | `2026-08-27` |
| Progress updates (W) — add newest line | `21/08/26 - Pilot of Soundcloud now in place.` | Prepend: `27/08/26 - Kevin shared updated DPIA v0.5 for Marie's review / Stage 7 sign-off.` |
| Status details (AB) | `On Target` | **Kevin to decide** — deadline is 31 Aug and the doc is still awaiting Marie's signature; consider `At risk` if sign-off will not land by then |

**Sources:** `command-centre` t009 / `work-inbox/inbox_suggestions.json` applied_update — `[27 Aug 2026]` (email subject: 'Kevin Lelitte shared "PeopleXD - Data Protection Impact Assessment v0.5" with you', 27 Aug 08:50). Granola *Roadmap 21/08*: "People XD DPIA: on Marie's list; health and safety questionnaire took priority; SoundCloud pilot now in place" — consistent with current text.
**Do not conflate:** `command-centre` t2608111719551 ("Review updated DPIA and DPS documents for college record to PXD", Anne Mortimer, 11 Aug) is the **DTP1092 college-record DPIA**, a different document — not row 136.

---

#### Row **DTP1334** — Health & Safety Management System  · Lead: Kevin · Status: In Progress

| Field | Current | Proposed |
|---|---|---|
| Next checkpoint (Z) | `2026-08-27` (today — now stale) | Roll forward to the early-September project-board shortlisting date (Kevin to set; ~`2026-09-11`) |
| Deadline (T) | `2026-09-25` | **No change** — already correct (workstream moved to 25 Sept) |
| Progress updates (W) | `21/08/26 - Kevin and Marie have reviewed 6 supplier questionnaires and forwarded their findings … extended this phase … to end of September.` | Optionally append detail: `Scoring inconsistencies found and corrected; possible prior-knowledge bias on one supplier noted to the project board. Project board aggregates scores and shortlists in early September; supplier workshops begin 25 Sept.` |

**Sources:** Granola *HR Systems Roadmap 21/08* ("Health and Safety Module Supplier Evaluation" section). `command-centre` t2608131801210 / t2608131801211 (DTP1334 supplier evaluation, 21 Aug deadline).
**Related but separate items:** IRIS funding is approved but no PO raised (Granola *James 1-1 21/08*) — that belongs on **t017 / IRIS**, not DTP1334.

---

### PRIORITY B — items Kevin contributes to where the master is behind

---

#### Row **CA104_2526 — "August update"** — Hierarchy Restructuring  · Lead: FA, HRA · Status: Scheduled · **Deadline 2026-09-09**

**Current:** Progress updates (W) **empty**; Next steps (X) **empty**; Date last reviewed (Y) **empty**; Next checkpoint (Z) `2026-08-28`; Start `2026-08-17`.

**Proposed Progress updates (W):**
```
27/08/26 - To be actioned via the Portal (first time; previously back office). U environment confirmed safe to use; C environment cloned/replicated. Documentation to be updated alongside. Team catch-up planned w/c 1 Sept.
19/08/26 - Draft University PACS Organisational Structure update circulated (orgstructure@admin.ox.ac.uk, 12 Aug; forwarded by Simon 18 Aug): wholesale move of College / Society entities from PACS level 2 to level 3, plus a Subsidiary Companies correction. Separately, three new PACS management units to be created for the HR Systems reorg.
```
**Proposed Next steps (X):**
```
- Kevin to review the PACS level 2 -> 3 draft for HR Systems implications.
- Create the three new PACS management units via the Portal.
- Update related guidance / documentation.
- Team catch-up w/c 1 Sept.
```
**Proposed:** Date last reviewed (Y) → `2026-08-27`.

**Sources:** Granola *SK 1-1 19/08* ("three new pack [PACS] management units to be created … Portal approach … safe to use U environment; C environment cloned and replicated"); Granola *Michael 1-1 20/08* ("Org structure work coming up: first time on the portal … team catch-up week after next"). `command-centre` task-1787072363309 ("URGENT — Organisational Structure Update - August 2026 - FINAL") and t2608121801282 (email: Simon Burford — "FW: Organisational Structure Update - August 2026 - DRAFT", 18 Aug). `work-inbox/briefing.json` `needs`: "RE: Org Structure Update" from Organisational Structure, 19 Aug, to Kevin & Simon.
**FLAG for Kevin:** (1) Confirm CA104_2526 "August update" is the right home for **both** the routine reorg **and** the University-wide PACS level 2→3 college move, or whether the PACS move needs its own row. (2) The 21 Aug handover also cited a *Sarah Rowles HESA-timing question* and an *H&S dashboard org-mapping risk* tied to this — **neither is corroborated in this cycle's inbox / command-centre / Granola data** — confirm whether they are real and need capturing here.

---

#### Row **208** — Migrating departments onto 38 day balances  · Lead: Julie · Team: Kevin, Simon, Michael, Marie C · Status: In Progress

**Current:** Progress updates (W) **empty**; Date last reviewed (Y) `2026-07-30`; Next steps (X) = `- Julie to ocntact departments … - Kevin to update balance/workgroup configuration - Kevin to discuss what steps need to take place with Michael`; Deadline (T) `2026-09-30`; Next checkpoint (Z) `2026-08-28`.

**Proposed Progress updates (W):**
```
27/08/26 - Chemistry (first to request) compiling its work-group list; 131 work groups identified for amendment (Michael, 27 Aug). Marie reviewing effort with Kevin in Julie's absence.
20/08/26 - Michael 1-1: target update window 1-2 Oct, ahead of 7 Oct rollover; work-group holiday-scheme swap is a single field update per work group (~1-2 min each), can only run after leave-year end.
19/08/26 - Planning meeting (Julie / Kevin / Simon / Michael). Chemistry proceeding; Maths advised to pause until next leave year; Biology declined (too late this year); GLAM (large, complex rosters) on hold pending Chemistry's work-group count. Treated as a pilot, not a standard service. Departments to submit work-group lists by 28 Aug; Kevin to update the holiday scheme per confirmed work group from 5 Oct.
```
**Proposed Next steps (X):**
```
- Departments to submit work-group lists (code + description) by 28 Aug.
- Kevin to update the holiday scheme attached to each confirmed work group from 5 Oct, priority order by submission date, liaising with Michael on mechanics.
- Brief first-line support (Emma) ahead of the Oct rollover for staff unable to book bank holidays.
- Julie to send a summary email to all departments (cc Kevin, Simon) as the shared thread.
- Revisit a charging mechanism for future years (GLAM offered to pay; none in place).
```
**Proposed:** Date last reviewed (Y) → `2026-08-27`; Next checkpoint (Z) → `2026-10-02`.

**Sources:** Granola *Planning for depts move to 38 day balance 19/08* (full detail, incl. rollover 7 Oct, work starts 5 Oct, 28 Aug submission deadline, pilot framing, GLAM/Maths/Biology positions); Granola *Michael 1-1 20/08*. `command-centre` t2608111507360, t2608121801280, t2608181501150, t2608270801360 (`[27 Aug]` Marie forwarding Chemistry's request), inbox_suggestions applied_update t2608191643001 (`[27 Aug]` Michael — "131 workgroups"). `work-inbox/briefing.json` `needs`/`fyi`: Julie Hickman 19–20 Aug ("38 day balance … decisions needed", department contacts), Marie Cooksey 26 Aug ("FW: changing to 38 day balance - workgroups for updating"), Michael O'Sullivan 27 Aug ("it is the 131 workgroups listed that will need to be amended").
**Do not conflate** with row 72 (Clinical Pay Uplift 2024 — Complete), row 184 (automatic carry-over — Not Delivered), or CA138_a (UCEA main uplift). These are separate.

---

#### Row **CA138_a** — UCEA Main Pay Uplift  · Lead: Athena · Team: Michael · Status: Pending/Expected

| Field | Current | Proposed |
|---|---|---|
| Progress updates (W) | `16/07/2026 - Planning meeting … sketched out timeframe for Sept implementation …` | Prepend: `20/08/26 - Non-clinical (main) uplift delayed pending union decision; October implementation ruled out (payroll increments that month); November or later now more likely. September decision point flagged by Jessica Oldershaw.` |
| Date last reviewed (Y) | *(blank)* | `2026-08-27` |

**Sources:** Granola *Michael 1-1 20/08* ("Non-clinical pay uplift (2%) delayed pending union decision; October ruled out … November or later more likely"). `command-centre` t2608121801281 ("Review PeopleXD uplift timeline from Jessica Oldershaw … September decision point").

---

#### Row **DTP1092** — Research management data for REF and research quality  · Team incl. Kevin · Status: In Progress

This row was reviewed today (Y = `2026-08-27`) and its multi-company content is current. **One alignment point only:**

- The **ORCID sub-thread** carried inside this row has an open action assigned to Kevin — Next steps (X) `====ORCID====` section: *"Research Services have provided requirements for how they want the ORCID page to be updated. Kevin to take this forward."* — with progress lines `30/07/26 - ORCID requirements have been passed back to Kevin to take forward.` and `24/04/26 - Decision made … amend the existing tile and the audience …`. **No progress recorded on the ORCID action since 30/07/26**, and it appears nowhere in command-centre, work-inbox, or any Granola note from 10–27 Aug (checked directly).
- **Proposed:** Kevin to add a dated progress line reflecting the true current state of the ORCID page update (he holds that knowledge), or confirm at FA Catch-up that it remains open and un-started. Per carry-over rules this is surfaced, not closed.
- **Data-quality fix:** Deadline (T) is the text string **`31/09/2026`** — an invalid date (September has 30 days). Suggest correcting to `30/09/2026`.

**Sources:** live master DTP1092 cells W and X; `HR Systems Roadmap - Handover/docs/HANDOVER.md` (2026-08-21) which first raised the ORCID-sequencing gap; absence confirmed by direct search of the cross-reference sources.

---

### PRIORITY C — empty "New" rows that need a decision

---

#### Row **198** — WFM Remaining departments go live  · Status: New · all fields empty

**Evidence it is live:** Granola *Sickness Absence Survey working group 25/08* — "3 departments not yet migrated to People XD: SBS, Paediatrics, and GLAM." Granola *Managers Meeting 20/08* — "confirmation needed that all departments are on board for October go-live; Kevin to be invited to the next WFM meeting." `command-centre` t035 ("WFM / GLAM Rostering — set up resolution meeting … Three areas … outstanding: SBS, PEDS, GLAM").

**Proposed (if Kevin confirms this row belongs on the roadmap and this is its scope):**
- Description (D): `Complete WFM go-live for the departments still outside PeopleXD / WFM: SBS, Paediatrics, GLAM.`
- Status (AA): `In Progress` · System (M): `WFM`
- Progress (W): `25/08/26 - 3 departments still to migrate: SBS, Paediatrics, GLAM. Outstanding backdated-sickness data loads ("Upload 2") are tied to this. / 20/08/26 - Managers meeting: confirmation needed that all departments are on board for October go-live; Kevin to be invited to the next WFM meeting.`
- Next steps (X): `- Kevin to attend the next WFM project meeting. / - Resolution meeting to be set up (Kevin, Simon, Marie, Michelle, +/- Julie) on outstanding loads for SBS / PEDS / GLAM.`

**FLAG:** WFM go-live may be owned by a separate project outside the HR Systems Roadmap — Kevin to confirm whether row 198 should be populated or removed. Overlaps with the sickness-absence data-gap work (see §4).

---

#### Row **199** — Botanic Gardens Rostering set up  · Status: New · all fields empty

**Evidence:** `command-centre` t2608181201061 ("Resolve GLAM rostering requirements — Botanic Gardens Ticket Office and Ashmolean Security", email from Anna Carter-Windle, Kevin bumped 19 Aug). Granola *FA Team Catch-up 19/08* ("two areas in Glam … where annual leave through WFM isn't working … exploring whether rostering would help"). Granola *Planning for depts move to 38 day balance 19/08* ("Glam rostering issue is a separate, larger piece of work: not resourced to take on now … significant BA and implementation work … Glam will need to wait").

**Proposed (if Kevin confirms scope):**
- Description (D): `Set up WFM rostering for GLAM Botanic Gardens Ticket Office and Ashmolean Security, where annual leave via WFM does not work for concentrated / non-standard shift patterns.`
- System (M): `WFM` · Status (AA): `On Hold` · Status details (AB): `On Hold - Work Deprioritised`
- Progress (W): `19/08/26 - Raised via Anna Carter-Windle (GLAM). Considered during 38-day balance planning; significant BA and implementation effort. Team capacity stretched — position is that GLAM rostering waits. Separate, larger piece of work from the 38-day balance change.`
- Next steps (X): `- Requirements gathering with the GLAM Gardens team when resource allows.`

**FLAG:** Kevin to confirm row 199's intended scope and that it does not duplicate row 198 or belong under an existing GLAM/WFM item.

---

### PRIORITY D — stale checkpoints / smaller updates (Kevin's call)

| Row | Observation | Suggested |
|---|---|---|
| **176** — Rollout of ER Case Management to Departments | Next checkpoint (Z) `2026-06-26` is stale; W says "support model due to be reviewed on 30/07, Kevin will be attending" — that review has passed with no recorded outcome | Kevin to add the 30 Jul review outcome and roll Z forward, or confirm Status stays `On Hold` pending Issy Stokoe |
| **192_a** — New annual leave duty from 6 April 2026 (report build) | Already current (Y `2026-08-21`, notes Kevin's AG scoping-call request). Only gap: the Access Group build has a reference — case `69001638`, ~2,800 flex points, 3 reports (Annual Leave Record by Person + 2) — not captured | Optionally add the case ref for precision. Confirm the "Holiday Records 3 Reports" AG build and 192_a's "report build" are the same deliverable (they appear to be) |
| **CA102_2526** — Annual Leave Year End Rollover 2026 | Progress (W) is just `October` | Optionally add from Granola *Michael 1-1 20/08*: `20/08/26 - ~80 balance calendars being manually extended per environment (U done, Z in progress, then C, then live). Rollover runs from Mon 5 Oct once the prior leave year is locked; run in one test env first, then live, then remaining test envs.` |
| **ITS214** — ORCID via onboarding | Status `Complete` but last note (21/02/2025) still asks "a tile has been created — is this live?"; live ORCID tile work now sits inside DTP1092 | Leave as `Complete` (carry-over rules: never propose un-completing). Noted for awareness only — the open ORCID work is tracked on DTP1092 |

---

## 4. New candidate items — proposals only, not decided

Surfaced from cross-reference; **not** presented as agreed additions. Kevin decides whether any becomes a roadmap row.

1. **Quality System funded consultant work (Cority / EcoOnline)** — funds approved; PO £4,500 received 17 Jul; agreed consultant priority order: Compliance reports → Primary job positions / business rules → Teams/Outlook integration → Health surveillance business rules & subquery optimisation. *Sources:* Granola *James 1-1 21/08*; `command-centre` t1781099896490, t2608251201190 (Sophie Levy, PO E22033553), t017. May warrant its own H&S line, or a phase under an existing IRIS/Cority item.
2. **Sickness-absence WFM data-gap remediation** — "Upload 2" backdated sickness data (~2,859 rows) never loaded for SBS / Paediatrics / GLAM; 45 departments show zero sickness records; Marie seeking a funded BA (Mel) recharged to SBS/Paediatrics; target data loaded by 25 Sept ahead of the ~9 Oct UCEA survey. *Sources:* Granola *Sickness Absence Data Catch-up 21/08* and *Sickness Absence Survey working group 25/08*; `command-centre` task-1787652746063 / task-1787652746064. Currently only implied under `148_b` (UCEA Sickness Absence Survey) — Kevin to decide if the data-remediation needs its own visible line.
3. **Application form — internal-candidate identification / "Do you work for Oxford University?" question split** — request from Laura Porter / Phil Taylor; to be t-shirt-sized with Michael, then Marie decides whether to progress. *Sources:* Granola *SK 1-1 19/08*, *Michael 1-1 20/08*; `command-centre` t2608191801190, t2608201500590. **Pre-decision** — likely too early for a roadmap row; watch item.
4. **Auto job-alert notification email — text changes (Laura Porter)** — approved Feb 2026, implementation stalled. *Source:* `command-centre` task-1787044968753. Small, but has been open a long time.

---

## 5. Explicitly NO CHANGE — already aligned

The following active items carry `Date last reviewed = 2026-08-21` or `2026-08-27` and their content matches the 21 Aug Roadmap meeting / current cross-reference data. **No change proposed:**

`196_a` EVO · `197_a` Eploy · `174_b` H&S dashboards · `187` REF Substantive link dataset · `173` Workforce Profile Dashboard · `48` Applicant cleardown · `133` FTC Monitoring by person Dashboard · `172_a`/`172_b` Athena Swan redevelopment · `143_a`/`143_b` Resourcing Dashboard migration · `177` ER Case Management Institutional Reporting · `178` HESA Staff Consultation Outcomes (correctly shows review resuming late Nov) · `183` Sickness Absence Dashboard · `191` REF SPRE · `192_b` annual leave insight report (Henry) · `148_b` UCEA Sickness Absence Survey (has 25 Aug note) · `200` DWH Fabric Migration · `202` Fire Risk Assessment Dashboards · `207` Volunteering leave → employee-bookable (reviewed today, "ready for UAT") · `CA105_d_2526` HESA Staff Return 2025/26 · `CA108`/`CA112`/`CA129` year-end HRA items · `DTP1211` ORMS · `DTP1092` multi-company content (ORCID sub-point excepted, §3) · `UOX008` Data Platform · `211` EDI leadership-training analysis (added today).

Long-dormant `On Hold` items (rows 5, 36, 40, 53, 67, 79, 83, 94, 110, 119, 120, 130, 149, 151, 18_g, 22_c/d, 23_c, 68_b, 80_b, 86_a, etc.) — no new evidence of movement in any cross-reference source; **no change**.

---

## 6. Gaps / could not verify

| Item | Status |
|---|---|
| OneDrive master access | **OK** — read live |
| Granola access | **OK** — API reachable via `GRANOLA_API_KEY`; 10 notes since 10 Aug retrieved |
| command-centre / work-inbox | **OK** — local copies current (git HEAD 2026-08-27) |
| Original emails behind command-centre entries | **Not accessible** — no mailbox access; command-centre log wording is a paraphrase, flagged inline |
| 21 Aug handover's *Sarah Rowles HESA-timing question* on the org-structure change | **Not corroborated** in this cycle's sources — Kevin to confirm if real |
| 21 Aug handover's *H&S dashboard org-mapping risk* | **Not corroborated** in this cycle's sources — Kevin to confirm if real, and where it should be captured (CA104_2526 or 174_b) |
| DTP1092 ORCID onboarding-*sequencing* point (27/02/26: "where it appears in the onboarding list") | No later resolution found in the master or any source — open, surfaced not closed |

---

## 7. Next action & checkpoint

**Exact next action:** Kevin reviews §3–§4 above and hand-enters the approved rows into
`C:\Users\admin\OneDrive - Nexus365\HR Systems Roadmap Master\HR Systems Roadmap MASTER.xlsm`,
ready for Friday 28 Aug 2026. Nothing here has been written to the roadmap or to `hr-projects`.

**Blockers / notes for the record:**
- Repo copy of the master in `hr-projects` is ~12 weeks stale — anyone reading it will get wrong facts. (Not Lauren's to fix; flag to whoever owns `hr-projects` hygiene.)
- `roadmap-items.json` / `build_roadmap.py` were **not** used or touched — the 21 Aug pipeline-freeze on `tools/speaking-briefs/build_roadmap.py` is untouched and still stands. This pass read the master directly.

**Read-only compliance:** `hr-projects` and both `.xlsm` copies were opened read-only from scratch copies. The only write this session is this checkpoint document.
