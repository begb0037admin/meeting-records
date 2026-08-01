import json
from brief_chrome import SCRATCH, e, render_page

with open(fr"{SCRATCH}\hs-items.json", encoding="utf-8") as f:
    ITEMS = json.load(f)

# ---- pill assignment: On hold / Not started direct from Status; "In progress"
#      items split into overdue (past Expected Delivery Date) vs ontrack (green,
#      on schedule) so on-track "In progress" is visually distinct from "On hold";
#      "With Supplier" gets its own blue pill, distinct from all of the above ----
PILL = {
    "HSB002": "onhold", "HSB079": "new", "HSB073": "overdue", "HSB061": "ontrack",
    "HSB075": "onhold", "HSB076": "onhold", "HSB085": "overdue", "HSB087": "ontrack", "HSB088": "ontrack",
    "HSB025": "new", "HSB050": "info", "HSB089": "new",
}
PILL_TEXT = {"onhold": "On hold", "new": "Not started", "overdue": "Overdue", "ontrack": "In progress", "info": "With supplier"}

# ---- hand-authored "say this" line per item, from the latest logged comment ----
SAY = {
    "HSB002": "Health surveillance compliance reporting — funding's been provisional since 6 July, still waiting on APC sign-off. Can we get a firm answer today?",
    "HSB079": "Retention and purge rules — this is a Must Have, statutory, and it's sat as Not Started since Rob Green first raised it in March. We need to establish the business rules for archiving and purging Cority data.",
    "HSB073": "Cardinus feed — funding confirmed 30 July, but the expected delivery date of 30 July has now passed. James needs to liaise with the Azure team on next steps; three outstanding issues (SBS inclusion, contractor DSE needs, non-Uni-email users) are still open.",
    "HSB061": "The 498 duplicate Cority records from the PXD migration — merging is progressing but slowly, about 2 hours a week. James asked on 27 July whether Kevin can pick this up on his return.",
    "HSB075": "Org structure missing for inactive clients — same funding-approval holding pattern as HSB002, provisional since 6 July, awaiting APC. There's also an open dependency noted against HSB075 itself around business-rule execution order.",
    "HSB076": "Org structure missing for active clients — same funding chain as the other two Cority org-structure items, provisional since 6 July, awaiting APC approval.",
    "HSB085": "Safety Officers report — expected delivery was 4 July, nearly a month ago, still shows In Progress with no comment logged since. Chris — where's this at?",
    "HSB087": "Chase-email suppression for health surveillance — configured and working for Baseline Respiratory on Test as of 23 July, but we need a decision on whether it applies to all SEGs and all H&S emails before rolling further.",
    "HSB088": "Immunisation recall autopopulation — one of 75 business rules configured and working (Hepatitis B, 2nd dose) as of March; the other 74 still need the same treatment. James, is there a plan to work through the rest?",
    "HSB025": "Odyssey monthly returns prompts — the blocking reporting issues were resolved back in March, but this hasn't moved off Not Started since. James, is there anything stopping this from being picked up now?",
    "HSB050": "Smart notes drafting — this has been bouncing around Cority's release notes since November with no firm date. 6 July note says it's on hold pending the funding request work. Kevin, worth a decision on whether to keep chasing or park it properly.",
    "HSB089": "Med Students dashboard — waiting on Gill Wilson for more detail since 15 July, two and a half weeks with no reply. James, want me to help chase, or are you across it?",
}
# Items included regardless of Must Have / In Progress filter, because they're
# owned by James or Kevin — added at Kevin's explicit instruction (1 Aug 2026):
# "every item that has the name James or Kevin needs to be listed on here
# regardless." Grid stays 3-across; more rows are added as this set grows.
FORCE_INCLUDE = {"HSB025", "HSB050", "HSB089"}


def render_updates(updates):
    if not updates:
        return '<p class="empty">No dated comment history logged for this item.</p>'
    rows = []
    for date, text in updates:
        rows.append(f'<li><span class="u-date">{e(date)}</span><span class="u-text">{e(text)}</span></li>')
    return f'<ul class="update-log">{"".join(rows)}</ul>'


