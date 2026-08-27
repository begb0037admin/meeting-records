# HR Systems Roadmap — Alignment Pass — 27 August 2026

**Type:** Alignment / source-cited change proposal only. **No meeting this cycle, no speaking brief.**
Marie asked Kevin to update the live HR Systems Roadmap master directly, ready for **Friday 28 Aug 2026**.
Kevin hand-enters every approved change into the `.xlsm` himself. Nothing in this document has been written to the roadmap.

> **Follow-up sections added 27 Aug (later):** §8 when the roadmap was genuinely last updated (evidence, not assumption) · §9 full before/after table (verbatim current cell content vs proposed) · §10 owner-coverage sweep of all 268 rows for Kevin / Simon / Marie / Michael / James / Asta · §11 rows added to the proposal from that sweep (204, 183, ITS960) plus owner flags.

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

---

## 8. When was the roadmap genuinely last updated?

Determined from evidence, not assumption. Three signals checked: every row's `Date last reviewed` (col Y), every dated `DD/MM/YY -` line in the Progress column (col W), and the file's modified time.

### The master is updated ROLLING, not once per cycle

There is no single "last updated" date for the sheet. Rows are stamped **individually** with their own `Date last reviewed`. The `Y` values span ~90 distinct dates from Feb 2024 to today; **25 active rows** carry a blank or pre-July 2026 review date.

### Most recent update pass: today, Thursday 27 Aug 2026

- **10 rows** carry `Date last reviewed = 2026-08-27` AND a matching `27/08/26 -` Progress line: **133** (FTC Monitoring), **200** (DWH Fabric), **207** (Volunteering leave), **DTP1092**, **143_b** (TA Dashboard), **172_a** (Athena Swan), **CA105_d_2526** (HESA Staff Return), **CA112_2526** (Year-End Reporting), **CA129_2526** (PSED datasets), **211** (EDI leadership analysis — a brand-new row).
- OneDrive file modified time: **2026-08-27 16:24**.
- **Conclusion:** someone (Simon and/or Kevin — content is dashboards / HESA / REF / FA items) worked a batch of rows into the master **earlier today**, ahead of the Friday deadline. This is the current baseline.

### Last full cycle before that: the 21 Aug 2026 Roadmap meeting

- **14 rows** at `Date last reviewed = 2026-08-21`; **12** also have a `21/08/26 -` Progress line: 196_a, 197_a, 174_b, 192_a, 187, 173, 136, 177, 178, 192_b, 143_a, 148_b, CA108_2526, DTP1334.
- Matches the Granola note *HR Systems Roadmap 21/08* — a genuine, logged cycle.

### Was a cycle skipped? Yes — Friday 22 Aug.

- **No row anywhere** carries a `Date last reviewed` or Progress line dated 22, 23 or 24 Aug 2026. The Roadmap meeting runs weekly on Fridays (`meeting-records/CLAUDE.md`); the **Friday 22 Aug cycle produced no roadmap updates** — it either did not run or nothing was logged.
- The only touch between 21 Aug and today was one `25/08/26 -` line on **148_b** (from the 25 Aug Sickness Absence Survey working group).
- The repo's own meeting-outcome record also stops earlier: the last `Meeting Reviews/HR Systems Roadmap — DD-MM.md` is **`— 03-07.md` (3 July 2026)**. Nothing captured there 11 Jul → 21 Aug (Kevin on leave / post-surgery from 10 Jul, back w/c 17 Aug). The 21 Aug meeting outcome lives only in Granola + `HANDOVER.md`.

### Data-entry errors found (flag for Kevin)

- Row **180** (Entra ID groups, Complete): `Date last reviewed = 2026-12-18` — a future date, almost certainly a typo.
- Row **CA120_2526** (Complete): a Progress line dated `29/05/2029` — typo for 2025.
- Row **DTP1092**: `Deadline = 31/09/2026` — invalid (September has 30 days).

### Plain answer for Kevin

> The roadmap is kept as a rolling document — each row carries its own last-reviewed date, not a single sheet-wide one. It was **last worked on today (27 Aug): a ~10-row batch of dashboard / HESA / REF / FA items** (file saved 16:24). Before that, the **last full meeting cycle was 21 Aug** (14 rows). The **Friday 22 Aug cycle was skipped** — nothing in the sheet is dated 22–24 Aug. About **25 active rows still carry a blank or pre-July review date** and are the genuinely stale ones (mostly long-dormant On Hold items and seasonal Scheduled/Pending rows).

