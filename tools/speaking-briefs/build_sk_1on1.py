from brief_chrome import SCRATCH, e, render_page, write_brief_output

# ---- SK 1-1 (Kevin / Simon Burford fortnightly 1-1), including leave
#      handovers. First 1-1-style brief on this template — no tracked-items
#      master behind it, so this uses a different card shape from
#      build_roadmap.py / build_hs_roadmap.py: agenda-point cards (same
#      shape as build_managers_meeting.py's render_item) PLUS two things
#      that shape doesn't need — a "carry-over actions" table (open actions
#      Kevin owes Simon / Simon owes Kevin, tracked separately from the
#      discussion points) and a "leave handover" table (workstreams handed
#      over for Kevin's 10-27 July leave that aren't already a full agenda
#      item below).
#
# Sources — verified live in begb0037admin/meeting-records, 1 Aug 2026:
#   - Meeting Reviews/1-1 Simon — 26-06.md            (last CAPTURED 1-1 outcome)
#   - SK - Handover/docs/sessions/2026-06-24-sk-1on1.md (same-cycle PREP doc;
#     "Meeting Notes" section left "to be completed after the meeting" and
#     never was — superseded by the 26-06 capture, used here only as
#     corroborating context, not as a separate later meeting)
#   - Meeting Reviews/Leave Handover — Jul 2026.md     (Kevin's leave handover,
#     surgery 10 Jul, return 27 Jul — dated ~9-10 Jul, so newer than 26-06
#     on the items it touches)
#   - Meeting Reviews/HR Systems Roadmap — 03-07.md, HR Systems Managers
#     Meeting — 24-06.md, WFM Rostering — 30-06.md (cross-checks for
#     overlapping items)
#   - SK - Handover/docs/STATUS.md checked and found stale (last touched
#     1 Jun, still pointing at un-migrated legacy Work-account docs from
#     Apr/May) — NOT used as a source beyond confirming it has nothing more
#     current than the above.
#
# NOT checked: Granola. The Granola MCP connector was not connected in the
# session that built this script (repeated calls returned "not connected"),
# so it was not possible to confirm whether a more recent SK 1-1 exists
# there. Flagged prominently in the brief itself — do not remove that flag
# without actually checking Granola first.
#
# No SK 1-1 outcome is captured anywhere in the repo after 26 June, and that
# gap spans Kevin's own leave (10-27 July). The next sitting's date is not
# confirmed, so the brief title/meta deliberately does not invent one — though
# Work Inbox confirms it cannot be before Tue 4 Aug (Simon on leave until then).
#
# Work Inbox / Command Centre cross-reference (added per scope update, 1 Aug
# 2026 — read-only, every brief must be checked against these before being
# considered finished): checked begb0037admin/work-inbox/data/briefing.json
# (refreshed 31 Jul 11:31) and data/inbox_suggestions.json (generated 31 Jul
# 11:30), plus begb0037admin/command-centre/data/tasks.json (master task
# tracker, ids t001-t046, entries dated through 30 Jul). This surfaced real,
# dated progress the repo sources didn't have — notably that the REF-via-ESS
# UDF (item 6) was actually built and activated 7 Jul, before Kevin's leave,
# and that Command Centre's t025 (sourced from Julie Hickman's original
# email) resolves the w/c 1 vs w/c 6 July date conflict in favour of 6 July.
# Searched and found NOT tracked in either source: "Business rules for Data
# Warehouse", PFST/Sopra Steria, Accessplanit by name — noted as such rather
# than left silently unchecked. See each AGENDA item's "current" field and
# the Unresolved conflicts section for what changed and why.

