from datetime import datetime
from brief_chrome import SCRATCH, e, render_page, write_brief_output

# ---- FIFTH PASS, 16 Sept 2026 (meeting day): FULL REPLACE of everything
#      built in the four earlier same-day passes (the 24-June/20-Aug
#      15-item agenda, the reorder, and the "recent activity" section) --
#      per Kevin's explicit instruction, none of that carries forward.
#
#      This build is sourced entirely from two real captured meetings:
#      SK 1-1 (19 Aug 2026, Simon Burford -> Kevin) and HR Systems Managers
#      Meeting (20 Aug 2026). The Managers Meeting had two independently
#      relayed to-do lists (v1/v2) with real discrepancies -- both were
#      cross-checked against the actual Granola transcript (not just the
#      machine summary) before reconciling. See the "Reconciliation notes"
#      risk-block in SECTIONS for exactly what was corrected and why.
#
#      One item present in the real SK 1-1 transcript (a colleague's
#      upcoming maternity leave, mentioned in passing under first-line
#      support capacity) is deliberately excluded from every field below,
#      per Kevin's standing instruction earlier the same day that this is
#      confidential and must leave no trace in any brief, script, or
#      committed record. Not referenced further here.
#
#      Eight additional items (Staff Request Audit/Insight, My Development
#      Reviews, IRIS Enhancements & Eco Online Rollout, Sickness Absence
#      Survey/Data Completeness, New Insight Reports for Annual Leave Duty,
#      Organisational Structure Update, SHSMS/H&S Module Supplier Evaluation,
#      38-Day Balance Rollout) were added across two follow-up instructions
#      after the full-replace request -- sourced from the live September
#      2026 Monthly Standing Agenda deck (local OneDrive), same source
#      already verified earlier the same day; IRIS also corroborated by a
#      9 Sept Granola note. Presented separately below, not as full agenda
#      cards. Kevin confirmed this is the last batch.
#
#      Meeting day note: today is Wednesday 16 September 2026 -- this is
#      TODAY's 10:00 sitting, not tomorrow's.

