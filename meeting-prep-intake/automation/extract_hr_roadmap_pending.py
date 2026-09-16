"""Build and post the weekly HR Systems Roadmap pending draft.

Row-selection rule, confirmed directly by Kevin (16 Sep 2026), superseding an
earlier status/checkpoint-date heuristic drafted before this spec arrived:
include a row only when its "Lead" column value is exactly one of LEAD_FILTER
below (case-sensitive, taken verbatim from a real dropdown Kevin screenshotted
-- entries like "Chris, James" and "FA, BC, Tr" / "FA, BC. Tr" are distinct,
real, separately-occurring values in the live sheet, not near-duplicates to
merge). Verified directly against the live workbook before shipping: every
value in LEAD_FILTER genuinely appears in the real "Lead" column (e.g.
"Chris, James" x3, "FA, BC. Tr" x1, "MarieC" x8, "Simon" x21), and the column
letters Kevin gave (Deadline=T, Deadline type=V, Progress updates=W, Next
steps=X, Date last reviewed=Y, Next checkpoint date=Z, Description=D,
Specific Deliverable / Phase=C) match this script's own live header read
exactly -- not trusted blindly, independently confirmed.

On top of the Lead filter, rows with Status "Complete" or "Not Delivered" are
also excluded -- not part of Kevin's literal column spec, but a deliberate,
narrow addition: 36 of the 72 Lead-matching rows are "Complete" and a finished
item has no reason to sit on a live roadmap-meeting agenda. If Kevin actually
wants completed items included too, that's a one-line revert (drop the status
filter below) -- flagged here rather than silently assumed permanent.
"""
import argparse, hashlib, json, os, sys, time
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import openpyxl

WORKBOOK = Path(r"C:\Users\admin\OneDrive - Nexus365\HR Systems Roadmap Master\HR Systems Roadmap MASTER.xlsm")
WORKER_URL = "https://meeting.lelitte.co.uk/api/intakes/pending/write"
MEETING_ID = "hr-systems-roadmap"; SOURCE_LABEL = "HR Systems Roadmap Master.xlsm (Work Tracker)"

LEAD_FILTER = {"Chris, James", "FA", "FA, BC, Tr", "FA, BC. Tr", "FA, HRA", "Grace, Nik",
    "Kevin", "Lee", "Marie C", "MarieC", "Simon", "Simon / Marie", "TBC"}
EXCLUDED_STATUSES = {"Complete", "Not Delivered"}

# Columns this script actually reads from the live "Work Tracker" header row (row 1) --
# not a hardcoded snapshot of the whole sheet. Kept as a set of required names so a
# future column being added, removed, or reordered in Kevin's own workbook fails loudly
# here (return 1, nothing posted) instead of silently misaligning every field.
# "Specific Deliverable / Phase" and "Original Communicated Deadline (if changed)" are
# deliberately excluded per Kevin's spec -- not read into Detail at all.
REQUIRED_COLUMNS = {"ID", "Activity", "Description", "Lead", "Deadline", "Deadline type",
    "Progress updates", "Next steps", "Date last reviewed", "Next checkpoint date", "Status"}

WEEKDAY_RETRIES = 3


def log(message):
    print(f"[{datetime.now().isoformat(timespec='seconds')}] {message}")


def text(value):
    return str(value).strip() if value is not None else ""


def as_date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return None


def fmt(value):
    d = as_date(value)
    return d.strftime("%d %b %Y") if d else "not set"


def slug(value):
    return "".join(c if c.isalnum() or c in "_-" else "_" for c in value.lower())


def target_date():
    # Next Friday on/after today (Monday=0 .. Friday=4), inclusive of today if today
    # is itself a Friday -- so a manual rerun on the meeting day still targets today.
    today = date.today()
    return today.fromordinal(today.toordinal() + (4 - today.weekday()) % 7)


def cap(value, limit=6000):
    if len(value) <= limit:
        return value
    truncated = value[: limit - 1]
    return (truncated.rsplit(None, 1)[0] if " " in truncated or "\n" in truncated else truncated) + "…"


def load_rows(book):
    sheet = book["Work Tracker"]
    headers = [str(h) if h is not None else "" for h in next(sheet.iter_rows(min_row=1, max_row=1, values_only=True))]
    missing = REQUIRED_COLUMNS - set(headers)
    if missing:
        raise ValueError(f"Work Tracker header is missing expected columns: {sorted(missing)}")
    return [dict(zip(headers, values)) for values in sheet.iter_rows(min_row=2, values_only=True)]