AGENDA = [
    {
        "id": "1", "title": "Support cover, w/c 6 July — did it hold, and how did 13 July go?",
        "pill": "onhold", "owner": "Kevin",
        "desc": "Michael O'Sullivan and Emma both on leave w/c 6 July; Kevin on phased return (4hrs/day, mornings). Left no meaningful first-line HR Systems cover that week. Michael flagged as highest-risk absence: clinical pay uplift testing, OSPS pension changes, WFM lead, PeopleXD config queries.",
        "lu_date": "26 Jun", "lu_text": "Ask of Simon: does he need to be involved in agreeing the cover plan or communicating it to adjacent teams? Kevin to confirm the plan is signed off this week.",
        "current": "Command Centre task t025 (sourced directly from Julie Hickman's original 23&nbsp;June email, not a meeting note) confirms <b>w/c 6&nbsp;July is the correct date</b> &mdash; see Unresolved conflicts below, now resolved. t025 is still open (not marked done) with no cover arrangement ever logged. The pattern recurred almost immediately after: per the 3&nbsp;July Roadmap session, Kevin was out from 10&nbsp;July for ~2 weeks, Michael and Emma absent from 6&nbsp;July, Marie off 7&ndash;17&nbsp;July, and from 13&nbsp;July Sarah was the only manager standing (escalation chain Simon&nbsp;&rarr;&nbsp;Renu&nbsp;&rarr;&nbsp;Sarah). Separately, Work Inbox (refreshed 31&nbsp;Jul) shows the same pattern still recurring at the end of July: Michael and Beth both off sick 30&nbsp;July, Simon on annual leave until Tue&nbsp;4&nbsp;Aug, Sarah off until Mon&nbsp;3&nbsp;Aug.",
        "say": "Support cover w/c 6 July — did that actually hold up? And more importantly, how did the 13 July gap go while I was out — did the escalation chain get used? And are we about to repeat this again this week with Michael and Beth both off sick and you just back?",
    },
    {
        "id": "2", "title": "DTP1334 SHSMS — dedicated project resource",
        "pill": "raise", "owner": "Kevin",
        "desc": "H&amp;S Management System evaluation live. Implementation expected to start 20 July. Kevin's position: HR Systems needs dedicated project resource for this, not BAU capacity. Marie aware; rough recruiting timeline end Sept/Oct.",
        "lu_date": "26 Jun", "lu_text": "Ask of Simon: does he support the case for dedicated resource? Any levers to accelerate recruiting given the mid-July evaluation window?",
        "current": "Command Centre (t032) marks this <b>done</b>, but the underlying actions only show Kevin's side of the process moving &mdash; not proof the dedicated-resource ask was actually granted. Confirmed dated activity: Kevin sent his resourcing position to Marie and Simon directly on 3&nbsp;July (\"Evo/PeopleXD &mdash; resource requirement\"); Christopher Sanders sent legal-compliance requirements from the evaluation on 7&nbsp;July. The 3&nbsp;July Roadmap session flagged the 31&nbsp;July deadline as unachievable, and the 20&nbsp;July implementation start date has passed with nothing on record confirming it happened. Separately, and possibly connected: Work Inbox shows a new email from James Salas Guillen (30&nbsp;Jul) &mdash; funding for <b>Cority consultancy hours</b> now approved, James has proposed an allocation, Kevin needs to review, confirm allocation across the team, and arrange onboarding. Worth checking with Simon whether this is the dedicated-resource ask actually landing, or a separate line item.",
        "say": "SHSMS — I sent Marie and you my resourcing position back on 3 July. Did that land anywhere formal? And is the Cority consultancy hours funding James mentioned on 30 July connected to that ask, or something separate I need to allocate myself?",
    },
    {
        "id": "3", "title": "DPIA (Roadmap 136) — 30 June deadline",
        "pill": "overdue", "owner": "Marie Cooksey (sign-off) &middot; Kevin/Simon co-reviewed",
        "desc": "PeopleXD DPIA at Stage 7. Sign-off sitting with Marie Cooksey. Deadline was the day of the 26&nbsp;June 1-1 itself. Kevin and Simon co-reviewed the DPIA together in their March 1-1.",
        "lu_date": "26 Jun", "lu_text": "Ask of Simon: has he heard anything from Marie? Kevin chasing separately but flagging in case Simon has more direct visibility.",
        "current": "Command Centre (t009, still open) explains part of the delay: as of 4&nbsp;July, Marie was on annual leave and Kevin was assessing whether to chase for an expedited signature or defer until her return. Separately, SoundCloud (Oxford's new DPIA/security-assessment pilot tool) was proposed at the 24&nbsp;June Roadmap session with the WFM DPIA as the pilot case &mdash; Kevin was to be included in the SoundCloud team contact, but no confirmation that contact was ever made. No resolution on Stage&nbsp;7 sign-off itself has been captured anywhere &mdash; over five weeks on from the original 30&nbsp;June deadline.",
        "say": "DPIA sign-off was due 30 June — more than five weeks ago now. Did Marie ever get back to you once she was back from leave? And did the SoundCloud pilot contact ever happen?",
    },
    {
        "id": "4", "title": "WFM / GLAM rostering — resolution meeting outcome",
        "pill": "onhold", "owner": "Kevin",
        "desc": "Three areas outstanding: SBS, PEDS, GLAM. GLAM did not load rostering data at the last minute, blocking Sarah Rowles from running UC dashboards and reports. Kevin setting up a resolution meeting: Kevin, Simon, Marie, Michelle, Julie.",
        "lu_date": "26 Jun", "lu_text": "Ask of Simon: what days work next week? Kevin to send the invite.",
        "current": "The resolution meeting was held Monday 30&nbsp;June (attendees: Kevin, Simon, Marie, Michelle, Julie, Michael, Anna Carter-Windle). Intended outputs were a written action plan, an agreed GLAM position (re-engage / close out / escalate), and a formal reply to Cathy Hamer &amp; Linda Pope (Support Call#&nbsp;11688462). Command Centre (t035) is still open and shows nothing past the 24&nbsp;June meeting note either &mdash; the cross-check confirms the gap rather than closing it. No outcome document exists confirming what was actually decided, or whether Sarah's UC dashboards were ever unblocked.",
        "say": "The WFM/GLAM resolution meeting happened 30 June — where did we land on GLAM: re-engage, close out, or escalate? And did Sarah ever get her UC dashboards unblocked?",
    },
    {
        "id": "5", "title": "FP 68261303 — Multi Company Setup (DTP1092: Research Management Data for REF &amp; Research Quality)",
        "pill": "info", "owner": "Simon",
        "desc": "Underlying purpose is REF / research-quality reporting data; the active technical workstream is loading College/Halls staff data into PeopleXD (previously logged here only as \"College Staff into PXD\" — the tracker labels the sub-workstream, not the project's real purpose). Simon updated Conor O'Brien (Access Group) with the team's post-design proposal on 23 June.",
        "lu_date": "26 Jun", "lu_text": "Ask of Simon: is he expecting a substantive response from Conor? Anything Kevin needs to know before reviewing?",
        "current": "Command Centre marks the related tasks (t021 Multi Company Setup, t005 REF2029 pay admin codes, t020 COREPORTAL_ADMIN) as <b>done</b>, with dated progress through early July, then a real jump this month: as of 21&nbsp;Aug (confirmed live, this 1-1), the 40 REF2029 Pay Administered By codes are <b>fully configured in UOXU</b>, and the project has moved into <b>integrations testing</b> (Command Centre t2608031500570, target completion was 14&nbsp;Aug). Testing runs in <b>Company&nbsp;90</b> &mdash; Simon clarified 17&nbsp;Aug this was only ever a temporary WFM workgroup-attachment shell, not the permanent company setup, so it's being ignored in unrelated config work (e.g. balance periods) but remains the live testing surface here. Michael O'Sullivan confirmed 18&ndash;19&nbsp;Aug the UOXP&rarr;UOXC environment clone (not UOXU) completed and Access Group is proceeding on that basis. One live risk: Michael flagged a PeopleXD maintenance window <b>Friday 28&nbsp;August, 8&ndash;10pm</b>, that could land mid-test.",
        "say": "DTP1092 — remember this is really about our REF and research-quality reporting data, not just \"college staff into PXD.\" REF2029 codes are configured in UOXU, and we're testing in Company 90 — worth remembering that's your temporary WFM shell, not the permanent company setup. One flag: PeopleXD maintenance on the 28th, 8 to 10pm, could land mid-test — want to check that doesn't collide with anything.",
    },
    {
        "id": "6", "title": "REF attributes via ESS — deadline has moved on",
        "pill": "overdue", "owner": "Nathan / Sarah Rowles, Simon, Kevin",
        "desc": "Person-level UDF, three fields per appointment (REF qualifying contract, Unit of Assessment, academic employment function), RA indicator excluded. Nathan to arrange a scoping meeting with Kevin, Simon, and Michelle.",
        "lu_date": "26 Jun", "lu_text": "Ask of Simon: has he received the scoping meeting invite from Nathan? Worth a nudge if not.",
        "current": "Command Centre (t031, still open) shows this moved further than either repo source suggested: Kevin actually created the REF Outcomes UDF in UOXU and activated the data labels on <b>7&nbsp;July</b> &mdash; three days before going on leave &mdash; and Nathan confirmed the same day that all 12 required fields were displaying correctly for his testing. Kevin's July leave handover reframes the real deadline as 18&nbsp;September (load determinations into self-service), staff bulletin 21&nbsp;September, copy due 16&nbsp;September, with Nathan's remaining actions being the HESA population report (HF029) and the ISM request. Nothing confirms any progress on those since 7&nbsp;July.",
        "say": "REF via ESS — I got the UDF built and activated on 7 July before I left, and Nathan confirmed the fields were testing fine. Where's he got to on the HESA report and the ISM request since?",
    },
    {
        "id": "7", "title": "Sickness absence report — open-absence bug, pay impact",
        "pill": "new", "owner": "Simon (task number) &middot; Kevin (investigating)",
        "desc": "Report not picking up unclosed absences. Staff have gone onto half pay as a result. Simon flagged this at Managers Meeting 24 June; a task number was shared in that meeting.",
        "lu_date": "26 Jun", "lu_text": "Ask of Simon: can he provide the task number? Kevin investigating whether this is a SQL/RDL fix or a data quality issue.",
        "current": "Command Centre (t034, still open) confirms this is still unresolved and adds one link: on 3&nbsp;July, Sarah Rowles emailed about an OSM request for manager access to UOXU, which Kevin flagged as connected to this same investigation. The task number Simon was to share at the 24&nbsp;June meeting was still not logged as of that entry. No mention anywhere (3&nbsp;July Roadmap, 30&nbsp;June WFM Rostering, the July leave handover, or Command Centre) of the task number being retrieved or the root cause identified &mdash; status unknown, over five weeks on. Given the pay impact already confirmed (staff on half pay), this is one of the more consequential unresolved items in this brief.",
        "say": "The sickness absence report bug — staff going onto half pay because unclosed absences aren't being picked up. Did you ever send me that task number? I want eyes on this given the pay impact.",
    },
]