**Baseline for the before/after table:** each row's own current verbatim cell content — there is no single prior snapshot to diff against; the live master *is* the baseline, row by row.

---

## 9. Before / after — verbatim current cell content vs proposed

`W-top` = the current newest line in the Progress column (col W), quoted verbatim; full histories stay in the master. "Prepend" = add above that line, keeping everything below. Nothing here is written — Kevin types it.

### Priority A — Kevin's lead items

**Row 179 — Migration of HR Reporting Users to SSO**

| Field | CURRENT (verbatim) | PROPOSED |
|---|---|---|
| Owner (G) | `Kevin` | no change |
| Status (AA) | `On Hold` | no change (see flag) |
| Status details (AB) | `On Target` | no change |
| Date last reviewed (Y) | `2026-07-03` | `2026-08-27` |
| Progress W-top | `03/07/26 - Migration has been placed on hold until Visual Studio 2022 licences become available, as there is a compatability issue with older versions of Visual Studio. Main poijnt of contact in IT is Svetlana Kuznetsova.` | Prepend: `25/08/26 - IT Services (Louise Piper) notified OSM users of authentication issues affecting login; may affect migration testing.` / `03/08/26 - Nexus team confirmed the six PeopleXD data access groups populated in Entra ID with the user lists Asta provided on 16 July, advancing SSO migration work.` |

Sources: command-centre `t033` log `[03 Aug 2026]` (email: Simon Burford, "FW: Creation of your 6 PeopleXD data access groups in Entra ID"); work-inbox `inbox_suggestions.json` applied_update on `t033` `[25 Aug 2026]` (email: Louise Piper, "OSM: Authentication Issues"). Both are command-centre/inbox log wording, not primary email.
Flag: the "on hold pending VS2022 licences" blocker (03/07) has no recorded resolution — Kevin to confirm it still holds.

**Row 136 — PeopleXD Data Protection Impact Assessment**

| Field | CURRENT (verbatim) | PROPOSED |
|---|---|---|
| Owner (G) | `Kevin` | no change |
| Status (AA) | `In Progress` | no change |
| Status details (AB) | `On Target` | Kevin to decide — `At risk`? deadline is 31 Aug, still awaiting Marie's signature |
| Date last reviewed (Y) | `2026-08-21` | `2026-08-27` |
| Progress W-top | `21/08/26 - Pilot of Soundcloud now in place.` | Prepend: `27/08/26 - Kevin shared updated DPIA v0.5 for Marie's review / Stage 7 sign-off.` |

Sources: command-centre `t009` / work-inbox `inbox_suggestions.json` applied_update `[27 Aug 2026]` (email subject: 'Kevin Lelitte shared "PeopleXD - Data Protection Impact Assessment v0.5" with you', 27 Aug 08:50). Do not conflate with `t2608111719551` (college-record DPIA, DTP1092).

**Row DTP1334 — Health & Safety Management System**

| Field | CURRENT (verbatim) | PROPOSED |
|---|---|---|
| Owner (G) | `Kevin` | no change |
| Status (AA) / details (AB) | `In Progress` / `On Target` | no change |
| Date last reviewed (Y) | `2026-08-21` | `2026-08-27` (or date Kevin next reviews) |
| Next checkpoint (Z) | `2026-08-27` (today — stale) | early-Sept board shortlisting date, ~`2026-09-11` |
| Deadline (T) | `2026-09-25` | no change — already correct |
| Progress W-top | `21/08/26 - Kevin and Marie have reviewed  6  supplier questionnaires and forwarded their findings and feedback to the project team. Project team have extended this phase (identifying a software supplier) to end of September.` | Optional detail append: `Scoring inconsistencies found and corrected; possible prior-knowledge bias on one supplier noted to the project board. Board aggregates scores and shortlists early September; supplier workshops begin 25 Sept.` |

Sources: Granola *HR Systems Roadmap 21/08*; command-centre `t2608131801210` / `t2608131801211`.

### Priority B — items Kevin contributes to, master behind

**Row CA104_2526 (phase "August update") — Hierarchy Restructuring**