def render_item(ref):
    d = ITEMS[ref]
    updates = d["updates"]
    last_date, last_text = (updates[0][0], updates[0][1]) if updates else ("", "")
    facts = [
        ("System", d.get("system")),
        ("Type of request", d.get("type")),
        ("MoSCoW", d.get("moscow")),
        ("T-shirt size", d.get("tshirt")),
        ("Owner", d.get("owner") or "Unassigned"),
        ("Start date", d.get("start")),
        ("Expected delivery", d.get("exp_delivery") or "None set"),
        ("OSM reference", d.get("osm")),
    ]
    facts_html = "".join(f'<div class="fact"><span class="fact-k">{e(k)}</span><span class="fact-v">{e(v)}</span></div>' for k, v in facts if v)

    return f'''
  <article class="item card">
    <header class="item-head">
      <span class="item-id">{e(ref)}</span>
      <h3 class="item-title">{e(d["item_name"])}</h3>
      <span class="pill pill-{PILL[ref]}">{PILL_TEXT[PILL[ref]]}</span>
      <p class="item-owner">{e(d.get("owner") or "Unassigned")} &nbsp;&middot;&nbsp; {e(d.get("system"))}</p>
    </header>

    <p class="item-desc">{e(d.get("detail") or "")}</p>

    <div class="last-update">
      <span class="lu-label">Last logged update{f" &middot; {e(last_date)}" if last_date else ""}</span>
      <p>{e(last_text) or "No dated update on record."}</p>
    </div>

    <blockquote><span class="say-label">Say this</span><p>&ldquo;{SAY[ref]}&rdquo;</p></blockquote>

    <details class="expand">
      <summary>Full history &amp; background <span class="chev">&#9662;</span></summary>
      <div class="expand-body">
        {f'<p class="impact"><span class="fact-k">Expected benefit</span>{e(d.get("benefit"))}</p>' if d.get("benefit") else ""}
        <div class="facts-grid">{facts_html}</div>
        <h4>Comment history <span class="count">({len(updates)} logged)</span></h4>
        {render_updates(updates)}
      </div>
    </details>
  </article>'''


ITEM_ORDER = ["HSB073", "HSB085", "HSB002", "HSB075", "HSB076", "HSB061", "HSB087", "HSB088", "HSB079",
              "HSB025", "HSB050", "HSB089"]
ITEMS_HTML = "\n".join(render_item(i) for i in ITEM_ORDER)

GLANCE_ROWS = []
for ref in ITEM_ORDER:
    d = ITEMS[ref]
    pill = PILL[ref]
    GLANCE_ROWS.append(
        f'<tr><td class="idcell">{e(ref)}</td><td>{e(d["item_name"])}</td><td>{e(d.get("system"))}</td>'
        f'<td>{e(d.get("owner") or "Unassigned")}</td><td><span class="pill pill-{pill}">{PILL_TEXT[pill]}</span></td></tr>'
    )
GLANCE_TABLE = f"""<table>
          <thead><tr><th>Ref</th><th>Item</th><th>System</th><th>Owner</th><th>Status</th></tr></thead>
          <tbody>
            {''.join(GLANCE_ROWS)}
          </tbody>
        </table>"""

