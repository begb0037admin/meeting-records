from datetime import datetime
from brief_chrome import SCRATCH, e, render_page, write_brief_output

# ---- SIXTH PASS, 16 Sept 2026 (meeting day): decluttering pass on the fifth
#      pass's full rebuild, per Kevin's feedback that it read too noisy.
#      Converted the SK 1-1 / Managers Meeting item cards into compact table
#      rows (item + one tight status line + pill), trimmed the reconciliation
#      notes down to resolved facts only (the working-out lives in Lauren's
#      own memory record, not the brief), and tightened wording throughout.
#      No item, source tag, date, or the Athena exclusion was dropped -- this
#      is a presentation cut, not a content cut. Full history of every prior
#      same-day pass (agenda refresh, fold-in, reorder, recent-activity
#      section, full replace from SK1-1/20Aug transcripts, the REF 2029 HESA
#      addition) is in Lauren's memory (`managers-meeting-16sep-second-pass.md`
#      and its addenda), not repeated here.
#
#      One item from the SK 1-1 transcript (a colleague's confidential
#      upcoming leave) remains deliberately excluded throughout, per Kevin's
#      standing instruction earlier the same day.

SK_ITEMS = [
    {"id": "1", "title": "Org structure work &mdash; new management units &amp; docs", "pill": "info", "owner": "Kevin",
     "note": "Create the 3 new pack management units, update docs as you go. No confirmation found since 19&nbsp;Aug that they've been created."},
    {"id": "2", "title": "Cority Applicant Data Import (RECSUP20) &mdash; report fixes &amp; provenance question", "pill": "raise", "owner": "Kevin / James Salas Guillen / Simon Burford",
     "note": "RECSUP20_Applicant Cority Interface File needs fixing at source in PXD: strip quotation marks, fix column headers splitting across CSV rows, format DOB dd/mm/yyyy with no time, ensure all 27 expected columns present even if blank (James, 11&nbsp;Aug) &mdash; plus a possible Cority column-mapping mismatch, separate support ticket open. Simon tested the export 18&nbsp;Aug: headers look fine in Notepad++, open question whether Cority handles quote-wrapped comma-containing fields (e.g. \"MATHS, PHYSICAL &amp; LIFE SCIENCES\"), DOB fix in progress. Simon also asked whether it's OK to strip spaces from column headings, and flagged a real provenance gap &mdash; no copy on the QA server, no change request on record, doesn't appear to have followed standard report development process. <i>Source: pasted email thread (\"Cority - Applicant Data Import file\") &mdash; not connector/Granola-verified, per Kevin's instruction. Distinct from any other Cority-related item elsewhere in this brief.</i>"},
    {"id": "3", "title": "38-day leave balance &mdash; how-to guide with Michael", "pill": "info", "owner": "Kevin",
     "note": "Clockify ref 208 already on Roadmap. Guide's write-up not confirmed since 19&nbsp;Aug."},
    {"id": "4", "title": "Relieve pressure on Michael &amp; Asta &mdash; take on PeopleXD work", "pill": "info", "owner": "Kevin",
     "note": "Meeting with Michael set 20&nbsp;Aug to identify handover; not confirmed since."},
    {"id": "5", "title": "T-shirt size application-form question change with Michael", "pill": "info", "owner": "Kevin",
     "note": "Trigger: \"Application form &ndash; identification of internal candidates,\" fwd by Simon Burford 19&nbsp;Aug 15:51; Kevin's effort estimate sent 9&nbsp;Sept. Original sender (Laura Porter vs Phil Taylor) and whether Marie was cc'd &mdash; not confirmed from available connector data, no live Outlook/Graph search attempted."},
    {"id": "6", "title": "Internal job-site portal 404 bug &mdash; raise as official ticket", "pill": "raise", "owner": "Kevin",
     "note": "Workaround only in place. No ticket confirmed raised since 19&nbsp;Aug."},
    {"id": "7", "title": "Cover / plus-one for Simon at meetings", "pill": "info", "owner": "Kevin",
     "note": "Standing arrangement, confirmed verbatim in the transcript (distinct from the separate Crispin PM-absence situation)."},
    {"id": "8", "title": "Manage own workload &mdash; calendar breaks, avoid back-to-back meetings", "pill": "info", "owner": "Kevin",
     "note": "Agreed as Kevin's return-to-work approach. No specific update found."},
    {"id": "9", "title": "Book PDR with Simon &mdash; late September", "pill": "resolved", "owner": "Kevin",
     "note": "<b>Resolved</b> &mdash; confirmed for today, 15:00&ndash;16:00 (Google Calendar)."},
    {"id": "10", "title": "Decide on remaining 2.5 days annual leave", "pill": "onhold", "owner": "Kevin",
     "note": "No decision communicated to Simon on record since 19&nbsp;Aug."},
]