def render_item(a):
    return f'''
  <article class="item card">
    <header class="item-head">
      <span class="item-id">{a["id"]}</span>
      <h3 class="item-title">{a["title"]}</h3>
      <span class="pill pill-{a["pill"]}">{ {"raise":"Raise","onhold":"Historic — unresolved","info":"Update","overdue":"Overdue","resolved":"Resolved","new":"New"}[a["pill"]] }</span>
      <p class="item-owner">{a["owner"]}</p>
    </header>

    <p class="item-desc">{a["desc"]}</p>

    <div class="last-update">
      <span class="lu-label">Last logged update &middot; {a["lu_date"]}</span>
      <p>{a["lu_text"]}</p>
    </div>

    <p class="item-current"><span class="cur-label">Current position (this brief)</span>{a["current"]}</p>

    <blockquote><span class="say-label">Say this</span><p>&ldquo;{a["say"]}&rdquo;</p></blockquote>
  </article>'''


ITEMS_HTML = "\n".join(render_item(a) for a in AGENDA)

GLANCE_TABLE = """<table>
          <thead><tr><th>ID</th><th>Item</th><th>Owner</th><th>Type</th></tr></thead>
          <tbody>
            <tr><td class="idcell">1</td><td>Support cover w/c 6 Jul (+ 13 Jul gap)</td><td>Kevin</td><td><span class="pill pill-onhold">Historic</span></td></tr>
            <tr><td class="idcell">2</td><td>SHSMS dedicated resource</td><td>Kevin</td><td><span class="pill pill-raise">Raise</span></td></tr>
            <tr><td class="idcell">3</td><td>DPIA sign-off (Roadmap 136)</td><td>Marie</td><td><span class="pill pill-overdue">Overdue</span></td></tr>
            <tr><td class="idcell">4</td><td>WFM/GLAM resolution meeting outcome</td><td>Kevin</td><td><span class="pill pill-onhold">Historic</span></td></tr>
            <tr><td class="idcell">5</td><td>DTP1092 — REF/research-quality data (Company 90 testing)</td><td>Simon</td><td><span class="pill pill-info">Update</span></td></tr>
            <tr><td class="idcell">6</td><td>REF attributes via ESS</td><td>Nathan</td><td><span class="pill pill-overdue">Overdue</span></td></tr>
            <tr><td class="idcell">7</td><td>Sickness absence report bug</td><td>Simon</td><td><span class="pill pill-new">New</span></td></tr>
          </tbody>
        </table>"""