SK_ITEMS = [
    {
        "id": "1", "title": "Org structure work &mdash; new management units &amp; documentation",
        "pill": "info", "owner": "Kevin",
        "desc": "Focus on the org structure work: create the three new pack management units in the system, and update documentation as you go.",
        "lu_date": "19 Aug", "lu_text": "Three new pack management units confirmed needed; portal approach expected easier than the old back-end process; safe to use the U environment (C environment cloned/replicated).",
        "current": "No further confirmation found in Work Inbox or Command Centre since 19&nbsp;Aug on whether the units have actually been created &mdash; worth a quick status check.",
        "say": "Get the three new pack management units created, and keep documentation updated as you go.",
    },
    {
        "id": "2", "title": "Support James &mdash; applicant data import report",
        "pill": "info", "owner": "Kevin",
        "desc": "Support James on the applicant data import report &mdash; dig into Lee/Grace's old emails for background on the report's setup and change history.",
        "lu_date": "19 Aug", "lu_text": "Meeting with James set for 20&nbsp;Aug to go through the report and background.",
        "current": "Not independently confirmed whether that meeting happened or what it found. <b>Don't conflate with the separate Cority Applicant Data Import thread</b> &mdash; different system, tracked separately elsewhere.",
        "say": "Confirm with James where the background-digging landed, and whether the report/change-history question is settled.",
    },
    {
        "id": "3", "title": "38-day leave balance &mdash; how-to guide with Michael",
        "pill": "info", "owner": "Kevin",
        "desc": "Put together a how-to guide for the 38-day leave balance issue with Michael, and identify PeopleXD tasks Kevin can pick up to relieve pressure.",
        "lu_date": "19 Aug", "lu_text": "Meeting with Michael moved to 20&nbsp;Aug (Michael off that Friday); Clockify item already raised and on the Roadmap (reference 208).",
        "current": "The wider 38-day-balance departmental rollout is now genuinely live and moving fast (Chemistry piloting, 131 workgroups) &mdash; worth checking whether this specific how-to guide ever got written, separately from the rollout itself.",
        "say": "Did the how-to guide with Michael actually get written, and is it usable now the rollout's under way?",
    },
    {
        "id": "4", "title": "Relieve pressure on Michael &amp; Asta &mdash; take on PeopleXD work",
        "pill": "info", "owner": "Kevin",
        "desc": "Michael and Asta are under significant pressure post-WFM go-live (high incident/sysadmin volume). Kevin asked to start picking up more PeopleXD tasks directly.",
        "lu_date": "19 Aug", "lu_text": "Meeting with Michael set for 20&nbsp;Aug to identify what can be taken on; Asta said she was on top of her own queue for now.",
        "current": "No dedicated record found of what was actually handed over &mdash; worth confirming rather than assuming it happened.",
        "say": "What PeopleXD work did I actually end up picking up from Michael, and is it still the right split?",
    },
    {
        "id": "5", "title": "T-shirt size application-form question change with Michael",
        "pill": "info", "owner": "Kevin",
        "desc": "T-shirt size the application-form question change request (Laura Porter / Phil Taylor) with Michael, before Marie decides whether to progress it.",
        "lu_date": "19 Aug", "lu_text": "Meeting with Laura already scheduled for the following week (separate internal job-site confusion query).",
        "current": "No update found since 19&nbsp;Aug on the sizing outcome or Marie's decision.",
        "say": "Has the application-form change actually been sized with Michael, and did Marie make a call on progressing it?",
    },
    {
        "id": "6", "title": "Internal job-site portal 404 bug &mdash; raise as an official ticket",
        "pill": "raise", "owner": "Kevin",
        "desc": "The internal job-site portal 404 bug has a workaround applied pre-leave; needs a proper fix raised as an official ticket.",
        "lu_date": "19 Aug", "lu_text": "Workaround only in place &mdash; no permanent fix yet.",
        "current": "No record found of a ticket actually being raised since 19&nbsp;Aug.",
        "say": "Has the 404 bug actually been logged as an official ticket yet, or is it still running on the workaround?",
    },
    {
        "id": "7", "title": "Cover / plus-one for Simon at meetings",
        "pill": "info", "owner": "Kevin",
        "desc": "Be Simon's cover and plus-one at relevant meetings if he's unable to attend, particularly while the org structure work runs without dedicated PM cover.",
        "lu_date": "19 Aug", "lu_text": "Agreed directly between Simon and Kevin in the 1-1 &mdash; confirmed verbatim in the transcript, distinct from the separate Crispin PM-absence situation.",
        "current": "Standing arrangement, not a one-off action &mdash; no specific instance to check yet.",
        "say": "Confirm this is still the working arrangement, and flag if it's actually been used yet.",
    },
    {
        "id": "8", "title": "Manage own workload &mdash; calendar breaks, avoid back-to-back meetings",
        "pill": "info", "owner": "Kevin",
        "desc": "Put breaks into the calendar, avoid excessive back-to-back meetings, and flag early to Simon if struggling &mdash; part of Kevin's return-to-work approach.",
        "lu_date": "19 Aug", "lu_text": "Agreed as the working approach for Kevin's return &mdash; no phased return, self-managed with breaks.",
        "current": "No specific update found &mdash; a personal check-in rather than a work item.",
        "say": "How's the calendar-breaks approach actually working in practice?",
    },
    {
        "id": "9", "title": "Book PDR with Simon &mdash; late September",
        "pill": "resolved", "owner": "Kevin",
        "desc": "Book PDR with Simon for late September 2026; Simon to send the calendar invite.",
        "lu_date": "19 Aug", "lu_text": "Simon said he'd send a calendar invite for late September.",
        "current": "<b>Resolved</b> &mdash; Kevin's 2026 PDR is confirmed for <b>today, 16&nbsp;Sept, 15:00&ndash;16:00</b> (Google Calendar), per Lauren's own PDR 2026 build record.",
        "say": "Confirmed &mdash; PDR's booked for later today. Nothing further needed on this one.",
    },
    {
        "id": "10", "title": "Decide on remaining 2.5 days annual leave",
        "pill": "onhold", "owner": "Kevin",
        "desc": "Decide whether to use or carry over the remaining 2.5 days of annual leave, then let Simon know (Jonathan needs to update the system if carrying over).",
        "lu_date": "19 Aug", "lu_text": "No decision needed immediately &mdash; carry-over likely fine.",
        "current": "No record found of a decision having been communicated since 19&nbsp;Aug.",
        "say": "Has a decision on the 2.5 days actually gone back to Simon yet?",
    },
]

