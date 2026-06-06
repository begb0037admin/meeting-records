# Meeting Review — This Week (w/c 20 Apr 2026)
**Generated:** 22 April 2026
**Meetings covered:** 3

---

## Meetings

### H&S Roadmap 20/04 — Monday 20 April, 8:55 AM
**Attendees:** Kevin + team (Chris, James, Rob referenced; Joanne, Jonathan, Sharon, Sonia also mentioned)
**Summary:** Covered Cority applicant upload progress — handover to James is complete and the first production upload is targeted for Friday next week, with recurring merges the week after. A major new workstream was flagged: a retention policies project starting July that covers complex multi-rule scenarios (ionising radiation, COSH, etc.) and carries significant compliance risk. Kevin and Chris need to draft a business case for executive funding.
**Decisions:**
- James to take ownership of applicant merge process going forward
- Retention policies project to be scoped with a business case and priority matrix
- Kevin to include DSE system update in Azure Integrations meeting the following day

**Actions:**
- [ ] James: Install GPG (Cleopatra), compare current report with month-old snapshot
- [ ] James: Present data quality questions to Chris at Monday's roadmap meeting
- [ ] Kevin: Reach out to Chris and Rob to schedule retention policies business case development
- [ ] Kevin: Confirm DSE update included in Azure Integrations meeting (Tue 21)
- [ ] Chris: Follow up on LTC/Odyssey communication to avoid duplication
- [ ] Chris: Arrange forced standing meeting with unresponsive contact
- [ ] Kevin & Chris: Draft retention policies summary paper with Rob, including priority matrix and resource requirements

---

### Azure Integration Platform Sprint Review — Tuesday 21 April, 8:59 AM
**Attendees:** Kevin + Azure integration team (David, Shazad, Climatics team referenced)
**Summary:** Sprint 38 review covered three successful go-lives in two weeks: Saïd Business School, Employee Self-Service, and Extended StuTalk. Two technical demos were presented — PACS mapping tool (automated department code changes via durable functions) and DSE integration solution (Cosmos DB export with configurable CSV/JSON output). Key risk flagged: 164 failed Halo webhook records across 3 sprints due to outdated department reference data on the Halo side.
**Decisions:**
- Oracle integration POC complete; solution design workshop to follow on Thursday
- Symplectic API replacement to be explored (current BizTalk integration has data quality issues)
- Data loader deployment delayed pending Kingsway soft upgrade (planned next sprint)
- DSE to be deployed to sandbox for client testing in Sprint 39

**Actions:**
- [ ] Team: Schedule Oracle planning meeting (tomorrow from Sprint Review date — Wed 22 Apr)
- [ ] Halo team: Update their reference data to clear 164 failed webhook records — flag if this needs a chase from Kevin
- [ ] Team: PACS mapping tool — final testing and potential go-live in Sprint 39
- [ ] Team: Begin card and registration data integration design in Sprint 39
- [ ] Team: Kick off Orms integration sprint zero (planning, ways of working, regular catchups)

---

### DTP1092 College Staff in PXD 21/04 — Tuesday 21 April, 2:00 PM
**Attendees:** Kevin + project team (Connor, Steve, Simon, Melanie Furness referenced)
**Summary:** Progressed the college staff data upload configuration for PXD. Key decisions made on the two-stage upload process (Connor's base load first, then UDF data with appointment IDs), and field requirements were locked down including additional UDFs for Academic title, Fellowship, and HE-SIR REF fields. Upcoming training on new reference data and hierarchy is confirmed for Monday 27 April — Kevin prefers this date as he's off the following week.
**Decisions:**
- Two-stage upload approach confirmed: Connor's load first, then UDF data
- Person-level data (diversity, address, contact info) will not overwrite existing records
- Existing employees to be identified by employee number; personal data not updated
- Files to be shared via SharePoint in Excel format; HR converts to pipe-delimited CSV

**Actions:**
- [ ] Kevin: Accept invite for Friday hierarchy clarification meeting
- [ ] Kevin: Speak with Simon about data warehouse integration requirements
- [ ] Kevin: Confirm Monday 27 April afternoon session for reference data/hierarchy training
- [ ] Steve: Determine testing parameters and develop test scripts
- [ ] Melanie Furness: Assist with impact assessment
- [ ] Team: Define lookup process to identify existing vs new records before upload
- [ ] Research Services: Specify BI report requirements for college staff data

---

## Consolidated Actions

| Action | Owner | Meeting |
|---|---|---|
| Install GPG (Cleopatra), compare report with month-old snapshot | James | H&S Roadmap |
| Present data quality questions to Chris at Monday's roadmap meeting | James | H&S Roadmap |
| Draft retention policies business case with Chris and Rob | Kevin | H&S Roadmap |
| Follow up on LTC/Odyssey communication to avoid duplication | Chris | H&S Roadmap |
| Arrange forced standing meeting with unresponsive contact | Chris | H&S Roadmap |
| Chase Halo team to update reference data (164 failed webhook records) | Kevin / Team | Azure Sprint Review |
| PACS mapping tool — final testing and go-live | Team | Azure Sprint Review |
| Begin card and registration data integration design | Team | Azure Sprint Review |
| Kick off Orms integration sprint zero | Team | Azure Sprint Review |
| Accept invite for Friday hierarchy clarification meeting | Kevin | College Staff PXD |
| Speak with Simon re data warehouse integration requirements | Kevin | College Staff PXD |
| Confirm Mon 27 Apr afternoon training session | Kevin | College Staff PXD |
| Determine testing parameters and develop test scripts | Steve | College Staff PXD |
| Define lookup process for existing vs new employee records | Team | College Staff PXD |
| Specify BI report requirements for college staff data | Research Services | College Staff PXD |
