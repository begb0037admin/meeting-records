import json
from brief_chrome import SCRATCH, e, PILL_LABEL, render_page

with open(fr"{SCRATCH}\roadmap-items.json", encoding="utf-8") as f:
    ITEMS = json.load(f)

# ---- per-item hand-authored "say this" + narrative overlay (from the 3 July prep + Command Centre / Work Inbox cross-check) ----
OVERLAY = {
    "136": {
        "title": "PeopleXD Data Protection Impact Assessment",
        "owner": "Kevin / Simon",
        "status_pill": "overdue",
        "current": "Command Centre confirms this is unchanged since 3 July: Stage 7 sign-off is still sitting with Marie Cooksey, nothing logged as resolved.",
        "say": "DPIA — still nothing back from Marie on Stage 7, five weeks on from when I last raised it. I want to escalate this properly today rather than keep chasing informally.",
    },
    "DTP1334": {
        "title": "Health &amp; Safety Management System",
        "owner": "Kevin / James, Marie C",
        "status_pill": "overdue",
        "current": "Still active per Command Centre. The 3 July brief already flagged 31 Jul as unachievable and proposed revising to end-September — worth confirming whether that was ever formally agreed.",
        "say": "H&amp;S system — the deadline I flagged as unachievable on 3 July has now passed. Did we ever formally agree the revised date? If not, I want that nailed down today.",
    },
    "DTP1092": {
        "title": "Research management data for REF and research quality",
        "owner": "Nathan / Marie C, Kevin",
        "status_pill": "overdue",
        "current": "Command Centre's REF-via-ESS task (Sarah Rowles) is still open past its end-July deadline.",
        "say": "REF via ESS — the end-of-July deadline has now passed with this task still open. I need a status check before I can tell the room whether we're on track or slipping.",
    },
    "ITS1004": {
        "title": "WFM Rollout",
        "owner": "Michael",
        "status_pill": "overdue",
        "current": "The GLAM resolution call flagged as next step on 3 July still appears open in Command Centre — doesn't look like it's happened yet.",
        "say": "WFM — the GLAM call I flagged as the next step on 3 July is still sitting as an open task. Has that conversation with Simon and Marie happened?",
    },
    "179": {
        "title": "Migration of HR Reporting Users to SSO",
        "owner": "Kevin / Asta",
        "status_pill": "overdue",
        "current": "The 3 July decision-day outcome isn't reflected anywhere available — Command Centre still lists Managed Desktop migration as open.",
        "say": "SSO migration — 3 July was supposed to be the decision day on this. I don't have a record of what was decided. Asta, where did this land?",
    },
    "174_b": {
        "title": "Health &amp; Safety dashboards",
        "owner": "David / Simon, James, Chris",
        "status_pill": "overdue",
        "current": "No open Command Centre task references this directly. Last known blocker (3 July) was Brian's stakeholder comms.",
        "say": "H&amp;S dashboards — last I had, Brian still hadn't sent stakeholder comms, a month past the self-imposed deadline. Has that moved at all in five weeks?",
    },
    "22_c": {
        "title": "Security Model Review (Phase 1)",
        "owner": "Tonya / Simon, Asta",
        "status_pill": "onhold",
        "current": "No change indicated anywhere.",
        "say": "Security Model Review — still no movement, still pending a strategic decision.",
    },
    "22_d": {
        "title": "Security Model Review (University-wide access)",
        "owner": "Tonya / Simon, Asta, Michael, Lee, Sarah, Athena",
        "status_pill": "onhold",
        "current": "Status still “New”, last reviewed over a year ago (27 Jun 2025) — no activity on record since.",
        "say": "Security Model Review, phase 2 — this one hasn't moved since it was logged over a year ago. Worth asking whether it's still live at all.",
    },
}


def render_updates(updates):
    if not updates:
        return '<p class="empty">No progress-update history recorded in the Roadmap Master.</p>'
    rows = []
    for date, text in updates:
        rows.append(f'<li><span class="u-date">{e(date) or "undated"}</span><span class="u-text">{e(text)}</span></li>')
    return f'<ul class="update-log">{"".join(rows)}</ul>'


def render_next_steps(steps):
    if not steps:
        return '<p class="empty">No next steps recorded.</p>'
    return '<ul class="next-steps">' + "".join(f"<li>{e(s)}</li>" for s in steps) + "</ul>"