MM_ITEMS = [
    {
        "id": "1", "title": "Clockify budget decision &mdash; chase Jonathan",
        "pill": "raise", "owner": "Kevin",
        "desc": "Chase Jonathan this week on Clockify budget/approval; if no funding, begin evaluating Jibble as a backup and extract all existing Clockify data before any transition.",
        "lu_date": "20 Aug", "lu_text": "Jonathan to be asked directly; assume no funding if no response, then evaluate alternatives.",
        "current": "No Work Inbox or Command Centre record of Jonathan's decision since 20&nbsp;Aug &mdash; still genuinely open.",
        "say": "Has Jonathan actually given a yes/no on Clockify funding yet?",
    },
    {
        "id": "2", "title": "Locate historical Clockify project code (2024 hours)",
        "pill": "onhold", "owner": "Kevin",
        "desc": "Find or confirm the Clockify project code for the historical ~2024 logged hours, in case it's needed.",
        "lu_date": "20 Aug", "lu_text": "Raised as an open ask in the meeting &mdash; \"if anybody finds it, let me know.\"",
        "current": "No record of this being found since 20&nbsp;Aug.",
        "say": "Has anyone actually turned up that old 2024 Clockify code?",
    },
    {
        "id": "3", "title": "Leavers checklist &amp; incident-response one-pager",
        "pill": "raise", "owner": "Kevin",
        "desc": "Book a session with Kevin to draft the leavers checklist and incident-response one-pager while details are fresh.",
        "lu_date": "20 Aug", "lu_text": "No fixed date agreed &mdash; Kevin to book the session.",
        "current": "No record of the session having happened since 20&nbsp;Aug.",
        "say": "Has that session with me on the leavers/incident checklist actually happened yet?",
    },
    {
        "id": "4", "title": "WhatsApp group membership review",
        "pill": "onhold", "owner": "Kevin",
        "desc": "Review Work-related WhatsApp group membership at the team meeting next week; send the link out beforehand, and double-check membership against the full team list to catch anyone missing.",
        "lu_date": "20 Aug", "lu_text": "Confirmed some people in the group shouldn't be, and some entries have no names attached &mdash; data-breach risk cited as the driver.",
        "current": "No record of the review actually happening.",
        "say": "Did the WhatsApp membership review happen at last week's team meeting, or is it still outstanding?",
    },
    {
        "id": "5", "title": "WFM meeting invite &mdash; data completeness",
        "pill": "onhold", "owner": "Kevin",
        "desc": "Add Kevin to the invite for the next WFM meeting (data completeness ahead of October go-live).",
        "lu_date": "20 Aug", "lu_text": "Some departments showing only one sickness record for the year despite 300+ staff; David engaged to confirm departmental readiness.",
        "current": "Overlaps live activity already elsewhere on this brief's radar (38-day-balance departmental rollout moving fast today) &mdash; worth checking whether October go-live confidence has genuinely improved.",
        "say": "Has David confirmed all departments are actually on board for October go-live?",
    },
    {
        "id": "6", "title": "Signals absence reporting &mdash; meeting Tuesday",
        "pill": "onhold", "owner": "Kevin",
        "desc": "Add Kevin to the invite for the <b>Signals absence reporting</b> meeting, happening Tuesday &mdash; a genuinely separate item from the WFM meeting above, confirmed as its own named thing in the raw transcript.",
        "lu_date": "20 Aug", "lu_text": "Kevin flagged he wasn't sure of current status after being away; team agreed to get him onto the Tuesday invite.",
        "current": "No record found either way since 20&nbsp;Aug &mdash; genuinely unconfirmed whether Kevin actually got added.",
        "say": "Did I actually get added to the Signals absence reporting invite for Tuesday?",
    },
    {
        "id": "7", "title": "Tableau &mdash; email Jasmine and Sarah",
        "pill": "raise", "owner": "Kevin",
        "desc": "Email Jasmine and Sarah, looping them in on updating the Tableau spreadsheet for the equal pay audit.",
        "lu_date": "20 Aug", "lu_text": "Equal pay audit due roughly every 3 years (next due ~July 2027).",
        "current": "No record of that email having gone out since 20&nbsp;Aug.",
        "say": "Did the email to Jasmine and Sarah on Tableau actually go out?",
    },
    {
        "id": "8", "title": "Tableau &mdash; final audit run + migration on Roadmap",
        "pill": "raise", "owner": "Kevin",
        "desc": "Run the equal pay audit in Tableau one final time ahead of the July 2027 deadline, then add the Tableau migration to the Roadmap with documented rationale.",
        "lu_date": "20 Aug", "lu_text": "Plan: one last Tableau run (~1 week effort), then migrate properly over three years.",
        "current": "No record of a new Roadmap entry for this migration since 20&nbsp;Aug.",
        "say": "Is the Tableau migration actually on the Roadmap yet, with the rationale written down?",
    },
    {
        "id": "9", "title": "PDR tracker &mdash; reshare with leads",
        "pill": "info", "owner": "Kevin",
        "desc": "Reshare the PDR tracker link with leads so booked/completed sessions stay visible.",
        "lu_date": "20 Aug", "lu_text": "Simon had booked his PDR at the time; other leads still to follow.",
        "current": "Kevin's own 2026 PDR is confirmed for <b>today</b> &mdash; worth checking this is being modelled for the wider team too, not just Kevin's own round.",
        "say": "Has the PDR tracker link actually gone back out to leads?",
    },
    {
        "id": "10", "title": "Susan's acting-up allowance business case",
        "pill": "raise", "owner": "Kevin",
        "desc": "Raise Susan's acting-up allowance business case (approx. &pound;300 total spend) with Renu in person, at the next one-to-one after Renu's return from leave.",
        "lu_date": "20 Aug", "lu_text": "Two-page business proposal drafted; no guarantees on approval.",
        "current": "No record of that one-to-one with Renu having happened yet.",
        "say": "Has the Renu conversation on Susan's case actually happened?",
    },
    {
        "id": "11", "title": "PSP work &mdash; sign-off via lead, escalate to Renu if unresolved",
        "pill": "onhold", "owner": "Kevin",
        "desc": "Team should not accept Professional Services Programme (PSP) work without it coming via the lead first, with backfill agreed if taken on; unresolved requests escalate to Renu.",
        "lu_date": "20 Aug", "lu_text": "Sarah Kay reviewing HR Systems under a strategic workforce planning review on Renu's behalf; JDs under review.",
        "current": "No update found in Work Inbox or Command Centre since 20&nbsp;Aug &mdash; needs a live check in the room.",
        "say": "Are we actually holding the line on PSP work needing to come via the lead first?",
    },
    {
        "id": "12", "title": "Nathan's AI inbox-logging skill",
        "pill": "new", "owner": "Nathan",
        "desc": "Nathan has a fledgling AI skill that opens HR Reporting, reads the applicant-inbox folder, and logs requests into a spreadsheet &mdash; still rough, needs tweaking. Sharing it more widely could free up Anne and Henry's time on applicant-inbox cover.",
        "lu_date": "20 Aug", "lu_text": "Nathan gave a live demo in the meeting; not yet refined.",
        "current": "No record of this being shared more widely or refined further since 20&nbsp;Aug.",
        "say": "Has Nathan's inbox-logging skill moved on at all since his demo?",
    },
    {
        "id": "13", "title": "Executive dashboard &mdash; on hold pending data structure",
        "pill": "onhold", "owner": "Kevin",
        "desc": "The executive dashboard is on hold until the underlying calculation data is properly structured &mdash; visuals can't be built without it.",
        "lu_date": "20 Aug", "lu_text": "Progress made on the data structure, but not complete.",
        "current": "No update found since 20&nbsp;Aug on whether the calculation data is now ready.",
        "say": "Where's the calculation data got to &mdash; any closer to being able to build the dashboard?",
    },
    {
        "id": "14", "title": "Broken SharePoint links &mdash; Julian to review/fix",
        "pill": "info", "owner": "Julian",
        "desc": "Julian to review and fix the broken SharePoint links identified via the Codex output; majority of current breaks are in the cyber security section.",
        "lu_date": "20 Aug", "lu_text": "Codex output gives page name, URL, and hyperlink name for each break.",
        "current": "No record of Julian's fixes being completed since 20&nbsp;Aug.",
        "say": "How far has Julian got through the broken-links list?",
    },
    {
        "id": "15", "title": "OSM data access &mdash; for AI-driven FAQ/theme analysis",
        "pill": "onhold", "owner": "Kevin",
        "desc": "Follow up on getting broader, more direct access to OSM data, to support analysing themes in FAQ-style requests using AI (Power Automate ruled out &mdash; not a Microsoft tool).",
        "lu_date": "20 Aug", "lu_text": "Early-stage thinking only; described as potentially complex.",
        "current": "No update found since 20&nbsp;Aug.",
        "say": "Has there been any movement on getting proper access to the OSM data for this?",
    },
]


