"""Render one submitted Meeting Prep Intake record with the established chrome.

This renderer deliberately reads only the supplied locked JSON record.  It does
not look up other repository files, chat history, or source uploads.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from brief_chrome import e, render_page, write_brief_output

REQUIRED = ("itemId", "position", "priority", "title", "tone", "detail", "confirmedContext", "speakerNoteSeed")
TONES = {"update", "raise", "fyi", "decision-needed"}

def fail(message):
    raise ValueError(message)

def load_record(path):
    with Path(path).open(encoding="utf-8") as source:
        record = json.load(source)
    if record.get("schemaVersion") != 1 or record.get("status") != "submitted":
        fail("Input must be a schemaVersion 1 submitted intake record.")
    meeting = record.get("meeting", {})
    if not all(meeting.get(key) for key in ("title", "date", "kind")):
        fail("Submitted record has incomplete meeting fields.")
    if not isinstance(record.get("items"), list):
        fail("Submitted record items must be a list.")
    return record

def say_this(item):
    seed = item["speakerNoteSeed"].strip()
    if seed:
        return seed
    context = item["confirmedContext"].strip() or item["detail"].strip()
    if item["tone"] == "update":
        return f"Status update: {context}"
    if item["tone"] == "raise":
        return f"I want to raise: {context}"
    if item["tone"] == "decision-needed":
        return f"I need a decision on: {context}"
    return f"For awareness: {context}"

def validate_items(items):
    seen = set()
    for item in items:
        missing = [key for key in REQUIRED if key not in item]
        if missing:
            fail(f"Item {item.get('itemId', '<unknown>')} is missing required field(s): {', '.join(missing)}.")
        if item["itemId"] in seen or not isinstance(item["position"], int) or not isinstance(item["priority"], int):
            fail("Every item needs a unique itemId plus integer position and priority.")
        if item["tone"] not in TONES or not all(isinstance(item[key], str) and item[key].strip() for key in ("title", "detail")):
            fail(f"Item {item['itemId']} has invalid required content or tone.")
        seen.add(item["itemId"])

def table(items):
    rows = []
    for item in sorted(items, key=lambda row: row["position"]):
        status = item["confirmedContext"].strip() or "No additional confirmed context supplied."
        rows.append(f"<tr><td>{item['position']}. {e(item['title'])} <span class=\"pill pill-info\">{e(item['tone'])}</span><br><small>Priority {item['priority']}</small></td><td><b>What:</b> {e(item['detail'])}<br><span class=\"cur-label\">Status</span> {e(status)}</td><td><span class=\"say-label\">Say</span> &ldquo;{e(say_this(item))}&rdquo;</td></tr>")
    return "<table class=\"fixed-grid\"><colgroup><col style=\"width:24%\"><col style=\"width:51%\"><col style=\"width:25%\"></colgroup><thead><tr><th>Item</th><th>What / Status</th><th>Say This</th></tr></thead><tbody>" + "\n".join(rows) + "</tbody></table>"

def render(record):
    validate_items(record["items"])
    meeting = record["meeting"]
    sections = f"<h2>Agenda items</h2>{table(record['items'])}"
    return render_page(title=f"{meeting['title']} — {meeting['date']}", app_name=meeting["title"], kicker="Speaking Brief · Locked intake", h1=f"{e(meeting['title'])} — {meeting['date']}", meta_spans=[f"<b>Meeting</b> {meeting['date']}", "<b>Source</b> Locked submitted intake only"], flag_label="Locked source", flag_paragraphs=["This brief was rendered only from the submitted intake record."], glance_label="At a glance", glance_sub=f"{len(record['items'])} agenda item(s)", glance_table_html="<table class=\"fixed-grid\"><thead><tr><th>Item</th><th>Value</th></tr></thead><tbody><tr><td>Meeting type</td><td>" + e(meeting["kind"]) + "</td></tr></tbody></table>", sections_html=sections, footnote_html="<div class=\"footnote\">Locked intake renderer — no external source content used.</div>")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("intake", help="Submitted intake JSON path")
    parser.add_argument("--output", help="Optional local HTML output path (avoids canonical meetings write)")
    args = parser.parse_args()
    record = load_record(args.intake)
    html = render(record)
    if args.output:
        Path(args.output).write_text(html, encoding="utf-8")
        print(f"written {args.output} ({len(html)} chars)")
    else:
        write_brief_output(html, record["meeting"]["title"], date=datetime.fromisoformat(record["meeting"]["date"]))

if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