MM_ITEMS = [
    {"id": "1", "title": "Clockify budget decision &mdash; chase Jonathan", "pill": "raise", "owner": "Kevin",
     "note": "No decision on record since 20&nbsp;Aug &mdash; still open."},
    {"id": "2", "title": "Locate historical Clockify project code (2024 hours)", "pill": "onhold", "owner": "Kevin",
     "note": "Not found on record since 20&nbsp;Aug."},
    {"id": "3", "title": "Leavers checklist &amp; incident-response one-pager", "pill": "raise", "owner": "Kevin",
     "note": "No fixed date agreed 20&nbsp;Aug; session not confirmed held since."},
    {"id": "4", "title": "WhatsApp group membership review", "pill": "onhold", "owner": "Kevin",
     "note": "Due at \"the team meeting next week\" (transcript-confirmed wording); not confirmed done."},
    {"id": "5", "title": "WFM meeting invite &mdash; data completeness", "pill": "onhold", "owner": "Kevin",
     "note": "David engaged on Oct go-live readiness; not reconfirmed since 20&nbsp;Aug."},
    {"id": "6", "title": "Signals absence reporting &mdash; meeting Tuesday", "pill": "onhold", "owner": "Kevin",
     "note": "Separate item from #5 above (transcript confirms two distinct meetings, not one). Invite status unconfirmed."},
    {"id": "7", "title": "Tableau &mdash; email Jasmine and Sarah", "pill": "raise", "owner": "Kevin",
     "note": "Not confirmed sent since 20&nbsp;Aug."},
    {"id": "8", "title": "Tableau &mdash; final audit run + migration on Roadmap", "pill": "raise", "owner": "Kevin",
     "note": "Migration not confirmed added to the Roadmap since 20&nbsp;Aug."},
    {"id": "9", "title": "PDR tracker &mdash; reshare with leads", "pill": "info", "owner": "Kevin",
     "note": "Kevin's own PDR is today; wider reshare to leads not confirmed."},
    {"id": "10", "title": "Susan's acting-up allowance business case", "pill": "raise", "owner": "Kevin",
     "note": "1-1 with Renu not confirmed held since 20&nbsp;Aug."},
    {"id": "11", "title": "PSP work &mdash; via lead first, escalate to Renu if unresolved", "pill": "onhold", "owner": "Kevin",
     "note": "No update on record since 20&nbsp;Aug &mdash; needs a live check."},
    {"id": "12", "title": "Nathan's AI inbox-logging skill", "pill": "new", "owner": "Nathan",
     "note": "Real, demoed live 20&nbsp;Aug (confirmed via transcript). No further refinement/sharing on record."},
    {"id": "13", "title": "Executive dashboard &mdash; on hold pending data structure", "pill": "onhold", "owner": "Kevin",
     "note": "Blocked on calculation-data structuring; no update since 20&nbsp;Aug."},
    {"id": "14", "title": "Broken SharePoint links &mdash; Julian to review/fix", "pill": "info", "owner": "Julian",
     "note": "Majority of breaks in cyber security section. No completion on record."},
    {"id": "15", "title": "OSM data access &mdash; for AI-driven FAQ/theme analysis", "pill": "onhold", "owner": "Kevin",
     "note": "Early-stage only. No movement on record since 20&nbsp;Aug."},
]