def render_item(a, label="Say this"):
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

    <blockquote><span class="say-label">{label}</span><p>&ldquo;{a["say"]}&rdquo;</p></blockquote>
  </article>'''


SK_HTML = "\n".join(render_item(a, label="Kevin's next step") for a in SK_ITEMS)
MM_HTML = "\n".join(render_item(a, label="Say this") for a in MM_ITEMS)

GLANCE_TABLE = """<table>
          <thead><tr><th>Meeting</th><th>Items</th></tr></thead>
          <tbody>
            <tr><td>SK 1-1, 19 Aug 2026 (Simon &rarr; Kevin)</td><td>10 action items</td></tr>
            <tr><td>HR Systems Managers Meeting, 20 Aug 2026</td><td>15 reconciled to-do items (from two conflicting relayed lists, verified against the real transcript)</td></tr>
            <tr><td>Also confirmed live (addendum)</td><td>8 items, from the live Sept 2026 Standing Agenda deck</td></tr>
          </tbody>
        </table>"""

SECTIONS = f"""
  <h2>SK 1-1, 19 August 2026 <span class="h2-sub">Actions for Kevin, from Simon &mdash; verified against the real Granola transcript, not just the summary</span></h2>
  <div class="item-grid">
{SK_HTML}
  </div>

  <h2>HR Systems Managers Meeting, 20 August 2026 <span class="h2-sub">Reconciled to-do list &mdash; two independently relayed versions (v1/v2) cross-checked against the real transcript, not merged blindly</span></h2>
  <div class="item-grid">
{MM_HTML}
  </div>

  <h2 class="h2-warn">Reconciliation notes &mdash; v1 vs v2 of the 20 Aug meeting</h2>
  <div class="risk-block">
    <p class="risk-head">"WFM/signals absence" vs "WFM/sickness" &mdash; these are two separate items, not one</p>
    <p class="body-loose">Both relayed versions merged this into a single item. The raw transcript has Kevin asking separately about "the signals absence reporting" (its own named meeting, next sitting confirmed Tuesday) and, moments later, a separate remark about "the wfm stuff" with no date attached. Split into items&nbsp;5 and&nbsp;6 above &mdash; don't re-merge them.</p>
  </div>
  <div class="risk-block">
    <p class="risk-head">WhatsApp review timing &mdash; "next week" confirmed correct</p>
    <p class="body-loose">v1 said "next team meeting," v2 said "next week's team meeting." Transcript: "can somebody just add it for the team meeting next week?" &mdash; v2 was right, item&nbsp;4 above uses that wording.</p>
  </div>
  <div class="risk-block">
    <p class="risk-head">Nathan's AI inbox-logging skill and the executive dashboard &mdash; real, and restored</p>
    <p class="body-loose">v2 dropped both. The raw transcript confirms both are genuine, live discussion points from the meeting (Nathan's demo; the dashboard's data-structure blocker) &mdash; restored as items&nbsp;12 and&nbsp;13 above.</p>
  </div>
  <div class="risk-block">
    <p class="risk-head">PSP / Renu sign-off &mdash; corrected</p>
    <p class="body-loose">v2's "get sign-off from Renu before accepting any further PSP work" overstates it. The transcript is clear PSP requests should come via the team lead first, with escalation to Renu only if unresolved. Item&nbsp;11 above reflects the transcript, not either relayed version verbatim.</p>
  </div>
  <div class="risk-block">
    <p class="risk-head">Not included &mdash; couldn't independently confirm</p>
    <p class="body-loose">v1's inferred item "share the Codex broken-links output more widely with the team, beyond Julian" isn't clearly evidenced in the transcript passages checked (only Julian's own involvement is confirmed). Left out rather than guessed at &mdash; flagging here instead of asserting it as a to-do.</p>
  </div>

  <h2>Also confirmed live &mdash; additional active items <span class="h2-sub">Added per two follow-up instructions, sourced from the live September 2026 Monthly Standing Agenda deck (local OneDrive)</span></h2>
  <table>
    <thead><tr><th>Item</th><th>Status (from the deck's own notes)</th></tr></thead>
    <tbody>
      <tr><td>Staff Request Audit / Insight</td><td>Reviewing the audit capability within Insight following recent enhancements applied by Access Group.</td></tr>
      <tr><td>My Development Reviews</td><td>Being recreated ready for next year's cycle.</td></tr>
      <tr><td>IRIS Enhancements &amp; Eco Online Rollout</td><td>Project kickoff took place 9&nbsp;Sept (also corroborated by a Granola note dated the same day); go-live confirmed night of Mon 28&nbsp;Sept.</td></tr>
      <tr><td>Sickness Absence Survey / Data Completeness</td><td>Biweekly WG; survey due 9&nbsp;Oct, submission deadline 27&nbsp;Nov; Power BI dashboard targeted end Sept.</td></tr>
      <tr><td>New Insight Reports for Annual Leave Duty</td><td>With Access Group; Holiday Records split into 3 reports; first scoping meeting Fri 18&nbsp;Sept.</td></tr>
      <tr><td>Organisational Structure Update</td><td>Final PACS draft available; College/Hall entities moving level 2&rarr;3; College REF-structure work deferred.</td></tr>
      <tr><td>SHSMS / H&amp;S Module Supplier Evaluation</td><td>Supplier workshops begin 25&nbsp;Sept (revised deadline); Entra ID admin handover and score approval next.</td></tr>
      <tr><td>38-Day Balance Rollout &ndash; Departmental</td><td>Chemistry first (131 workgroups), GLAM next; period-end activities start 5&nbsp;Oct.</td></tr>
    </tbody>
  </table>
"""

FOOTNOTE = """<div class="footnote">
    Prepared/rebuilt 16 Sept 2026 for today's 10:00 sitting &middot; This build fully replaces four earlier same-day drafts, per Kevin's instruction &mdash; sourced entirely from real Granola transcripts: SK 1-1 (not_dIj3MwTSbme10y, 19 Aug 2026) and HR Systems Managers Meeting (not_ZSu5h6SBdMTD9o, 20 Aug 2026), both cross-checked against the raw transcript text, not just the machine-generated summary. Addendum items from Monthly Standing Agenda September 2026.pptx (local OneDrive).<br>
    One item from the SK 1-1 transcript (a colleague's confidential upcoming leave, mentioned in passing) is deliberately omitted throughout, per Kevin's standing instruction earlier the same day.<br>
    Fifth same-day authorized exception to the 21 Aug 2026 pipeline-review content-push freeze &mdash; see meeting-pipeline-review-21aug.md. Not a general lifting of that freeze.<br>
    Branding: command-centre/BRANDING.md v2.0 (4 Jul 2026) &mdash; Oxford Navy, Inter, canonical crest. Template shared with the HR Systems Roadmap brief via brief_chrome.py.
  </div>"""

html_out = render_page(
    title="HR Systems Managers Meeting — 16/09",
    app_name="HR Systems Managers Meeting",
    kicker="Speaking Brief &middot; Draft",
    h1="HR Systems Managers Meeting — 16/09",
    meta_spans=[
        "<b>Meeting</b> Today, Wednesday 16 September 2026, 10:00",
        "<b>Built from</b> SK 1-1 (19 Aug) &amp; Managers Meeting (20 Aug) &mdash; verified against real transcripts",
        "<b>Status</b> Full rebuild 16 Sept 2026 &mdash; ready for review",
    ],
    flag_label="Before anything else",
    flag_paragraphs=[
        "This brief was fully rebuilt today from two real captured meetings rather than the 24 June/20 Aug agenda used in earlier drafts. The 20&nbsp;Aug Managers Meeting had two independently relayed to-do lists with real discrepancies between them &mdash; both were checked against the actual Granola transcript before reconciling, not merged blindly. See the Reconciliation notes section for exactly what was corrected.",
        "Almost everything below is dated 19&ndash;20&nbsp;Aug with no confirmed update since &mdash; that's not padding, it's an honest reflection of what Work Inbox and Command Centre actually show (or don't) as of today. Tell me what's actually moved and I'll correct the record.",
    ],
    glance_label="At a glance",
    glance_sub="10 SK 1-1 items + 15 reconciled Managers Meeting items + 8 addendum items",
    glance_table_html=GLANCE_TABLE,
    sections_html=SECTIONS,
    footnote_html=FOOTNOTE,
)

# Named for the meeting date (16 Sept), not the generation date -- matches
# the convention every other brief in this pipeline follows.
write_brief_output(html_out, "HR Systems Managers Meeting", date=datetime(2026, 9, 16))
