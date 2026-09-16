from datetime import datetime
from brief_chrome import SCRATCH, e, render_page, write_brief_output

# ---- EIGHTH PASS, 16 Sept 2026 (meeting day): added a "what this is" context
#      line and a speaker-note line to every item, on top of the sixth pass's
#      decluttered table format. Every item now carries three parts: What
#      (1-2 sentence context, so the item is recognisable without re-reading
#      source), Status (current position, unchanged from the sixth pass),
#      and Say (a short talking point in Kevin's own voice, grounded in the
#      same real source already gathered for that item -- not generic
#      filler, same standing pattern as the KPI Presentation deck's speaker
#      notes). The addendum table gets one speaker-note line at the section
#      level rather than per-row, since those are lower-stakes reference
#      items, not agenda discussion items -- "per item or per section" was
#      explicitly allowed.
#
#      NINTH PASS, same day: Kevin's What lines weren't concrete enough --
#      several read as a restated title rather than the actual specific
#      change/issue plus who raised it and when. Rewrote every SK 1-1 and
#      Managers Meeting item's What field to lead with the concrete
#      specific (using the same transcript/task/email material already
#      verified in earlier passes, not new research) and name the
#      requester/date where the source actually supports it -- and to say
#      plainly where it doesn't (several 20 Aug items have no requester
#      named in the transcript beyond "raised at the meeting"; that's
#      stated as fact, not filled in with a guess). The addendum table's
#      status lines were left as-is -- they're standing-team-deck project
#      status entries, not requests, so "who requested" doesn't apply the
#      same way; already had a section-level speaker note as agreed.
#
#      No item, source tag, date, or the Athena exclusion was dropped. Full
#      pass-by-pass history is in Lauren's memory
#      (`managers-meeting-16sep-second-pass.md` and its addenda), not
#      repeated here.
#
#      One item from the SK 1-1 transcript (a colleague's confidential
#      upcoming leave) remains deliberately excluded throughout, per Kevin's
#      standing instruction earlier the same day.