| Field | CURRENT (verbatim) | PROPOSED |
|---|---|---|
| Owner (G) | `FA, HRA` | consider naming Kevin as Lead for the PXD/Portal part (Jan-update precedent had G=`Kevin`) |
| Status (AA) / details (AB) | `Scheduled` / `Pending` | Kevin's call — `In Progress` once the Portal work starts |
| Date last reviewed (Y) | *(blank)* | `2026-08-27` |
| Next checkpoint (Z) | `2026-08-28` | keep or advance |
| Progress (W) | *(empty)* | `27/08/26 - To be actioned via the Portal (first time; previously back office). U environment confirmed safe to use; C environment cloned/replicated. Documentation to be updated alongside. Team catch-up planned w/c 1 Sept.` / `19/08/26 - Draft University PACS Organisational Structure update circulated (orgstructure@admin.ox.ac.uk, 12 Aug; forwarded by Simon 18 Aug): wholesale move of College / Society entities from PACS level 2 to level 3, plus a Subsidiary Companies correction. Separately, three new PACS management units to be created for the HR Systems reorg.` |
| Next steps (X) | *(empty)* | `- Kevin to review the PACS level 2 -> 3 draft for HR Systems implications.` / `- Create the three new PACS management units via the Portal.` / `- Update related guidance / documentation.` / `- Team catch-up w/c 1 Sept.` |

Sources: Granola *SK 1-1 19/08*, *Michael 1-1 20/08*; command-centre `task-1787072363309`, `t2608121801282` (email: Simon Burford, "FW: Organisational Structure Update - August 2026 - DRAFT", 18 Aug); work-inbox `briefing.json` `needs`: "RE: Org Structure Update" (from Organisational Structure, 19 Aug, to Kevin & Simon).
Flag: confirm this row is the home for BOTH the routine reorg AND the University PACS level 2→3 move, or split. Sarah Rowles HESA-timing question + H&S org-mapping risk (21 Aug handover) not corroborated this cycle.

**Row 208 — Migrating departments onto 38 day balances**

| Field | CURRENT (verbatim) | PROPOSED |
|---|---|---|
| Owner (G) | `Julie` | no change (Team H = `Kevin, Simon, Michael, Marie C` — Kevin does the config) |
| Status (AA) / details (AB) | `In Progress` / `On Target` | no change |
| Date last reviewed (Y) | `2026-07-30` | `2026-08-27` |
| Next checkpoint (Z) | `2026-08-28` | `2026-10-02` |
| Progress (W) | *(empty)* | `27/08/26 - Chemistry (first to request) compiling its work-group list; 131 work groups identified for amendment (Michael, 27 Aug). Marie reviewing effort with Kevin in Julie's absence.` / `20/08/26 - Michael 1-1: target update window 1-2 Oct, ahead of 7 Oct rollover; work-group holiday-scheme swap is a single field update per work group (~1-2 min each), can only run after leave-year end.` / `19/08/26 - Planning meeting (Julie / Kevin / Simon / Michael). Chemistry proceeding; Maths advised to pause until next leave year; Biology declined (too late this year); GLAM (large, complex rosters) on hold pending Chemistry's work-group count. Treated as a pilot, not a standard service. Departments to submit work-group lists by 28 Aug; Kevin to update the holiday scheme per confirmed work group from 5 Oct.` |
| Next steps (X) | `- Julie to ocntact departments who have requested this to run through what it will mean and the work required.` / `- Kevin to update balance/workgroup configuration` / `- Kevin to discuss what steps need to take place with Michael` | `- Departments to submit work-group lists (code + description) by 28 Aug.` / `- Kevin to update the holiday scheme attached to each confirmed work group from 5 Oct, priority order by submission date, liaising with Michael on mechanics.` / `- Brief first-line support (Emma) ahead of the Oct rollover.` / `- Julie to send a summary email to all departments (cc Kevin, Simon) as the shared thread.` / `- Revisit a charging mechanism for future years (GLAM offered to pay; none in place).` |

Sources: Granola *Planning for depts move to 38 day balance 19/08*, *Michael 1-1 20/08*; command-centre `t2608111507360`, `t2608121801280`, `t2608181501150`, `t2608270801360` `[27 Aug]`, inbox_suggestions applied_update `t2608191643001` `[27 Aug]` (Michael, "131 workgroups"); work-inbox `briefing.json`/`fyi`: Julie Hickman 19–20 Aug, Marie Cooksey 26 Aug, Michael O'Sullivan 27 Aug.

