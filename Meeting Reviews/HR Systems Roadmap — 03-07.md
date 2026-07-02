# HR Systems Roadmap — 03/07

**Date:** Friday 3 July 2026, 10:00
**Follow-on from:** Friday 26 June 2026
**Prepared from:** Live roadmap (hr-projects/HR Systems Roadmap MASTER.xlsm, read-only), Granola (FA Catch-up 01/07, WFM Rostering Internal Review 30/06, Michael 1-1 Handover 02/07, Evo Implementation Meeting 01/07, Emergency Planning 01/07, HESA REF Meeting 01/07, HR Roadmap 26/06, FA Catch-up 26/06), briefing.json and tasks.json unavailable this session

---

## 1. Headline position

Four active FA projects are past their original deadlines. Two events this week materially change the picture: the WFM resolution meeting on 30 June established the approach for the GLAM/SBS/PEDS gap, and Evo/PeopleXD purchase was confirmed on 1 July — a new project not yet on the roadmap. The DPIA Stage 7 deadline was 30 June and remains unconfirmed. SSO Migration reaches its decision point today. Kevin's surgery is 10 July; from Monday Michael and Emma are both absent; from 13 July Sarah is the last manager standing.

> **Note on item currency:** WFM, REF/ESS, Evo, PACS org structure, and July cover reflect genuine updates from this week's meetings. DPIA (Stage 7 still with Marie — deadline now passed), H&S Dashboards (Brian still blocking — no movement since last Friday), and SSO Migration (decision today — outcome from morning catch-up) are unchanged in substance; the roadmap Excel has not been updated since 26 June.

---

## 2. Team items — status by item

---

**136 — PeopleXD DPIA**
Lead: Kevin | Team: Simon | Deadline: 30 Jun 2026 ⚠️ PASSED

**Current position:** v0.2 complete through Stages 1–6. Stage 7 sign-off is sitting with Marie Cooksey. No confirmation received as of this morning. The SoundCloud DPIA pilot (Kevin to be included when the WFM DPIA team makes contact) is a separate track. Deadline passed on 30 June — this is now overdue. No change since last Friday.

**What to say:** *"DPIA — Stage 7 is still sitting with Marie. The 30 June deadline has passed. I am chasing her again today. From our side the document is complete. Has anyone had any contact from Marie or the Information Compliance Team on this? The SoundCloud pilot for Oxford DPIAs will use the WFM DPIA as the test case — I want to be in that conversation when the contact comes through."*

---

**DTP1334 — Health & Safety Management System**
Lead: Kevin | Team: James, Marie C | Deadline: 31 Jul 2026 | Last reviewed: Jan 2026

**Current position:** Evaluation is proceeding. Follow-up meeting with the evaluation team was yesterday (2 July) — no Granola transcript available; Kevin to update from James's debrief at the morning catch-up. Evaluator briefings are 14 July. Supplier responses expected ~21 July. Kevin's resourcing position (cannot absorb into BAU) was sent to Chris and James on 30 June. The 31 July roadmap deadline is not achievable given the evaluation window extends to late July. Scoring process agreed at the 1 July FA catch-up: shared document, one week for comments, one-hour alignment session.

**What to say:** *"H&S modular system — evaluation is proceeding. I had the follow-up meeting yesterday and the evaluator briefings are 14 July. Supplier responses come back around 21 July, which means the 31 July roadmap deadline is not achievable. I want to propose a revised deadline today — I'd suggest end of September to allow time for evaluation, decision, and any procurement steps. More importantly: I am repeating my resourcing position. This project cannot sit with the FA team as BAU. We have proven that model fails. Marie is looking at a September/October recruiting window for a dedicated resource. I want that formally noted."*

---

**DTP1092 — Research Management Data / REF**
Lead: Nathan | Team: Marie C, Kevin | Deadline: None on roadmap | Last reviewed: Feb 2026

**Current position — REF attributes via ESS (end-July deadline, updated this week):** Approach confirmed at the HESA meeting on 1 July. Person-level UDF with three fields per appointment: appointment ID, REF call-on status, panel/Unit of Assessment. Up to four appointments per person (cap likely sufficient — Nathan to confirm via HF029 SQL report). Research Assistant indicator explicitly excluded. Nathan to raise ISM request for the build. Kevin needs to test UDF display before surgery on 10 July — window is this week or early next. Staff bulletin goes out 21 September; loading target is 18 September.

**Current position — org hierarchy / multi-company:** Simon updated Conor O'Brien (Access Group) on 23 June with the post-design multi-company setup proposal. COREPORTAL_ADMIN change 20020472 is in test — Kevin to test with Simon on Company 90 before extending to other services.