SK_ITEMS = [
    {"id": "1", "title": "Org structure work &mdash; new management units &amp; docs", "pill": "info",
     "what": "Org structure: create three new pack management units in the system (a portal approach, not the old back-end process) and keep documentation updated &mdash; raised by Simon as Kevin's main focus item in the 19&nbsp;Aug 1-1.",
     "status": "No confirmation found since 19&nbsp;Aug that they've been created.",
     "say": "Let's get those three management units built and keep the docs updated as we go &mdash; has that actually started?"},
    {"id": "2", "title": "Cority Applicant Data Import (RECSUP20) &mdash; report fixes &amp; provenance question", "pill": "raise",
     "what": "RECSUP20's Cority interface file needs source-level PXD fixes (quote-stripping, CSV header/DOB formatting, 27-column completeness) and has a real provenance gap &mdash; no QA-server copy or change request on record for how it was built. A separate Cority column-mapping mismatch has its own support ticket open.",
     "status": "<i>Source: pasted email thread (\"Cority - Applicant Data Import file\" &mdash; Simon Burford/James Salas Guillen/Kevin Lelitte) &mdash; not connector/Granola-verified, per Kevin's instruction. Distinct from any other Cority-related item elsewhere in this brief.</i>",
     "say": "The Cority applicant import report needs real fixes at source, and nobody can tell me how it was originally built &mdash; I want an actual plan, not another patch."},
    {"id": "3", "title": "38-day leave balance &mdash; how-to guide with Michael", "pill": "info",
     "what": "38-day leave balance: write a how-to guide with Michael so the fix is repeatable (Clockify ref 208 already on the Roadmap) &mdash; raised by Simon in the 19&nbsp;Aug 1-1.",
     "status": "Guide's write-up not confirmed since 19&nbsp;Aug.",
     "say": "Did we actually get that how-to guide written with Michael, or is it still just in my head from the 1-1?"},
    {"id": "4", "title": "Relieve pressure on Michael &amp; Asta &mdash; take on PeopleXD work", "pill": "info",
     "what": "PeopleXD workload: take on more PeopleXD tasks directly to relieve Michael and Asta, who are stretched post-WFM go-live (high incident/sysadmin volume) &mdash; raised by Simon in the 19&nbsp;Aug 1-1.",
     "status": "Meeting with Michael set 20&nbsp;Aug to identify handover; not confirmed since.",
     "say": "What PeopleXD work did I actually end up taking off Michael's plate, and is it still the right split?"},
    {"id": "5", "title": "T-shirt size application-form question change with Michael", "pill": "info",
     "what": "Application form change: add internal-candidate identification to the application form &mdash; requested by Laura Porter/Phil Taylor, forwarded by Simon Burford 19&nbsp;Aug 15:51 (Kevin's effort estimate sent back 9&nbsp;Sept). To be t-shirt sized with Michael before Marie decides whether to progress it.",
     "status": "Sizing outcome not confirmed. Original sender (Laura Porter vs Phil Taylor) and whether Marie was cc'd &mdash; not confirmed from available connector data, no live Outlook/Graph search attempted.",
     "say": "Has the application-form change actually been sized with Michael, and did Marie decide whether to progress it?"},
    {"id": "6", "title": "Internal job-site portal 404 bug &mdash; raise as official ticket", "pill": "raise",
     "what": "Job-site bug: the internal job-site portal 404s, currently patched only with a pre-leave workaround &mdash; Kevin's own open item from the 19&nbsp;Aug 1-1, needs raising as an official ticket.",
     "status": "No ticket confirmed raised since 19&nbsp;Aug.",
     "say": "Has that 404 bug actually been logged as an official ticket yet?"},
    {"id": "7", "title": "Cover / plus-one for Simon at meetings", "pill": "info",
     "what": "Meeting cover: be Simon's stand-in/plus-one when he can't attend, particularly while the org structure work runs without dedicated PM cover &mdash; agreed directly between Simon and Kevin, confirmed verbatim in the 19&nbsp;Aug transcript (distinct from the separate Crispin PM-absence situation).",
     "status": "Standing arrangement &mdash; no specific instance to check yet.",
     "say": "Just confirming &mdash; I'm still your plus-one if you can't make a meeting, right?"},
    {"id": "8", "title": "Manage own workload &mdash; calendar breaks, avoid back-to-back meetings", "pill": "info",
     "what": "Workload management: calendar breaks and no back-to-back meetings, flagging early to Simon if struggling &mdash; part of Kevin's own return-to-work approach after surgery, agreed in the 19&nbsp;Aug 1-1.",
     "status": "Agreed approach; no specific update found.",
     "say": "The calendar-breaks approach is genuinely working &mdash; I'll flag you directly if that changes."},
    {"id": "9", "title": "Book PDR with Simon &mdash; late September", "pill": "resolved",
     "what": "PDR booking: Simon agreed to send Kevin a calendar invite for his PDR in late September &mdash; agreed in the 19&nbsp;Aug 1-1.",
     "status": "<b>Resolved</b> &mdash; confirmed for today, 15:00&ndash;16:00 (Google Calendar).",
     "say": "PDR's booked for later today &mdash; nothing needed from you on this one."},
    {"id": "10", "title": "Decide on remaining 2.5 days annual leave", "pill": "onhold",
     "what": "Annual leave: 2.5 days remaining need a decision &mdash; use them or carry over, with Jonathan updating the system if carried &mdash; raised by Kevin himself in the 19&nbsp;Aug 1-1.",
     "status": "No decision communicated to Simon on record since 19&nbsp;Aug.",
     "say": "I still owe you a decision on those 2.5 days &mdash; let me get back to you on that today."},
]