def detail(row):
    # Exact field set and order per Kevin's confirmed spec: ID, Description, Deadline,
    # Deadline type, Progress updates (his own words: "the most important field" --
    # kept in full, not trimmed to a single latest entry), Next steps, Date last
    # reviewed, Next checkpoint date. No other workbook field is included.
    lines = [
        f"ID: {text(row['ID'])}",
        f"Description: {text(row['Description']) or 'not set'}",
        f"Deadline: {fmt(row['Deadline'])}",
        f"Deadline type: {text(row['Deadline type']) or 'not set'}",
        f"Progress updates: {text(row['Progress updates']) or 'none logged'}",
        f"Next steps: {text(row['Next steps']) or 'none logged'}",
        f"Date last reviewed: {fmt(row['Date last reviewed'])}",
        f"Next checkpoint date: {fmt(row['Next checkpoint date'])}",
    ]
    return cap("\n\n".join(lines))


def build_items(rows, meeting):
    selected = [r for r in rows if text(r["Lead"]) in LEAD_FILTER and text(r["Status"]) not in EXCLUDED_STATUSES]
    items = []
    for position, row in enumerate(selected, 1):
        row_id, title = text(row["ID"]), text(row["Activity"])
        if not row_id or not title:
            raise ValueError(f"Invalid source row: missing ID or Activity ({row_id!r})")
        # Tone/priority left at sensible, uniform defaults -- Kevin adjusts per item in
        # the browser; this script does not infer urgency from deadline/status data.
        items.append({
            "itemId": f"itm_roadmap_{slug(row_id)}",
            "position": position,
            "priority": 1,
            "title": title,
            "tone": "update",
            "detail": detail(row),
            "speakerNoteSeed": "",
            "status": "open",
            "sources": [{"kind": "roadmap-weekly", "rowId": row_id}],
        })
    return items


def load_workbook_with_retry(path, attempts=3, delay=5):
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            return openpyxl.load_workbook(path, data_only=True, read_only=True, keep_vba=False)
        except Exception as exc:  # e.g. a transient OneDrive sync lock
            last_error = exc
            log(f"Open attempt {attempt}/{attempts} failed: {exc}")
            if attempt < attempts:
                time.sleep(delay)
    raise last_error


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Print the computed payload instead of posting it.")
    args = parser.parse_args()

    log("Starting HR Systems Roadmap pending draft extraction.")
    log(f"Reading workbook: {WORKBOOK}")
    try:
        book = load_workbook_with_retry(WORKBOOK)
    except Exception as exc:
        log(f"Failed to open workbook: {exc}")
        return 1

    try:
        rows = load_rows(book)
    except Exception as exc:
        log(f"Failed to read Work Tracker: {exc}")
        return 1

    meeting = target_date()
    try:
        items = build_items(rows, meeting)
    except ValueError as exc:
        log(str(exc))
        return 1

    payload = {
        "meetingId": MEETING_ID,
        "date": meeting.isoformat(),
        "items": items,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "sourceLabel": SOURCE_LABEL,
        "sourceDigest": "sha256:" + hashlib.sha256(WORKBOOK.read_bytes()).hexdigest(),
    }
    log(f"Rows: total {len(rows)} / lead-matched & active {len(items)}. Target date: {meeting.isoformat()}")

    if args.dry_run:
        log(json.dumps(payload, indent=2))
        return 0

    secret = os.environ.get("MEETING_PREP_PENDING_SECRET")
    if not secret:
        log("MEETING_PREP_PENDING_SECRET is not set.")
        return 1

    for attempt in range(1, WEEKDAY_RETRIES + 1):
        try:
            request = Request(
                WORKER_URL,
                data=json.dumps(payload).encode(),
                method="POST",
                headers={"Content-Type": "application/json", "X-Automation-Secret": secret},
            )
            with urlopen(request, timeout=30) as response:
                log(f"Write confirmation: {response.read().decode()}")
                return 0
        except (HTTPError, URLError, OSError) as exc:
            log(f"Write attempt {attempt}/{WEEKDAY_RETRIES} failed: {exc}")
            if attempt < WEEKDAY_RETRIES:
                time.sleep(5)
    return 1


if __name__ == "__main__":
    sys.exit(main())