**Row CA138_a — UCEA Main Pay Uplift**

| Field | CURRENT (verbatim) | PROPOSED |
|---|---|---|
| Owner (G) | `Athena` (Team H = `Michael`) | no change |
| Status (AA) / details (AB) | `Pending/Expected` / `Pending` | no change |
| Date last reviewed (Y) | *(blank)* | `2026-08-27` |
| Progress W-top | `16/07/2026 - Planning meeting with all involved teams, sketched out timeframe for Sept implementation (as August implementation already too late). ...` | Prepend: `20/08/26 - Non-clinical (main) uplift delayed pending union decision; October implementation ruled out (payroll increments that month); November or later now more likely. September decision point flagged by Jessica Oldershaw.` |

Sources: Granola *Michael 1-1 20/08*; command-centre `t2608121801281`. Kept distinct from row 72 (Clinical Pay Uplift 2024, Complete) and row 208 (38-day balances).

**Row DTP1092 — Research management data for REF and research quality**

| Field | CURRENT (verbatim) | PROPOSED |
|---|---|---|
| Owner (G) / Status | `Nathan` / `In Progress` (Team H = `Marie C, Kevin`) | no change |
| Date last reviewed (Y) | `2026-08-27` | no change — current |
| Deadline (T) | `31/09/2026` | `30/09/2026` (invalid date fix) |
| Progress (W) — ORCID sub-thread | contains `30/07/26 - ... - ORCID requirements have been passed back to Kevin to take forward.` and `24/04/26 - Decision made on approach to ORCID - we will amend the existing tile and the audience ...` | Kevin to add a `27/08/26 -` line stating the true current state of the ORCID page update, OR confirm at FA Catch-up it is still open/un-started |
| Next steps (X) — `====ORCID====` block | `- Research Services have provided requirments for how they want the ORCID page to be updated. Kevin to take this forward.` | unchanged unless Kevin has progressed it |

Sources: live master DTP1092 W/X cells; `HANDOVER.md` 2026-08-21. No ORCID movement found in command-centre / work-inbox / any Granola note 10–27 Aug. Per carry-over rules: surfaced, not closed.

### Priority C — empty "New" rows needing a decision

**Row 198 — WFM Remaining departments go live**

| Field | CURRENT (verbatim) | PROPOSED (only if Kevin confirms this row belongs on the roadmap) |
|---|---|---|
| Owner (G) | *(blank)* | assign — FA / Kevin, or the WFM project |
| Status (AA) | `New` | `In Progress` |
| everything else | *(blank)* | Description: `Complete WFM go-live for the departments still outside PeopleXD / WFM: SBS, Paediatrics, GLAM.` · System: `WFM` · W: `25/08/26 - 3 departments still to migrate: SBS, Paediatrics, GLAM. Outstanding backdated-sickness data loads ("Upload 2") tied to this.` / `20/08/26 - Managers meeting: confirmation needed all departments on board for Oct go-live; Kevin to be invited to the next WFM meeting.` · X: `- Kevin to attend the next WFM project meeting.` / `- Resolution meeting to be set up (Kevin, Simon, Marie, Michelle, +/- Julie) on outstanding loads for SBS / PEDS / GLAM.` |

Sources: Granola *Sickness Absence Survey working group 25/08*, *Managers Meeting 20/08*; command-centre `t035`.

**Row 199 — Botanic Gardens Rostering set up**

| Field | CURRENT (verbatim) | PROPOSED (only if Kevin confirms scope) |
|---|---|---|
| Owner (G) | *(blank)* | assign — FA / TBC |
| Status (AA) | `New` | `On Hold` · details `On Hold - Work Deprioritised` |
| everything else | *(blank)* | Description: `Set up WFM rostering for GLAM Botanic Gardens Ticket Office and Ashmolean Security, where annual leave via WFM does not work for concentrated / non-standard shift patterns.` · System: `WFM` · W: `19/08/26 - Raised via Anna Carter-Windle (GLAM). Considered during 38-day balance planning; significant BA and implementation effort. Team capacity stretched — position is that GLAM rostering waits. Separate, larger piece of work from the 38-day balance change.` · X: `- Requirements gathering with the GLAM Gardens team when resource allows.` |