SECTIONS = f"""
  <h2>Backlog items — full context <span class="h2-sub">Must Have + In Progress, plus every James/Kevin-owned item regardless &middot; full dated comment history &middot; expand for background</span></h2>
  <div class="item-grid">
{ITEMS_HTML}
  </div>

  <h2 class="h2-warn">Risks and dependencies</h2>

  <div class="risk-block">
    <p class="risk-head">Six-week gap in captured meeting outcomes</p>
    <p class="body-loose">No H&amp;S Roadmap meeting outcome has been captured in meeting-records since 22&nbsp;June. Unlike the HR Systems Roadmap gap, the underlying backlog workbook itself has stayed live and current &mdash; comments logged as recently as 30&nbsp;July &mdash; so the item detail below is genuinely up to date. What's missing is a record of what was actually discussed and agreed <i>as a group</i> in that time, not the data itself.</p>
  </div>

  <div class="risk-block">
    <p class="risk-head">Three Must Have Cority items blocked on the same funding approval</p>
    <p class="body-loose">Provisional funding was secured 6&nbsp;July; still awaiting APC approval three weeks later. All three are owned by Marie and have been open since late 2025 / January. Worth raising as <b>one</b> funding blocker, not three separate items:</p>
    <ul class="risk-list">
      <li><b>HSB002</b> &mdash; Health surveillance compliance reporting</li>
      <li><b>HSB075</b> &mdash; Org structure missing for inactive clients</li>
      <li><b>HSB076</b> &mdash; Org structure missing for active clients (sibling bug to HSB075 &mdash; both trace to the same Cority business-rule conflict around the "primary job position" flag)</li>
    </ul>
  </div>

  <div class="risk-block">
    <p class="risk-head">Two items past their Expected Delivery Date</p>
    <ul class="risk-list">
      <li><b>HSB073</b> &mdash; Cardinus feed &mdash; due 30&nbsp;July</li>
      <li><b>HSB085</b> &mdash; Safety Officers report &mdash; due 4&nbsp;July, no comment logged at all since it started</li>
    </ul>
    <p class="body-loose">Worth a direct check with Chris on HSB085's status.</p>
  </div>

  <h2>Unresolved conflicts</h2>
  <p class="body-loose">None between sources &mdash; this brief is built entirely from the live H&amp;S Systems Backlog workbook, which is self-consistent. The open question is process, not data: whether the funding approvals blocking HSB002/075/076 and the SEG-scope decision blocking HSB087 need this meeting to move, or are already progressing elsewhere.</p>
"""

FOOTNOTE = """<div class="footnote">
    Prepared 1 Aug 2026 &middot; Source: HR Systems Workflow Overview &mdash; Health and Safety Systems.xlsx, "Backlog Items" sheet (read-only, full field + comment history), filtered to Must Have priority and/or In Progress status, plus every James/Kevin-owned item regardless (12 of 33 currently active items) per Kevin's scoping choice<br>
    Draft only &mdash; not committed to meeting-records. Nothing published, sent, or scheduled.<br>
    Branding: command-centre/BRANDING.md v2.0 (4 Jul 2026) &mdash; Oxford Navy, Inter, canonical crest. Template shared with the HR Systems Roadmap and Managers Meeting briefs via brief_chrome.py.
  </div>"""

html_out = render_page(
    title="H&amp;S Roadmap — 03/08",
    app_name="H&amp;S Roadmap",
    kicker="Speaking Brief &middot; Draft",
    h1="H&amp;S Roadmap — 03/08",
    meta_spans=[
        "<b>Meeting</b> Monday 3 August 2026",
        "<b>Follow-on from</b> 22 June 2026",
        "<b>Status</b> Draft — not yet approved",
    ],
    flag_label="Before anything else",
    flag_paragraphs=[
        "No H&amp;S Roadmap meeting outcome is captured in meeting-records since 22&nbsp;June &mdash; six weeks. Unlike the HR Systems Roadmap, though, the underlying H&amp;S Systems Backlog workbook has stayed live throughout, with comments logged as recently as 30&nbsp;July, so the item detail in this brief is current. What's missing is a record of what was actually agreed as a group in that time, not the underlying data.",
        "This brief covers the 9 items rated <b>Must Have</b> and/or currently <b>In&nbsp;Progress</b>, plus 3 more added because they're owned by <b>James</b> or <b>Kevin</b> regardless of priority or status (HSB025, HSB050, HSB089) &mdash; 12 of 33 active backlog items. As more James/Kevin items move active, they'll be added here too, same 3-across format.",
    ],
    glance_label="At a glance",
    glance_sub="12 featured items &middot; Must Have / In Progress + every James/Kevin item, out of 33 active in the backlog",
    glance_table_html=GLANCE_TABLE,
    sections_html=SECTIONS,
    footnote_html=FOOTNOTE,
)

out_path = fr"{SCRATCH}\hs-roadmap-brief-03-08.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html_out)
print("written", out_path, len(html_out), "chars")