MM_ITEMS = [
    {"id": "1", "title": "Clockify budget decision &mdash; chase Jonathan", "pill": "raise",
     "what": "Clockify decision: the team's proposed move to Clockify for time-tracking needs Jonathan's budget sign-off, or falls back to evaluating Jibble and extracting existing data first &mdash; raised at the 20&nbsp;Aug meeting; Kevin to chase Jonathan directly.",
     "status": "No decision on record since 20&nbsp;Aug &mdash; still open.",
     "say": "Has Jonathan actually given us a yes or no on the Clockify budget?"},
    {"id": "2", "title": "Locate historical Clockify project code (2024 hours)", "pill": "onhold",
     "what": "Historical Clockify code: trace an old Clockify project code covering roughly 2024's logged hours &mdash; raised as an open team-wide ask at the 20&nbsp;Aug meeting (no specific requester named in the transcript).",
     "status": "Not found on record since 20&nbsp;Aug.",
     "say": "Did anyone ever track down that old 2024 Clockify code?"},
    {"id": "3", "title": "Leavers checklist &amp; incident-response one-pager", "pill": "raise",
     "what": "Leavers/incident one-pager: draft a one-pager covering who to inform and what to check when someone leaves or an incident happens &mdash; raised at the 20&nbsp;Aug meeting following a recent incident near-miss; Kevin asked to book the drafting session (specific requester not named in the transcript).",
     "status": "No fixed date agreed 20&nbsp;Aug; session with Kevin not confirmed held since.",
     "say": "I still owe the team that leavers/incident one-pager &mdash; let's get a session booked."},
    {"id": "4", "title": "WhatsApp group membership review", "pill": "onhold",
     "what": "WhatsApp membership: the work WhatsApp group used for team-wide alerts has stale/unclear membership (people who've left still in it, unnamed numbers) &mdash; a data-breach risk raised at the 20&nbsp;Aug meeting.",
     "status": "Due at \"the team meeting next week\" (transcript-confirmed wording); not confirmed done.",
     "say": "Did the WhatsApp membership review actually happen at last week's team meeting?"},
    {"id": "5", "title": "WFM meeting invite &mdash; data completeness", "pill": "onhold",
     "what": "WFM data completeness: some departments show only one sickness record for the whole year despite 300+ staff, a risk ahead of October's WFM go-live &mdash; raised at the 20&nbsp;Aug meeting; David already engaged on departmental readiness.",
     "status": "Not reconfirmed since 20&nbsp;Aug.",
     "say": "Has David actually confirmed every department's ready for the October go-live?"},
    {"id": "6", "title": "Signals absence reporting &mdash; meeting Tuesday", "pill": "onhold",
     "what": "Signals absence reporting: a separate recurring meeting Kevin needs adding back onto after being away &mdash; raised by Kevin himself at the 20&nbsp;Aug meeting, genuinely distinct from the WFM meeting above (transcript confirms two separate things, not one).",
     "status": "Invite status unconfirmed.",
     "say": "Did I actually get added to the Signals absence reporting invite for Tuesday?"},
    {"id": "7", "title": "Tableau &mdash; email Jasmine and Sarah", "pill": "raise",
     "what": "Tableau spreadsheet: update the spreadsheet behind the statutory equal pay audit (due roughly every 3 years) and loop in Reward-team contacts Jasmine and Sarah by email &mdash; raised at the 20&nbsp;Aug meeting (specific requester not named in the transcript).",
     "status": "Not confirmed sent since 20&nbsp;Aug.",
     "say": "Did that email to Jasmine and Sarah on the Tableau spreadsheet actually go out?"},
    {"id": "8", "title": "Tableau &mdash; final audit run + migration on Roadmap", "pill": "raise",
     "what": "Tableau migration: run the equal pay audit in Tableau one final time ahead of the July 2027 deadline, then migrate off Tableau over three years, added to the Roadmap with documented rationale &mdash; agreed at the 20&nbsp;Aug meeting.",
     "status": "Not confirmed added since 20&nbsp;Aug.",
     "say": "Is the Tableau migration actually written into the Roadmap yet, with the reasoning behind it?"},
    {"id": "9", "title": "PDR tracker &mdash; reshare with leads", "pill": "info",
     "what": "PDR tracker: reshare the tracker link with leads so booked/completed sessions stay visible across the whole team &mdash; raised at the 20&nbsp;Aug meeting as a general reminder to leads.",
     "status": "Kevin's own PDR is today; wider reshare to leads not confirmed.",
     "say": "Has the PDR tracker link actually gone back out to the leads?"},
    {"id": "10", "title": "Susan's acting-up allowance business case", "pill": "raise",
     "what": "Susan's business case: Kevin drafted a two-page business case (approx. &pound;300 total) for Susan's acting-up allowance at the 20&nbsp;Aug meeting, to raise with Renu in person once she's back from leave &mdash; no guarantee of approval.",
     "status": "1-1 with Renu not confirmed held since 20&nbsp;Aug.",
     "say": "Have you had that conversation with Renu on Susan's case yet?"},
    {"id": "11", "title": "PSP work &mdash; via lead first, escalate to Renu if unresolved", "pill": "onhold",
     "what": "PSP work process: PSP requests should route via the team lead first, with backfill agreed before it's taken on, escalating to Renu only if unresolved &mdash; discussed at the 20&nbsp;Aug meeting, part of a wider strategic workforce review Sarah Kay is running on Renu's behalf.",
     "status": "No update on record since 20&nbsp;Aug &mdash; needs a live check.",
     "say": "Are we actually holding the line on PSP work coming via the lead first?"},
    {"id": "12", "title": "Nathan's AI inbox-logging skill", "pill": "new",
     "what": "Nathan's AI skill: a rough prototype that reads the applicant inbox and logs requests into a spreadsheet automatically, demoed live by Nathan at the 20&nbsp;Aug meeting &mdash; could free up Anne and Henry's time on inbox cover once refined.",
     "status": "Real, demoed live 20&nbsp;Aug (confirmed via transcript). No further refinement/sharing on record.",
     "say": "Has Nathan's inbox-logging skill moved on at all since his demo?"},
    {"id": "13", "title": "Executive dashboard &mdash; on hold pending data structure", "pill": "onhold",
     "what": "Executive dashboard: can't be built until the underlying calculation data is properly structured &mdash; status update given at the 20&nbsp;Aug meeting.",
     "status": "Progress made, not complete; no update since 20&nbsp;Aug.",
     "say": "Where's the calculation data got to &mdash; any closer to being able to build that dashboard?"},
    {"id": "14", "title": "Broken SharePoint links &mdash; Julian to review/fix", "pill": "info",
     "what": "Broken SharePoint links: a Codex scan Kevin ran surfaced broken hyperlinks across SharePoint pages (majority in the cyber security section), shared at the 20&nbsp;Aug meeting &mdash; Julian has the output (page, URL, link name) to work through.",
     "status": "No completion on record.",
     "say": "How far through the broken-links list has Julian actually got?"},
    {"id": "15", "title": "OSM data access &mdash; for AI-driven FAQ/theme analysis", "pill": "onhold",
     "what": "OSM data access: early thinking on getting more direct access to OSM's support-request data, to use AI (not Power Automate &mdash; ruled out, non-Microsoft) to spot themes and maybe automate FAQ-style responses &mdash; discussed at the 20&nbsp;Aug meeting.",
     "status": "Early-stage only. No movement on record since 20&nbsp;Aug.",
     "say": "Has there been any real movement on getting proper access to that OSM data?"},
]