Sources: command-centre `t2608181201061` (email: Anna Carter-Windle, Kevin bumped 19 Aug); Granola *FA Team Catch-up 19/08*, *Planning for depts move to 38 day balance 19/08*.
Flag: confirm 199's scope and that it does not duplicate 198.

### Priority D — stale checkpoints / smaller

**Row 176 — Rollout of ER Case Management to Departments**

| Field | CURRENT (verbatim) | PROPOSED |
|---|---|---|
| Owner (G) | *(blank)* | assign — Marie C (owns the Issy Stokoe follow-up) or Kevin |
| Status (AA) / details | `On Hold` / `On Hold - Waiting for strategic decision` | Kevin to confirm after the 30 Jul review |
| Date last reviewed (Y) | `2026-06-19` | update to the 30 Jul review date (or later) |
| Next checkpoint (Z) | `2026-06-26` (stale) | roll forward |
| Progress W-top | `26/06/26 - Dawn not happy to rollout further until backlog is cleared.` | add the outcome of the 30 Jul support-model review Kevin was due to attend (W line `19/06/2026` says "support model due to be reviewed on 30/07, Kevin will be attending") |

Source: live master; no cross-reference corroboration of the 30 Jul outcome — Kevin holds that.

**Row 192_a — New annual leave duty from 6 April 2026 (report build)**

| Field | CURRENT (verbatim) | PROPOSED |
|---|---|---|
| Owner (G) / Status | `Athena` / `In Progress` (Team H = `Michelle, MarieC`) | no change |
| Date last reviewed (Y) | `2026-08-21` | current — optional bump only |
| Progress W-top | `21/08/26 - Kevin has reached out to AG this week to ask them to arrange a scoping call to discuss the report build. He has suggested a few dates, awaiting response. Marie to chase KFJ ...` | already current. The AG case ref (`69001638`, 2800 flex points, 3 Holiday Records reports) is on the `12/06/26` line — optionally add the case number for precision |

Note: **not a gap** — this row already captures the Holiday Records / Access Group report-build work end to end. Confirm the "Holiday Records 3 Reports" and 192_a's "report build" are the same deliverable (they appear to be).

**Row CA102_2526 — Annual Leave Year End Rollover 2026**

| Field | CURRENT (verbatim) | PROPOSED |
|---|---|---|
| Owner (G) | `FA, BC. Tr` | consider `Michael` (doing the work per his 1-1) or `FA` |
| Status (AA) / details | `Scheduled` / `Pending` | no change |
| Date last reviewed (Y) | *(blank)* | `2026-08-27` |
| Progress (W) | `October` | `20/08/26 - ~80 balance calendars being manually extended per environment (U done, Z in progress, then C, then live). Rollover runs from Mon 5 Oct once the prior leave year is locked; run in one test env first, then live, then remaining test envs.` |

Source: Granola *Michael 1-1 20/08*.

**Row ITS214 — ORCID via onboarding**

| Field | CURRENT (verbatim) | PROPOSED |
|---|---|---|
| Status (AA) / details | `Complete` / `Delayed` | **no change — do not propose un-completing** (carry-over rule) |
| Progress W-top | `21/02/2025 - may actually be finished; need an update from FA to confirm. A tile has been created - is this live?` | none — noted for awareness only; the live ORCID tile work is now tracked inside DTP1092 |

### Rows added from the owner sweep (§10, §11)

**Row 204 — REF Appeal Process Self Service (ESS)  ·  deadline 2026-08-28 — tomorrow**

| Field | CURRENT (verbatim) | PROPOSED |
|---|---|---|
| Owner (G) | `Nathan` (Team H = `FA` / `BC`) | no change |
| Status (AA) / details | `In Progress` / `On Target` | Kevin/Nathan to confirm against the 28 Aug deadline |
| Date last reviewed (Y) | `2026-08-07` | `2026-08-27` |
| Next checkpoint (Z) | `2026-08-28` | roll forward once deadline position known |
| Progress W-top | `07/08/26 - Nathan undertook testing in UOXU using one of the test profiles. Demonstrated to Anne Mortimer.` | Prepend: `27/08/26 - REF2029 UDF being promoted to UOXP production (Nathan flagged 26 Aug; Kevin confirmed promotion to live 27 Aug). This UDF carries the REF-status values the ESS appeal screen displays.` |