CARRYOVER_TABLE = """<div class="table-wrap card">
        <table>
          <thead><tr><th>Action</th><th>Owed by</th><th>Raised</th><th>Status</th></tr></thead>
          <tbody>
            <tr><td>Written response on org hierarchy / SharePoint documentation gap &mdash; guidance wasn't updated when the shared drive moved to SharePoint; Kevin to explain root cause and propose a team alignment meeting</td><td class="idcell">Kevin</td><td class="datecell">8 Jun</td><td><span class="pill pill-overdue">Outstanding</span> &mdash; Command Centre t006 confirms still open, nothing past 09 Jun</td></tr>
            <tr><td>P5 Incident #11687334 &mdash; review thread, confirm whether there's an agreement with LOD (Marie copied in by Simon)</td><td class="idcell">Kevin</td><td class="datecell">&le;26 Jun</td><td><span class="pill pill-resolved">Marked done</span> in Command Centre (t027) &mdash; but the logged action list still just says "review thread", no resolution written down. Worth a one-line confirm of what was actually decided.</td></tr>
            <tr><td>Business rules for Data Warehouse &mdash; review Simon's 22 June email, confirm if any action is required</td><td class="idcell">Kevin</td><td class="datecell">22 Jun</td><td><span class="pill pill-overdue">Outstanding</span> &mdash; not tracked in either Command Centre or Work Inbox; still purely Kevin's own action from Simon's email</td></tr>
            <tr><td>Set up 40 REF2029 Pay Administered By codes in UOXU &mdash; blocks further DTP1092 progress on Kevin's side</td><td class="idcell">Kevin</td><td class="datecell">&le;24 Jun</td><td><span class="pill pill-resolved">Marked done</span> in Command Centre (t005), with dated Company 90 testing progress through 7 Jul (Tony Boydell's Acceptance Criteria, Crispin's testing update)</td></tr>
          </tbody>
        </table>
      </div>"""