# Pasted directly by Kevin (Oxford tenant thread already in hand) -- no
# connector/Granola verification needed or attempted for this one, per his
# own instruction. Source-tagged accordingly.
REF_HESA_WHAT = (
    "REF 2029 UDF upload file for the HESA annual return &mdash; Person-level UDF (not appointment-level), "
    "using the current CorePortal template, all 12 field columns retained even if blank (Contract Id / Appointment ID "
    "blank for person-level records)."
)
REF_HESA_STATUS = (
    "<b>Updated 15&nbsp;Sept (yesterday):</b> Nathan has matched the UDF template structure to the data items and "
    "re-confirmed the team is on track for delivery; Kevin gave technical guidance on keeping the Contract ID column "
    "and confirmed the current UDF template download is needed. "
    "<b>Deadline Thursday 17&nbsp;Sept &mdash; tomorrow</b> (moved up from 18&nbsp;Sept per Kevin's own 10&nbsp;Sept email). "
    "<i>Source: Command Centre task t2609141649162 (dated 15&nbsp;Sept) for the updated status; original item from a pasted "
    "email thread (Kevin &harr; Nathan Kirwan, cc Sarah Rowles) &mdash; neither connector/Granola-verified beyond the "
    "Command Centre task itself, per Kevin's instruction.</i>"
)
REF_HESA_SAY = "Good news on the HESA UDF &mdash; Nathan's confirmed the template structure matches and we're on track for tomorrow's upload."


