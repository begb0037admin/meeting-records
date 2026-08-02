from brief_chrome import SCRATCH, e, render_page

# ---- agenda items, carried forward from the last captured Managers Meeting
#      (24 June 2026) and cross-checked against the 3 July HR Systems Roadmap
#      session + Command Centre / Work Inbox where an item overlaps with a
#      tracked Roadmap item. No Managers Meeting has been captured since
#      24 June (fortnightly cadence: 8 Jul and 22 Jul both missing).
AGENDA = [
    {
        "id": "1", "title": "H&amp;S Modular System (SHSMS) — resourcing concern",
        "pill": "raise", "owner": "Kevin",
        "desc": "H&amp;S Management System evaluation. Implementation was due to start 20 July — Kevin's position: this needs dedicated project resource, not team BAU capacity, or every delayed-project pattern in the team's history repeats.",
        "lu_date": "24 Jun", "lu_text": "Scoring methodology agreed (Requirements 65% / Price 30% / References 5%). Evaluator briefings 14 July, supplier responses ~21 July. Marie aware of the resourcing ask; rough recruiting timeline end Sept/Oct.",
        "current": "The 3&nbsp;July Roadmap session (DTP1334) flagged the 31&nbsp;July deadline as unachievable and noted a Tony Bordell quote sent to Marie for approval. The 20&nbsp;July implementation start date has now passed with no confirmation on record of whether it happened, or whether the dedicated-resource ask was settled.",
        "say": "H&amp;S system — implementation was meant to start 20 July, now nearly two weeks ago. Did that happen, and did we land the dedicated resource, or is this still sitting on team BAU?",
    },
    {
        "id": "2", "title": "Support cover gap, w/c 1 July — and the pattern repeating",
        "pill": "onhold", "owner": "Kevin",
        "desc": "Kevin on phased return (4hrs/day, mornings, remote); Michael O'Sullivan and Emma both on leave the week of 1 July — a significant HR Systems Support cover gap. Flagged by Julie Hickman (23 Jun).",
        "lu_date": "24 Jun", "lu_text": "Kevin working on a cover plan in that morning's FA team catch-up.",
        "current": "No record of how that specific week was covered. Worth flagging that the same pattern recurred almost immediately after: per the 3&nbsp;July Roadmap session, Kevin was out from 10&nbsp;July for ~2 weeks, Michael and Emma absent from 6&nbsp;July, Marie off 7–17&nbsp;July, and from 13&nbsp;July Sarah was the only manager standing (escalation chain Simon → Renu → Sarah).",
        "say": "Support cover — did w/c 1 July hold up alright? And more importantly, how did the 13 July gap actually go, since I was out for it — did the escalation chain get used?",
    },
    {
        "id": "3", "title": "Holiday Records reports — scheduling",
        "pill": "info", "owner": "Kevin",
        "desc": "Flex points approved for case 69001638 — Holiday Records, 3 reports (2,800 flex points, Alan Quirke / Access Group): Annual Leave Record by Person and Leave Year; Holiday Pay and Accrual Record for Variable-Hours and Casual Arrangements; Holiday Pay in Lieu on Termination.",
        "lu_date": "24 Jun", "lu_text": "Access Group expected to make contact within 3 weeks to agree delivery timelines. Kevin's preference: push delivery past July given the July capacity picture.",
        "current": "No record of Access Group making contact, or of a delivery date being agreed. The flex-point grace period runs to roughly 29&nbsp;September, so there's still runway, but the scheduling conversation flagged on 24&nbsp;June doesn't appear to have happened yet.",
        "say": "Holiday Records reports — has Access Group been in touch yet? We're six weeks past approval with no delivery date on record.",
    },
    {
        "id": "4", "title": "REF attributes via ESS",
        "pill": "overdue", "owner": "Nathan / Sarah Rowles, Simon, Kevin",
        "desc": "New Roadmap item: share specific REF attributes with staff via Employee Self-Service by end of July 2026, to enable the REF appeals process. Not a like-for-like repeat of the last REF cycle.",
        "lu_date": "24 Jun", "lu_text": "Approach still being scoped — open question on whether a new UDF is needed or an existing one can be reused; Sarah flagged the team is thin on the ground in July.",
        "current": "The 3&nbsp;July Roadmap session confirmed the approach (person-level UDF, three fields per appointment, Research Assistant indicator excluded) and set Kevin to test before going off on 10&nbsp;July. The end-of-July deadline has now passed with no confirmation on record of the test result or Nathan's ISM request.",
        "say": "REF via ESS — deadline was end of July, now passed. Did my testing happen before the 10th, and did Nathan's ISM request go in?",
    },
    {
        "id": "5", "title": "OSM / Self-Service major incident",
        "pill": "resolved", "owner": "Kevin",
        "desc": "The IT major incident affecting Oxford Service Manager and Self-Service (raised w/c 17 June) was confirmed fully resolved 23 June. Normal approvals resumed; any queued or deferred changes should be resubmitted.",
        "lu_date": "24 Jun", "lu_text": "Kevin has an outstanding change (20020472 — COREPORTAL_ADMIN org hierarchy options) that may have been affected and may need resubmitting.",
        "current": "No record since 24&nbsp;June of whether change 20020472 was resubmitted or completed.",
        "say": "Quick one — did my COREPORTAL_ADMIN change (20020472) ever get resubmitted once the OSM incident cleared?",
    },
    {
        "id": "6", "title": "College Staff in PeopleXD — multi-company setup",
        "pill": "info", "owner": "Simon",
        "desc": "Ongoing project: multi-company configuration for College Staff in PeopleXD.",
        "lu_date": "23 Jun", "lu_text": "Simon updated Conor O'Brien (Access Group) with the team's post-design proposal on FP 68261303. Design phase concluding.",
        "current": "No captured update since 24&nbsp;June on whether the design phase formally closed out or moved into build.",
        "say": "College Staff in PeopleXD — last I had, design was concluding. Has that moved into build yet?",
    },
    {
        "id": "7", "title": "UKVI requirement for Skilled Workers",
        "pill": "new", "owner": "Kevin",
        "desc": "CoreHR HEI Group email (23 June) raised a UKVI requirement for Skilled Workers, with potential system implications.",
        "lu_date": "24 Jun", "lu_text": "Not yet actioned. Open question: is this already on someone's radar, and are system changes expected?",
        "current": "No further mention found in Command Centre, Work Inbox, or Granola since 24&nbsp;June — status unknown, five weeks on.",
        "say": "UKVI Skilled Worker requirement — has anyone picked this up, or is it still sitting untouched since June?",
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
            <tr><td class="idcell">2</td><td>Support cover gap (w/c 1 Jul + pattern)</td><td>Kevin</td><td><span class="pill pill-onhold">Historic</span></td></tr>
            <tr><td class="idcell">3</td><td>Holiday Records reports scheduling</td><td>Kevin</td><td><span class="pill pill-info">Update</span></td></tr>
            <tr><td class="idcell">4</td><td>REF attributes via ESS</td><td>Nathan</td><td><span class="pill pill-overdue">Overdue</span></td></tr>
            <tr><td class="idcell">5</td><td>OSM / Self-Service incident</td><td>Kevin</td><td><span class="pill pill-resolved">Resolved</span></td></tr>
            <tr><td class="idcell">6</td><td>College Staff in PeopleXD</td><td>Simon</td><td><span class="pill pill-info">Update</span></td></tr>
            <tr><td class="idcell">7</td><td>UKVI Skilled Workers requirement</td><td>Kevin</td><td><span class="pill pill-new">New</span></td></tr>
          </tbody>
        </table>"""

SECTIONS = f"""
  <h2>Agenda items — full context <span class="h2-sub">Carried forward from 24 June &middot; cross-checked against the 3 July Roadmap session where items overlap</span></h2>
  <div class="item-grid">
{ITEMS_HTML}
  </div>

  <h2 class="h2-warn">Risks and dependencies</h2>
  <p class="body-loose">The core risk is the same shape as the Roadmap brief: <b>three fortnightly cycles with no captured Managers Meeting outcome</b> (8 July, 22 July both missing before this 5 August sitting). Several of the items above were already thin on confirmation in June — five more weeks without a captured meeting means there's no record of whether they were even raised again, let alone resolved.</p>
  <p class="body-loose">Kevin's own 24&nbsp;June "open floor" heads-up list overlaps directly with tracked Roadmap items also flagged in the 7 Aug Roadmap brief: DPIA Stage&nbsp;7 sign-off (item 136, overdue since 30&nbsp;June), the H&amp;S Modular System evaluation window (item&nbsp;1 above), and REF attributes via ESS (item&nbsp;4 above, now overdue). The Annual Leave Carryover rollout (Michael's workstream, October 2026 deadline) has no update on record since 24&nbsp;June either.</p>

  <h2>Unresolved conflicts</h2>
  <div class="risk-block">
    <p class="risk-head">Sources agree &mdash; no cross-source conflict</p>
    <p class="body-loose">The 24&nbsp;June Managers Meeting notes, the 3&nbsp;July Roadmap session, and Command Centre agree wherever they overlap.</p>
  </div>
  <div class="risk-block">
    <p class="risk-head">What's actually unresolved: two missing Managers Meeting cycles</p>
    <p class="body-loose">The real gap is the same one flagged at the top &mdash; the absence of any captured Managers Meeting for two full fortnightly cycles, which this brief cannot responsibly fill in on your behalf.</p>
  </div>
"""

FOOTNOTE = """<div class="footnote">
    Prepared 1 Aug 2026 &middot; Sources: HR Systems Managers Meeting &mdash; 24-06.md (last captured outcome), HR Systems Roadmap &mdash; 03-07.md (cross-check for overlapping items), Granola (checked directly &mdash; no Managers Meeting found after 24 Jun), Command Centre tasks, Work Inbox briefing<br>
    Draft only &mdash; not committed to meeting-records. Nothing published, sent, or scheduled.<br>
    Branding: command-centre/BRANDING.md v2.0 (4 Jul 2026) &mdash; Oxford Navy, Inter, canonical crest. Template shared with the HR Systems Roadmap brief via brief_chrome.py.
  </div>"""

html_out = render_page(
    title="HR Systems Managers Meeting — 05/08",
    app_name="HR Systems Managers Meeting",
    kicker="Speaking Brief &middot; Draft",
    h1="HR Systems Managers Meeting — 05/08",
    meta_spans=[
        "<b>Meeting</b> Wednesday 5 August 2026 (fortnightly)",
        "<b>Follow-on from</b> 24 June 2026",
        "<b>Status</b> Draft — not yet approved",
    ],
    flag_label="Before anything else",
    flag_paragraphs=[
        "No HR Systems Managers Meeting outcome is captured in Granola, and no prep or outcome document exists in this repo, since 24&nbsp;June — meaning the two fortnightly sittings in between (8&nbsp;July, 22&nbsp;July) are both missing before this one. Everything below carries the <b>24&nbsp;June agenda</b> forward, cross-checked against the 3&nbsp;July HR Systems Roadmap session and Command Centre/Work Inbox wherever an item overlaps — not a confirmed account of what was actually raised or resolved at any meeting since.",
        "Tell me what actually happened in July and I'll correct the record before this goes anywhere near a commit.",
    ],
    glance_label="At a glance",
    glance_sub="7 agenda items &middot; carried forward from 24 Jun, 2 fortnightly cycles missing",
    glance_table_html=GLANCE_TABLE,
    sections_html=SECTIONS,
    footnote_html=FOOTNOTE,
)

out_path = fr"{SCRATCH}\hr-managers-meeting-brief-05-08.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html_out)
print("written", out_path, len(html_out), "chars")
