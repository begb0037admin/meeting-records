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

It is not yet clear who "Emma" refers to in this context — whether she is part of the HR Systems FA team or first-line Support — but Julie's message makes clear she is a named cover resource who would normally pick up that week.

This needs a named cover plan agreed in this meeting. The week starts in 8 days.

---

### 2. James — DSE SBS exclusion: Azure CR work item 126017 needs Kevin's sign-off
**Ask:** Has Kevin reviewed work item 126017 and signed off the Azure CR? If not, do it today.

**Background:** The DSE (Display Screen Equipment) online assessment data feed went live on 3 June 2026. One issue identified immediately after go-live was that Saïd Business School (SBS) was being included in the feed despite having opted out. SBS runs its own DSE provision and HWP charges per licence, so Oxford is paying for licences SBS will not use.

Marie asked James to raise a service request to get a cost estimate. Tony Boydell has now drafted the Azure change request as work item 126017 in Azure DevOps (Oxford University / Integration project). Kevin's sign-off is the immediate next step. Tony Boydell emailed Kevin and James directly on 23 June (received 10:29).

---

### 3. James — H&S Dashboards (Roadmap ID 174_b): end-of-June deadline in 6 days
**Ask:** Has Brian sent comms to the key stakeholders yet? If not, what is the escalation plan?

**Background:** A suite of H&S dashboards drawing on Cority data has been ready for release for some time. The blocker is Brian (H&S office) — he needs to send comms to key stakeholders before the dashboards can be formally published. The team set a self-imposed deadline of end of June — 6 days away. James has the most direct relationship with the H&S side and is now back from leave. What is the escalation route if Brian continues to delay past 30 June?

---

### 4. Asta — COREPORTAL_ADMIN org hierarchy menu options: comparison still awaited
**Ask:** Has Asta sent the full comparison of currently enabled vs required menu options on COREPORTAL_ADMIN?

**Background:** Org structure management was never migrated from Back Office to Portal when PeopleXD was originally configured. Simon Burford identified 16 menu options across two groups (Hierarchy Group and Post Management Group) that need enabling on COREPORTAL_ADMIN. Change 20020472 is raised in OSM and showing as Coordination Required with Kevin as Coordinator. Nothing can be enabled until Asta's comparison arrives.

---

### 5. Asta — SSO Migration (Roadmap ID 179): 3 July decision point approaching
**Ask:** What is the current position? Is no one else migrating until the remote apps issue is resolved? The 3 July deadline is 9 days away.

**Background:** During the week of 15 June, Kevin and James were migrated to Oxford SSO and a problem emerged: remote apps became inaccessible after migration. The rest of the team were advised not to migrate until this is resolved. At the catch-up on 22 June the position was to kick the deadline out to 3 July to determine whether to proceed or abandon the migration entirely.

---

### 6. Michael — WFM Rollout (Roadmap ID ITS1004)
**Ask:** Any update on the parameter review from last week's session? Anything to flag on the two departments still not live?

**Background:** A working session was held on 17 June. Michael took a task to review some parameters; Simon took a task to look at reports for first-line support staff. The group is due to reconvene in a couple of weeks. Michael is the only person with substantive WFM knowledge on the team.

---

### 7. Chemistry bulk delete — awaiting Reenu's live confirmation
**For info / action if no confirmation received:** Kevin signed off UAT on 23 Jun and instructed Reenu Delaney at Access Group to proceed to live. Still awaiting Reenu's confirmation email.

If no confirmation email has arrived by the time of this meeting, chase Reenu directly today.

---

### 8. IM Principles URL — Maura's config fix: Kevin to review and confirm
**Ask:** Has Kevin reviewed Maura McGlynn's config fix for case 69001555? The old URL retired yesterday.

**Background:** Kevin encountered a "Sorry But Page Not Found" error in all three environments when trying to update the URL in Search Appointments V4 E-Form Maintenance. Maura McGlynn applied a config fix and reports changes are now saving. Kevin needs to confirm before completing the remaining URL updates on the three intranet pages.

---

### 9. Asta — Holiday Records reports delivery: scheduling and involvement
**For info and action.** Flex points have been approved for case 69001638 (Holiday Records - 3 Reports Created). Access Group will make contact within 3 weeks to agree delivery timelines.

**Ask of Asta:** Kevin would like Asta to be involved in the delivery of these reports. Flag this now so Asta is aware and can factor it into her workload.

**Reports in scope (3 total, built by Payroll + WFM Consultant):**
- Annual Leave Record by Person and Leave Year
- Holiday Pay and Accrual Record for Variable-Hours and Casual Arrangements
- Holiday Pay in Lieu on Termination

**Context on timing:** Given July is thin on the ground (Michael and Emma absent w/c 1 July, Kevin on reduced hours, SHSMS evaluation workstream starting), the Managers Meeting will be used to agree when to schedule delivery. No commitment on timing yet — this is flagging Asta's involvement in advance.

---

### 10. REF attributes via ESS — new Roadmap item, end of July
**For awareness.** Sarah Rowles has added a new item to the HR Systems Roadmap: sharing specific REF attributes with staff via Employee Self-Service (ESS) by end of July 2026, to enable the REF appeals process. Simon Burford and Kevin Lelitte are named. Nathan (Sarah's team) is looking at it from the technical side.

**Key open question:** Will this require a new UDF to be set up and data loaded, or can existing UDFs be re-used? Athena Artuso noted in the thread that UDFs were set up in advance for future REF cycles, so the setup stage may already be done — it likely depends on exactly which REF attributes need to be surfaced. If it's just a data load, it should be straightforward.

**What Sarah has flagged:** The team is thin on the ground in July. This will need FA input, testing time, and business change support for user instructions. Anne is sharing last time's guidance, but this is NOT a like-for-like repeat.

**Ask of the team:** Is anyone already across what the specific REF attributes are? Can Asta confirm whether the UDFs already exist to cover them?

---

## Note for Kevin

Priority actions after this call:
- Confirm or chase Maura's E-Form fix (case 69001555) and complete the IM URL updates
- Review and sign off Azure CR work item 126017 (DSE SBS exclusion)
- Chase Reenu Delaney if no Chemistry live deployment confirmation received

---

*Prepared: 23 June 2026 | Updated: 24 June 2026 | Sources: Granola (FA Catch-up 18/06, HR Systems Roadmap 19/06), Command Centre tasks.json, Work Inbox briefing.json (refreshed 17:31 Tue 23 Jun), Access Group Project Scope Document case 69001638 V1.0*