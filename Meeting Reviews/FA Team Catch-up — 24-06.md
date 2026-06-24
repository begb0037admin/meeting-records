# FA Team Catch-up — 24/06
**Date:** Wednesday 24 June 2026  
**Purpose:** Fortnightly FA team check-in  
**Time needed:** ~25 minutes

---

## Items to raise

---

### 1. Support cover — w/c 1 July (URGENT — resolve today)
**Ask:** Both Michael and Emma are absent w/c 1 July. Who covers Support that week, and what does that cover look like?

**Background:** Kevin is on a phased return from leave — 4 hours per day, mornings only, fully remote. On 19 June Kevin emailed the team (Julie Hickman, Sarah Rowles, Marie Cooksey, Simon Burford, Athena Artuso) asking them to plan support cover for his own periods of reduced availability in early July.

Julie replied on 23 June (15:23) with a more serious update: Michael O'Sullivan and Emma are both on leave during the week commencing 1 July — not just Kevin. This significantly compounds the coverage gap. Michael is one of the most technically active members of the team right now: he is currently running clinical pay uplift testing, handling the OSPS pension rate changes, leading on WFM, and is the go-to person for PeopleXD configuration queries. His absence for a full week, combined with Kevin's reduced hours, leaves the team very thin.

It is not yet clear who "Emma" refers to in this context — whether she is part of the HR Systems FA team or first-line Support — but Julie's message makes clear she is a named cover resource who would normally pick up that week. Julie's warning is that her absence removes what was presumably a planned fallback.

This needs a named cover plan agreed in this meeting. The week starts in 8 days.

---

### 2. James — DSE SBS exclusion: Azure CR work item 126017 needs Kevin's sign-off
**Ask:** Has Kevin reviewed work item 126017 and signed off the Azure CR? If not, do it today.

**Background:** The DSE (Display Screen Equipment) online assessment data feed went live on 3 June 2026. The feed automatically pushes HR data from PeopleXD into Healthy Working Plus (HWP), the DSE system, so staff assessments are linked to their employment records. James Salas was the lead on this project.

One of the issues identified immediately after go-live was that Saïd Business School (SBS) was being included in the feed despite having opted out of the university-wide DSE system. SBS runs its own DSE provision. Because HWP charges per licence, Oxford is paying for SBS licences that SBS does not need and will not use. The SBS exclusion was discussed verbally during requirements but was never formally documented, so Tony Boydell's Azure integrations team did not build it into the original feed. Tony Boydell is known for working strictly to written requirements — if it's not in writing, he won't build it. This was flagged as disappointing at the time (it was a known requirement) but the position is clear: it needs to be formally raised now.

Marie asked James to raise a service request to get a cost estimate. James has done this. Tony Boydell has now drafted the Azure change request as work item 126017 in Azure DevOps (Oxford University / Integration project). Kevin's sign-off is the immediate next step before this can progress. There may be a cost attached — since the exclusion wasn't in the original spec, it may not be covered under the existing contract. Marie is aware and said to flag the cost to her when it's known.

Note: as of 23 June, Tony Boydell also emailed Kevin and James directly about this CR — it is in the inbox as a 'Needs action' item (received 10:29, 23 Jun). Kevin should review and sign off today if he has not already done so.

---

### 3. James — H&S Dashboards (Roadmap ID 174_b): end-of-June deadline in 6 days
**Ask:** Has Brian sent comms to the key stakeholders yet? If not, what is the escalation plan?

**Background:** David (data warehouse team) built a suite of Health and Safety dashboards drawing on Cority data that James loads into the data warehouse. James fixed the underlying report and got all data loads working back in October 2025. The dashboards cover H&S metrics and were built primarily for the H&S management team. They were socialised with SEG and Council and were well received.

The dashboards have been ready for release for some time. The blocker is Brian (H&S office) — he needs to send comms to key stakeholders before the dashboards can be formally published, so that the right people know they exist and how to access them. Brian has not done this despite the matter being open for months.

At the H&S Roadmap meeting on 22 June, this was still unresolved. The team set a self-imposed fixed deadline of end of June — that is now 6 days away. If Brian has not moved by now, this needs to be escalated. James is the right person to raise this in this meeting as he has the most direct relationship with the H&S side and is now back from leave. What is the escalation route if Brian continues to delay past 30 June?

---

### 4. Asta — COREPORTAL_ADMIN org hierarchy menu options: comparison still awaited
**Ask:** Has Asta sent the full comparison of currently enabled vs required menu options on COREPORTAL_ADMIN?