def render_row(a):
    return f'''<tr>
            <td class="idcell">{a["id"]}</td>
            <td>{a["title"]} <span class="pill pill-{a["pill"]}">{ {"raise":"Raise","onhold":"Historic — unresolved","info":"Update","overdue":"Overdue","resolved":"Resolved","new":"New"}[a["pill"]] }</span></td>
            <td><b>What:</b> {a["what"]}<br><span class="cur-label">Status</span> {a["status"]}</td>
            <td><span class="say-label">Say</span> &ldquo;{a["say"]}&rdquo;</td>
          </tr>'''


def rows_table(items):
    rows = "\n".join(render_row(a) for a in items)
    return f'''<table>
          <thead><tr><th>#</th><th>Item</th><th>What / Status</th><th>Say this</th></tr></thead>
          <tbody>
{rows}
          </tbody>
        </table>'''


SK_TABLE = rows_table(SK_ITEMS)
MM_TABLE = rows_table(MM_ITEMS)

GLANCE_TABLE = """<table>
          <thead><tr><th>Section</th><th>Items</th></tr></thead>
          <tbody>
            <tr><td>Urgent &mdash; REF 2029 HESA UDF (pasted thread)</td><td>1 item, deadline tomorrow (17 Sept)</td></tr>
            <tr><td>SK 1-1, 19 Aug 2026 (Simon &rarr; Kevin)</td><td>10 action items</td></tr>
            <tr><td>HR Systems Managers Meeting, 20 Aug 2026</td><td>15 reconciled to-do items</td></tr>
            <tr><td>Also confirmed live (addendum)</td><td>8 items, live Sept 2026 Standing Agenda deck</td></tr>
          </tbody>
        </table>"""

SECTIONS = f"""
  <h2 class="h2-warn">Urgent &mdash; REF 2029 HESA UDF upload, deadline tomorrow</h2>
  <p class="body-loose"><b>REF 2029 HESA UDF Upload &mdash; Nathan Kirwan (Research Services).</b> {REF_HESA_WHAT} {REF_HESA_STATUS}</p>
  <p class="body-loose"><span class="say-label">Say</span> &ldquo;{REF_HESA_SAY}&rdquo;</p>

  <h2>SK 1-1, 19 August 2026 <span class="h2-sub">Actions for Kevin, from Simon &mdash; verified against the real transcript</span></h2>
  {SK_TABLE}

  <h2>HR Systems Managers Meeting, 20 August 2026 <span class="h2-sub">Reconciled to-do list &mdash; two relayed versions cross-checked against the real transcript</span></h2>
  {MM_TABLE}

  <h2 class="h2-warn">Reconciliation notes &mdash; resolved facts only</h2>
  <ul class="body-loose">
    <li>"WFM/signals absence" and "WFM/sickness" were wrongly merged in both relayed versions &mdash; they're two separate items (5 and 6 above).</li>
    <li>WhatsApp review timing confirmed as "next week," not "next team meeting."</li>
    <li>Nathan's AI inbox-logging skill and the executive dashboard are real and restored (items 12&ndash;13) after being dropped from one relayed version.</li>
    <li>PSP requests route via the team lead first, escalating to Renu only if unresolved &mdash; not "sign-off from Renu" directly (item 11).</li>
    <li>Not included: one inferred item ("share Codex broken-links output beyond Julian") &mdash; couldn't independently confirm, left out rather than guessed.</li>
  </ul>

  <h2>Also confirmed live &mdash; additional active items <span class="h2-sub">Live Sept 2026 Standing Agenda deck (local OneDrive)</span></h2>
  <p class="body-loose"><span class="say-label">Say</span> &ldquo;A few more things ticking along from the team's own Standing Agenda &mdash; nothing needs deciding here today, just flagging where they're at.&rdquo;</p>
  <table>
    <thead><tr><th>Item</th><th>Status</th></tr></thead>
    <tbody>
      <tr><td>Staff Request Audit / Insight</td><td>Reviewing PeopleXD's Insight audit capability for staff requests, following recent Access Group enhancements.</td></tr>
      <tr><td>My Development Reviews</td><td>The "My Development Reviews" process is being recreated ready for next year's appraisal cycle.</td></tr>
      <tr><td>IRIS Enhancements &amp; Eco Online Rollout</td><td>H&amp;S incident-system enhancements and the Eco Online rollout &mdash; kickoff 9&nbsp;Sept (also a Granola note same day); go-live confirmed night of Mon 28&nbsp;Sept.</td></tr>
      <tr><td>Sickness Absence Survey / Data Completeness</td><td>Biweekly WG validating sickness data ahead of the annual survey; survey due 9&nbsp;Oct, submission 27&nbsp;Nov; Power BI dashboard targeted end Sept.</td></tr>
      <tr><td>New Insight Reports for Annual Leave Duty</td><td>New Insight reports being built with Access Group for annual-leave audit duty; Holiday Records split into 3 reports; scoping meeting Fri 18&nbsp;Sept.</td></tr>
      <tr><td>Organisational Structure Update</td><td>Final PACS draft available; College/Hall entities moving level 2&rarr;3; College REF-structure deferred.</td></tr>
      <tr><td>SHSMS / H&amp;S Module Supplier Evaluation</td><td>Supplier requirements evaluation for the H&amp;S Management System; workshops begin 25&nbsp;Sept; Entra ID handover and score approval next.</td></tr>
      <tr><td>38-Day Balance Rollout &ndash; Departmental</td><td>Departmental rollout of the 38-day leave balance changes; Chemistry first (131 workgroups), GLAM next; period-end starts 5&nbsp;Oct.</td></tr>
    </tbody>
  </table>
"""

