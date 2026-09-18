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
#      TENTH PASS, same day: synced newer REF 2029 HESA UDF status (15 Sept,
#      via Command Centre task t2609141649162) into that item -- see the
#      REF_HESA_STATUS block below.
#
#      ELEVENTH PASS, same day: SK 1-1 item 4 replaced with real team ticket
#      queue stats (Linda/ticket system, pasted directly by Kevin) --
#      distilled to the 4 points actually worth raising in the room (209-day
#      escalation, 45% unassigned backlog, Michael's 3 stale CRs, Asta's
#      near-stale ticket) per Kevin's own follow-up correction; the full
#      per-person/per-ticket breakdown is NOT in this brief, only in Lauren's
#      memory record. Three items removed entirely, not shortened, per
#      Kevin's explicit noise-cut instructions: "Cover / plus-one for Simon
#      at meetings," "Manage own workload -- calendar breaks," and "Decide
#      on remaining 2.5 days annual leave." SK_ITEMS renumbered 1-7
#      (was 1-10) to close the gaps; no cross-references elsewhere in this
#      brief depended on SK item numbers (the Reconciliation-notes section
#      only references Managers Meeting item numbers, a separate table with
#      its own independent numbering).
#
#      TWELFTH PASS, same day: the RECSUP20/Cority provenance question (item
#      2) is now genuinely resolved via a real Codex Outlook connector search
#      of Kevin's own Sent Items (the plugin is actually wired up on this
#      machine -- checked `~/.codex/config.toml`, found `outlook-email@
#      openai-curated` enabled; ran `codex exec -s read-only
#      --skip-git-repo-check "<search prompt>"`, took ~2.5 min, found a real
#      match: Kevin's own 20 Aug reply to Simon Burford/James Salas Guillen
#      confirming Grace built the report originally and that CR 20020740 has
#      since been raised for retrospective change control). This is the
#      first genuinely connector-verified answer in this brief rather than a
#      pasted thread -- tagged accordingly, distinct from the item's
#      remaining pasted-thread content (the actual fix list).
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
    {"id": "1", "title": "Org structure work &mdash; TT2026 Implementation Track Plan (129 rows)", "pill": "raise",
     "what": "Organisational Structure Update (TT2026): 129 rows across three independent tracks &mdash; Track A (Department/HESA, 17 rows), Track B (Subsidiary companies, 26 rows), Track C (Colleges/Societies/REF, 86 rows &mdash; 43 colleges/societies &times; 2 rows each). Tracks A and B run in parallel and don't depend on Track C; roughly 43 rows are actionable now between them. (This is the same underlying work as Simon's 19&nbsp;Aug 1-1 note on \"three new management units\" &mdash; Track A's three creates.)",
     "status": "Track A: 3 creates, 2 dependent updates, 3 other updates/deletes, 7 zero-risk renames, 2 HESA notes &mdash; blocked on today's B8 code decision (meeting with Anna) and Anthony's active-people check on row 12 (KB). Track B: 5 deletions, 4 renames, 15 real creates (1 no-op pair skipped) &mdash; blocked on the same Anna meeting (subsidiary pay-admin/DEP-DIV codes) and active-people checks on 5 wind-down deletions. Track C is parked, not started &mdash; needs a joint session with Nathan and Simon on whether this is name-only or a real hierarchy move, and how Company&nbsp;90/REF codes are handled; none of the three payroll colleges (St Cross, Kellogg, Reuben) move until resolved. 6 open questions logged, biggest being the B8 decision and subsidiary DEP/DIV codes. Evidence approach: baseline saved; build/diff/file/promote done per track, not all at once. <i>Source: Implementation Track Plan.html (local, verified directly), updated 15&nbsp;Sept.</i>",
     "say": "Org structure update &mdash; 129 rows across three tracks. A and B, about 43 rows, are actionable now and mainly blocked on today's B8 decision and a couple of active-people checks. Track C, the 86 colleges/societies rows, stays parked until I've had a joint session with Nathan and Simon on the hierarchy question."},
    {"id": "2", "title": "Cority Applicant Data Import (RECSUP20) &mdash; CR raised, automation in progress", "pill": "raise",
     "what": "Provenance resolved: the report was originally built by Grace (not Lee), with a handover summary &mdash; James and Lee picked it up after she left, likely misattributed to Lee for want of a formal handover record. RECSUP20_Applicant Cority Interface File_V1 existed only in HR Reporting DEV, never QA/Production, never change-controlled. Kevin raised <b>CR 20020740</b> (9&nbsp;Sept) to formalise it, and has pulled together Grace's original SQL (incl. an unfinished/untested draft revision changing INNER to LEFT OUTER joins &mdash; a draft, not current logic), her testing plan/evidence, two rounds of test output, and her handover notes &mdash; shared at <code>I:\\ADMN\\PS\\HR Systems\\Support\\Analysis Team\\Grace - Investigations\\2025-03 Cority Applicant Data\\</code>. Grace's own notes flag what's outstanding: Cority-side testing, duplication-check training, and automating the pull/save process (always the intended fix for the current manual export).",
     "status": "<b>Live progress, 9&nbsp;Sept &mdash; not an unresolved gap:</b> Simon has built a test subscription report exporting CSV to <code>\\\\connect.ox.ac.uk\\ADMN\\PS\\HR Systems\\Support\\Analysis Team\\Cority Interface\\TESTING</code>, and asked James to test uploading it to Cority and check data/format. <b>Currently blocked:</b> automated export to the SharePoint folder is erroring (no detail/screenshot in the chain). Column-header rendering on the CSV auto-export is also unresolved (workaround under consideration: a reference header list to paste in). Two Cority questions remain genuinely unconfirmed &mdash; null handling (NULL vs N/A vs \"-\") and whether UTF-8 encoding is acceptable &mdash; not to be assumed resolved. Date format (UK vs US) also still needs confirming, and quote-wrapping around comma-containing fields (e.g. \"MATHS, PHYSICAL &amp; LIFE SCIENCES\") is being flagged as an error by Cority's upload process, raised separately with the Cority consultant. One simplification confirmed by James: column headers don't need to retain spaces/exact original names as long as column order is correct. <i>Source: pasted email chain, 9&nbsp;Sept &mdash; supersedes both the earlier pasted fix-list and the earlier Codex-connector-found Sent Items answer (20&nbsp;Aug), which had less detail than this chain.</i>",
     "say": "Where we are on Cority &mdash; provenance's sorted, Grace built it and CR 20020740's raised. Simon's got the automation build under way but blocked on a SharePoint export error. I'm flagging three things: the status of that blocker, James's CSV upload test results, and Cority's still-unconfirmed answers on nulls, encoding, and date format."},
    {"id": "3", "title": "38-day leave balance &mdash; how-to guide with Michael", "pill": "info",
     "what": "38-day leave balance: write a how-to guide with Michael so the fix is repeatable (Clockify ref 208 already on the Roadmap) &mdash; raised by Simon in the 19&nbsp;Aug 1-1.",
     "status": "Guide's write-up not confirmed since 19&nbsp;Aug.",
     "say": "The how-to guide with Michael hasn't been confirmed written yet &mdash; still an open action from the 1-1."},
    {"id": "4", "title": "Team ticket queue &mdash; 209-day escalation &amp; unassigned backlog", "pill": "raise",
     "what": "Team ticket queue snapshot as of today: 33 tickets total, 15 unassigned (45%), 5 stale (30+ days) &mdash; oldest is 209 days (James, #50929404, Odyssey-related, still only \"Accepted\"). Michael is carrying 3 stale CRs; Asta has one about to cross the stale threshold.",
     "status": "<i>Source: pasted ticket-system (Linda) data, supplied directly by Kevin as of today &mdash; not connector-verified. Full per-person/per-ticket breakdown kept in Lauren's own memory record, not in this brief.</i>",
     "say": "Two things from the ticket queue stand out: James's #50929404 has sat at 209 days and still isn't closed &mdash; that needs urgent escalation. And 45% of the queue, 15 of 33 tickets, is sitting unassigned. Separately, Michael's carrying three stale CRs and Asta has one about to cross the stale line."},
    {"id": "5", "title": "T-shirt size application-form question change with Michael", "pill": "info",
     "what": "Application form change: add internal-candidate identification to the application form &mdash; requested by Laura Porter/Phil Taylor, forwarded by Simon Burford 19&nbsp;Aug 15:51 (Kevin's effort estimate sent back 9&nbsp;Sept). To be t-shirt sized with Michael before Marie decides whether to progress it.",
     "status": "Sizing outcome not confirmed. Original sender (Laura Porter vs Phil Taylor) and whether Marie was cc'd &mdash; not confirmed from available connector data, no live Outlook/Graph search attempted.",
     "say": "The application-form change hasn't been confirmed sized with Michael yet, and Marie hasn't decided whether to progress it."},
    {"id": "6", "title": "Internal job-site portal 404 bug &mdash; raise as official ticket", "pill": "raise",
     "what": "Job-site bug: the internal job-site portal 404s, currently patched only with a pre-leave workaround &mdash; Kevin's own open item from the 19&nbsp;Aug 1-1, needs raising as an official ticket.",
     "status": "No ticket confirmed raised since 19&nbsp;Aug.",
     "say": "The 404 bug is still only patched with a workaround &mdash; it hasn't been logged as an official ticket yet."},
    {"id": "7", "title": "Book PDR with Simon &mdash; late September", "pill": "resolved",
     "what": "PDR booking: Simon agreed to send Kevin a calendar invite for his PDR in late September &mdash; agreed in the 19&nbsp;Aug 1-1.",
     "status": "<b>Resolved</b> &mdash; confirmed for today, 15:00&ndash;16:00 (Google Calendar).",
     "say": "PDR's booked for later today &mdash; nothing needed from you on this one."},
]