**Background:** PeopleXD's org structure management — creating and editing departments, cost centres, pay admin codes, the hierarchy itself — has historically been done in the old Back Office interface. The problem surfaced during Kevin's leave: when team members tried to process org structure changes via the Portal, the relevant menu options simply were not there. Michael confirmed on 17 June that this is because org structure management was never migrated from Back Office to Portal when PeopleXD was originally configured. It has always been a gap, and the college data input migration (DTP1092) has now exposed it.

Simon Burford identified the specific menu options that need enabling on the COREPORTAL_ADMIN profile. They fall into two groups: the **Hierarchy Group** (Show org Hierarchy, Delete hierarchy by business units, Show my hierarchy, Get hierarchy by business units, Set hierarchy items, Log/link hierarchy items, Set hierarchy levels, Update hierarchy by business units) and the **Post Management Group** (Post Management, Post Appointment Maintenance, Post Management Parameters, Post Profile Maintenance, Post Restructuring, Post Profile Section History, Structure Setup, Terms and Conditions Maintenance, View Post Appointments). Michael flagged that some of this functionality may sit under COREPORTAL_SUPPORT or COREPORTAL_HR_ADMIN_WEB rather than COREPORTAL_ADMIN — Asta's comparison will clarify exactly which profile needs which options.

A change request (change 20020472, titled "Org Hierarchy Migration: Enable 16 COREPORTAL_ADMIN Menu Options") was raised in OSM on 17 June and is currently showing as Coordination Required with Kevin listed as Coordinator. The plan is to enable the confirmed options in UOXU first as a proof of concept, then roll out to DEV, TEST, QA, and LIVE. Kevin will also produce Portal-specific How-To guidance for org hierarchy management as part of this work — nothing currently exists. None of this can move forward until Asta's comparison arrives.

---

### 5. Asta — SSO Migration (Roadmap ID 179): 3 July decision point approaching
**Ask:** What is the current position? Is no one else migrating until the remote apps issue is resolved? The 3 July deadline to decide whether to proceed or abandon is 9 days away.

**Background:** HR Reporting users currently log in with a separate set of credentials — a username and password specific to HR Reporting, separate from the Oxford Single Sign-On (SSO) used for everything else. The SSO Migration project (Roadmap ID 179) aims to bring HR Reporting users onto Oxford SSO, removing the need for separate accounts and reducing admin overhead for the team.

As of the last substantive update (March 2026), Richard Jessett had shared a list of desktop users and Asta had sent a trial migration list to the project team. Desktop services were preparing to migrate test users. User guidance, account provisioning, and first-line support documentation still needed updating before a broader rollout.

During the week of 15 June, Kevin and James were migrated and a problem emerged: remote apps became inaccessible after migration. The rest of the team were advised not to migrate until this is resolved. At the catch-up on 22 June the position was to kick the deadline out to 3 July to determine whether to proceed with the migration or abandon it entirely. That date is now 9 days away. Confirm with Asta that no one else has migrated in the meantime, and what the current read is on whether the issue has been investigated.

---

### 6. Michael — WFM Rollout (Roadmap ID ITS1004)
**Ask:** Any update on the parameter review from last week's session? Anything to flag on the two departments still not live?

**Background:** WFM (Workforce Management) is the rostering and timesheet module within PeopleXD, used for casual and variable-hours staff. This has been a funded project running for over two years. From an HR Systems perspective, the core build is complete — two departments (the Business School and one other) have chosen not to go live yet, opting to wait until the start of the new leave year. That is their decision, not a systems issue. Their employees already have self-service access.

A working session was held on 17 June between Michael, Julie Hickman, Beth, Emma, and Simon Burford to work through WFM issues being raised by departments. The group agreed to focus on one issue at a time rather than trying to tackle everything at once. Michael took a task to review some parameters; Simon took a task to look at what reports might help first-line support staff handle WFM queries. The group is due to reconvene in a couple of weeks.

Michael is the only person with substantive WFM knowledge on the team — Tom Harlos, who led the original pilot, left very little documentation. Quick check: has the parameter review surfaced anything worth flagging, or is it progressing as expected?

---

### 7. Chemistry bulk delete — awaiting Reenu's live confirmation
**For info / action if no confirmation received:** Kevin signed off UAT yesterday (23 Jun) and instructed Reenu Delaney at Access Group to proceed to live. Still awaiting Reenu's confirmation email that the deployment is complete.

