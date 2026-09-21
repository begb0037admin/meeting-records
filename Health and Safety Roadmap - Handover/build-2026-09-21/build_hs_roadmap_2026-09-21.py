import json
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import brief_chrome
from brief_chrome import e, render_page, write_brief_output


ROOT = Path(__file__).resolve().parent
with (ROOT / "hs-items.json").open(encoding="utf-8") as handle:
    ITEMS = json.load(handle)
with (ROOT / "content.json").open(encoding="utf-8") as handle:
    CONTENT = json.load(handle)

ITEM_ORDER = CONTENT["item_order"]
PILL = CONTENT["pill"]
PILL_TEXT = CONTENT["pill_text"]
SAY = CONTENT["say"]


def validate_content():
    missing_items = [ref for ref in ITEM_ORDER if ref not in ITEMS]
    missing_pills = [ref for ref in ITEM_ORDER if ref not in PILL]
    missing_say = [ref for ref in ITEM_ORDER if ref not in SAY]
    unknown_pills = [
        (ref, PILL[ref])
        for ref in ITEM_ORDER
        if ref in PILL and PILL[ref] not in PILL_TEXT
    ]
    problems = []
    if missing_items:
        problems.append(f"missing hs-items.json refs: {', '.join(missing_items)}")
    if missing_pills:
        problems.append(f"missing pill entries: {', '.join(missing_pills)}")
    if missing_say:
        problems.append(f"missing say entries: {', '.join(missing_say)}")
    if unknown_pills:
        problems.append(
            "missing pill labels: "
            + ", ".join(f"{ref}={pill}" for ref, pill in unknown_pills)
        )
    if problems:
        raise ValueError("Invalid roadmap content: " + "; ".join(problems))


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

    pill = PILL[ref]
    return f'''
  <article class="item card">
    <header class="item-head">
      <span class="item-id">{e(ref)}</span>
      <h3 class="item-title">{e(d["item_name"])}</h3>
      <span class="pill pill-{e(pill)}">{e(PILL_TEXT[pill])}</span>
      <p class="item-owner">{e(d.get("owner") or "Unassigned")} &nbsp;&middot;&nbsp; {e(d.get("system"))}</p>
    </header>

    <p class="item-desc">{e(d.get("detail") or "")}</p>

    <div class="last-update">
      <span class="lu-label">Last logged update{f" &middot; {e(last_date)}" if last_date else ""}</span>
      <p>{e(last_text) or "No dated update on record."}</p>
    </div>

    <blockquote><span class="say-label">Say this</span><p>&ldquo;{e(SAY[ref])}&rdquo;</p></blockquote>

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


def generated_timestamp():
    now = datetime.now(ZoneInfo("Europe/London"))
    return now.strftime("%a %d %b %Y, %H:%M %Z")


def build_sections():
    glance_rows = []
    for ref in ITEM_ORDER:
        d = ITEMS[ref]
        pill = PILL[ref]
        glance_rows.append(
            f'<tr><td class="idcell">{e(ref)}</td><td>{e(d["item_name"])}</td><td>{e(d.get("system"))}</td>'
            f'<td>{e(d.get("owner") or "Unassigned")}</td><td><span class="pill pill-{e(pill)}">{e(PILL_TEXT[pill])}</span></td></tr>'
        )
    glance = f'''
  <h2>At a glance <span class="h2-sub">{len(ITEM_ORDER)} featured items</span></h2>
  <div class="table-wrap card"><table class="fixed-grid">
    <colgroup><col style="width:9%"><col style="width:47%"><col style="width:12%"><col style="width:12%"><col style="width:20%"></colgroup>
    <thead><tr><th>Ref</th><th>Item</th><th>System</th><th>Owner</th><th>Status</th></tr></thead>
    <tbody>{"".join(glance_rows)}</tbody>
  </table></div>
'''
    cards = "\n".join(render_item(ref) for ref in ITEM_ORDER)
    return (
        CONTENT["pre_grid_html"]
        + glance
        + CONTENT["grid_heading_html"]
        + '\n  <div class="item-grid">\n'
        + cards
        + '\n  </div>\n'
        + CONTENT["post_grid_html"]
    )


def main():
    validate_content()
    generated = generated_timestamp()
    meta_spans = [span.replace("{{GENERATED}}", generated) for span in CONTENT["meta_spans"]]
    footnote = CONTENT["footnote_html"].replace("{{GENERATED}}", generated)

    html_out = render_page(
        title=CONTENT["title"],
        app_name=CONTENT["app_name"],
        kicker=CONTENT["kicker"],
        h1=CONTENT["h1"],
        meta_spans=meta_spans,
        flag_label=CONTENT["flag_label"],
        flag_paragraphs=CONTENT["flag_paragraphs"],
        sections_html=build_sections(),
        footnote_html=footnote,
    )

    if os.environ.get("HS_BRIEF_TEST") == "1":
        brief_chrome.MEETINGS_DIR = os.path.join(brief_chrome.SCRATCH, "out_test")

    write_brief_output(
        html_out,
        "Health and Safety Roadmap",
        date=datetime(2026, 9, 21),
    )


if __name__ == "__main__":
    main()
