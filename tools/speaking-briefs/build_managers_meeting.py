from datetime import datetime
from brief_chrome import SCRATCH, e, render_page, write_brief_output

# ---- agenda items. Refreshed 15 Sept 2026 for the 16 Sept 2026 sitting (a
#      Wednesday) — the next real fortnightly meeting after the last captured
#      outcome (24 June 2026). No Managers Meeting outcome has been captured
#      since 24 June (fortnightly cadence: 8 Jul and 22 Jul both missing,
#      plus the cycles since), so the 24 June agenda is still the structural
#      base — but every item below has now been cross-checked and updated
#      against live Work Inbox (data/briefing.json) and Command Centre
#      (data/tasks.json), both pulled 15 Sept 2026, plus the 27 Aug Roadmap
#      alignment worksheet where an item overlaps a tracked Roadmap row.
#      Granola could not be reached this session (no GRANOLA_API_KEY set).
#      Refresh authorized by Kevin as a one-time exception to the 21 Aug
#      pipeline-review freeze on ad hoc build_*.py content pushes — see
#      meeting-pipeline-review-21aug.md and
#      managers-meeting-15sep-stale-script-and-meetingsdir-write.md in
#      Lauren's memory.
AGENDA = [
    {
        "id": "1", "title": "H&amp;S Modular System (SHSMS) — resourcing concern",
        "pill": "raise", "owner": "Kevin",
        "desc": "H&amp;S Management System supplier evaluation (Roadmap item DTP1334). Kevin's position stands: this needs dedicated project resource, not team BAU capacity, or the delayed-project pattern repeats.",
        "lu_date": "10 Sep", "lu_text": "Moderation Meeting held with Helen Harbour to review evaluation scores; evaluation window extended to end Sept, deadline now 25 Sept.",
        "current": "Six supplier questionnaires reviewed by Kevin/Marie (21&nbsp;Aug). Evaluation deadline has moved to <b>25&nbsp;Sept 2026</b>. As of today (15&nbsp;Sept), Helen Harbour is scheduling a <b>second</b> follow-up moderation meeting off the back of the 10&nbsp;Sept session. The original resourcing question — dedicated project resource vs team BAU capacity — is still genuinely unanswered.",
        "say": "H&amp;S system — evaluation's now running to 25&nbsp;Sept with a second moderation meeting being set up. Good progress on process, but I still don't have an answer on dedicated resource vs BAU. Can we settle that today?",
    },
    {
        "id": "2", "title": "Support cover gap — recurring pattern",
        "pill": "onhold", "owner": "Kevin",
        "desc": "Kevin on phased return; HR Systems Support cover gaps recurring whenever more than one team member is out at once. First flagged w/c 1 July by Julie Hickman.",
        "lu_date": "19 Aug", "lu_text": "Recurred again — Beth unwell, no helpdesk cover on the day (19 Aug).",
        "current": "No structural fix has landed. The w/c&nbsp;1&nbsp;July gap, the 13&nbsp;July gap (Kevin out, only Sarah standing, escalation chain Simon&nbsp;→&nbsp;Renu&nbsp;→&nbsp;Sarah), and now the <b>19&nbsp;Aug</b> gap are three separate instances of the same unaddressed pattern.",
        "say": "Support cover keeps recurring — most recently 19&nbsp;Aug when Beth was unwell with no helpdesk cover. Three instances now. Can we agree an actual standing cover plan rather than handling each one ad hoc?",
    },
    {
        "id": "3", "title": "Holiday Records reports — scheduling",
        "pill": "resolved", "owner": "Kevin",
        "desc": "Flex points approved for case 69001638 — Holiday Records, 3 reports (2,800 flex points, Alan Quirke / Access Group).",
        "lu_date": "9 Sep", "lu_text": "Access Group made contact; kickoff call confirmed for Friday 18 Sept, 2pm.",
        "current": "<b>Resolved</b> — the scheduling question from June is answered. Kickoff call is <b>Friday 18&nbsp;Sept, 2pm</b>; Kevin is awaiting the calendar invite.",
        "say": "Holiday Records reports — kickoff call is locked in for Friday, 2pm. Nothing needed from the room, just flagging it's finally moving.",
    },
    {
        "id": "4", "title": "REF attributes via ESS",
        "pill": "resolved", "owner": "Nathan / Sarah Rowles, Simon, Kevin",
        "desc": "Roadmap item 204 — REF attributes shared with staff via Employee Self-Service, enabling the REF appeals process.",
        "lu_date": "26–27 Aug", "lu_text": "REF2029 UDF carrying the REF-status values promoted to live UOXP production.",
        "current": "<b>Resolved and delivered.</b> Nathan tested in UOXU and demonstrated to Anne Mortimer on 7&nbsp;Aug; the UDF went live in production 26–27&nbsp;Aug, confirmed by Kevin.",
        "say": "REF via ESS — this one's done. Live in production since 26/27&nbsp;Aug, tested and demoed beforehand. Closing this off the agenda after today.",
    },
    {
        "id": "5", "title": "OSM / Self-Service — change 20020472",
        "pill": "onhold", "owner": "Kevin",
        "desc": "The IT major incident affecting Oxford Service Manager and Self-Service (w/c 17 June) was confirmed resolved 23 June. Kevin has an outstanding change (20020472 — COREPORTAL_ADMIN org hierarchy options) that may have been affected.",
        "lu_date": "24 Jun", "lu_text": "Change may need resubmitting once the incident cleared.",
        "current": "Still unconfirmed whether 20020472 was ever resubmitted or completed — no record either way. Separately, a <b>new and unrelated</b> OSM authentication/incoming-mail issue surfaced late Aug (Louise Piper, 24–25&nbsp;Aug) — a distinct incident, not a continuation of this one; don't conflate the two.",
        "say": "Quick one — did my COREPORTAL_ADMIN change (20020472) ever get resubmitted? Separately, heads up Louise Piper flagged a different OSM auth issue in late Aug — worth keeping the two straight.",
    },
    {
        "id": "6", "title": "College Staff in PeopleXD — multi-company setup",
        "pill": "info", "owner": "Simon",
        "desc": "Ongoing project: multi-company configuration for College Staff in PeopleXD (FP 68261303).",
        "lu_date": "12 Aug", "lu_text": "Multi Company Setup work continuing per Conor O'Brien.",
        "current": "Active — a separate 'DTP1092 College Staff into PXD' weekly team-meeting series is also running (notes through 8–10&nbsp;Sept). <b>Flag for Kevin to confirm:</b> the Roadmap master's own DTP1092 row is titled 'Research management data for REF and research quality' (an ORCID sub-thread), with no mention of College Staff. Whether the DTP1092 thread and the FP&nbsp;68261303 multi-company work are the same initiative, sub-strands of one programme, or two separate items sharing a coincidental label needs settling — not asserted either way here.",
        "say": "College Staff in PeopleXD — work's active. One to check with me directly after: I think there may be a naming clash between this and Roadmap item DTP1092, which is actually titled around ORCID/REF research data, not College Staff. Can we confirm those are genuinely separate before it causes confusion on the Roadmap?",
    },
    {
        "id": "7", "title": "UKVI requirement for Skilled Workers",
        "pill": "onhold", "owner": "Kevin",
        "desc": "CoreHR HEI Group email (23 June) raised a UKVI requirement for Skilled Workers, with potential system implications.",
        "lu_date": "24 Jun", "lu_text": "Not yet actioned. Open question: is this already on someone's radar, and are system changes expected?",
        "current": "Still nothing found in Command Centre, Work Inbox, or Granola since 24&nbsp;June — genuinely stale, now nearly three months untouched.",
        "say": "UKVI Skilled Worker requirement — this has had zero movement since June. Is it actually on anyone's radar, or has it dropped entirely?",
    },
    {
        "id": "8", "title": "Organisational Structure Update — August 2026 (FINAL)",
        "pill": "raise", "owner": "Simon / Sarah",
        "desc": "'Organisational Structure Update — August 2026 — FINAL' document is live, but Simon and Sarah have had unanswered questions on it sitting open.",
        "lu_date": "17 Aug", "lu_text": "Simon/Sarah raised open questions on the FINAL document; no reply on record since.",
        "current": "Nearly a month with no response logged. Given Simon's direct involvement, this is worth resolving in the room rather than leaving it sitting. New this brief — not on the 24&nbsp;June agenda.",
        "say": "Simon — you and Sarah had questions on the Org Structure Update FINAL doc back on 17&nbsp;Aug that I don't think ever got answered. Can we close those out today?",
    },
    {
        "id": "9", "title": "Cority Applicant Data Import — data exposure",
        "pill": "raise", "owner": "Kevin",
        "desc": "Real applicant PII visible in a raw production file as part of the Cority Applicant Data Import work.",
        "lu_date": "18 Aug", "lu_text": "Unresolved question raised to Kevin about the exposure; no resolution on record since.",
        "current": "Four weeks unresolved. This is a live data-protection exposure, not a routine backlog item — warrants explicit sign-off on how it's being closed down, not just noted. New this brief — not on the 24&nbsp;June agenda.",
        "say": "One I need to raise directly — there's real applicant PII sitting in a raw production file from the Cority import, flagged to me on 18&nbsp;Aug and still not resolved. I want an explicit plan for closing this down, not just leaving it open.",
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
            <tr><td class="idcell">1</td><td>H&amp;S Modular System resourcing</td><td>Kevin</td><td><span class="pill pill-raise">Raise</span></td></tr>
            <tr><td class="idcell">2</td><td>Support cover gap (recurring pattern)</td><td>Kevin</td><td><span class="pill pill-onhold">Historic</span></td></tr>
            <tr><td class="idcell">3</td><td>Holiday Records reports scheduling</td><td>Kevin</td><td><span class="pill pill-resolved">Resolved</span></td></tr>
            <tr><td class="idcell">4</td><td>REF attributes via ESS</td><td>Nathan</td><td><span class="pill pill-resolved">Resolved</span></td></tr>
            <tr><td class="idcell">5</td><td>OSM / Self-Service change 20020472</td><td>Kevin</td><td><span class="pill pill-onhold">Historic</span></td></tr>
            <tr><td class="idcell">6</td><td>College Staff in PeopleXD</td><td>Simon</td><td><span class="pill pill-info">Update</span></td></tr>
            <tr><td class="idcell">7</td><td>UKVI Skilled Workers requirement</td><td>Kevin</td><td><span class="pill pill-onhold">Historic</span></td></tr>
            <tr><td class="idcell">8</td><td>Organisational Structure Update (FINAL)</td><td>Simon / Sarah</td><td><span class="pill pill-raise">Raise</span></td></tr>
            <tr><td class="idcell">9</td><td>Cority Applicant Data Import — data exposure</td><td>Kevin</td><td><span class="pill pill-raise">Raise</span></td></tr>
          </tbody>
        </table>"""

SECTIONS = f"""
  <h2>Agenda items — full context <span class="h2-sub">Carried forward from 24 June &middot; refreshed against live Work Inbox / Command Centre 15 Sept 2026</span></h2>
  <div class="item-grid">
{ITEMS_HTML}
  </div>

  <h2 class="h2-warn">Risks and dependencies</h2>
  <p class="body-loose">The core structural risk is unchanged from earlier drafts: <b>no HR Systems Managers Meeting outcome has been captured since 24&nbsp;June 2026</b> — three-plus fortnightly cycles missing before tomorrow's 16&nbsp;Sept sitting. This brief has been actively refreshed against live Work Inbox and Command Centre data (pulled 15&nbsp;Sept) rather than left to run on stale June content, but it is still not a substitute for a captured meeting outcome.</p>
  <p class="body-loose"><b>DPIA Stage&nbsp;7 sign-off (Roadmap item 136) is PARKED</b>, per Kevin's explicit instruction — not an open action item on this agenda. It sits at v0.5, with several review round-trips through Marie Cooksey across late Aug/early Sept; sign-off itself is still not logged as done, but this is being held deliberately rather than chased in this meeting.</p>

  <h2>Unresolved conflicts</h2>
  <div class="risk-block">
    <p class="risk-head">Sources agree &mdash; no cross-source conflict</p>
    <p class="body-loose">Work Inbox, Command Centre, and the 27&nbsp;Aug Roadmap alignment worksheet agree wherever they overlap with items on this agenda.</p>
  </div>
  <div class="risk-block">
    <p class="risk-head">What's actually unresolved: the DTP1092 / College Staff naming question</p>
    <p class="body-loose">Item&nbsp;6's caution is the one genuine open ambiguity in this brief &mdash; whether the "DTP1092 College Staff into PXD" work-inbox thread and the Roadmap's own DTP1092 row (titled around ORCID/REF research data, no mention of College Staff) are the same initiative or two separately-tracked items sharing a label. Flagged for Kevin to confirm, not asserted either way here.</p>
  </div>
"""

FOOTNOTE = """<div class="footnote">
    Prepared 15 Sept 2026 for the 16 Sept 2026 sitting &middot; Sources: HR Systems Managers Meeting &mdash; 24-06.md (last captured outcome), HR Systems Roadmap alignment worksheet 27-08 (cross-check for overlapping items), Work Inbox data/briefing.json + Command Centre data/tasks.json (pulled 15 Sept 2026), Granola (not reachable this session &mdash; no GRANOLA_API_KEY set)<br>
    Refreshed as a one-time authorized exception to the 21 Aug 2026 pipeline-review content-push freeze &mdash; see meeting-pipeline-review-21aug.md. Not a general lifting of that freeze.<br>
    Branding: command-centre/BRANDING.md v2.0 (4 Jul 2026) &mdash; Oxford Navy, Inter, canonical crest. Template shared with the HR Systems Roadmap brief via brief_chrome.py.
  </div>"""

html_out = render_page(
    title="HR Systems Managers Meeting — 16/09",
    app_name="HR Systems Managers Meeting",
    kicker="Speaking Brief &middot; Draft",
    h1="HR Systems Managers Meeting — 16/09",
    meta_spans=[
        "<b>Meeting</b> Wednesday 16 September 2026 (fortnightly)",
        "<b>Follow-on from</b> 24 June 2026",
        "<b>Status</b> Refreshed 15 Sept 2026 &mdash; ready for review",
    ],
    flag_label="Before anything else",
    flag_paragraphs=[
        "No HR Systems Managers Meeting outcome is captured in Granola, and no prep or outcome document exists in this repo, since 24&nbsp;June &mdash; meaning the fortnightly sittings in between are still missing before this one. Everything below carries the <b>24&nbsp;June agenda</b> forward, but has now been actively cross-checked and updated against live Work Inbox and Command Centre data (pulled 15&nbsp;Sept) &mdash; 5 of the original 7 items had material, dated updates, and 2 new items (Organisational Structure Update, Cority Applicant Data Import) have been added.",
        "Tell me what actually happened at the meeting and I'll correct the record afterwards.",
    ],
    glance_label="At a glance",
    glance_sub="9 agenda items &middot; carried forward from 24 Jun, refreshed against live Work Inbox / Command Centre 15 Sept 2026",
    glance_table_html=GLANCE_TABLE,
    sections_html=SECTIONS,
    footnote_html=FOOTNOTE,
)

# Named for the meeting date (16 Sept), not the generation date -- matches
# the convention every other brief in this pipeline follows.
write_brief_output(html_out, "HR Systems Managers Meeting", date=datetime(2026, 9, 16))