HANDOVER_ABSENCE_TABLE = """<div class="table-wrap card">
        <table>
          <thead><tr><th>Person</th><th>Dates</th><th>Returned</th></tr></thead>
          <tbody>
            <tr><td>Michael</td><td class="datecell">6&ndash;10 Jul</td><td class="datecell">Mon 13 Jul</td></tr>
            <tr><td>Marie C</td><td class="datecell">7&ndash;16 Jul</td><td class="datecell">Fri 17 / Mon 20 Jul</td></tr>
            <tr><td>Kevin</td><td class="datecell">From 10 Jul</td><td class="datecell">Mon 27 Jul</td></tr>
            <tr><td>Athena</td><td class="datecell">9&ndash;16 Jul</td><td class="datecell">After 16 Jul</td></tr>
            <tr><td>Chris</td><td class="datecell">13&ndash;23 Jul</td><td class="datecell">Thu 24 Jul</td></tr>
            <tr><td>David J</td><td class="datecell">13&ndash;16 Jul</td><td class="datecell">Mon 20 Jul</td></tr>
            <tr><td>Marie K</td><td class="datecell">13&ndash;20 Jul</td><td class="datecell">Tue 21 Jul</td></tr>
            <tr><td>Julie</td><td class="datecell">20&ndash;22 Jul</td><td class="datecell">Thu 23 Jul</td></tr>
            <tr><td>Asta</td><td class="datecell">22 Jul &ndash; 5 Aug</td><td class="datecell">Wed 6 Aug</td></tr>
            <tr><td>Sarah</td><td class="datecell">27&ndash;30 Jul</td><td class="datecell">Fri 31 Jul</td></tr>
          </tbody>
        </table>
      </div>"""