MM_ITEMS = [
    {"id": "1", "title": "Clockify budget decision &mdash; chase Jonathan", "pill": "raise",
     "what": "Clockify decision: the team's proposed move to Clockify for time-tracking needs Jonathan's budget sign-off, or falls back to evaluating Jibble and extracting existing data first &mdash; raised at the 20&nbsp;Aug meeting; Kevin to chase Jonathan directly.",
     "status": "No decision on record since 20&nbsp;Aug &mdash; still open.",
     "say": "Jonathan hasn't given a yes or no on the Clockify budget yet &mdash; I'll chase him directly this week."},
    {"id": "2", "title": "Locate historical Clockify project code (2024 hours)", "pill": "onhold",
     "what": "Historical Clockify code: trace an old Clockify project code covering roughly 2024's logged hours &mdash; raised as an open team-wide ask at the 20&nbsp;Aug meeting (no specific requester named in the transcript).",
     "status": "Not found on record since 20&nbsp;Aug.",
     "say": "Nobody's tracked down that old 2024 Clockify code yet."},
    {"id": "3", "title": "Leavers checklist &amp; incident-response one-pager", "pill": "raise",
     "what": "Leavers/incident one-pager: draft a one-pager covering who to inform and what to check when someone leaves or an incident happens &mdash; raised at the 20&nbsp;Aug meeting following a recent incident near-miss; Kevin asked to book the drafting session (specific requester not named in the transcript).",
     "status": "No fixed date agreed 20&nbsp;Aug; session with Kevin not confirmed held since.",
     "say": "I still owe the team that leavers/incident one-pager &mdash; I'll get a session booked."},
    {"id": "4", "title": "WhatsApp group membership review", "pill": "onhold",
     "what": "WhatsApp membership: the work WhatsApp group used for team-wide alerts has stale/unclear membership (people who've left still in it, unnamed numbers) &mdash; a data-breach risk raised at the 20&nbsp;Aug meeting.",
     "status": "Due at \"the team meeting next week\" (transcript-confirmed wording); not confirmed done.",
     "say": "The WhatsApp membership review hasn't been confirmed done yet."},
    {"id": "5", "title": "WFM meeting invite &mdash; data completeness", "pill": "onhold",
     "what": "WFM data completeness: some departments show only one sickness record for the whole year despite 300+ staff, a risk ahead of October's WFM go-live &mdash; raised at the 20&nbsp;Aug meeting; David already engaged on departmental readiness.",
     "status": "Not reconfirmed since 20&nbsp;Aug.",
     "say": "David hasn't confirmed yet that every department's ready for the October go-live."},
    {"id": "6", "title": "Signals absence reporting &mdash; meeting Tuesday", "pill": "onhold",
     "what": "Signals absence reporting: a separate recurring meeting Kevin needs adding back onto after being away &mdash; raised by Kevin himself at the 20&nbsp;Aug meeting, genuinely distinct from the WFM meeting above (transcript confirms two separate things, not one).",
     "status": "Invite status unconfirmed.",
     "say": "I still don't have confirmation I was added to the Signals absence reporting invite for Tuesday."},
    {"id": "7", "title": "PDR tracker &mdash; reshare with leads", "pill": "info",
     "what": "PDR tracker: reshare the tracker link with leads so booked/completed sessions stay visible across the whole team &mdash; raised at the 20&nbsp;Aug meeting as a general reminder to leads.",
     "status": "Kevin's own PDR is today; wider reshare to leads not confirmed.",
     "say": "The PDR tracker link hasn't been confirmed as resent to the leads yet."},
    {"id": "8", "title": "Nathan's AI inbox-logging skill", "pill": "new",
     "what": "Nathan's AI skill: a rough prototype that reads the applicant inbox and logs requests into a spreadsheet automatically, demoed live by Nathan at the 20&nbsp;Aug meeting &mdash; could free up Anne and Henry's time on inbox cover once refined.",
     "status": "Real, demoed live 20&nbsp;Aug (confirmed via transcript). No further refinement/sharing on record.",
     "say": "Nathan's inbox-logging skill hasn't moved on since his demo, as far as I can see."},
    {"id": "9", "title": "Executive dashboard &mdash; on hold pending data structure", "pill": "onhold",
     "what": "Executive dashboard: can't be built until the underlying calculation data is properly structured &mdash; status update given at the 20&nbsp;Aug meeting.",
     "status": "Progress made, not complete; no update since 20&nbsp;Aug.",
     "say": "The calculation data still isn't ready &mdash; the dashboard build is still blocked on that."},
    {"id": "10", "title": "OSM data access &mdash; for AI-driven FAQ/theme analysis", "pill": "onhold",
     "what": "OSM data access: early thinking on getting more direct access to OSM's support-request data, to use AI (not Power Automate &mdash; ruled out, non-Microsoft) to spot themes and maybe automate FAQ-style responses &mdash; discussed at the 20&nbsp;Aug meeting.",
     "status": "Early-stage only. No movement on record since 20&nbsp;Aug.",
     "say": "There's been no real movement yet on getting proper access to that OSM data."},
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


# Column layout, applied consistently to every fixed-grid table in this
# brief: narrow-ish Item column, deliberately widest What/Status column
# (holds the most content), moderate Say This column. No standalone "#"
# column -- numbering is folded into the Item cell's own text instead.
ITEM_COLGROUP = '''<colgroup><col style="width:24%"><col style="width:51%"><col style="width:25%"></colgroup>'''


def render_row(a):
    return f'''<tr>
            <td>{a["id"]}. {a["title"]} <span class="pill pill-{a["pill"]}">{ {"raise":"Raise","onhold":"Historic — unresolved","info":"Update","overdue":"Overdue","resolved":"Resolved","new":"New"}[a["pill"]] }</span></td>
            <td><b>What:</b> {a["what"]}<br><span class="cur-label">Status</span> {a["status"]}</td>
            <td><span class="say-label">Say</span> &ldquo;{a["say"]}&rdquo;</td>
          </tr>'''


def rows_table(items):
    rows = "\n".join(render_row(a) for a in items)
    return f'''<table class="fixed-grid">
          {ITEM_COLGROUP}
          <thead><tr><th>Item</th><th>What / Status</th><th>Say this</th></tr></thead>
          <tbody>
{rows}
          </tbody>
        </table>'''


SK_TABLE = rows_table(SK_ITEMS)
MM_TABLE = rows_table(MM_ITEMS)

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
    <li>Nathan's AI inbox-logging skill and the executive dashboard are real and restored (items 8&ndash;9) after being dropped from one relayed version.</li>
    <li>Not included: one inferred item ("share Codex broken-links output beyond Julian") &mdash; couldn't independently confirm, left out rather than guessed.</li>
  </ul>

  <h2>Also confirmed live &mdash; additional active items <span class="h2-sub">Live Sept 2026 Standing Agenda deck (local OneDrive)</span></h2>
  <p class="body-loose"><span class="say-label">Say</span> &ldquo;A few more things ticking along from the team's own Standing Agenda &mdash; nothing needs deciding here today, just flagging where they're at.&rdquo;</p>
  <table class="fixed-grid">
    <colgroup><col style="width:32%"><col style="width:68%"></colgroup>
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
Same-day authorized exception (many, same day) to the 21 Aug 2026 pipeline-review content-push freeze &mdash; not a general lifting of it. Full pass-by-pass history in Lauren's memory, not repeated here.<br>
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
    sections_html=SECTIONS,
    footnote_html=FOOTNOTE,
)

# Named for the meeting date (16 Sept), not the generation date -- matches
# the convention every other brief in this pipeline follows.
write_brief_output(html_out, "HR Systems Managers Meeting", date=datetime(2026, 9, 16))