Sources: command-centre `t2608261500530` (email: Nathan Kirwan, "REF29 UDF - Promotion to UOXP", 26 Aug) and inbox_suggestions applied_update `[27 Aug 2026]` (email: Kevin to Nathan Kirwan, "Re: REF29 UDF - Promotion to UOXP").
Flag: roadmap deadline is **tomorrow** — Kevin/Nathan to set the real position (met / slipping / extend).

**Row 183 — Sickness Absence Dashboard (Executive Summary)**

| Field | CURRENT (verbatim) | PROPOSED |
|---|---|---|
| Owner (G) | `Sarah` (Team H = `Simon, Athena, Chris, MarieC`) | no change |
| Status (AA) / details | `In Progress` / `On Target` | consider `At risk` — FTE calculations broken, blocking the exec dashboard |
| Date last reviewed (Y) | `2026-07-03` | `2026-08-27` |
| Progress W-top | `07/08/26 - Chris has shared user stories with Sarah this week.` | Prepend: `25/08/26 - UCR calculations nearly complete in test workbook; divisional slicing broke again after adding the division field; FTE values corrected. Star schema not yet loaded into Power BI.` / `21/08/26 - Dashboard mostly green but FTE-dependent calculations unreliable; Sarah reworking the data model (Simon's approach as reference), blocking ~1 day/week alongside HESA. Executive dashboard on hold until the underlying data model is fixed.` |

Sources: Granola *Sickness Absence Data Catch-up 21/08*, *Sickness Absence Survey working group 25/08*, *HR Systems Roadmap 21/08*.

**Row ITS960 — DSE Online Assessment**

| Field | CURRENT (verbatim) | PROPOSED |
|---|---|---|
| Owner (G) | `Grace, Nik` (Team H = `Simon`; James heavily involved) | Kevin to confirm current owner |
| Status (AA) / details | `In Progress` / `Delayed` | **Kevin / James to confirm at FA Catch-up** — Granola *James 1-1 21/08* states "DSE already delivered and closed (~£2,000 for a filter)". If confirmed complete, close it; per carry-over rules this is surfaced, not closed unilaterally |
| Date last reviewed (Y) | `2026-08-07` | `2026-08-27` |
| Next steps (X) | `- James / Marie to confirm if it's gone live` | resolve this open question — James 1-1 indicates it has |

Source: Granola *James 1-1 21/08*.

---

## 10. Owner-coverage sweep — all 268 Work Tracker rows

Ownership read from **col G (Lead)**. Active = Status is one of On Hold / In Progress / Not Delivered / Pending/Expected / Planning / Scheduled / New.

### Summary by name

| Owner | Active rows they LEAD | In this proposal? | Overlooked (with update) |
|---|---|---|---|
| **Kevin** | 3 — `179`, `136`, `DTP1334` | **All 3** | none |
| **Simon** | ~12 — `133`, `200`, `207` (reviewed 27 Aug, current), `173`, `48`, `UOX008`, `181`, `36`, `53`, `22_d`, `23_c`, `80_b` | via §5 no-change | `181`, `UOX008` — flags below |
| **Marie C** | ~9 — `196_a`, `197_a`, `177`, `178`, `148_b` (reviewed 21 Aug), `202`, `149`, `193`, `79` | via §5 no-change | `202`, `149`, `193` — flags below |
| **Marie K** | 3 — `CA121_2526`, `CA123_2526`, `CA134_2526` (all `Pending/Expected`, future-dated seasonal surveys) | no | none — genuinely not due |
| **Michael** | **0** — leads no active row (`ITS1004` WFM Rollout is `Complete`) | n/a | **not an omission — structural** |
| **James** | 1 — `94` Biohazardous Materials Management (`On Hold - Waiting for funding`, blank review) | `94` flagged below | `ITS960` (James-driven, added §9); Cority/Quality funded work (§4 candidate 1) |
| **Asta** | **0** — leads no active row | n/a | **not an omission — structural** |

### Michael and Asta — why zero, and where their live work actually sits