HANDOVER_FOLLOWUP_TABLE = """<div class="table-wrap card">
        <table>
          <thead><tr><th>Workstream</th><th>Status at handover (~9&ndash;10 Jul)</th><th>Ask now</th></tr></thead>
          <tbody>
            <tr><td>Non-Clinical Pay Uplift</td><td>Clinical live 27 Jul, Michael leading. Non-clinical TBC, likely August; Tracy testing. Command Centre adds: kick-off notification received 2&nbsp;Jul from Jasmin Khokhra &mdash; UCEA communication expected soon, needs coordinating ahead of holiday season.</td><td>Did clinical go live on the 27th as planned? Is non-clinical still tracking to August, and has the UCEA piece moved?</td></tr>
            <tr><td>Volunteering Absence Type</td><td>Option 2 (new pay code) confirmed as right approach. Oct/Nov timeline agreed; going on POG backlog for prioritisation. Command Centre (t036, still open) hasn't caught up to this &mdash; it still shows the earlier, pre-decision state (forward Matt Thomas's thread to Marie, awaiting her reply), not a contradiction, just staler.</td><td>Has this actually made it onto the POG backlog yet, or is it still sitting with Marie? Did Marie ever reply to Matt Thomas directly?</td></tr>
            <tr><td>PFST &mdash; Sopra Steria Data Assessment</td><td>8-week window, time-critical. Follow-up to be coordinated via Tom Harlos only. Not tracked in either Command Centre or Work Inbox &mdash; checked, found nothing.</td><td>Where did this land &mdash; is the 8-week window still on track?</td></tr>
            <tr><td>Julie &mdash; Training Checks (Accessplanit/Cosy)</td><td><b>Wed 22 July flagged as uncovered</b> &mdash; gates system access for users. Michelle asked but not confirmed at handover time. Command Centre (t039, still open) adds: Esther flagged as the cover option, Morgan's Power Automate tool and an OSM/Cosy integration are in progress but timeline unclear, and the mandatory training framework is going to People Committee for clearer ownership.</td><td>Did 22 July actually get covered in the end? Did Esther confirm, and where did the People Committee framework land?</td></tr>
          </tbody>
        </table>
      </div>"""