**What to say:** *"DTP1092 — two threads. First, REF via ESS: we confirmed the approach on Tuesday — person-level UDF, three fields per appointment, Research Assistant indicator is out. Nathan is raising the ISM request for the build. My testing window is this week or early next before I'm off on the 10th — that's a hard constraint. The loading target is 18 September, staff bulletin 21 September. I want to make sure the scoping meeting with Simon and Michelle is in Nathan's diary before end of next week. Second, multi-company: COREPORTAL_ADMIN is in test. I'll be testing with Simon on Company 90 shortly."*

---

**ITS1004 — WFM Rollout**
Lead: Michael | Team: Tonya, Julie, Simon, Asta | Deadline: 29 May 2026 ⚠️ PASSED | Last reviewed: Oct 2025

**Current position (updated — resolution meeting held 30 June):** Root cause of GLAM gap established: GLAM HR shared service stopped maintaining records because no departments were actively using rostering (variable hours complexity and descoped job title functionality are the two structural blockers). Plan agreed: convene a single call with GLAM stakeholders — Kathy, Harriet Webb (Botanical Gardens ticketing), Sarah Mann (Ashmolean security), Ashmolean security manager. Present rostering as-is, including explicit limitations, and let them decide whether to proceed or descope. Botanical Gardens has its own separate TeamSeer licence not managed by GLAM HR — this may need to remain regardless. SBS and PEDS were told at project close to provide their own data — Michelle to confirm contact has been made. Upload 2 (Mel's sickness batch, ~600–700 rows with date and character formatting issues) needs cleaning before it can be handed to Michael. Second internal WFM meeting needed before the GLAM call — Kevin to speak with Simon and Marie first on direction. Michael on annual leave from Monday. Sarah Rowles still blocked on UC dashboards.

**What to say:** *"WFM — we held the resolution meeting on Monday and I now have a clear picture. Three areas still outstanding: SBS, PEDS, and GLAM. On GLAM: the root cause is that nobody in GLAM is actively using rostering — variable hours and the descoped job title feature are the two structural blockers, and GLAM HR stopped maintaining records because departments weren't using the system. The plan is a collective call with GLAM stakeholders — Botanical Gardens, Ashmolean security, and GLAM HR — where we present what rostering can and can't do and let them decide. Descoping is a valid outcome and doesn't affect the rest of GLAM on leave and absence. I'll set that call next week after I've spoken with Simon and Marie on direction. On SBS and PEDS: Michelle, can you confirm whether contact has been made? I'd like to propose a revised deadline for this item: October. I also want to flag Sarah Rowles — she is still blocked on UC dashboards. I will give her a clear update once the GLAM position is agreed."*

---

**179 — HR Reporting SSO Migration**
Lead: Kevin | Team: Asta | Deadline: 30 Apr 2026 ⚠️ PASSED | Last reviewed: Mar 2026

**Current position:** Stalled since w/c 15 June when remote apps became inaccessible after Kevin and James migrated. No further migrations since. Blocker is Visual Studio 2022 — resolves the compatibility issue but was on trial licence only. Today (3 July) is the decision point set at last week's meeting. No change in substance since last Friday — outcome depends on Asta's VS2022 licensing check with Desktop Services. Remaining trial users: Simon, David Sanders, Asta.

**What to say:** *"SSO migration — today is the decision point I flagged last week. [Report Asta's update from the morning catch-up.] Either VS2022 licensing is confirmed and we proceed with the remaining three users — Simon, David Sanders, and Asta — or we park this formally. I'll have a clear answer for the group."*

---

**174_b — Health & Safety Dashboards**
Lead: David | Team: Simon, James, Chris | Deadline: 31 Mar 2026 ⚠️ PASSED | Last reviewed: Mar 2026

**Current position:** Build complete, socialised with SEG and Council. Brian (H&S) has still not sent stakeholder comms as of this morning — no change since last Friday. Last Friday was the self-imposed end-of-June deadline. Brian's budget approval is also blocking IRIS/ECO Online enhancements and the DSE SBS fix — one person is now a blocker across three separate items.

**What to say:** *"H&S dashboards — the build is done, it went through SEG and Council, and we are still waiting for Brian to send stakeholder comms. It is now more than three months past the original deadline and a week past the self-imposed June deadline. [Update from James in the catch-up.] Brian's budget is now a single-point blocker across three items: the dashboards comms, the IRIS/ECO Online enhancements, and the DSE SBS fix. I would like the group's view on whether this now needs to be escalated above Brian."*

---

**22_c / 22_d — Security Model Review**
Lead: Tonya | Team: Simon, Asta (22_c); Simon, Asta, Michael, Lee, Sarah, Athena (22_d) | Status: 22_c On Hold; 22_d New

**What to say:** *"Security Model Review — no change on either item. 22_c remains on hold pending strategic direction; 22_d is still new with no activity."*

---

## 3. New this week

**Evo / PeopleXD implementation — purchase confirmed 1 July**
Not yet on the roadmap. Purchase confirmed 1 July. Funding approved as part of the three-year settlement (~£35k). IT Services will provide the project manager. Access Group estimate is 12–16 weeks for implementation. Target: early academic year 2026–27 (not June 2027). Budget not available until August; goal is to have everything ready to start by then. Evo is a platform layer over PeopleXD — not a replacement of the system. Key risks: authentication change (Evo wraps around PXD, SSO route changes), infosec sign-off for the Evo app, Copilot document access (SharePoint pages not natively readable — Power Automate may be needed). HR team wants to lead on requirements definition; Access Group consultant will lead technical delivery. Two workstreams: technical (auth, navigation, infosec, Evo app) and benefits realisation (backlog review, change management, KPI agreement).

**What to say:** *"I want to flag a new project that isn't on the roadmap yet: Evo/PeopleXD. Purchase was confirmed on Tuesday. Funding is in place (~£35k from the three-year settlement), IT is providing the PM, and Access Group will provide a consultant. The implementation estimate is 12–16 weeks. The Chief Digital Officer wants this done early in the academic year — not June 2027. I'll be bringing a formal proposal to add this to the roadmap at the next meeting, but I want the group to be aware now. The biggest concern from our side is authentication — Evo changes how users access PeopleXD and we'll need infosec sign-off. I'll be coordinating with IT to define requirements before budget is available in August."*

---

**PACS org structure — Colleges L2 to L3**
Simon asked Kevin on 29 June to assess the impact of moving Colleges from Level 2 to Level 3 in the org hierarchy, for REF/DARS purposes. ORMS and IAM have both confirmed no impact for their systems. James is assessing the H&S system impact with Chris. Kevin needs to report back to Simon by next week.

**What to say:** *"Simon asked us last week to assess the PeopleXD and H&S impact of moving Colleges from L2 to L3 in the org hierarchy. ORMS and IAM are both clear. I'll have an update from James on the H&S side [from morning catch-up]. PeopleXD looks likely fine but I want to confirm before I give Simon a formal position. Full response to Simon by next week."*

---

**July cover — management gap**
Kevin's surgery is 10 July (Friday next week), with approximately two weeks' recovery. Michael and Emma are both absent from Monday 6 July. Marie is off 7–17 July. From 13 July Sarah is the last manager standing. Escalation chain: Simon → Renu → Sarah. All managers are creating Microsoft Loop handover documents to be embedded in the HR Systems Management Team chat.

**What to say:** *"Cover position — just for the group's awareness. From Monday we lose Michael and Emma. My surgery is next Friday the 10th. Marie is off from the 7th. From the 13th Sarah is the only manager. Simon and Renu are briefed; escalation chain is clear. I am collecting Loop handover links from the team today."*

---

## 4. Concerns and watching brief

| Item | Concern | Action |
|---|---|---|
| **136 DPIA** | Stage 7 overdue — sitting with Marie Cooksey | Chase Marie today; escalate if no response by end of week |
| **174_b H&S Dashboards** | Three items now blocked by Brian's budget | Raise escalation question with the group at 10:00 |
| **ITS1004 WFM** | Michael absent from Monday; Upload 2 uncleaned; Sarah Rowles still blocked | GLAM call next week after Simon/Marie direction; give Sarah Rowles a clear update |
| **DTP1334** | 31 Jul deadline unachievable; dedicated resource still unconfirmed | Propose revised deadline (Sep) and press resourcing case at 10:00 |
| **179 SSO Migration** | Decision TODAY — VS2022 licensing outcome | Report decision at 10:00; no further migrations until confirmed |
| **REF via ESS** | End-July deadline; Kevin's testing window closes 10 July | Nathan to confirm ISM request raised; Kevin to test UDF this week or early next |
| **Evo** | Not on roadmap; authentication risk; budget available August | Formally propose roadmap addition next week; begin IT coordination |
| **July capacity** | Kevin out 10 Jul; Michael/Emma out Mon; Marie out 7–17 Jul | Loop handover docs embedded in team chat by end of today |

---

## 5. Items complete — no update needed

- 185 — WFM Reports fix: live Mar 2026
- CA101_2526 — Payroll Year End 2026: complete Mar 2026
- CA104_2526 — Hierarchy Restructuring: complete Feb 2026

---

*Prepared: 3 July 2026 | Sources: HR Systems Roadmap MASTER.xlsm (read-only, hr-projects, base64 decoded via openpyxl), Granola (FA Catch-up 01/07, WFM Rostering Internal Review 30/06, Michael 1-1 Handover 02/07, Evo Implementation Meeting 01/07, Emergency Planning Meeting 01/07, HESA REF Meeting 01/07, HR Roadmap 26/06, FA Catch-up 26/06), briefing.json and tasks.json unavailable this session*