- **Michael** leads nothing active. His live work is entirely as **Team member (col H)** on other people's rows — all of which ARE in this proposal: `208` (38-day balances), `CA102_2526` (annual-leave rollover), `CA104_2526` "August update" (org structure — Portal work), `CA138_a` (UCEA uplift).
- **Asta** leads nothing active. Her live work is as Team on `179` (SSO — in this proposal) and the dormant `22_c` / `22_d` Security Model Review (On Hold, no cross-reference activity — genuinely no change).
- **This is not a filtering error.** The first pass was Kevin-weighted because, on the Lead column, few of the six names have active items at all — Simon and Marie C carry most of the other-owner active load, and those are swept below.

### Simon-led / Marie C-led active rows NOT in the proposal — no-change vs overlooked

| Row | Owner | Status / Reviewed | Verdict |
|---|---|---|---|
| `133` FTC Monitoring by person Dashboard | Simon | In Progress / **2026-08-27** | **No change** — reviewed today, `27/08/26` line present |
| `200` DWH Fabric Migration | Simon | In Progress / **2026-08-27** | **No change** — reviewed today |
| `207` Volunteering leave → employee-bookable | Simon | In Progress / **2026-08-27** | **No change** — reviewed today ("ready for UAT") |
| `173` Workforce Profile Dashboard | Simon / Marie | In Progress / 2026-08-21 | **No change** — 21 Aug cycle; Granola *Roadmap 21/08* matches |
| `48` Applicant cleardown | Simon | In Progress / 2026-08-07 | **No change** — `07/08/26` line current; no later cross-ref activity |
| `181` Salary and Allowance Data in DWH | Simon | Planning / 2026-07-01 | **Overlooked — flag.** Next checkpoint `2026-08-28` falls now; W last line 01/07/26; X = "going onto the dashboard roadmap for 2026-27, needs SLG sign-off". No Granola/inbox/CC hit. Simon to refresh review date + confirm still parked to 2026-27. |
| `UOX008` Data Platform Project | Simon | In Progress / 2026-07-31 | **Overlooked — flag.** Progress column **entirely empty**; deadline `2026-12-31` (Fixed - compulsory); X = "All to review Fabric documentation". Related to `200` (current). Simon to confirm scope vs `200` and add a progress line. |
| `196_a` EVO / `197_a` Eploy | Marie C | In Progress / 2026-08-21 | **No change** — 21 Aug; Granola *Roadmap 21/08* Evo/Eploy section matches |
| `177` ER Case Mgmt Institutional Reporting | Marie C | In Progress / 2026-08-21 | **No change** — 21 Aug; deadline 2026-08-31 but no new evidence |
| `178` HESA Staff Consultation Outcomes | Marie C | In Progress / 2026-08-21 | **No change** — correctly parked, review resumes late Nov (matches Granola) |
| `148_b` UCEA Sickness Absence Survey 25-26 | Marie C | In Progress / 2026-08-21 | **No change to this row** — `25/08/26` line already present. (Related dashboard work is `183`, added §9.) |
| `202` Fire Risk Assessment Dashboards | Marie C | In Progress / 2026-07-31 | **Overlooked — flag.** Progress column **empty**. Granola *Roadmap 21/08*: "MarieC met with Kate Vickers and Alex Gray on 11/8 to discuss resourcing to further develop H&S dashboard with specific focus on fire safety" — currently recorded only under `174_b`; may belong here too. |
| `149` Support ACRF consultation mailing | Marie C | On Hold / 2026-01-30 | **Overlooked — flag.** "Annalisa to confirm requirements in HT2026" — Hilary Term 2026 has passed; W last real entry 01/07/25. Confirm still live or close. |
| `193` Pay & Conditions Modelling | Marie C | Pending/Expected / **blank** | **Flag.** All date fields blank on an active row; only content is "Sara Willis to provide requirements". Confirm still expected. |
| `79` EDI DQ promotional campaign | Marie C | On Hold / 2024-05-10 | **No change** — dormant 15 months, no cross-ref activity |
| `36`, `53`, `22_d`, `23_c`, `80_b` | Simon | On Hold, all reviewed 2024–2025 | **No change** — long-dormant, no cross-reference activity in any source |

### James-led — row 94

`94` **Biohazardous Materials Management** — `On Hold - Waiting for funding`, Lead `Chris, James`, blank review date, empty Progress. Granola *James 1-1 21/08* notes H&S funds were approved for **DSE, Quality and IRIS** — Biohazardous was **not** mentioned. **Flag:** Kevin/James to confirm the funding blocker on 94 is unchanged and add a review date.