# Pasted directly by Kevin (Oxford tenant thread already in hand) -- no
# connector/Granola verification needed or attempted for this one, per his
# own instruction. Source-tagged accordingly.
REF_HESA_NOTE = (
    "Person-level UDF via CorePortal template, 12 field columns retained (Contract Id / Appointment ID blank). "
    "Nathan preparing the file; last confirmed correct 10&nbsp;Sept. "
    "<b>Deadline Thursday 17&nbsp;Sept &mdash; tomorrow</b> (moved up from 18&nbsp;Sept per Kevin's own 10&nbsp;Sept email). "
    "<i>Source: pasted email thread (Kevin &harr; Nathan Kirwan, cc Sarah Rowles) &mdash; not connector/Granola-verified, per Kevin's instruction.</i>"
)


def render_row(a):
    return f'''<tr>
            <td class="idcell">{a["id"]}</td>
            <td>{a["title"]} <span class="pill pill-{a["pill"]}">{ {"raise":"Raise","onhold":"Historic — unresolved","info":"Update","overdue":"Overdue","resolved":"Resolved","new":"New"}[a["pill"]] }</span></td>
            <td>{a["note"]}</td>
          </tr>'''


def rows_table(items):
    rows = "\n".join(render_row(a) for a in items)
    return f'''<table>
          <thead><tr><th>#</th><th>Item</th><th>Current position</th></tr></thead>
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
  <p class="body-loose"><b>REF 2029 HESA UDF Upload &mdash; Nathan Kirwan (Research Services).</b> {REF_HESA_NOTE}</p>

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
  <table>
    <thead><tr><th>Item</th><th>Status</th></tr></thead>
    <tbody>
      <tr><td>Staff Request Audit / Insight</td><td>Reviewing audit capability after Access Group enhancements.</td></tr>
      <tr><td>My Development Reviews</td><td>Being recreated for next year's cycle.</td></tr>
      <tr><td>IRIS Enhancements &amp; Eco Online Rollout</td><td>Kickoff 9&nbsp;Sept (also a Granola note same day); go-live confirmed night of Mon 28&nbsp;Sept.</td></tr>
      <tr><td>Sickness Absence Survey / Data Completeness</td><td>Biweekly WG; survey due 9&nbsp;Oct, submission 27&nbsp;Nov; Power BI dashboard targeted end Sept.</td></tr>
      <tr><td>New Insight Reports for Annual Leave Duty</td><td>With Access Group; Holiday Records split into 3 reports; scoping meeting Fri 18&nbsp;Sept.</td></tr>
      <tr><td>Organisational Structure Update</td><td>Final PACS draft available; College/Hall entities moving level 2&rarr;3; College REF-structure deferred.</td></tr>
      <tr><td>SHSMS / H&amp;S Module Supplier Evaluation</td><td>Supplier workshops begin 25&nbsp;Sept; Entra ID handover and score approval next.</td></tr>
      <tr><td>38-Day Balance Rollout &ndash; Departmental</td><td>Chemistry first (131 workgroups), GLAM next; period-end starts 5&nbsp;Oct.</td></tr>
    </tbody>
  </table>
"""

FOOTNOTE = """<div class="footnote">
    Rebuilt 16 Sept 2026 for today's 10:00 sitting, decluttered same day per Kevin's feedback &middot; Sources: SK 1-1 transcript (not_dIj3MwTSbme10y, 19 Aug), Managers Meeting transcript (not_ZSu5h6SBdMTD9o, 20 Aug), Monthly Standing Agenda September 2026.pptx (local OneDrive), a pasted email thread for the REF 2029 HESA UDF item (not connector-verified, per Kevin), Work Inbox + Command Centre (pulled 15&ndash;16 Sept).<br>
    One SK 1-1 transcript item (a colleague's confidential upcoming leave) is deliberately omitted throughout, per Kevin's standing instruction.<br>
    Sixth same-day authorized exception to the 21 Aug 2026 pipeline-review content-push freeze &mdash; not a general lifting of it. Full pass-by-pass history in Lauren's memory, not repeated here.<br>
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
        "<b>Status</b> Decluttered rebuild, 16 Sept 2026",
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