FOOTNOTE = """<div class="footnote">
    Rebuilt 16 Sept 2026 for today's 10:00 sitting; context lines and speaker notes added same day per Kevin's request &middot; Sources: SK 1-1 transcript (not_dIj3MwTSbme10y, 19 Aug), Managers Meeting transcript (not_ZSu5h6SBdMTD9o, 20 Aug), Monthly Standing Agenda September 2026.pptx (local OneDrive), a pasted email thread for the REF 2029 HESA UDF item and the Cority/RECSUP20 item (neither connector-verified, per Kevin), Work Inbox + Command Centre (pulled 15&ndash;16 Sept).<br>
    One SK 1-1 transcript item (a colleague's confidential upcoming leave) is deliberately omitted throughout, per Kevin's standing instruction.<br>
    Tenth same-day authorized exception to the 21 Aug 2026 pipeline-review content-push freeze &mdash; not a general lifting of it. Full pass-by-pass history in Lauren's memory, not repeated here.<br>
    Branding: command-centre/BRANDING.md v2.0 &mdash; Oxford Navy, Inter, canonical crest. Template shared via brief_chrome.py.
  </div>"""

html_out = render_page(
    title="HR Systems Managers Meeting — 16/09",
    app_name="HR Systems Managers Meeting",
    kicker="Speaking Brief &middot; Draft",
    h1="HR Systems Managers Meeting — 16/09",
    meta_spans=[
        "<b>Meeting</b> Today, Wednesday 16 September 2026, 10:00",
        "<b>Built from</b> SK 1-1 (19 Aug) &amp; Managers Meeting (20 Aug), transcript-verified",
        "<b>Status</b> Context lines + speaker notes added, 16 Sept 2026",
    ],
    flag_label="Before anything else",
    flag_paragraphs=[
        "REF 2029 HESA UDF upload is due tomorrow &mdash; see the top item.",
        "Everything else is dated 19&ndash;20&nbsp;Aug with no confirmed update since, per Work Inbox/Command Centre as of today. That's the honest picture, not padding.",
    ],
    glance_label="At a glance",
    glance_sub="1 urgent + 10 SK 1-1 + 15 Managers Meeting + 8 addendum items",
    glance_table_html=GLANCE_TABLE,
    sections_html=SECTIONS,
    footnote_html=FOOTNOTE,
)

# Named for the meeting date (16 Sept), not the generation date -- matches
# the convention every other brief in this pipeline follows.
write_brief_output(html_out, "HR Systems Managers Meeting", date=datetime(2026, 9, 16))