SECTIONS = f"""
  <h2>Agenda items — full context <span class="h2-sub">Carried forward from 26 June &middot; cross-checked against the 3 July Roadmap session, 24 June Managers Meeting, 30 June WFM Rostering, and the July leave handover where items overlap</span></h2>
  <div class="item-grid">
{ITEMS_HTML}
  </div>

  <h2>Carry-over actions — Kevin owes Simon <span class="h2-sub">From the 26 June 1-1, not discussion points in their own right</span></h2>
  {CARRYOVER_TABLE}

  <h2>Leave handover — closing the loop (10&ndash;27 July) <span class="h2-sub">Workstreams handed over during Kevin's leave that aren't already a full agenda item above</span></h2>
  <p class="body-loose">Team absence during Kevin's leave, for context &mdash; all dates below have now passed:</p>
  {HANDOVER_ABSENCE_TABLE}
  <p class="body-loose" style="margin-top:1.2rem;">Handed-over workstreams with no confirmed close-out on record since Kevin's 27 July return:</p>
  {HANDOVER_FOLLOWUP_TABLE}

  <h2 class="h2-warn">Risks and dependencies</h2>
  <p class="body-loose">The core risk is the same shape as the Managers Meeting and Roadmap briefs: <b>no SK 1-1 outcome has been captured for over five weeks</b>, and unlike those two, this gap directly overlaps Kevin's own leave (10&ndash;27 July) &mdash; the period with the least first-hand visibility of anyone. Three items above (SHSMS resourcing, REF via ESS, DPIA sign-off) are also live in the 5&nbsp;August Managers Meeting brief; a confirmed answer in one context should be carried into the other rather than re-asked from scratch.</p>
  <p class="body-loose">The sickness absence report bug (item 7) has a direct pay impact already confirmed (staff on half pay) and no follow-up captured anywhere &mdash; this is worth treating as higher priority than its "new" pill suggests, given the financial impact is not hypothetical.</p>
  <p class="body-loose">Granola was not reachable when this brief was built (connector not connected in that session) &mdash; the usual cross-check this template relies on to catch anything more recent than the last captured document could not be performed. Treat this brief as resting on repo documents only until Granola has been checked directly.</p>

  <h2>Unresolved conflicts</h2>
  <div class="risk-block">
    <p class="risk-head">Support-cover date resolved (Work Inbox / Command Centre cross-reference)</p>
    <p class="body-loose">The 24&nbsp;June SK 1-1 prep document (<code>SK - Handover/docs/sessions/2026-06-24-sk-1on1.md</code>) described the support-cover gap as w/c&nbsp;1&nbsp;July, while the 26&nbsp;June captured 1-1 outcome (<code>Meeting Reviews/1-1 Simon — 26-06.md</code>) described the same gap as w/c&nbsp;6&nbsp;July. Command Centre task t025 is sourced directly from Julie Hickman's original 23&nbsp;June email (not a meeting note, so a step closer to the primary source) and states <b>w/c 6&nbsp;July</b> &mdash; the same date the 26&nbsp;June review used. Treating the 24-06 prep doc's "w/c 1 July" as a slip rather than a second, real gap.</p>
  </div>
  <div class="risk-block">
    <p class="risk-head">Still unresolved: SK - Handover folder mid-migration, not fully pulled in</p>
    <p class="body-loose">The <code>SK - Handover</code> folder's own STATUS.md (last touched 1&nbsp;June) still describes itself as mid-migration, pointing at legacy Work-account documents ("Handover meeting preparation with Simon Burford", 28 Apr; "Kevin Lelitte leave handover w/c 4 May 2026", 29 Apr) that were never pulled into this repo. Those predate everything used in this brief and were not chased down &mdash; flagging in case either contains something still relevant.</p>
  </div>
  <div class="risk-block">
    <p class="risk-head">Command Centre &ldquo;done&rdquo; flags without a written resolution</p>
    <p class="body-loose">Command Centre marks t020, t021, t005, t027, and t032 as <b>done</b>, but for at least two of those (t020's own action list still ends on "awaiting Asta's comparison" / TODOs; t027's ends on "review thread" with no outcome recorded) the "done" flag isn't backed by a written resolution. Treat "done" in Command Centre as "someone closed this out," not as "the outcome is documented here."</p>
  </div>
"""