**Background:** This is a bulk deletion of appraisal cycle assignments in PeopleXD for the Chemistry department. The appraisal cycle in question is '(DO NOT USE) CDR2025Chemistry'. A total of 5,568 staff were incorrectly assigned to this cycle and need to be removed. The work is being done by Reenu Delaney at Access Group under cases 68974493 and 67938206. Payment is £525 via flex points, approved by Marie Cooksey.

Julie Hickman ran the affected employee report and shared the export via OneDrive in June. Kevin forwarded the cycle name and employee list to Reenu. Reenu completed the work in a UAT environment; Kevin reviewed and signed off UAT on 23 June, instructing Reenu to proceed to live. A confirmation email from Reenu when the live deployment is complete is the only remaining step.

If no confirmation email has arrived by the time of this meeting, chase Reenu directly today.

---

### 8. IM Principles URL — Maura's config fix: Kevin to review and confirm
**Ask:** Has Kevin reviewed Maura McGlynn's config fix for case 69001555? If not, this needs to happen today — the old URL retired yesterday.

**Background:** The Internal Mobility (IM) Principles page was moved to a new OxIntranet URL earlier this month. Three pages across the intranet still link to the old location: the main Operations intranet page, the Professional Services search page, and individual vacancy application pages. The new URL is https://unioxfordnexus.sharepoint.com/sites/OXINTRANET-working-here/SitePages/internal-mobility-principles.aspx. The old page was scheduled to retire on 23/24 June — that is today or yesterday. Laura Porter (the intranet owner) confirmed on 20 June that the URL change approach is working well.

The problem Kevin ran into yesterday was a blocker: when trying to update the URL in Search Appointments V4 E-Form Maintenance in the PeopleXD back-end, the system returned a "Sorry But Page Not Found" error in all three environments (Production, OXU, OXZ). Kevin could not save any changes. He escalated urgently to Maura McGlynn at Access Group and to Sarah Murphy. Maura applied a configuration fix and reported that changes are now saving successfully. Kevin has not yet confirmed this himself.

Kevin needs to log in to Search Appointments V4, test the fix, and confirm it works before completing the remaining URL updates on the three intranet pages. This is time-critical: the old URL is already retired or retiring today.

---

### 9. Flex points — Holiday Records - 3 Reports Created, case 69001638
**Ask:** Quote has arrived — approve flex points for case 69001638 today or tomorrow. Quote expires 26 June.

**Quote details (received 24 Jun, prepared by Alan Quirke, Access Group, V1.0 dated 12 Jun):**
- **Scope:** 3 reports — Annual Leave Record by Person and Leave Year; Holiday Pay and Accrual Record for Variable-Hours and Casual Arrangements; Holiday Pay in Lieu on Termination
- **Payroll Consultant:** 2.5 days = 1,750 flex points
- **WFM Consultant:** 1.5 days = 1,050 flex points
- **Total: 2,800 flex points** (£4,400)
- **Quote valid until: 26 June 2026** (14 days from 12 Jun) — 2 days remaining
- **Next step:** Provide PO or FlexPoints approval to Access Group; within 3 weeks of approval, consultant will reach out to agree delivery timelines

**Important T&C:** Where FlexPoints are due to expire, the customer has **3 months to utilise them from the date of expiry**. The 29 June expiry is therefore not a hard cliff — Oxford has until approximately 29 September 2026 to use committed points. However, the **quote itself expires 26 June** regardless, so approval must be given by Thursday.

**Background:** Kevin holds 2,935 flex points expiring 29 June 2026. Chemistry bulk deletion (£525) is already committed and in flight (UAT signed off 23 Jun). Marie Cooksey's sign-off on the Holiday Records flex points spend was sought on 17 June — confirm whether that has been given.

---

## Note for Kevin

Wednesday's calendar shows no other meetings scheduled. Priority actions after this call:
- Confirm or chase Maura's E-Form fix (case 69001555) and complete the IM URL updates
- Review and sign off Azure CR work item 126017 (DSE SBS exclusion)
- Chase Reenu Delaney if no Chemistry live deployment confirmation received
- **Approve flex points for case 69001638 before 26 June** — quote expires Thursday

---

*Prepared: 23 June 2026 | Updated: 24 June 2026 (flex points quote received) | Sources: Granola (FA Catch-up 18/06, HR Systems Roadmap 19/06), Command Centre tasks.json, Work Inbox briefing.json (refreshed 17:31 Tue 23 Jun), Access Group Project Scope Document case 69001638 V1.0*