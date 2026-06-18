# FA Team Morning Catch-up — Pre-Roadmap Meeting Prep
**Date:** Friday 19 June 2026
**Purpose:** Quick team check-in before 10:00 HR Systems Roadmap meeting
**Time needed:** ~20 minutes

---

## Items to raise

---

### 1. Asta — HR Reporting SSO Migration (Roadmap ID 179)
**Ask:** What is the current position? Any movement since March?

**Background:** HR Reporting currently has users logging in via separate username and password credentials. The project is to migrate those users onto Oxford's Single Sign-On (SSO) — same login they use for everything else — removing the need for separate HR Reporting accounts and reducing admin overhead.

As of the last roadmap update (27 March 2026): Richard Jessett had shared a list of desktop users; Asta had sent the trial migration list to the project team; desktop services were preparing to migrate test users. User guidance, account provisioning process, and first-line support documentation still needed updating before a broader rollout could happen.

The recorded deadline was 30 April 2026. That has passed with no roadmap update since March. This will come up at 10:00 — need a one-line position before walking in.

---

### 2. Asta — Org Hierarchy COREPORTAL_ADMIN menu options
**Ask:** Has the comparison of enabled vs required menu options been completed and sent?

**Background:** PeopleXD org structure management (creating and editing the org hierarchy — departments, cost centres, pay admin codes) has always been done in the Back Office. During Kevin's absence, when the team tried to process org structure changes they found the Portal simply did not have the right menu options enabled. The root cause, confirmed by Michael on 17 June, is that org structure management was never migrated from Back Office to Portal when PeopleXD was originally configured — it has always been a gap.

Simon identified the specific options that need enabling across two groups in UOXU: the Hierarchy Group (Show org Hierarchy, Delete hierarchy by business units, Show my hierarchy, Get hierarchy by business units, Set hierarchy items, Log/link hierarchy items, Set hierarchy levels, Update hierarchy by business units) and the Post Management Group (Post Management, Post Appointment Maintenance, Post Management Parameters, Post Profile Maintenance, Post Restructuring, Post Profile Section History, Structure Setup, Terms and Conditions Maintenance, View Post Appointments). Some functionality may also sit under COREPORTAL_SUPPORT or COREPORTAL_HR_ADMIN_WEB — Asta's comparison will clarify.

A change request was raised in OSM on 17 June. The plan is to enable the confirmed options in UOXU first as a proof of concept, then roll out to DEV, TEST, QA, and LIVE. Kevin will produce How-To guidance as part of this work — no Portal-specific documentation currently exists. This is shaping up into a project in its own right.

Waiting on Asta's full confirmed comparison list before enabling anything.

---

### 3. James — H&S Dashboards (Roadmap ID 174_b)
**Ask:** Where did this land after March? Complete, or still in progress?

**Background:** David built a suite of Health and Safety dashboards drawing on Cority data that James loaded into the data warehouse (James fixed the underlying report and got all data loads working in October 2025). The dashboards cover H&S metrics and were built for the H&S management team. By February/March 2026 they were in a socialising phase — presented to SEG and Council, next steps agreed.

The roadmap's own recorded next step from March was to move onto Lucasz's project and release the dashboards to specific people, with the project team taking it forward from there. The recorded deadline was 31 March 2026. James was on leave until today — this is the first opportunity to find out whether this work completed, is ongoing, or has moved into a different stream.

---

### 4. James — DSE data feed post-go-live issues
**Ask:** HWP tickets with Gail Miller — any immediate actions needed? SBS exclusion — confirmed resolved by Azure team?

**Background:** The DSE (Display Screen Equipment) online assessment system data feed went live on 3 June 2026. This automatically uploads HR data (from PeopleXD) into the DSE system so staff assessments can be linked to their employment records. James was the lead on this. Three issues emerged immediately after go-live:

1. **SBS (Saïd Business School)** opted out of the main DSE system (they have their own) but were included in the initial feed. The Azure integrations team picked this up and are handling the exclusion. This was a known requirement that should have been built into the original feed — noted as disappointing at the time.
2. **Contractors** are missing from PeopleXD and therefore absent from the feed, despite having DSE requirements. A manual addition process is needed.
3. **Users without university email addresses** cannot get standard access — James was investigating this with the DSE supplier before he went on leave.

Separately, two open tickets in Healthy Working Plus (HWP) were pending a conversation with Gail Miller. James confirmed before his leave that these could wait until he was back. He is back today. James also confirmed on 10 June that the DSE automated data upload to HWP went live on 3 June and the overall dataset looks good.

---

### 5. Michael — WFM Rollout (Roadmap ID ITS1004)
**Ask:** Did the meeting with Julie happen? What is the current plan and revised timeline?

**Background:** WFM (Workforce Management) is the rostering and timesheet module within PeopleXD, used for casual and variable-hours staff. This has been a funded project since 2024 — the first stage was hierarchy setup for rostering (Michael met with Ralph Watson in May 2024 to begin configuration). The project has been running for over two years.

The recorded deadline on the roadmap is 29 May 2026. That has passed. The roadmap has not been updated since October 2025 — eight months ago — and carries no RAG status. This is the most significant gap in the roadmap and will definitely be raised at 10:00.

Context on why progress has been slow: Tom Harlos led the original WFM pilot as a solo worker and held almost all the knowledge. Very little was documented or passed on. Michael is the current lead and is the only person who can meaningfully assist with WFM queries coming in.

As of last week: Julie wanted to meet with Michael about WFM tasks that are coming in from departments. Michael pushed the meeting to the end of last week as he was prioritising clinical pay uplift and visa/HEAT record processing first. Need to know: did that meeting happen, and what is the current position and a realistic revised date to bring to the roadmap meeting?

---

### 6. Michael — OSPS Pension Employer Rates
**Ask:** Testing timeline — when can Tracy push payroll forward to October? Is the clinical pay uplift dependency still holding?

**Background:** OSPS (Oxford Staff Pension Scheme) employer contribution rates are changing in October 2026. A change has been raised in PeopleXD, tasks have been logged, and the support ticket has been closed — so the configuration work is underway.

Testing is currently blocked: to test the October rate changes, Tracy needs to push the payroll system forward to October, and that cannot happen until the current clinical pay uplift work is complete (clinical pay uplift is in test now and is Michael's top priority this week).

A separate change has also been raised for the April 2027 employee rate changes — so there are two pension-related changes in the pipeline.

One process note: the pensions contact had been coming via an old email chain rather than through the support route. Simon has since redirected them to raise support tickets properly.

This item is not currently on the roadmap. Michael is across it and it appears to be on track, but it needs visibility given the hard October deadline and the dependency chain. Worth raising today whether it should be added as a roadmap entry.

---

## Note for Kevin
The two items to get a confirmed position on before 10:00 are **Michael (WFM — ITS1004)** and **Asta (SSO Migration — 179)**. Both have passed deadlines and will be questioned directly. Even a one-line verbal update from each — current position and a rough revised date — is enough to walk into the meeting with confidence.

Insert any updates from this catch-up into the Roadmap Meeting Prep doc before the 10:00 start.