def render_item(item_id):
    d = ITEMS[item_id]
    o = OVERLAY[item_id]
    updates = d["updates"]
    last_date, last_text = (updates[0][0], updates[0][1]) if updates else ("", "")
    facts = []
    if d.get("category"): facts.append(("Category", d["category"]))
    if d.get("type"): facts.append(("Type", d["type"]))
    if d.get("mandate"): facts.append(("Mandate", d["mandate"]))
    if d.get("system"): facts.append(("System", d["system"]))
    if d.get("customer"): facts.append(("Primary customer", d["customer"]))
    if d.get("priority"): facts.append(("Business priority", d["priority"]))
    if d.get("last_reviewed"): facts.append(("Master last reviewed", d["last_reviewed"]))
    if d.get("next_checkpoint"): facts.append(("Next checkpoint (per Master)", d["next_checkpoint"]))

    facts_html = "".join(f'<div class="fact"><span class="fact-k">{e(k)}</span><span class="fact-v">{e(v)}</span></div>' for k, v in facts)

    return f'''
  <article class="item card">
    <header class="item-head">
      <span class="item-id">{e(item_id)}</span>
      <h3 class="item-title">{o["title"]}</h3>
      <span class="pill pill-{o["status_pill"]}">{PILL_LABEL[o["status_pill"]]}</span>
      <p class="item-owner">{o["owner"]} &nbsp;·&nbsp; deadline {e(d.get("deadline") or "none set")}</p>
    </header>

    <p class="item-desc">{e(d.get("description") or d.get("phase") or "")}</p>

    <div class="last-update">
      <span class="lu-label">Last logged update{f" &middot; {e(last_date)}" if last_date else ""}</span>
      <p>{e(last_text) or "No dated update on record."}</p>
    </div>

    <p class="item-current"><span class="cur-label">Current position (this brief)</span>{o["current"]}</p>

    <blockquote><span class="say-label">Say this</span><p>&ldquo;{o["say"]}&rdquo;</p></blockquote>

    <details class="expand">
      <summary>Full history &amp; background <span class="chev">&#9662;</span></summary>
      <div class="expand-body">
        {f'<p class="impact"><span class="fact-k">Expected impact / benefit</span>{e(d.get("impact"))}</p>' if d.get("impact") else ""}
        {f'<div class="facts-grid">{facts_html}</div>' if facts_html else ""}
        <h4>Progress update history <span class="count">({len(updates)} logged)</span></h4>
        {render_updates(updates)}
        <h4>Next steps on record</h4>
        {render_next_steps(d["next_steps"])}
      </div>
    </details>
  </article>'''


ITEM_ORDER = ["136", "DTP1334", "DTP1092", "ITS1004", "179", "174_b", "22_c", "22_d"]
ITEMS_HTML = "\n".join(render_item(i) for i in ITEM_ORDER)

GLANCE_TABLE = """<table>
          <thead><tr><th>ID</th><th>Item</th><th>Lead</th><th>Deadline</th><th>Status</th></tr></thead>
          <tbody>
            <tr><td class="idcell">136</td><td>PeopleXD DPIA</td><td>Kevin</td><td class="datecell">30 Jun</td><td><span class="pill pill-overdue">Overdue</span></td></tr>
            <tr><td class="idcell">DTP1334</td><td>H&amp;S Management System</td><td>Kevin</td><td class="datecell">31 Jul</td><td><span class="pill pill-overdue">Overdue</span></td></tr>
            <tr><td class="idcell">DTP1092</td><td>REF via ESS</td><td>Nathan</td><td class="datecell">end-Jul</td><td><span class="pill pill-overdue">Overdue</span></td></tr>
            <tr><td class="idcell">ITS1004</td><td>WFM Rollout</td><td>Michael</td><td class="datecell">29 May</td><td><span class="pill pill-overdue">Overdue</span></td></tr>
            <tr><td class="idcell">179</td><td>SSO Migration</td><td>Kevin</td><td class="datecell">30 Apr</td><td><span class="pill pill-overdue">Overdue</span></td></tr>
            <tr><td class="idcell">174_b</td><td>H&amp;S Dashboards</td><td>David</td><td class="datecell">31 Mar</td><td><span class="pill pill-overdue">Overdue</span></td></tr>
            <tr><td class="idcell">22_c</td><td>Security Model Review (Phase 1)</td><td>Tonya</td><td class="datecell">&mdash;</td><td><span class="pill pill-onhold">On hold</span></td></tr>
            <tr><td class="idcell">22_d</td><td>Security Model Review (Univ.-wide)</td><td>Tonya</td><td class="datecell">&mdash;</td><td><span class="pill pill-onhold">On hold</span></td></tr>
          </tbody>
        </table>"""