FOOTNOTE_HTML = """<div class="footnote">
    Prepared 1 Aug 2026 &middot; Sources: 1-1 Simon &mdash; 26-06.md (last captured 1-1 outcome), SK - Handover/docs/sessions/2026-06-24-sk-1on1.md (same-cycle prep doc, not a captured outcome), Leave Handover &mdash; Jul 2026.md, HR Systems Roadmap &mdash; 03-07.md, HR Systems Managers Meeting &mdash; 24-06.md, WFM Rostering &mdash; 30-06.md, work-inbox/data/briefing.json (refreshed 31 Jul 11:31) and data/inbox_suggestions.json (generated 31 Jul 11:30), command-centre/data/tasks.json (master task tracker, entries dated through 30 Jul). Granola NOT checked &mdash; connector was not connected in the session that built this brief; SK - Handover/docs/STATUS.md checked and found stale, not used as a source.<br>
    Draft only &mdash; not committed to meeting-records. Nothing published, sent, or scheduled. Next SK 1-1 sitting date is unconfirmed but cannot be before Tue 4 Aug (Simon on leave until then) &mdash; check with Simon.<br>
    Branding: command-centre/BRANDING.md v2.0 (4 Jul 2026) &mdash; Oxford Navy, Inter, canonical crest. Template shared with the other speaking briefs via brief_chrome.py.
  </div>"""

html_out = render_page(
    title="SK 1-1 — Kevin / Simon",
    app_name="SK 1-1 — Kevin / Simon",
    kicker="Speaking Brief &middot; Draft",
    h1="SK 1-1 — Kevin / Simon",
    meta_spans=[
        "<b>Meeting</b> Kevin / Simon fortnightly 1-1 &middot; not before Tue 4 Aug (Simon on leave)",
        "<b>Last captured outcome</b> Friday 26 June 2026",
        "<b>Status</b> Draft — not yet approved",
    ],
    flag_label="Before anything else",
    flag_paragraphs=[
        "No SK 1-1 outcome has been captured anywhere in this repo since <b>26&nbsp;June 2026</b> &mdash; over five weeks, and that gap spans Kevin's own leave (10&ndash;27&nbsp;July, surgery + recovery). Everything below carries the 26&nbsp;June agenda forward, cross-checked against the 3&nbsp;July HR Systems Roadmap session, the 24&nbsp;June HR Systems Managers Meeting, the 30&nbsp;June WFM Rostering resolution-meeting prep, Kevin's own July leave handover, and (as of this update) Work Inbox and Command Centre &mdash; not a confirmed account of what was actually raised or resolved at any 1-1 since.",
        "<b>Simon is on annual leave, returning Tuesday 4&nbsp;August</b> (Work Inbox, refreshed 31&nbsp;Jul 11:31) &mdash; the next SK 1-1 cannot happen before then. Michael and Beth were also both off sick as of 30&nbsp;July, so the same first-line cover gap flagged in item&nbsp;1 may already be recurring. The exact date of the next sitting is still not confirmed and has deliberately been left blank rather than guessed.",
        "<b>Work Inbox and Command Centre have now been checked</b> (read-only cross-reference, per scope) &mdash; several items below were updated as a result, most significantly item&nbsp;6 (REF via ESS: UDF was actually built and activated 7&nbsp;July, before Kevin's leave) and the w/c&nbsp;1/6&nbsp;July date conflict, now resolved in favour of 6&nbsp;July. See each item's \"Current position\" for what changed and its source.",
        "<b>Granola could not be checked</b> in the session that built this brief &mdash; the connector was not connected, and repeated attempts to reach it failed. It was not possible to confirm whether a more recent SK 1-1 exists there. Check Granola directly before relying on this.",
        "Tell me if I've got the wrong sources, or if anything below is out of date, and I'll correct it before this goes anywhere near a commit.",
    ],
    glance_label="At a glance",
    glance_sub="7 agenda items + 4 owed actions + 4 leave-handover follow-ups — carried forward from 26 Jun, cross-checked against Work Inbox/Command Centre through 31 Jul",
    glance_table_html=GLANCE_TABLE,
    sections_html=SECTIONS,
    footnote_html=FOOTNOTE_HTML,
)

write_brief_output(html_out, "SK 1-1")