### ACTIVE rows with a BLANK Lead, or a Lead outside the six names

| Row | Lead (G) verbatim | Status | Note |
|---|---|---|---|
| `40` Payroll reports review · `67` Experian Work Report · `119` TSS ePloy integration · `103_a` year-end processes · `68_b` Apprenticeship form | *(blank)* | On Hold | all dormant since 2024–early 2026 — need an owner only if reactivated |
| `176` Rollout of ER Case Management | *(blank)* | On Hold | **in proposal §9** — assign Marie C / Kevin |
| `198` WFM Remaining departments go live · `199` Botanic Gardens Rostering | *(blank)* | New | **in proposal §9** — need owner + decision |
| `203` IP Rights employment checking tool | *(blank)* | Pending/Expected | needs requirements gathering with Research Services (AnneM) — needs owner |
| `5` FTC End Date Reminders | `Lee` | On Hold | Lee no longer in team — reassign or leave dormant |
| `83`, `18_g` | `Michelle` | On Hold | not one of the six — dormant |
| `110`, `120`, `22_c` | `Tonya` | On Hold | not one of the six — dormant |
| `130`, `139`, `172_a-d`, `86_a`, `211`, `CA137_2526` | `Athena` / `Susan` | mixed | HRA/reporting-team; `172_a`, `211` reviewed 27 Aug (current); `172_c/d` blank (Pending); `CA137_2526` on track to 30 Sept |
| `186` TUPE Transfer improvements | `Ant` | On Hold | deprioritised 27/03/26 |
| `151`, `183`, `209` | `Sarah` / `SarahR` | On Hold / In Progress / Scheduled | `183` added §9; `151` on hold waiting HESA; `209` future-dated |
| `187`, `191`, `204`, `DTP1092` | `Nathan` | In Progress | `187` & `DTP1092` current; `204` added §9; **`191` flag** (reviewed 2026-06-19, deadline 2026-08-31, "no movement… focus on DTP1092" — Nathan/Kevin to extend or update) |
| `190`, `205`, `206`, `210`, `CA125_2425`, `CA125_2627` | `TBC` | Pending/Planning/On Hold | genuinely not yet owned — future / awaiting-trigger |
| `184`, `CA102_2526`, `CA103_2526`, `CA104_2526` | `FA` / `FA, BC, Tr` / `FA, HRA` | Not Delivered / Scheduled | FA-team; `CA102_2526` & `CA104_2526` in proposal |
| `CA105_c/d`, `CA108_2526`, `CA112_2526`, `CA113_2526`, `CA117_a/b/d_2526`, `CA128_2526`, `CA129_2526` | `HRA` / `BC, HRA` / `Sarah` | In Progress / Scheduled / Planning | HRA year-end seasonal block; `CA105_d`, `CA112`, `CA129` reviewed 27 Aug (current); rest scheduled future work |
| `ITS960` DSE | `Grace, Nik` | In Progress | **added §9** — Grace/Nik may no longer be the owners |
| `94` Biohazardous | `Chris, James` | On Hold | flag above |

### Data-entry / date errors (also in §8)

- `180` Entra ID groups — `Date last reviewed = 2026-12-18` (future date, typo).
- `CA120_2526` — Progress line dated `29/05/2029` (typo for 2025).
- `DTP1092` — `Deadline = 31/09/2026` (invalid; use 30/09/2026).

---

## 11. Net additions to the proposal from the sweep

Rows now added to the change list (full before/after in §9): **`204`** (REF Appeal ESS — deadline tomorrow, REF2029 UDF promotion), **`183`** (Sickness Absence Dashboard — data-model blocker from two Granola notes), **`ITS960`** (DSE — Granola says delivered/closed; confirm, do not close unilaterally).

Owner/date flags only — no content proposed, for the named owner (not Kevin) unless he chooses to enter them: **`181`**, **`UOX008`** (Simon); **`202`**, **`149`**, **`193`** (Marie C); **`94`** (James); **`191`** (Nathan); **`176`** (unassigned — assign Marie C / Kevin); date fixes **`180`**, **`CA120_2526`**, **`DTP1092`**.

Confirmed **no owner-filtering error**: Michael and Asta lead zero active rows by design; their live work sits under `208` / `CA102_2526` / `CA104_2526` / `CA138_a` / `179`, all already in the proposal.