SECTIONS = f"""
  <h2>Team items — full context <span class="h2-sub">Description &amp; impact from the Roadmap Master &middot; full dated history &middot; expand for background</span></h2>
  <div class="item-grid">
{ITEMS_HTML}
  </div>

  <h2 class="h2-warn">Risks and dependencies</h2>
  <p class="body-loose">The core risk is the same one the live front-door smoke test surfaced yesterday: <b>five straight Fridays with no captured Roadmap outcome.</b> Whatever the cause, real deadline slippage &mdash; six items now overdue &mdash; may be going into a second, third, or fourth cycle without anyone's explicit sign-off on record.</p>
  <p class="body-loose">Work Inbox (31 July) shows Simon off until 4 August and Sarah off until 3 August &mdash; a live capacity gap that plausibly explains missed captures, not necessarily missed meetings.</p>
  <p class="body-loose">Support cover, the Cority SFTP feed error, and the PACS org-structure impact assessment are all still open in Command Centre with no roadmap linkage resolved.</p>

  <h2>Progress updates to log <span class="h2-sub">Draft only &middot; hold until the July gap is resolved</span></h2>
  <div class="table-wrap card">
    <table>
      <thead><tr><th>ID</th><th>Item</th><th>Draft entry</th></tr></thead>
      <tbody>
        <tr><td class="idcell">136</td><td>PeopleXD DPIA</td><td>No update since 03/07; Stage 7 sign-off still outstanding with Marie Cooksey. (Source: HR Systems Roadmap 07/08)</td></tr>
        <tr><td class="idcell">DTP1334</td><td>H&amp;S Management System</td><td>31 Jul deadline passed without a confirmed revised date on record since 03/07. (Source: HR Systems Roadmap 07/08)</td></tr>
        <tr><td class="idcell">DTP1092</td><td>REF via ESS / research management data</td><td>End-July deadline (REF via ESS) passed, Command Centre task still open. (Source: HR Systems Roadmap 07/08)</td></tr>
        <tr><td class="idcell">ITS1004</td><td>WFM Rollout</td><td>GLAM resolution call still not confirmed as held. (Source: HR Systems Roadmap 07/08)</td></tr>
        <tr><td class="idcell">179</td><td>SSO Migration</td><td>03/07 decision-day outcome not recorded anywhere available. (Source: HR Systems Roadmap 07/08)</td></tr>
      </tbody>
    </table>
  </div>

  <h2>Unresolved conflicts</h2>
  <div class="risk-block">
    <p class="risk-head">Sources agree &mdash; no cross-source conflict</p>
    <p class="body-loose">Command Centre, Work Inbox, and the 3&nbsp;July prep agree with each other wherever they overlap.</p>
  </div>
  <div class="risk-block">
    <p class="risk-head">What's actually unresolved: four missing meeting records</p>
    <p class="body-loose">The real gap is the one flagged at the top &mdash; <b>absence</b> of any confirmed record for four Fridays' worth of meetings, which this brief cannot responsibly fill in without your input.</p>
  </div>
"""

FOOTNOTE = """<div class="footnote">
    Prepared 1 Aug 2026 &middot; Sources: HR Systems Roadmap MASTER.xlsm (read-only, full field history), HR Systems Roadmap &mdash; 03-07.md (last captured outcome), Work Inbox briefing (31 Jul), Command Centre tasks, Granola (checked directly &mdash; no HR Systems Roadmap meeting found after 3 Jul)<br>
    Draft only &mdash; not committed to meeting-records. Nothing published, sent, or scheduled.<br>
    Branding: command-centre/BRANDING.md v2.0 (4 Jul 2026) &mdash; Oxford Navy, Inter, canonical crest.
  </div>"""

html_out = render_page(
    title="HR Systems Roadmap — 07/08",
    app_name="HR Systems Roadmap",
    kicker="Speaking Brief &middot; Draft",
    h1="HR Systems Roadmap — 07/08",
    meta_spans=[
        "<b>Meeting</b> Friday 7 August 2026, 10:00",
        "<b>Follow-on from</b> 3 July 2026",
        "<b>Status</b> Draft — not yet approved",
    ],
    flag_label="Before anything else",
    flag_paragraphs=[
        "No HR Systems Roadmap outcome is captured in Granola, and no prep or outcome document exists in this repo, for 10, 17, 24, or 31 July — the last record either source holds is 3 July. You've said a meeting did happen in July; I can't independently confirm that yet. Everything below is built from the <b>3&nbsp;July position</b>, the Roadmap Master's own history, and what's changed in Command&nbsp;Centre and Work&nbsp;Inbox since — not a confirmed account of any July discussion.",
        "Tell me what actually happened and I'll correct the record before this goes anywhere near a commit.",
    ],
    glance_label="At a glance",
    glance_sub="8 tracked items &middot; 6 overdue against Roadmap Master deadlines",
    glance_table_html=GLANCE_TABLE,
    sections_html=SECTIONS,
    footnote_html=FOOTNOTE,
)

out_path = fr"{SCRATCH}\hr-roadmap-brief-07-08-v3.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html_out)
print("written", out_path, len(html_out), "chars")
