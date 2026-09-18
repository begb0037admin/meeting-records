"""Render one submitted Meeting Prep Intake record with the established chrome.

This renderer deliberately reads only the supplied locked JSON record.  It does
not look up other repository files, chat history, or source uploads.
"""
import argparse
import json
import re
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
    context = agenda_text(item["confirmedContext"]) or agenda_text(item["detail"])
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


_FIELD_LABEL = re.compile(
    r"(?:^|\n)\s*(?:ID|Description|Deadline|Deadline\s+type|Progress\s+updates|"
    r"Next\s+steps|Date\s+last\s+reviewed|Next\s+checkpoint\s+date)\s*:",
    re.IGNORECASE,
)
_PROGRESS_SECTION = re.compile(r"\bProgress\s+updates\s*:\s*", re.IGNORECASE)
_NEXT_SECTION = re.compile(r"\n\s*(?:Next\s+steps|Date\s+last\s+reviewed|Next\s+checkpoint\s+date)\s*:", re.IGNORECASE)
_DATED_UPDATE = re.compile(
    r"(?s)(?P<date>\d{1,2}/\d{1,2}/\d{2,4})\s*-\s*(?P<text>.+?)(?=\s*\d{1,2}/\d{1,2}/\d{2,4}\s*-|\Z)"
)


def _parse_date(raw):
    for fmt in ("%d/%m/%y", "%d/%m/%Y"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


def newest_dated_progress_entry(text):
    """Return the newest DD/MM/YY-prefixed entry inside a 'Progress updates:'
    section, if one exists. This is a fallback only -- see agenda_text()."""
    match = _PROGRESS_SECTION.search(text or "")
    if not match:
        return None
    section = (text or "")[match.end():]
    end = _NEXT_SECTION.search(section)
    if end:
        section = section[:end.start()]
    updates = []
    for entry in _DATED_UPDATE.finditer(section):
        date = _parse_date(entry.group("date"))
        if date:
            updates.append((date, " ".join(entry.group("text").split())))
    if not updates:
        return None
    newest = max(updates, key=lambda update: update[0])
    return f"{newest[0].strftime('%d/%m/%y')} - {newest[1]}"


# Backward-compatible alias (kept in case anything else imports the old name).
latest_progress_update = newest_dated_progress_entry


def agenda_text(text):
    """Extract just the genuinely latest update from a supplied detail/status
    string, formatted for readability. Real production data (the Roadmap
    Master export feeding the intake pipeline) puts the FRESHEST line first,
    ahead of a raw field dump (ID/Description/Deadline/... then a historical
    'Progress updates:' log) -- so the correct 'latest update' is normally
    whatever text precedes the first recognised field label, NOT the newest
    entry inside the historical log (that log can be a release behind the
    leading line, e.g. a leading '18/09/26 - ...' line dated the meeting day
    itself vs. a '21/08/26 - ...' entry buried in Progress updates:).

    Falls back to the newest dated Progress-updates entry only if there's no
    leading text to use, and finally to the plain supplied text unchanged --
    the normal/intended case for a short, already-concise intake item with no
    field-dump structure at all (graceful degradation, not a hard dependency
    on this malformed shape existing)."""
    clean = (text or "").strip()
    if not clean:
        return clean
    match = _FIELD_LABEL.search(clean)
    if not match:
        # No recognised field-dump structure at all -- the normal/intended
        # case (a short plain sentence). Nothing to trim.
        return clean
    head = clean[:match.start()].strip()
    if head:
        return head
    fallback = newest_dated_progress_entry(clean)
    if fallback:
        return fallback
    # Confirmed field-dump structure (ID:/Description:/... present), but no
    # leading freshest-line and no dated Progress-updates entry either --
    # genuinely nothing fresh on record (e.g. an item last reviewed over a
    # year ago). Say so honestly rather than either inventing a summary or
    # falling back to the raw multi-field dump -- matches this repo's own
    # existing convention for an empty progress log (see build_roadmap.py's
    # render_updates()) and the "shortest honest version, never fabricate"
    # rule in agent-commons meeting-records/styles/speaker-note-style.md.
    return "No dated update recorded in the supplied detail."

def table(items):
    rows = []
    for item in sorted(items, key=lambda row: row["position"]):
        detail = agenda_text(item["detail"])
        status = agenda_text(item["confirmedContext"])
        status_html = "" if not status or status == detail else f"<p class=\"agenda-status\"><span class=\"cur-label\">Status</span> {e(status)}</p>"
        rows.append(f"<tr><td>{item['position']}. {e(item['title'])} <span class=\"pill pill-info\">{e(item['tone'])}</span><br><small>Priority {item['priority']}</small></td><td><p class=\"agenda-latest\"><span class=\"cur-label\">What</span> {e(detail)}</p>{status_html}</td><td><span class=\"say-label\">Say</span> &ldquo;{e(say_this(item))}&rdquo;</td></tr>")
    return "<table class=\"fixed-grid\"><colgroup><col style=\"width:24%\"><col style=\"width:51%\"><col style=\"width:25%\"></colgroup><thead><tr><th>Item</th><th>What / Status</th><th>Say This</th></tr></thead><tbody>" + "\n".join(rows) + "</tbody></table>"

def render(record):
    validate_items(record["items"])
    meeting = record["meeting"]
    sections = f"<h2>Agenda items</h2>{table(record['items'])}"
    return render_page(title=f"{meeting['title']} — {meeting['date']}", app_name=meeting["title"], kicker="Speaking Brief · Locked intake", h1=f"{e(meeting['title'])} — {meeting['date']}", meta_spans=[f"<b>Meeting</b> {meeting['date']}", "<b>Source</b> Locked submitted intake only"], flag_label="Locked source", flag_paragraphs=["This brief was rendered only from the submitted intake record."], sections_html=sections, footnote_html="<div class=\"footnote\">Locked intake renderer — no external source content used.</div>")

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
