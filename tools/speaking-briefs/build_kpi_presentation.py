"""
KPI Presentation generator - general, reusable across months.

Reads a month's Source Data folder (Excel + H&S Word doc), following the
convention Kevin confirmed: source files land by email and get dropped into
Functional Analysis Team Monthly Statistics/{YYYY}/{MM Mon}/Source Data/.

Base deck: copies the PREVIOUS month's own finished deck (the real monthly
process, confirmed 2 Aug 2026 - the saved "Templates" file is stale and not
used) and edits it in place, so layout fixes (blank-row removal, chart image
positions - see memory/kpi-presentation-layout-fixes.md) persist forward
automatically without needing to be reapplied each month.

KNOWN GAP, permanent characteristic of the source data (not a bug): the H&S
per-system incident-volume breakdown (slide 2) and time-to-resolve band
breakdown (slide 3) only exist as a "last month" snapshot in each month's own
Word doc - there is no rolling multi-month series for these two tables, unlike
every PXD-sourced table/chart (slides 4-10), which get a full 15-month rolling
window each month and are fully self-contained (confirmed 7 Aug 2026: slides
6/7's time-to-complete bands ARE on a rolling sheet in the current month's own
Excel, so - unlike H&S - they need no cross-month lookup at all). So the
"previous month" column for slides 2 and 3 must come from somewhere other than
the current month's own source data.

RESOLVED 7 Aug 2026 (was an open gap, folded into build_month() below): the
prior month's own Source Data folder, when it still exists in the OneDrive
archive, carries the exact same "last month" snapshot for what WAS then the
current month - i.e. May's own H&S doc's "last month" table IS May's own
confirmed figures, byte-verified to match the real June deck's "May 26"
column exactly. build_month() auto-locates and reads it by default. This is
real carried-forward data, not invented - but it does depend on the archive
folder still being there; build_month() accepts an explicit prev_hs override
for the rare case it isn't.
"""
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from copy import deepcopy
import openpyxl
from docx import Document
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
import glob
import re
import os
import sys

ORANGE = "#ED7D31"
GREEN = "#70AD47"
DARKRED = "#843C0C"

# --- Slide 5, Table 4 "Incident - Other Type" ------------------------------
# ADR-0001 (2026-09-07, docs/decisions/0001-incident-other-table-scope.md):
# the table is 9 fixed named FA categories + one "Other" row that absorbs
# every source category not in the named set. Its Total row and every
# percentage base = the source sheet's own month total (NOT a sum of a
# trimmed subset). This makes Slide 5 Table 4 reconcile EXACTLY to Slide 7's
# band-count total every month (reconciliation registry R1) and makes each
# percentage equal the source sheet's own "Category %" column.
#
# The former hard-coded INCIDENT_OTHER_EXCLUDE blacklist is deleted. It was
# inherently reactive - a wrong deck shipped first, then the missing name
# was found - which is exactly how the July 2026 deck shipped with visible
# rows that did not sum to the displayed Total (Codex review + Michael
# O'Sullivan's 13 Aug 2026 email). Row 10 (was "Interfaces") is now "Other".
#
# (display_label, source Service Category name) - order is the row order.
INCIDENT_OTHER_NAMED = [
    ("People Management",        "People Management"),
    ("Time and Attendance",      "Time and Attendance"),
    ("Payroll",                  "Payroll"),            # exact - NOT "Payroll Costing Report", NOT "X5 - Costing Maintenance"
    ("HR Reporting",             "HR Reporting"),
    ("Data Protection Request",  "Data Protection Request"),
    ("Staff Requests",           "Staff Requests"),
    ("Work Groups & Managers",   "Work Groups and Managers"),
    ("Recruitment",              "Recruitment"),
    ("Roster (WFM)",             "Roster (WFM)"),
]

# Known-good Slide 5 Table 4 figures (post-ADR-0001) used as self-test
# oracles. June's circulated deck carried the pre-ADR-0001 defect (Total 68,
# no "Other" row), so it is NOT valid ground truth - these corrected values
# are (HANDOVER Part A4: "the June self-test oracle changes 68 -> 77").
IO_ORACLE = {
    (2026, 6): {"People Management": 28, "Time and Attendance": 18, "Payroll": 1,
                "HR Reporting": 5, "Data Protection Request": 7, "Staff Requests": 2,
                "Work Groups & Managers": 3, "Recruitment": 2, "Roster (WFM)": 0,
                "Other": 11, "__total__": 77},
    (2026, 8): {"People Management": 31, "Time and Attendance": 18, "Payroll": 2,
                "HR Reporting": 0, "Data Protection Request": 3, "Staff Requests": 1,
                "Work Groups & Managers": 3, "Recruitment": 0, "Roster (WFM)": 1,
                "Other": 2, "__total__": 61},
}


def pct2(n, d):
    """n/d as a percentage, 2 dp, ROUND_HALF_UP - the convention the Ivanti
    and H&S source reports use for their own "Category %" columns. Python's
    round() uses round-half-to-even and is also subject to float-repr
    surprises at the .xx5 boundary (e.g. round(40.625, 2) -> 40.62), which
    would make the hardened gate reject percentages that are actually
    correct against the source. Returns a Decimal."""
    if not d:
        return Decimal("0.00")
    return (Decimal(int(n)) / Decimal(int(d)) * 100).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP)


def pct_str(n, d):
    return f"{pct2(n, d):.2f}%"

# --- Month / folder conventions (7 Aug 2026 extension) -----------------
# Confirmed OneDrive layout: Functional Analysis Team Monthly Statistics\
# {YYYY}\{MM Mon}\ with a Source Data\ subfolder each month, and the
# finished deck for month N sitting alongside as
# "KPI presentation - {Month} {YYYY}.pptx". See memory/
# kpi-presentation-source-and-rebuild-poc.md (Lauren, confirmed 2 Aug 2026).
ONEDRIVE_BASE = (
    r"C:\Users\admin\OneDrive - Nexus365\Functional Analysis Team Monthly Statistics"
)
MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTH_FULL = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]


def month_dir(year, month):
    return os.path.join(ONEDRIVE_BASE, str(year), f"{month:02d} {MONTH_ABBR[month - 1]}")


def short_label(year, month):
    """e.g. (2026, 6) -> 'Jun 26' - matches the deck's own header style."""
    return f"{MONTH_ABBR[month - 1]} {year % 100:02d}"


def deck_path(year, month):
    return os.path.join(
        month_dir(year, month),
        f"KPI presentation - {MONTH_FULL[month - 1]} {year}.pptx",
    )


def prev_ym(year, month):
    return (year - 1, 12) if month == 1 else (year, month - 1)


def find_one(dirpath, pattern):
    """Locate exactly one file matching pattern in dirpath. Source filenames
    carry a variable export-timestamp suffix (e.g. '...202607010715.xlsx')
    so callers can't hardcode the full name - but there must be exactly one
    match, or something is wrong with the folder and we should say so rather
    than silently pick one."""
    matches = glob.glob(os.path.join(dirpath, pattern))
    if len(matches) != 1:
        raise FileNotFoundError(
            f"expected exactly 1 match for {pattern!r} in {dirpath!r}, found {len(matches)}: {matches}"
        )
    return matches[0]


def find_source_files(year, month):
    """Locate a given month's own Excel export and H&S Word doc inside its
    Source Data folder."""
    src = os.path.join(month_dir(year, month), "Source Data")
    excel_path = find_one(src, "HR_Systems_Functional_Team_Monthly_Report_Excel*.xlsx")
    hs_path = find_one(src, "Health and Safety Systems Support Statistics*.docx")
    return excel_path, hs_path


# --- Speaker notes (Part D, 7 Sep 2026 - closes a real process gap) --------
# Confirmed live: the July AND August decks both still carried JUNE's speaker
# notes verbatim (byte-identical notes_text_frame content) - populate_deck
# never touched notes_slide at all, so whatever the base deck's notes said
# just rode along. Kevin reads these aloud when presenting, so he was reading
# June's numbers in July and again in August. This was invisible to
# validate_deck() because it only ever checked tables/charts/reconciliation.
#
# Speaker notes are Lauren's authored content (drafted prose, not a pure
# data substitution), same status as a meeting brief - so they live in this
# repo, not OneDrive, and Drew's job is only to place approved text and
# refuse to build without it, never to draft or judge the wording.
NOTES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..",
    "KPI Presentation - Handover", "notes",
)
# Slides that must carry month-specific speaker notes (0-based slide index -
# Slides 2 through 10; Slide 1 is the title card and Slide 11 is "Thank you",
# neither carries data-specific notes).
NOTES_REQUIRED_SLIDES = set(range(1, 10))


def notes_path_for(year, month, notes_path=None):
    if notes_path:
        return notes_path
    return os.path.normpath(os.path.join(NOTES_DIR, f"speaker-notes-{year}-{month:02d}.md"))


def load_month_notes(year, month, notes_path=None):
    """Parse `## Slide N` markdown sections into {1-based slide number: body
    text}. Returns (None, resolved_path) if the file doesn't exist yet -
    callers decide what that means (build_month treats it as a hard stop)."""
    path = notes_path_for(year, month, notes_path)
    if not os.path.exists(path):
        return None, path
    raw = open(path, encoding="utf-8").read()
    parts = re.split(r"(?im)^##\s*slide\s+(\d+)\s*$", raw)
    notes = {}
    for i in range(1, len(parts), 2):
        notes[int(parts[i])] = parts[i + 1].strip()
    return notes, path


def parse_count_pct(s):
    """Parse a rolling-sheet cell like '112 (74.67%)' into (112, 74.67).
    Returns (0, 0.0) for a blank/None cell (a month with no recorded tasks
    in that band - a real possible value, not a parsing failure)."""
    if not s:
        return 0, 0.0
    m = re.match(r"\s*(-?\d+)\s*\(([-\d.]+)%\)\s*$", str(s))
    if not m:
        raise ValueError(f"unrecognised count/pct cell format: {s!r}")
    return int(m.group(1)), float(m.group(2))


def extract_pxd(excel_path):
    """Pull every PXD-sourced figure from the month's Excel export.
    Returns a dict keyed by the logical field each slide needs."""
    wb = openpyxl.load_workbook(excel_path, data_only=True)

    def sheet_row(sheet_name, row_label_col0):
        ws = wb[sheet_name]
        for row in ws.iter_rows(values_only=True):
            if row and row[0] == row_label_col0:
                return row
        raise KeyError(f"row {row_label_col0!r} not found in {sheet_name!r}")

    def monthly_by_category(sheet_name):
        """Sheets shaped like: title row, blank spacer row, header row of
        months, then one row per category. Returns {category: [15 monthly
        values]} plus the month header row (for locating which column is
        'this month' etc.).

        FIX (7 Aug 2026): header is row index 2, not 1 - row 1 is a blank
        spacer row on every sheet checked (confirmed across 7 sheets this
        function reads from). The original index-1 assumption meant `header`
        was always the blank row, and the data loop (starting at rows[2:])
        picked up the *real* header row as a bogus extra "category" whose
        row[0] label is the sheet's column-header text and whose "monthly
        values" are literally the month-label strings ('Apr 25', ... 'Jun
        26'). This was silently harmless everywhere the buggy version was
        already exercised - sheets whose header cell is None (Average Task
        Acceptance, Tasks, etc.) skip it via the `not label` check, and
        sheets where it produced a real string key (e.g. 'Parent Ticket
        Type HRIS') just added an unused dict entry nothing ever looked up.
        It broke immediately, though, on the newly-wired slide 6/7 band
        parsing (build_month(2026, 6, ...) raised ValueError parsing 'Jun
        26' as a count/pct cell) - see memory/kpi-presentation-assembly-gap.md,
        this is exactly the "genuinely new, unattempted, needs its own
        self-test" capability that surfaced it. Fixing the index also fixes
        a second, previously undetected bug: every *_months output
        (slide4_months, slide8_months, etc.) was always a tuple of all
        None - nothing in the original 9-check self-test compared month
        labels, so this went unnoticed until make_trend_chart's x-axis
        labels would have shown blank ticks."""
        ws = wb[sheet_name]
        rows = list(ws.iter_rows(values_only=True))
        header = rows[2]  # title (0), blank spacer (1), month header (2)
        data = {}
        for row in rows[3:]:
            if not row or row[0] in (None, "Description") or (isinstance(row[0], str) and row[0].startswith("Total")):
                continue
            label = row[0].strip() if isinstance(row[0], str) else row[0]
            if not label:
                continue
            data[label] = row[1:len(header)]
        return header[1:], data

    out = {}

    # Slide 4: PXD categories by month (Change / Incident-HR Self-Service /
    # Incident-Other / Service Request)
    months, cats = monthly_by_category("Tasks Completed by HRIS Analy2")
    out["slide4_months"] = months
    out["slide4_categories"] = {
        "Change": cats["Change"],
        "HR Self Service": cats["Incident - HR Self-Service"],
        "Incident – Other": cats["Incident - Other"],
        "Service Request": cats["Service Request"],
    }

    # Slide 5, Table 6: Service Request type breakdown, last month only
    ws = wb["Service Request Tasks complete"]
    rows = [r for r in ws.iter_rows(values_only=True) if r and r[0] not in (None, "Description") and not str(r[0]).startswith("Total")]
    label_map = {
        "Manager Self Service (MSS)": "Manager Self Service",
        "Work Group (HR Self-Service)": "WG - HR Self-Service",
        "Add New Shift Type (HR Self-Service)": "Add New Shift Type",
        "HR Systems User Access": "HR Systems User Access",
        "HR Systems People Data Dashboards": "People Data Dashboards",
        "HR Systems Enhancement and Changes": "Enhancement & Changes",
    }
    sr_breakdown = {}
    for r in rows[1:]:
        if r[0] in label_map:
            sr_breakdown[label_map[r[0]]] = (r[1] or 0, r[2] or "0.00%")
    out["slide5_service_request"] = sr_breakdown

    # Slide 5, Table 4: "Incident - Other Type" service-category breakdown,
    # last month only. Per ADR-0001 (see INCIDENT_OTHER_NAMED comment above):
    # 9 fixed named rows + one "Other" row (= source month total - sum of
    # named), Total & percentage base = the sheet's own month total row.
    ws = wb["Non-HR Self Service Incident T"]
    io_counts = {}          # source Service Category name -> count
    io_total = None         # the sheet's own month total row, shaped (<int>, 0, None)
    for r in ws.iter_rows(values_only=True):
        if not r:
            continue
        if isinstance(r[0], int) and r[1] == 0 and r[2] is None:
            io_total = r[0]
            continue
        if (isinstance(r[0], str) and r[0] != "Description"
                and not r[0].startswith("Total") and r[0].strip()
                and isinstance(r[1], int)):
            io_counts[r[0]] = r[1]
    if io_total is None:
        raise ValueError(
            "Non-HR Self Service Incident T: could not find the sheet's own "
            "month-total row (expected shape (<int>, 0, None))"
        )
    src_sum = sum(io_counts.values())
    if src_sum != io_total:
        raise ValueError(
            f"Non-HR Self Service Incident T: source does not add up - category "
            f"rows sum to {src_sum} but the sheet's own total row is {io_total}. "
            f"Refusing to build on inconsistent source data."
        )
    named_sum = 0
    io_display = {}
    for display_label, src_name in INCIDENT_OTHER_NAMED:
        c = io_counts.get(src_name, 0)
        named_sum += c
        io_display[display_label] = (c, pct_str(c, io_total))
    other_count = io_total - named_sum
    if other_count < 0:
        raise ValueError(
            f"Non-HR Self Service Incident T: the 9 named categories sum to "
            f"{named_sum}, which exceeds the month total {io_total}"
        )
    io_display["Other"] = (other_count, pct_str(other_count, io_total))
    out["slide5_incident_other"] = io_display          # {display_label: (count, "NN.NN%")}
    out["slide5_incident_other_total"] = io_total
    # FIX 2 (7 Sep 2026): raw source Service-Category -> count map, so
    # validate_deck() can trace every displayed Table 4 count back to a
    # specific source figure (defends against a coherently-wrong allocation
    # - e.g. two category rows swapped - that still self-reconciles).
    out["slide5_incident_other_source_counts"] = dict(io_counts)

    # Slides 6/7: completion-time % bands, monthly rolling
    _, sr_time = monthly_by_category("Time To Complete Service Requ1")
    _, oi_time = monthly_by_category("Time To Complete Other Incide1")
    out["slide6_bands"] = sr_time   # {'Same Day': [...], 'Next Day': [...], '3 - 5 days': [...], '6+ days': [...]}
    out["slide7_bands"] = oi_time

    # Slides 8/9: average days, monthly rolling
    months, acc = monthly_by_category("Average Task Acceptance (Days)")
    out["slide8_months"] = months
    out["slide8_values"] = acc["Tasks"]
    months, comp = monthly_by_category("Average Task Time to Complete ")
    out["slide9_months"] = months
    out["slide9_values"] = comp["Tasks"]

    # Slide 9 chart's "Total: N" annotation is NOT sum(slide9_values) (that
    # would be a meaningless sum of average-days figures) - it's the total
    # completed-tasks count from a *different* sheet. Confirmed 2 Aug 2026
    # by hand-summing against the proven picture-swap rebuild (see
    # memory/kpi-presentation-layout-fixes.md): slide 8's total is the
    # 'Tasks' sheet's Created sum (already available as slide10_created),
    # slide 9's is this sheet's Completed Tasks sum.
    _, analy3 = monthly_by_category("Tasks Completed by HRIS Analy3")
    out["slide9_completed_tasks"] = analy3["Completed Tasks"]

    # Slide 10: created vs completed, monthly rolling
    months, tasks = monthly_by_category("Tasks")
    out["slide10_months"] = months
    out["slide10_created"] = tasks["Created"]
    out["slide10_completed"] = tasks["Completed / Cancelled / Rejected"]

    return out


def extract_hs(docx_path):
    """Pull this month's H&S figures (last-month snapshot only - see module
    docstring for why there's no rolling series here).

    IMPORTANT: this doc has BOTH a "last month" and a "last 12 months"
    version of each table, with IDENTICAL column headers - text-matching on
    headers alone silently grabs the wrong (12-month cumulative) one. Must
    match on the preceding description paragraph's "last month" wording, not
    header shape. Table indices below were confirmed against June 2026's doc
    (verified 2 Aug 2026 self-test) but this walks the document body in
    order and matches on description text, so it isn't a hardcoded index -
    it should hold for any month using the same export template."""
    doc = Document(docx_path)
    body = doc.element.body
    out = {}
    pending_desc = ""
    for child in body.iterchildren():
        if child.tag.endswith("}p"):
            text = "".join(node.text or "" for node in child.iter() if node.tag.endswith("}t"))
            if "Description" in text or "last month" in text or "12 months" in text:
                pending_desc = text
        elif child.tag.endswith("}tbl"):
            from docx.table import Table
            t = Table(child, doc)
            rows = [[c.text for c in r.cells] for r in t.rows]
            if not rows:
                continue
            is_last_month = "last month" in pending_desc and "12 months" not in pending_desc
            if is_last_month and rows[0] == ["", "Category", "Category %"] and any("Cority" in r[0] for r in rows[1:] if r[0]):
                out["slide2_volumes"] = {r[0]: (int(r[1]), r[2]) for r in rows[1:]}
            if is_last_month and rows[0] == ["", "Time To Resolve (Days to 6+)", "Time To Resolve (Days to 6+) %"]:
                out["slide3_bands"] = {r[0]: (int(r[1]), r[2]) for r in rows[1:]}
    return out


def make_trend_chart(months, values, total, out_path, y_step):
    fig, ax = plt.subplots(figsize=(20, 12.88), dpi=100)
    fig.patch.set_facecolor("white")
    x = np.arange(len(months))

    def nice_floor(v, step):
        return np.floor(v / step) * step

    ymin = max(0, nice_floor(min(values), y_step) - y_step) if min(values) > y_step else 0
    ymax = max(values) + y_step * 2
    ax.set_xlim(-0.6, len(months) - 0.4)
    ax.set_ylim(ymin, ymax)

    grad = np.vstack([np.linspace(0, 1, 256)] * 2)
    ax.imshow(grad, extent=[*ax.get_xlim(), *ax.get_ylim()], aspect="auto", cmap="Greys", alpha=0.08, zorder=0)

    ax.bar(x, values, width=0.55, color=ORANGE, zorder=3, bottom=0)

    z = np.polyfit(x, values, 1)
    trend = np.poly1d(z)
    ax.plot(x, trend(x), color="#595959", linewidth=1.2, zorder=4)

    for xi, v in zip(x, values):
        ax.annotate(f"{v:.1f}", (xi, max(v, ymin)), xytext=(0, -18), textcoords="offset points",
                    ha="center", va="top", fontsize=13,
                    bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="#BFBFBF", lw=0.8))

    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=60, ha="right", fontsize=13)
    ax.yaxis.set_major_locator(mticker.MultipleLocator(y_step))
    ax.grid(axis="y", color="#E0E0E0", linewidth=0.8, zorder=1)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.text(0.995, 0.01, f"Total: {total}", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=13, color="#7F7F7F")
    fig.subplots_adjust(left=0.04, right=0.98, top=0.98, bottom=0.28)
    plt.savefig(out_path, facecolor="white")
    plt.close(fig)


def make_combo_chart(months, created, completed, out_path):
    fig, ax1 = plt.subplots(figsize=(20, 12.88), dpi=100)
    fig.patch.set_facecolor("white")
    x = np.arange(len(months))
    w = 0.38
    ax1.set_xlim(-0.6, len(months) - 0.4)
    ax1.set_ylim(0, max(max(created), max(completed)) + 50)
    grad = np.vstack([np.linspace(0, 1, 256)] * 2)
    ax1.imshow(grad, extent=[*ax1.get_xlim(), *ax1.get_ylim()], aspect="auto", cmap="Greys", alpha=0.08, zorder=0)
    ax1.bar(x - w / 2, created, width=w, color=ORANGE, zorder=3, label=f"Created ({sum(created)})")
    ax1.bar(x + w / 2, completed, width=w, color=GREEN, zorder=3, label=f"Completed / Cancelled / Rejected ({sum(completed)})")
    ax1.set_ylabel("Number of Tasks created and completed", fontsize=13, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(months, rotation=60, ha="right", fontsize=13)
    ax1.grid(axis="y", color="#E0E0E0", linewidth=0.8, zorder=1)
    ax1.set_axisbelow(True)
    ax1.spines["top"].set_visible(False)

    variance = [abs(c - r) for c, r in zip(completed, created)]
    ax2 = ax1.twinx()
    ax2.plot(x, variance, color=DARKRED, marker="o", linewidth=1.5, zorder=4, label="Variance *")
    ax2.set_ylim(0, max(variance) + 5)
    ax2.spines["top"].set_visible(False)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="lower center",
               bbox_to_anchor=(0.5, -0.32), ncol=3, frameon=True, fontsize=12)
    ax1.text(0.995, 1.02, f"Total: {sum(created) + sum(completed)}", transform=ax1.transAxes,
             ha="right", va="bottom", fontsize=13, color="#7F7F7F")
    fig.subplots_adjust(left=0.04, right=0.98, top=0.9, bottom=0.28)
    plt.savefig(out_path, facecolor="white")
    plt.close(fig)


def set_cell(cell, text):
    para = cell.text_frame.paragraphs[0]
    if para.runs:
        para.runs[0].text = text
        for extra in para.runs[1:]:
            extra.text = ""
    else:
        para.text = text


def find_table(slide, name):
    for shape in slide.shapes:
        if shape.has_table and shape.name == name:
            return shape.table
    raise RuntimeError(f"table {name!r} not found")


def _table_shape(slide, name):
    """The GraphicFrame shape (not the .table) for a named table - needed
    for its geometry when positioning a caption relative to it."""
    for shape in slide.shapes:
        if shape.has_table and shape.name == name:
            return shape
    raise RuntimeError(f"table shape {name!r} not found")


# The scope notes on Slides 4 & 5 are hosted as an INHERITED BODY placeholder
# (the "Title w Chart" layout's spare idx-11 placeholder), NOT a free
# add_textbox shape. Confirmed 7 Sep 2026: PowerPoint silently dropped the
# free text box when Kevin opened the delivered deck (the on-disk file came
# back with Slide 4's caption gone, which then failed validate_deck()). A
# layout-inherited placeholder is retained across an open/save round-trip -
# that is what placeholders are for. See SCOPE_NOTE_SIGNATURES / the gate's
# scope-note check for the "re-homed OK, absent = fail" rule.
SCOPE_NOTE_PH_IDX = 11


def _upsert_scope_note(slide, name, text, left, top, width, height, size_pt=9):
    """Place a small grey scope note on `slide` as an inherited BODY
    placeholder (idx SCOPE_NOTE_PH_IDX), positioned where told. Idempotent:
    if a shape called `name` is already there, just replace its text. The
    placeholder form survives a PowerPoint open/close; add_textbox did not."""
    shape = next((sh for sh in slide.shapes if sh.name == name), None)
    if shape is None:
        src = next((ph._element for ph in slide.slide_layout.placeholders
                    if ph.placeholder_format.idx == SCOPE_NOTE_PH_IDX), None)
        if src is None:
            raise RuntimeError(
                f"layout {slide.slide_layout.name!r} has no idx-{SCOPE_NOTE_PH_IDX} "
                f"placeholder to host the scope note - layout changed?"
            )
        el = deepcopy(src)
        cnvpr = el.find(qn("p:nvSpPr") + "/" + qn("p:cNvPr"))
        used = {int(x.get("id")) for x in slide.shapes._spTree.iter(qn("p:cNvPr"))}
        cnvpr.set("id", str(max(used) + 1 if used else 100))
        cnvpr.set("name", name)
        for ext in cnvpr.findall(qn("a:extLst")):   # drop layout's creationId GUID
            cnvpr.remove(ext)
        slide.shapes._spTree.append(el)
        shape = next(sh for sh in slide.shapes if sh.name == name)
    shape.left, shape.top, shape.width, shape.height = left, top, width, height
    tf = shape.text_frame
    tf.word_wrap = True
    try:
        tf.auto_size = None        # no spAutoFit - keep the box inert
    except Exception:
        pass
    tf.clear()
    para = tf.paragraphs[0]
    para.level = 0
    run = para.add_run()
    run.text = text
    run.font.size = Pt(size_pt)
    run.font.bold = False
    run.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
    return shape


# Canonical name of the slides 8/9/10 chart-image shape on a hand-made deck.
CHART_PICTURE_NAME = "Picture 2"


def find_chart_picture(slide):
    """Return the large chart-image Picture on a slides-8/9/10-style slide.

    Historically this shape was looked up by the literal name "Picture 2",
    which only exists on hand-made decks. python-pptx's add_picture()
    auto-assigns names ("Picture 13", "Picture 11", ...), so once a deck has
    itself been produced by this pipeline a name-only lookup breaks and the
    build stops being idempotent month-over-month. First month to hit this:
    August 2026, the first ever built on a pipeline-generated base deck.

    Resolution order:
      1. a Picture literally named "Picture 2" (unchanged behaviour on the
         hand-made May/June self-test bases), else
      2. the largest-area Picture on the slide - the chart image dwarfs the
         only other pictures present (the small Oxford crest / header logo).

    Returns None only if the slide carries no Picture shapes at all.
    """
    pics = [sh for sh in slide.shapes if sh.shape_type == 13]
    if not pics:
        return None
    for sh in pics:
        if sh.name == CHART_PICTURE_NAME:
            return sh
    return max(pics, key=lambda sh: (sh.width or 0) * (sh.height or 0))


def fmt_delta(cur, prev):
    d = cur - prev
    pct = f" ({d/prev*100:+.0f}%)" if prev else ""
    return f"{d:+d}{pct}"


def plain_delta(d):
    """Signed integer delta with no percentage - matches the real deck's
    style for slide 2/3/10 MoM columns and slide 10's Variance row (as
    opposed to fmt_delta's '+N (+P%)' style used on slides 4/10's
    Created/Completed rows). Zero renders as '0', not '+0' - confirmed
    against the real June deck (slide 2's DSE row, slide 3's Next Day row)."""
    return "0" if d == 0 else f"{d:+d}"


def set_pie_chart(shape, categories, value_map, series_name):
    """Replace a native pptx pie chart's series data in place via
    chart.replace_data() - the previously-unattempted capability (see
    memory/kpi-presentation-assembly-gap.md). Keeps the existing category
    order/labels the chart already uses so formatting/colours carry over;
    only the underlying numbers (and the generic default 'Sales' series
    name - proof-of-non-touch, per Lauren's byte-level verification) change.
    Values are written at full float precision; PowerPoint's own data-label
    number format on the chart (untouched here) governs display rounding,
    same as it always has."""
    cd = CategoryChartData()
    cd.categories = categories
    cd.add_series(series_name, [value_map.get(c) for c in categories])
    shape.chart.replace_data(cd)


def populate_deck(base_deck_path, pxd, hs_current, hs_prev, month_label, chart_dir, out_path, year, month, notes=None):
    """Assemble a full month's deck from a base (prior month's finished
    deck, already carrying the layout fixes) plus extracted figures.

    year/month are the current reporting month (e.g. 2026, 7 for July) -
    needed to relabel every table's month-column headers (e.g. slide 4's
    'Jun 25 / May 26 / Jun 26'), which stay stale otherwise since they're
    plain template text carried forward from whichever month the base deck
    was last for, not derived from data like the cells beneath them.

    notes: optional {1-based slide number: text} from load_month_notes().
    When given, each listed slide's speaker notes are replaced. When None,
    notes are left exactly as the base deck carried them - callers (i.e.
    build_month) are responsible for deciding whether that is acceptable."""
    prs = Presentation(base_deck_path)
    m = pxd["slide4_months"]  # 15-month label list, ends at current month
    cur, prev_i, yr_i = -1, -2, -13  # current, previous month, 12 months back +1

    py, pm = prev_ym(year, month)
    yy, ym = (year - 1, month)
    cur_lbl, prev_lbl, yr_lbl = short_label(year, month), short_label(py, pm), short_label(yy, ym)

    # Slide 1
    for shape in prs.slides[0].shapes:
        if shape.name == "Subtitle 2":
            set_cell_like(shape, f"{month_label.upper()} KPI STATISTICS | ")

    # Header month-column relabelling - every table below has its own body
    # values recomputed from this month's data, but the header row text
    # ('Jun 25', 'May 26', 'Jun 26' etc.) is separate static text that must
    # be updated in step or a July deck would show correct numbers under
    # wrong month labels. (slide_index, table_name): {col_index: label}
    header_updates = {
        (1, "Table 5"): {1: prev_lbl, 2: cur_lbl},                    # slide 2
        (2, "Table 5"): {1: prev_lbl, 3: cur_lbl},                    # slide 3
        (3, "Table 5"): {1: yr_lbl, 2: prev_lbl, 3: cur_lbl},         # slide 4
        (5, "Table 5"): {4: prev_lbl, 5: cur_lbl},                    # slide 6
        (6, "Table 5"): {4: prev_lbl, 5: cur_lbl},                    # slide 7
        (9, "Table 3"): {1: yr_lbl, 2: prev_lbl, 3: cur_lbl},         # slide 10
    }
    for (slide_i, table_name), cols in header_updates.items():
        t = find_table(prs.slides[slide_i], table_name)
        for ci, label in cols.items():
            set_cell(t.rows[0].cells[ci], label)
    # Slides 8/9's Table 11/10 use a 3-column month row at row index 2, no
    # other header text to preserve on that row.
    for slide_i, table_name in ((7, "Table 11"), (8, "Table 10")):
        t = find_table(prs.slides[slide_i], table_name)
        for ci, label in ((0, yr_lbl), (1, prev_lbl), (2, cur_lbl)):
            set_cell(t.rows[2].cells[ci], label)

    # Slide 2: H&S system volumes - Table 5 (counts + MoM) and native pie
    # chart (% share). Both previously pass-through (see memory/
    # kpi-presentation-assembly-gap.md) - genuinely written here.
    def hs_lookup(hs_dict, short):
        for full, (count, pct) in hs_dict.get("slide2_volumes", {}).items():
            if short in full:
                return count
        return 0

    t2 = find_table(prs.slides[1], "Table 5")
    s2_order = ["Cority", "Odyssey", "IRIS", "DSE"]
    for ri, short in enumerate(s2_order, start=1):
        c = hs_lookup(hs_current, short)
        p = hs_lookup(hs_prev, short)
        set_cell(t2.rows[ri].cells[1], str(p))
        set_cell(t2.rows[ri].cells[2], str(c))
        set_cell(t2.rows[ri].cells[3], plain_delta(c - p))
    s2_tot_c = sum(hs_lookup(hs_current, s) for s in s2_order)
    s2_tot_p = sum(hs_lookup(hs_prev, s) for s in s2_order)
    set_cell(t2.rows[5].cells[1], str(s2_tot_p))
    set_cell(t2.rows[5].cells[2], str(s2_tot_c))
    set_cell(t2.rows[5].cells[3], fmt_delta(s2_tot_c, s2_tot_p))

    slide2_pie = {}
    for short in s2_order:
        c = hs_lookup(hs_current, short)
        slide2_pie[short] = round(c / s2_tot_c * 100, 2) if c and s2_tot_c else None
    set_pie_chart(
        next(sh for sh in prs.slides[1].shapes if sh.has_chart),
        ["Cority", "Odyssey", "IRIS", "DSE"], slide2_pie, "H&S System Volume %",
    )

    # Slide 3: H&S time-to-resolve bands - Table 5 (count+pct, both months,
    # MoM) and native pie chart (current month %).
    t3 = find_table(prs.slides[2], "Table 5")
    s3_rows = [("Same Day", 1), ("Next Day", 2), ("3 - 5 days", 3), ("6+ days", 4)]
    s3_bands_c = hs_current.get("slide3_bands", {})
    s3_bands_p = hs_prev.get("slide3_bands", {})
    s3_tot_c = sum(v[0] for v in s3_bands_c.values())
    s3_tot_p = sum(v[0] for v in s3_bands_p.values())
    for label, ri in s3_rows:
        pc, ppct = s3_bands_p.get(label, (0, "0.00%"))
        cc, cpct = s3_bands_c.get(label, (0, "0.00%"))
        set_cell(t3.rows[ri].cells[1], str(pc))
        set_cell(t3.rows[ri].cells[2], ppct)
        set_cell(t3.rows[ri].cells[3], str(cc))
        set_cell(t3.rows[ri].cells[4], cpct)
        set_cell(t3.rows[ri].cells[5], plain_delta(cc - pc))
    set_cell(t3.rows[5].cells[1], str(s3_tot_p))
    set_cell(t3.rows[5].cells[3], str(s3_tot_c))
    set_cell(t3.rows[5].cells[5], plain_delta(s3_tot_c - s3_tot_p))

    slide3_pie = {label: (s3_bands_c.get(label, (0, 0))[0] / s3_tot_c * 100 if s3_tot_c else 0)
                  for label, _ in s3_rows}
    set_pie_chart(
        next(sh for sh in prs.slides[2].shapes if sh.has_chart),
        ["Same Day", "6+ Days", "Next Day", "3-5 Day"],
        {"Same Day": slide3_pie["Same Day"], "6+ Days": slide3_pie["6+ days"],
         "Next Day": slide3_pie["Next Day"], "3-5 Day": slide3_pie["3 - 5 days"]},
        "H&S Time to Resolve %",
    )

    # Slide 4: PXD categories, Jun25/May26/Jun26-equivalent + MoM/YoY
    t4 = find_table(prs.slides[3], "Table 5")
    order = ["Service Request", "Incident – Other", "HR Self Service", "Change"]
    for ri, cat in enumerate(order, start=1):
        vals = pxd["slide4_categories"][cat]
        c, p, y = vals[cur], vals[prev_i], vals[yr_i]
        row = [cat, str(y), str(p), str(c), fmt_delta(c, p), fmt_delta(c, y)]
        for ci, text in enumerate(row):
            set_cell(t4.rows[ri].cells[ci], text)
    tot_c = sum(pxd["slide4_categories"][k][cur] for k in order)
    tot_p = sum(pxd["slide4_categories"][k][prev_i] for k in order)
    tot_y = sum(pxd["slide4_categories"][k][yr_i] for k in order)
    tot_row = ["Total", str(tot_y), str(tot_p), str(tot_c), fmt_delta(tot_c, tot_p), fmt_delta(tot_c, tot_y)]
    for ci, text in enumerate(tot_row):
        set_cell(t4.rows[5].cells[ci], text)

    slide4_pie = {cat.replace("Incident – Other", "Incident - Other"):
                  round(pxd["slide4_categories"][cat][cur] / tot_c * 100, 2) if tot_c else 0
                  for cat in order}
    set_pie_chart(
        next(sh for sh in prs.slides[3].shapes if sh.has_chart),
        ["Service Request", "Change", "HR Self Service", "Incident - Other"],
        slide4_pie, "PXD Task Category %",
    )

    # Slide 5: Table 4 (incident - other) + Table 6 (service request)
    slide5 = prs.slides[4]
    io = pxd["slide5_incident_other"]
    t4_5 = find_table(slide5, "Table 4")
    # ADR-0001: 9 named rows + "Other" (row 10, formerly "Interfaces") + Total.
    # `io` is already keyed by display label with source-equivalent
    # percentages (pct_str), so no per-row relabelling / recompute here.
    io_order = [display_label for display_label, _ in INCIDENT_OTHER_NAMED] + ["Other"]
    for ri, label in enumerate(io_order, start=1):
        count, pct = io.get(label, (0, "0.00%"))
        set_cell(t4_5.rows[ri].cells[0], label)
        set_cell(t4_5.rows[ri].cells[1], str(count))
        set_cell(t4_5.rows[ri].cells[2], pct)
    set_cell(t4_5.rows[11].cells[1], str(pxd["slide5_incident_other_total"]))
    set_cell(t4_5.rows[11].cells[2], "100%")   # percentage base is now a visible row

    sr = pxd["slide5_service_request"]
    t6_5 = find_table(slide5, "Table 6")
    sr_order = ["Manager Self Service", "WG - HR Self-Service", "Add New Shift Type",
                "HR Systems User Access", "People Data Dashboards", "Enhancement & Changes"]
    for ri, cat in enumerate(sr_order, start=1):
        count, pct = sr.get(cat, (0, "0.00%"))
        set_cell(t6_5.rows[ri].cells[0], cat)
        set_cell(t6_5.rows[ri].cells[1], str(count))
        set_cell(t6_5.rows[ri].cells[2], pct)

    # Known fix 1 (Kevin, 2 Aug 2026, memory/kpi-presentation-layout-fixes.md):
    # Table 6's raw build includes a blank ['', '', ''] row before Total -
    # remove it, then reposition so its bottom lines up with Table 4's. Must
    # run BEFORE writing the Total row below - a real bug caught during this
    # extension's own self-test: the original code wrote the total to a
    # hardcoded row index (7) *before* this removal ran, which is only the
    # Total row once the blank row is gone. With the base deck already
    # carrying the un-fixed blank row forward (the real live decks never
    # actually had Kevin's manual fix applied - only a separate rebuild-TEST
    # file did), writing first and removing second silently planted the
    # total in the blank spacer row instead of the Total row, leaving the
    # real Total row stale. Folded into populate_deck itself now, not a
    # separate manual step, and ordered correctly.
    blank_ri = next(
        (ri for ri, row in enumerate(t6_5.rows) if all(not c.text.strip() for c in row.cells)),
        None,
    )
    if blank_ri is not None:
        tbl_el = t6_5._tbl
        tr = tbl_el.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/main}tr")[blank_ri]
        tbl_el.remove(tr)
    for shape in slide5.shapes:
        if shape.has_table and shape.name == "Table 6":
            shape.top, shape.left = 6563363, 2239340
            break

    set_cell(t6_5.rows[len(t6_5.rows) - 1].cells[1], str(sum(v[0] for v in sr.values())))

    # PART B (ADR-0001 section 4): run-time scope notes explaining why the
    # three "Incident - Other" figures on Slides 4, 5 and 7 legitimately
    # differ (registry D1 - three different Ivanti queries). Michael
    # O'Sullivan asked for this on-slide. Hosted as an INHERITED placeholder
    # (see _upsert_scope_note) so PowerPoint keeps them across an open/close;
    # the earlier free add_textbox version was silently dropped. No table /
    # row change. Idempotent: found by name and updated in place on re-runs.
    n_io = pxd["slide5_incident_other_total"]
    s5_tbl = _table_shape(slide5, "Table 4")
    _upsert_scope_note(
        slide5, "IncidentOtherScopeCaption",
        (f"Incident – Other (this table): non-self-service Incident tasks "
         f"completed last month, by service category — total {n_io}. "
         f"Slide 4's Incident – Other trend groups by HRIS parent ticket "
         f"type over a rolling 15-month window and will not match this total. "
         f"Slide 7 breaks down this same {n_io}-task population by time to "
         f"complete."),
        left=s5_tbl.left,
        top=s5_tbl.top + s5_tbl.height + 80000,
        width=s5_tbl.width,
        height=1300000,
    )
    s4_tbl = _table_shape(prs.slides[3], "Table 5")
    _upsert_scope_note(
        prs.slides[3], "IncidentOtherPointer",
        ("Incident – Other = tasks completed by HRIS parent ticket type "
         "(rolling 15-month window). Slide 5 shows last month's service-"
         "category breakdown."),
        left=s4_tbl.left,
        top=s4_tbl.top + s4_tbl.height + 80000,
        width=s4_tbl.width,
        height=760000,
    )

    # Slides 6/7: SR/OI time-to-complete bands. Table 5 is a combined
    # KPI-threshold summary (SAME OR NEXT DAY / LESS THAN 5 DAYS, both
    # months); chart is a current-month band-share pie. Both sourced from
    # the same rolling sheet already parsed into pxd - PXD data is fully
    # self-contained per month (unlike H&S), so no cross-folder read needed.
    #
    # NOTE on rounding (flagged, not silently resolved - see HANDOVER.md):
    # the real June deck's two combined percentages don't reconcile to a
    # single arithmetic rule to the last hundredth-of-a-percent against the
    # underlying counts - e.g. slide 7's Jun26 "LESS THAN 5 DAYS" is 87.02%
    # in the real deck, but exact count division (67/77) gives 87.01%
    # unambiguously (no rounding-boundary ambiguity in that division). This
    # implementation always uses exact count/total division (reproducible,
    # correct to the source data), which matches the real deck on 6 of 8
    # spot-checked cells and differs by 0.01 on 2 of them. Not invented or
    # guessed - it's the mathematically defensible value from the source
    # counts; flagged to Kevin as an open, sub-hundredth-of-a-percent
    # methodology question rather than silently claimed as byte-identical.
    for slide_i, table_name, sheet_key, pie_cats in (
        (5, "Table 5", "slide6_bands", ["Same Day", "6+ Days", "3-5 Days", "Next Day"]),
        (6, "Table 5", "slide7_bands", ["Same Day", "6+ Days", "3-5 Days", "Next Day"]),
    ):
        bands = pxd[sheet_key]  # {label: [15 monthly '123 (45.67%)' strings]}

        def band_counts(idx):
            out = {}
            for label, series in bands.items():
                count, _ = parse_count_pct(series[idx])
                out[label] = count
            return out

        cur_counts, prev_counts = band_counts(cur), band_counts(prev_i)
        cur_total, prev_total = sum(cur_counts.values()), sum(prev_counts.values())

        def combined_pct(counts, total, labels):
            # HARDENING FIX 5 (7 Sep 2026): use pct2 (Decimal ROUND_HALF_UP),
            # the SAME helper validate_deck() checks against - so the emitter
            # and the gate can never disagree on rounding direction next
            # month. (Previously round(), which is half-to-even + float-repr
            # sensitive and would risk a false gate failure on a .xx5 cell.)
            # Verified no-op for Jun/Jul/Aug: none of these cells sit on a
            # half-cent boundary.
            n = sum(counts.get(l, 0) for l in labels)
            return pct2(n, total)

        same_next = ["Same Day", "Next Day"]
        less_5 = ["Same Day", "Next Day", "3 - 5 days"]
        t = find_table(prs.slides[slide_i], table_name)
        set_cell(t.rows[1].cells[4], f"{combined_pct(prev_counts, prev_total, same_next):.2f}%")
        set_cell(t.rows[1].cells[5], f"{combined_pct(cur_counts, cur_total, same_next):.2f}%")
        set_cell(t.rows[2].cells[4], f"{combined_pct(prev_counts, prev_total, less_5):.2f}%")
        set_cell(t.rows[2].cells[5], f"{combined_pct(cur_counts, cur_total, less_5):.2f}%")

        pie_map = {
            "Same Day": float(pct2(cur_counts.get("Same Day", 0), cur_total)),
            "6+ Days": float(pct2(cur_counts.get("6+ days", 0), cur_total)),
            "3-5 Days": float(pct2(cur_counts.get("3 - 5 days", 0), cur_total)),
            "Next Day": float(pct2(cur_counts.get("Next Day", 0), cur_total)),
        }
        set_pie_chart(
            next(sh for sh in prs.slides[slide_i].shapes if sh.has_chart),
            pie_cats, pie_map, f"{table_name} Band %",
        )

    # Slides 8/9/10: KPI-threshold small tables (proven table-write pattern,
    # same as slide 4/5) plus the chart-image swap (proven picture-swap
    # mechanism from build_full_poc.py, SHA1-verified against the real deck
    # per memory/kpi-presentation-assembly-gap.md) - now generated fresh
    # from *this* month's own data instead of only ever having been run
    # against June's own pre-known figures.
    os.makedirs(chart_dir, exist_ok=True)

    # HARDENING FIX 4 (7 Sep 2026): the exact value arrays handed to
    # make_trend_chart / make_combo_chart are recorded on the Presentation so
    # validate_deck() can assert  source series == chart array == table cell
    # for Slides 8/9/10 (the chart itself is a matplotlib PNG that cannot be
    # read back). CHAIN: `acc`/`comp` here ARE `pxd["slide8_values"]` /
    # `pxd["slide9_values"]` (the source series); the same list object is
    # both drawn by make_trend_chart AND sliced [yr/prev/cur] into the KPI
    # table; likewise `created`/`completed` are `pxd["slide10_created"]` /
    # `pxd["slide10_completed"]` and feed both make_combo_chart and Table 3.
    chart_series = {}

    t8 = find_table(prs.slides[7], "Table 11")
    acc = pxd["slide8_values"]
    for ci, idx in ((0, yr_i), (1, prev_i), (2, cur)):
        set_cell(t8.rows[3].cells[ci], f"{acc[idx]:.1f}")
    img8 = os.path.join(chart_dir, "slide8_chart.png")
    chart_series["slide8_values"] = list(acc)
    make_trend_chart(pxd["slide8_months"], chart_series["slide8_values"], sum(pxd["slide10_created"]), img8, y_step=0.1)

    t9 = find_table(prs.slides[8], "Table 10")
    comp = pxd["slide9_values"]
    for ci, idx in ((0, yr_i), (1, prev_i), (2, cur)):
        set_cell(t9.rows[3].cells[ci], f"{comp[idx]:.1f}")
    img9 = os.path.join(chart_dir, "slide9_chart.png")
    chart_series["slide9_values"] = list(comp)
    make_trend_chart(pxd["slide9_months"], chart_series["slide9_values"], sum(pxd["slide9_completed_tasks"]), img9, y_step=0.5)

    t10 = find_table(prs.slides[9], "Table 3")
    created, completed = pxd["slide10_created"], pxd["slide10_completed"]
    chart_series["slide10_created"] = list(created)
    chart_series["slide10_completed"] = list(completed)
    for ci, idx in ((1, yr_i), (2, prev_i), (3, cur)):
        set_cell(t10.rows[1].cells[ci], str(created[idx]))
        set_cell(t10.rows[2].cells[ci], str(completed[idx]))
        set_cell(t10.rows[3].cells[ci], plain_delta(completed[idx] - created[idx]))
    set_cell(t10.rows[1].cells[4], fmt_delta(created[cur], created[prev_i]))
    set_cell(t10.rows[1].cells[5], fmt_delta(created[cur], created[yr_i]))
    set_cell(t10.rows[2].cells[4], fmt_delta(completed[cur], completed[prev_i]))
    set_cell(t10.rows[2].cells[5], fmt_delta(completed[cur], completed[yr_i]))
    var_cur = completed[cur] - created[cur]
    var_prev = completed[prev_i] - created[prev_i]
    var_yr = completed[yr_i] - created[yr_i]
    set_cell(t10.rows[3].cells[4], plain_delta(var_cur - var_prev))
    set_cell(t10.rows[3].cells[5], plain_delta(var_cur - var_yr))
    img10 = os.path.join(chart_dir, "slide10_chart.png")
    make_combo_chart(pxd["slide10_months"], chart_series["slide10_created"],
                     chart_series["slide10_completed"], img10)
    prs._kpi_chart_series = chart_series   # read by validate_deck (FIX 4)

    # Proven picture-swap positions, captured from Kevin's manual layout
    # pass on 2 Aug 2026 (build_full_poc.py, SHA1-verified against the real
    # deck) - reused verbatim, not re-derived.
    picture_swaps = {
        7: (img8, 5593036, 10726620),   # slide 8
        8: (img9, 5532711, 10823848),   # slide 9
        9: (img10, 4924159, 10751840),  # slide 10
    }
    for si, (img_path, new_top, new_left) in picture_swaps.items():
        slide = prs.slides[si]
        target = find_chart_picture(slide)
        if target is None:
            raise RuntimeError(
                f"slide {si + 1}: no chart picture found - layout may have changed"
            )
        width, height = target.width, target.height
        sp = target._element
        sp.getparent().remove(sp)
        new_pic = slide.shapes.add_picture(img_path, new_left, new_top, width, height)
        # Normalise the name so the swap stays idempotent month-over-month:
        # next month's build uses this deck as its base and must be able to
        # find this shape again. Without this, add_picture() would leave it
        # auto-named ("Picture 13" etc) and the following month would fall
        # back to the largest-area heuristic instead of a clean name match.
        new_pic.name = CHART_PICTURE_NAME

    # PART D (7 Sep 2026): speaker notes. Capture the BASE deck's per-slide
    # notes BEFORE any are overwritten, so validate_deck() can tell "updated
    # for this month" from "still carrying last time's text" - that
    # distinction is the entire point of this fix (see NOTES_DIR comment).
    prs._kpi_base_notes = {
        si: (sl.notes_slide.notes_text_frame.text if sl.has_notes_slide else "")
        for si, sl in enumerate(prs.slides)
    }
    if notes:
        for slide_num, text in notes.items():
            si = slide_num - 1
            if 0 <= si < len(prs.slides):
                prs.slides[si].notes_slide.notes_text_frame.text = text
        prs._kpi_notes_written = set(notes.keys())
    else:
        prs._kpi_notes_written = set()

    # NOTE: no longer saves here. build_month() runs validate_deck(prs, ...)
    # against this in-memory Presentation and only then writes it to disk, so
    # a deck that fails an internal or cross-slide check is never left at
    # out_path (HANDOVER Part C).
    return prs


# =====================================================================
# HARDENED SELF-TEST GATE (HANDOVER Part C)
# =====================================================================
# The pre-existing gate diffed a freshly built month against a hand-made
# reference deck for the SAME month. That cannot catch an error that is
# present in both (the reference June deck carried the very Slide 5 Table 4
# arithmetic defect this change fixes, and the gate still said ALL PASS).
# validate_deck() checks the freshly built month against itself and against
# the cross-slide reconciliation registry, independently of any reference
# deck. It is BLOCKING: build_month() calls it before saving and writes no
# deck on failure.

class DeckValidationError(Exception):
    """Raised by validate_deck() when the freshly built deck fails an
    internal-consistency or cross-slide reconciliation check."""


# Percentage-column-sum tolerance. Worst case accumulated half-up rounding
# error is 0.005 pp per displayed row; the widest table here has 10 category
# rows (Slide 5 Table 4) -> <=0.05 pp, so 0.10 pp is a safe ceiling that
# still catches a wrong percentage base or a dropped row (whole-point shift).
PCT_SUM_TOL = Decimal("0.10")
# Single-cell percentage tolerance (spec: abs diff <= 0.001).
PCT_CELL_TOL = Decimal("0.001")

# Cross-slide reconciliation registry, encoded from
# docs/reference/incident-other-reconciliation.md. Kept as data so the
# "reason" text ships with the failure message and so an un-registered
# repeated metric that mismatches can be named as such.
RECONCILIATION_MUST_EQUAL = [
    ("R1", "Slide 5 Table 4 Total == Slide 7 current-month band-count total"),
    ("R2", "Slide 5 Table 6 Total == Slide 4 Table 5 'Service Request' (cur) "
           "== Service-Request source total"),
    ("R-cur", "Slide 4 Table 5 'Total' (cur) == 'Tasks Completed by HRIS "
              "Analy3' Completed Tasks for the current month"),
]
RECONCILIATION_DIFFER_BY_DESIGN = [
    ("D1", "Slide 4 'Incident - Other' (cur) vs Slide 5 Table 4 Total vs "
           "Slide 7 band total - different Ivanti queries (Parent Ticket "
           "Type HRIS / rolling 15-month created window vs Service Category, "
           "last-month completed). Captions (Part B) are the resolution."),
    ("D2", "Slide 4 Table 5 'Total' (cur) vs Slide 10 Table 3 'Completed' "
           "(cur) - Slide 10 'Completed' is the broader "
           "Completed/Cancelled/Rejected disposition set."),
    ("D3", "Slide 4 Table 5 'Total' (yr/prev) vs Analy3 for those months - "
           "export-timing / late reclassification; +/-1 tolerated on "
           "historical columns, only the current month is asserted exact."),
    ("D4", "Slide 7 Table 5 'LESS THAN 5 DAYS' (cur) vs exact count "
           "division - documented sub-0.01 pp rounding-methodology "
           "ambiguity in the source; <=0.01 pp permitted on this cell only."),
]

# ---- Structural manifest (HARDENING FIX 1, 7 Sep 2026) --------------------
# The gate's data checks are per-table/per-metric and enumerated. This
# manifest + the structural sweep in validate_deck() turn a *structural*
# change (a new slide, table, Total row, caption, or native chart) into a
# hard build failure, so the gate cannot silently under-cover a deck that
# has grown. Keyed by 0-based slide index. If the deck layout legitimately
# changes, update this manifest AND add the matching data checks.
EXPECTED_SLIDE_COUNT = 11
EXPECTED_TABLES = {           # slide index -> set of table shape names
    1: {"Table 5"}, 2: {"Table 5"}, 3: {"Table 5"},
    4: {"Table 4", "Table 6"}, 5: {"Table 5"}, 6: {"Table 5"},
    7: {"Table 11"}, 8: {"Table 10"}, 9: {"Table 3"},
}
EXPECTED_NATIVE_CHART_SLIDES = {1, 2, 3, 5, 6}   # slides 8-10 use PNG images, not native charts
# Scope-note check. Was an absolute "a shape named X exists" check; that is
# too brittle now that PowerPoint has been seen to drop / re-home the shape.
# The gate now checks that the *explanatory text* is present SOMEWHERE on the
# slide (any shape) via these content signatures - a rename or a move is
# tolerated, the text being gone entirely is a hard failure (it carries the
# Slide 4-vs-5 reconciliation explanation Michael O'Sullivan asked for).
# Expected shape names are still checked, but only as a non-blocking advisory.
EXPECTED_CAPTION_NAMES = {3: "IncidentOtherPointer", 4: "IncidentOtherScopeCaption"}
SCOPE_NOTE_SIGNATURES = {
    3: ("HRIS parent ticket type", "Slide 5 shows"),
    4: ("by service category", "Slide 7 breaks down this same"),
}
# Slides that must carry month-specific speaker notes (PART D, 7 Sep 2026) -
# same set as NOTES_REQUIRED_SLIDES, aliased here so it lives with the rest
# of the structural manifest. Slide 1 (title) and Slide 11 (thank you) are
# excluded on purpose - they never carry data-specific notes.
EXPECTED_NOTES_SLIDES = NOTES_REQUIRED_SLIDES
# (slide index, table name) pairs whose "Total"-labelled row is covered by an
# explicit named check above. The structural sweep fails the build if it
# finds a Total-labelled row in a table NOT listed here.
COVERED_TOTAL_ROW_TABLES = {
    (1, "Table 5"), (2, "Table 5"), (3, "Table 5"),
    (4, "Table 4"), (4, "Table 6"),
}

_INT_RE = re.compile(r"^\d+$")
_PCT_RE = re.compile(r"^\d+(?:\.\d+)?%$")


def _dec2(x):
    """Round any float/int to 2 dp as a Decimal, ROUND_HALF_UP (same
    convention as pct2 - keeps chart-vs-table comparisons consistent)."""
    return Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _cint(table, ri, ci):
    return int(table.rows[ri].cells[ci].text.strip())


def _cpct(table, ri, ci):
    return Decimal(table.rows[ri].cells[ci].text.strip().rstrip("%").strip())


def _ctxt(table, ri, ci):
    return table.rows[ri].cells[ci].text.strip()


def _band_counts(series_map, idx):
    return {lab: parse_count_pct(s[idx])[0] for lab, s in series_map.items()}


def validate_deck(prs, pxd, hs_current, hs_prev, year, month, allow_no_chart_series=False, notes_required=True):
    """BLOCKING gate. Runs against the freshly built Presentation `prs`
    (not a reference deck) plus the same extracted inputs populate_deck
    used. Collects every failure, prints them, and raises
    DeckValidationError if there is at least one. Checks:
      * FIX 1 - structural manifest (slide / table / native-chart / caption
        inventory) + a sweep of every table for a "Total"-labelled row so a
        structural change forces a gate update
      * every Total row: category rows sum to the displayed Total (exact int)
      * FIX 2 - every displayed category count traces to its specific source
        figure (Slide 4 vs pxd; Slide 5 Table 4 vs the raw source category
        map) so a coherently-wrong allocation cannot pass
      * every single-category % cell == count / displayed Total (<=0.001)
      * every % column sums to 100 (<=0.10 pp)
      * FIX 3 - Slide 2 / Slide 3 counts == the H&S Word-doc source figures
      * combined-band cells (Slides 6 & 7) exact except registered D4
      * delta cells arithmetically correct (MoM / YoY / Variance)
      * pie chart series values == the matching table cell values
      * FIX 4 - Slides 8/9/10: source series == the array handed to
        make_trend_chart / make_combo_chart == the table cells
      * cross-slide registry: R1, R2, R-cur exact; D1-D4 registered as
        differ-by-design; any un-registered repeated metric that
        mismatches -> fail.
      * PART D (7 Sep 2026) - speaker notes on Slides 2-10: not empty, not
        byte-identical to the base deck's notes for that slide (i.e.
        genuinely updated), and the current month's name appears somewhere
        across them. LIMITS (stated here, not just in a comment further
        down): this can only prove the notes were CHANGED and reference the
        right month - it cannot verify the prose is factually correct.
        Content correctness stays Lauren's judgement call, same as
        everywhere else in this pipeline; a mandatory Codex numeric-accuracy
        pass on the notes is a separate, human-run step (see KPI_RUN_SOP.md).
        notes_required=False turns this into a soft, non-blocking note (for
        self-test coverage of a month whose notes aren't drafted yet); real
        builds (build_month) never set it False.
    """
    cur, prev_i, yr_i = -1, -2, -13
    failures = []

    def chk(cond, msg):
        if not cond:
            failures.append(msg)

    def check_pie(slide_i, exp_map, label):
        """exp_map: {chart_category_label: (count, denominator)}."""
        chart = next(sh.chart for sh in prs.slides[slide_i].shapes if sh.has_chart)
        plot = chart.plots[0]
        cats = list(plot.categories)
        vals = list(plot.series[0].values)
        series_sum = sum(float(v or 0) for v in vals)
        if any(d for _, d in exp_map.values()):
            chk(abs(Decimal(str(series_sum)) - 100) <= PCT_SUM_TOL,
                f"{label} pie: series values sum to {series_sum:.4f}, not 100 "
                f"(tol {PCT_SUM_TOL} pp)")
        seen = set()
        for cat, val in zip(cats, vals):
            if cat not in exp_map:
                continue
            seen.add(cat)
            n, d = exp_map[cat]
            want = pct2(n, d)
            got = _dec2(val or 0)
            chk(abs(got - want) <= PCT_CELL_TOL,
                f"{label} pie {cat!r}: chart shows {got}, table-derived value "
                f"is {want} (count {n}/{d})")
        missing = set(exp_map) - seen
        chk(not missing,
            f"{label} pie: expected categories not found on the chart: {sorted(missing)}")

    # ================= FIX 1: STRUCTURAL MANIFEST + SWEEP =================
    # (a) the deck's inventory of slides / tables / native charts / captions
    #     must match EXPECTED_* exactly - any structural change forces this
    #     manifest and the matching data checks to be updated.
    chk(len(prs.slides) == EXPECTED_SLIDE_COUNT,
        f"STRUCTURE: deck has {len(prs.slides)} slides, manifest expects {EXPECTED_SLIDE_COUNT}")
    actual_tables, actual_charts = {}, set()
    for si, sl in enumerate(prs.slides):
        names = {sh.name for sh in sl.shapes if sh.has_table}
        if names:
            actual_tables[si] = names
        if any(sh.has_chart for sh in sl.shapes):
            actual_charts.add(si)
    chk(actual_tables == EXPECTED_TABLES,
        f"STRUCTURE: table inventory changed. got {actual_tables}, expected {EXPECTED_TABLES} "
        f"- update EXPECTED_TABLES and add data checks for any new table.")
    chk(actual_charts == EXPECTED_NATIVE_CHART_SLIDES,
        f"STRUCTURE: native-chart slide set changed. got {sorted(actual_charts)}, "
        f"expected {sorted(EXPECTED_NATIVE_CHART_SLIDES)}.")

    # Scope notes (Slides 4 & 5): the EXPLANATORY TEXT must be present on the
    # slide (any shape) - a rename or a move is tolerated, the text being
    # gone entirely is a hard failure. PowerPoint has been seen to drop the
    # free-text-box form on open/close; the pipeline now hosts it as an
    # inherited placeholder, and this check no longer keys on the shape name.
    def _slide_text(sl):
        out = []
        for sh in sl.shapes:
            if sh.has_table:
                out += [c.text for r in sh.table.rows for c in r.cells]
            elif sh.has_text_frame:
                out.append(sh.text_frame.text)
        return "\n".join(out)
    for si, needles in SCOPE_NOTE_SIGNATURES.items():
        blob = _slide_text(prs.slides[si])
        missing = [n for n in needles if n not in blob]
        chk(not missing,
            f"STRUCTURE: Slide {si + 1} scope-note text is missing (no shape "
            f"contains {missing}). This is the Slide 4-vs-5 'Incident - Other' "
            f"reconciliation explanation Michael O'Sullivan asked for - it must "
            f"be present and durable on the delivered deck.")
        named = next((sh for sh in prs.slides[si].shapes
                      if sh.name == EXPECTED_CAPTION_NAMES[si]), None)
        if named is None:
            print(f"  validate_deck ADVISORY (non-blocking): Slide {si + 1} scope "
                  f"note is present but not in a shape named "
                  f"{EXPECTED_CAPTION_NAMES[si]!r} - it may have been re-homed "
                  f"(PowerPoint round-trip, or a manual edit). Text is intact.")
    missing_notes_slides = {si for si in EXPECTED_NOTES_SLIDES if not prs.slides[si].has_notes_slide}
    chk(not missing_notes_slides,
        f"STRUCTURE: slide(s) {sorted(missing_notes_slides)} (1-based "
        f"{[s+1 for s in sorted(missing_notes_slides)]}) have no notes slide "
        f"at all - expected every Slide 2-10 to carry a notes slide.")
    missing_notes_slides = {si for si in EXPECTED_NOTES_SLIDES if not prs.slides[si].has_notes_slide}
    chk(not missing_notes_slides,
        f"STRUCTURE: slide(s) {sorted(missing_notes_slides)} (1-based "
        f"{[s+1 for s in sorted(missing_notes_slides)]}) have no notes slide "
        f"at all - expected every Slide 2-10 to carry a notes slide.")

    # (b) sweep EVERY table: any row whose first cell is "Total" must have its
    #     integer columns sum to that row and its percentage column (if any)
    #     sum to 100 - and that (slide, table) must be in COVERED_TOTAL_ROW_TABLES
    #     (i.e. it also has a hand-written check above). A Total-labelled row
    #     in an unlisted table fails the build.
    for si, sl in enumerate(prs.slides):
        for sh in sl.shapes:
            if not sh.has_table:
                continue
            tbl = sh.table
            rows = list(tbl.rows)
            tot_idx = next((ri for ri, rw in enumerate(rows)
                            if rw.cells and rw.cells[0].text.strip().lower() == "total"), None)
            if tot_idx is None:
                continue
            chk((si, sh.name) in COVERED_TOTAL_ROW_TABLES,
                f"STRUCTURE: Slide {si + 1} {sh.name!r} has a 'Total' row but is not in "
                f"COVERED_TOTAL_ROW_TABLES - add an explicit check and register it.")
            ncols = len(rows[0].cells)
            cat_idx = range(1, tot_idx)
            for ci in range(1, ncols):
                cat_txt = [rows[ri].cells[ci].text.strip() for ri in cat_idx]
                tot_txt = rows[tot_idx].cells[ci].text.strip()
                if cat_txt and all(_INT_RE.match(x) for x in cat_txt) and _INT_RE.match(tot_txt):
                    s = sum(int(x) for x in cat_txt)
                    chk(s == int(tot_txt),
                        f"SWEEP: Slide {si + 1} {sh.name!r} col {ci}: category rows sum {s} "
                        f"!= Total row {tot_txt}")
                elif cat_txt and all(_PCT_RE.match(x) for x in cat_txt):
                    s = sum(Decimal(x.rstrip('%')) for x in cat_txt)
                    chk(abs(s - 100) <= PCT_SUM_TOL,
                        f"SWEEP: Slide {si + 1} {sh.name!r} col {ci}: % column sums to {s}, not 100")
                    if tot_txt:
                        chk(tot_txt in ("100%", "100.00%"),
                            f"SWEEP: Slide {si + 1} {sh.name!r} col {ci} Total-row % cell is "
                            f"{tot_txt!r}, expected '100%'")

    # ---- Slide 2 Table 5: H&S system volumes ----------------------------
    t = find_table(prs.slides[1], "Table 5")
    s2_prev = [_cint(t, ri, 1) for ri in range(1, 5)]
    s2_cur = [_cint(t, ri, 2) for ri in range(1, 5)]
    s2_pt, s2_ct = _cint(t, 5, 1), _cint(t, 5, 2)
    chk(sum(s2_prev) == s2_pt, f"Slide 2 Table 5: prev rows sum {sum(s2_prev)} != Total {s2_pt}")
    chk(sum(s2_cur) == s2_ct, f"Slide 2 Table 5: cur rows sum {sum(s2_cur)} != Total {s2_ct}")
    for ri, pv, cv in zip(range(1, 5), s2_prev, s2_cur):
        chk(_ctxt(t, ri, 3) == plain_delta(cv - pv),
            f"Slide 2 Table 5 row {ri} MoM: {_ctxt(t, ri, 3)!r} != {plain_delta(cv - pv)!r}")
    chk(_ctxt(t, 5, 3) == fmt_delta(s2_ct, s2_pt),
        f"Slide 2 Table 5 Total MoM: {_ctxt(t, 5, 3)!r} != {fmt_delta(s2_ct, s2_pt)!r}")
    check_pie(1, {"Cority": (s2_cur[0], s2_ct), "Odyssey": (s2_cur[1], s2_ct),
                  "IRIS": (s2_cur[2], s2_ct), "DSE": (s2_cur[3], s2_ct)}, "Slide 2")

    # FIX 3: Slide 2 counts must equal the H&S Word-doc source figures
    # (hs_current / hs_prev), not merely be internally self-consistent.
    def _hs_vol(hs_dict, short):
        for full, (cnt, _pct) in hs_dict.get("slide2_volumes", {}).items():
            if short in full:
                return cnt
        return 0
    for ri, short in zip(range(1, 5), ["Cority", "Odyssey", "IRIS", "DSE"]):
        chk(_cint(t, ri, 1) == _hs_vol(hs_prev, short),
            f"FIX3 Slide 2 {short} prev: deck {_cint(t, ri, 1)} != H&S source {_hs_vol(hs_prev, short)}")
        chk(_cint(t, ri, 2) == _hs_vol(hs_current, short),
            f"FIX3 Slide 2 {short} cur: deck {_cint(t, ri, 2)} != H&S source {_hs_vol(hs_current, short)}")

    # ---- Slide 3 Table 5: H&S time to resolve --------------------------
    t = find_table(prs.slides[2], "Table 5")
    s3 = [("Same Day", 1), ("Next Day", 2), ("3 - 5 days", 3), ("6+ days", 4)]
    s3_prev = [_cint(t, ri, 1) for _, ri in s3]
    s3_cur = [_cint(t, ri, 3) for _, ri in s3]
    s3_pt, s3_ct = _cint(t, 5, 1), _cint(t, 5, 3)
    chk(sum(s3_prev) == s3_pt, f"Slide 3 Table 5: prev rows sum {sum(s3_prev)} != Total {s3_pt}")
    chk(sum(s3_cur) == s3_ct, f"Slide 3 Table 5: cur rows sum {sum(s3_cur)} != Total {s3_ct}")
    for (_, ri), pv, cv in zip(s3, s3_prev, s3_cur):
        chk(abs(_cpct(t, ri, 2) - pct2(pv, s3_pt)) <= PCT_CELL_TOL,
            f"Slide 3 Table 5 row {ri} prev %: {_cpct(t, ri, 2)} != {pct2(pv, s3_pt)}")
        chk(abs(_cpct(t, ri, 4) - pct2(cv, s3_ct)) <= PCT_CELL_TOL,
            f"Slide 3 Table 5 row {ri} cur %: {_cpct(t, ri, 4)} != {pct2(cv, s3_ct)}")
        chk(_ctxt(t, ri, 5) == plain_delta(cv - pv),
            f"Slide 3 Table 5 row {ri} MoM: {_ctxt(t, ri, 5)!r} != {plain_delta(cv - pv)!r}")
    chk(abs(sum(_cpct(t, ri, 2) for _, ri in s3) - 100) <= PCT_SUM_TOL,
        f"Slide 3 Table 5: prev % column sums to {sum(_cpct(t, ri, 2) for _, ri in s3)}, not 100")
    chk(abs(sum(_cpct(t, ri, 4) for _, ri in s3) - 100) <= PCT_SUM_TOL,
        f"Slide 3 Table 5: cur % column sums to {sum(_cpct(t, ri, 4) for _, ri in s3)}, not 100")
    chk(_ctxt(t, 5, 5) == plain_delta(s3_ct - s3_pt),
        f"Slide 3 Table 5 Total MoM: {_ctxt(t, 5, 5)!r} != {plain_delta(s3_ct - s3_pt)!r}")
    check_pie(2, {"Same Day": (s3_cur[0], s3_ct), "Next Day": (s3_cur[1], s3_ct),
                  "3-5 Day": (s3_cur[2], s3_ct), "6+ Days": (s3_cur[3], s3_ct)}, "Slide 3")

    # FIX 3: Slide 3 band counts must equal the H&S Word-doc source figures.
    s3b_cur = hs_current.get("slide3_bands", {})
    s3b_prev = hs_prev.get("slide3_bands", {})
    for (lab, ri) in s3:
        chk(_cint(t, ri, 1) == s3b_prev.get(lab, (0,))[0],
            f"FIX3 Slide 3 {lab!r} prev: deck {_cint(t, ri, 1)} != H&S source {s3b_prev.get(lab, (0,))[0]}")
        chk(_cint(t, ri, 3) == s3b_cur.get(lab, (0,))[0],
            f"FIX3 Slide 3 {lab!r} cur: deck {_cint(t, ri, 3)} != H&S source {s3b_cur.get(lab, (0,))[0]}")

    # ---- Slide 4 Table 5: PXD categories ------------------------------
    t = find_table(prs.slides[3], "Table 5")
    # deck row -> the pxd["slide4_categories"] key it must trace to.
    s4 = [("Service Request", 1), ("Incident – Other", 2), ("HR Self Service", 3), ("Change", 4)]
    s4_yr = [_cint(t, ri, 1) for _, ri in s4]
    s4_prev = [_cint(t, ri, 2) for _, ri in s4]
    s4_cur = [_cint(t, ri, 3) for _, ri in s4]
    s4_yt, s4_pt, s4_ct = _cint(t, 5, 1), _cint(t, 5, 2), _cint(t, 5, 3)
    chk(sum(s4_yr) == s4_yt, f"Slide 4 Table 5: yr rows sum {sum(s4_yr)} != Total {s4_yt}")
    chk(sum(s4_prev) == s4_pt, f"Slide 4 Table 5: prev rows sum {sum(s4_prev)} != Total {s4_pt}")
    chk(sum(s4_cur) == s4_ct, f"Slide 4 Table 5: cur rows sum {sum(s4_cur)} != Total {s4_ct}")
    # FIX 2: every displayed count must trace to its specific source figure
    # in pxd["slide4_categories"] (defends against two category rows swapped
    # while the Total / pie / deltas still self-reconcile).
    for (pxdkey, ri) in s4:
        src = pxd["slide4_categories"][pxdkey]
        for col, idx in ((1, yr_i), (2, prev_i), (3, cur)):
            chk(_cint(t, ri, col) == src[idx],
                f"FIX2 Slide 4 Table 5 {pxdkey!r} col {col}: deck {_cint(t, ri, col)} "
                f"!= source {src[idx]}")
    for (_, ri), yv, pv, cv in zip(s4, s4_yr, s4_prev, s4_cur):
        chk(_ctxt(t, ri, 4) == fmt_delta(cv, pv),
            f"Slide 4 Table 5 row {ri} MoM: {_ctxt(t, ri, 4)!r} != {fmt_delta(cv, pv)!r}")
        chk(_ctxt(t, ri, 5) == fmt_delta(cv, yv),
            f"Slide 4 Table 5 row {ri} YoY: {_ctxt(t, ri, 5)!r} != {fmt_delta(cv, yv)!r}")
    chk(_ctxt(t, 5, 4) == fmt_delta(s4_ct, s4_pt),
        f"Slide 4 Table 5 Total MoM: {_ctxt(t, 5, 4)!r} != {fmt_delta(s4_ct, s4_pt)!r}")
    chk(_ctxt(t, 5, 5) == fmt_delta(s4_ct, s4_yt),
        f"Slide 4 Table 5 Total YoY: {_ctxt(t, 5, 5)!r} != {fmt_delta(s4_ct, s4_yt)!r}")
    check_pie(3, {"Service Request": (s4_cur[0], s4_ct), "Incident - Other": (s4_cur[1], s4_ct),
                  "HR Self Service": (s4_cur[2], s4_ct), "Change": (s4_cur[3], s4_ct)}, "Slide 4")

    # ---- Slide 5 Table 4: Incident - Other (ADR-0001) ----------------
    t = find_table(prs.slides[4], "Table 4")
    io_counts = [_cint(t, ri, 1) for ri in range(1, 11)]
    io_total_cell = _cint(t, 11, 1)
    chk(sum(io_counts) == io_total_cell,
        f"Slide 5 Table 4: category rows sum {sum(io_counts)} != displayed Total {io_total_cell}")
    chk(io_total_cell == pxd["slide5_incident_other_total"],
        f"Slide 5 Table 4: displayed Total {io_total_cell} != source month total "
        f"{pxd['slide5_incident_other_total']}")
    # FIX 2: reconstruct the expected 10 counts straight from the raw source
    # category map (independent of pxd["slide5_incident_other"], which
    # populate_deck consumed) and check every displayed count against it -
    # so a swapped/misallocated category cannot pass just because the Total
    # and percentages still add up.
    src_counts = pxd["slide5_incident_other_source_counts"]
    io_total_src = pxd["slide5_incident_other_total"]
    exp_named = [src_counts.get(src_name, 0) for _disp, src_name in INCIDENT_OTHER_NAMED]
    exp_io = exp_named + [io_total_src - sum(exp_named)]      # + "Other"
    io_labels = [d for d, _ in INCIDENT_OTHER_NAMED] + ["Other"]
    for i, ri in enumerate(range(1, 11)):
        chk(_ctxt(t, ri, 0) == io_labels[i],
            f"FIX2 Slide 5 Table 4 row {ri} label: {_ctxt(t, ri, 0)!r} != {io_labels[i]!r}")
        chk(io_counts[i] == exp_io[i],
            f"FIX2 Slide 5 Table 4 {io_labels[i]!r}: deck {io_counts[i]} != source-derived {exp_io[i]}")
    for i, ri in enumerate(range(1, 11)):
        chk(abs(_cpct(t, ri, 2) - pct2(io_counts[i], io_total_cell)) <= PCT_CELL_TOL,
            f"Slide 5 Table 4 row {ri} %: {_cpct(t, ri, 2)} != {pct2(io_counts[i], io_total_cell)} "
            f"(count {io_counts[i]}/{io_total_cell})")
    io_pct_sum = sum(_cpct(t, ri, 2) for ri in range(1, 11))
    chk(abs(io_pct_sum - 100) <= PCT_SUM_TOL,
        f"Slide 5 Table 4: % column sums to {io_pct_sum}, not 100 (tol {PCT_SUM_TOL} pp)")
    chk(_ctxt(t, 11, 2) in ("100%", "100.00%"),
        f"Slide 5 Table 4 Total % cell is {_ctxt(t, 11, 2)!r}, expected '100%'")

    # ---- Slide 5 Table 6: Service Request breakdown -----------------
    t = find_table(prs.slides[4], "Table 6")
    last6 = len(t.rows) - 1
    sr_counts = [_cint(t, ri, 1) for ri in range(1, last6)]
    sr_total_cell = _cint(t, last6, 1)
    chk(sum(sr_counts) == sr_total_cell,
        f"Slide 5 Table 6: category rows sum {sum(sr_counts)} != displayed Total {sr_total_cell}")
    for i, ri in enumerate(range(1, last6)):
        chk(abs(_cpct(t, ri, 2) - pct2(sr_counts[i], sr_total_cell)) <= PCT_CELL_TOL,
            f"Slide 5 Table 6 row {ri} %: {_cpct(t, ri, 2)} != {pct2(sr_counts[i], sr_total_cell)}")
    sr_pct_sum = sum(_cpct(t, ri, 2) for ri in range(1, last6))
    chk(abs(sr_pct_sum - 100) <= PCT_SUM_TOL,
        f"Slide 5 Table 6: % column sums to {sr_pct_sum}, not 100")
    chk(_ctxt(t, last6, 2) in ("100%", "100.00%"),
        f"Slide 5 Table 6 Total % cell is {_ctxt(t, last6, 2)!r}, expected '100%'")

    # ---- Slides 6 & 7 Table 5: combined KPI-threshold bands ----------
    for slide_i, key, is_d4 in ((5, "slide6_bands", False), (6, "slide7_bands", True)):
        t = find_table(prs.slides[slide_i], "Table 5")
        cc, pc = _band_counts(pxd[key], cur), _band_counts(pxd[key], prev_i)
        ct, pt = sum(cc.values()), sum(pc.values())

        def comb(counts, total, labels):
            return pct2(sum(counts.get(l, 0) for l in labels), total)

        same_next = ["Same Day", "Next Day"]
        less5 = ["Same Day", "Next Day", "3 - 5 days"]
        chk(abs(_cpct(t, 1, 4) - comb(pc, pt, same_next)) <= PCT_CELL_TOL,
            f"Slide {slide_i + 1} Table 5 'SAME OR NEXT DAY' prev: {_cpct(t, 1, 4)} != {comb(pc, pt, same_next)}")
        chk(abs(_cpct(t, 1, 5) - comb(cc, ct, same_next)) <= PCT_CELL_TOL,
            f"Slide {slide_i + 1} Table 5 'SAME OR NEXT DAY' cur: {_cpct(t, 1, 5)} != {comb(cc, ct, same_next)}")
        chk(abs(_cpct(t, 2, 4) - comb(pc, pt, less5)) <= PCT_CELL_TOL,
            f"Slide {slide_i + 1} Table 5 'LESS THAN 5 DAYS' prev: {_cpct(t, 2, 4)} != {comb(pc, pt, less5)}")
        l5_tol = Decimal("0.01") if is_d4 else PCT_CELL_TOL   # registry D4
        chk(abs(_cpct(t, 2, 5) - comb(cc, ct, less5)) <= l5_tol,
            f"Slide {slide_i + 1} Table 5 'LESS THAN 5 DAYS' cur: {_cpct(t, 2, 5)} != "
            f"{comb(cc, ct, less5)} (tol {l5_tol} pp)")
        check_pie(slide_i, {"Same Day": (cc.get("Same Day", 0), ct),
                            "Next Day": (cc.get("Next Day", 0), ct),
                            "3-5 Days": (cc.get("3 - 5 days", 0), ct),
                            "6+ Days": (cc.get("6+ days", 0), ct)}, f"Slide {slide_i + 1}")

    # ---- Slides 8, 9 & 10: chart-image value chain (FIX 4) ------------
    # The chart on these three slides is a matplotlib PNG that cannot be
    # read back. Instead assert the full chain so the image provably derives
    # from verified numbers:
    #     source series  ==  the array populate_deck handed to
    #     make_trend_chart / make_combo_chart  ==  the table cells.
    # populate_deck records the exact arrays on prs._kpi_chart_series.
    cs = getattr(prs, "_kpi_chart_series", None)
    if cs is None:
        chk(allow_no_chart_series,
            "FIX4: populate_deck did not record _kpi_chart_series - chart-image "
            "value chain cannot be verified. (allow_no_chart_series=True is only "
            "for auditing a reloaded .pptx; the inline build gate always has it.)")
        if allow_no_chart_series:
            print("  validate_deck NOTE: chart-array identity links skipped "
                  "(reloaded deck); source == table still enforced for Slides 8-10.")

    # source == table for the Slide 8/9 KPI value rows (always runs)
    for slide_i, tname, key in ((7, "Table 11", "slide8_values"), (8, "Table 10", "slide9_values")):
        t = find_table(prs.slides[slide_i], tname)
        src = list(pxd[key])
        for ci, idx in ((0, yr_i), (1, prev_i), (2, cur)):
            chk(_ctxt(t, 3, ci) == f"{src[idx]:.1f}",
                f"Slide {slide_i + 1} {tname} value col {ci}: {_ctxt(t, 3, ci)!r} != {src[idx]:.1f}")
        if cs is not None:                 # chart array == source == table
            chk(cs[key] == src,
                f"FIX4 Slide {slide_i + 1}: chart array != source series {key}")
            for ci, idx in ((0, yr_i), (1, prev_i), (2, cur)):
                chk(f"{cs[key][idx]:.1f}" == _ctxt(t, 3, ci),
                    f"FIX4 Slide {slide_i + 1} {tname} col {ci}: chart array {cs[key][idx]} "
                    f"!= table cell {_ctxt(t, 3, ci)!r}")
    if cs is not None:                     # Slide 10 combo chart: Created / Completed series
        t10c = find_table(prs.slides[9], "Table 3")
        for key, row in (("slide10_created", 1), ("slide10_completed", 2)):
            src = list(pxd[key])
            chk(cs[key] == src,
                f"FIX4 Slide 10: chart array != source series {key}")
            for ci, idx in ((1, yr_i), (2, prev_i), (3, cur)):
                chk(str(cs[key][idx]) == _ctxt(t10c, row, ci),
                    f"FIX4 Slide 10 Table 3 row {row} col {ci}: chart array {cs[key][idx]} "
                    f"!= table cell {_ctxt(t10c, row, ci)!r}")

    # ---- Slide 10 Table 3: created vs completed --------------------
    t = find_table(prs.slides[9], "Table 3")
    cr, cp = pxd["slide10_created"], pxd["slide10_completed"]
    for ci, idx in ((1, yr_i), (2, prev_i), (3, cur)):
        chk(_ctxt(t, 1, ci) == str(cr[idx]),
            f"Slide 10 Table 3 Created col {ci}: {_ctxt(t, 1, ci)!r} != {cr[idx]}")
        chk(_ctxt(t, 2, ci) == str(cp[idx]),
            f"Slide 10 Table 3 Completed col {ci}: {_ctxt(t, 2, ci)!r} != {cp[idx]}")
        chk(_ctxt(t, 3, ci) == plain_delta(cp[idx] - cr[idx]),
            f"Slide 10 Table 3 Variance col {ci}: {_ctxt(t, 3, ci)!r} != {plain_delta(cp[idx] - cr[idx])!r} "
            f"(Completed {cp[idx]} - Created {cr[idx]})")
    chk(_ctxt(t, 1, 4) == fmt_delta(cr[cur], cr[prev_i]), "Slide 10 Table 3 Created MoM wrong")
    chk(_ctxt(t, 1, 5) == fmt_delta(cr[cur], cr[yr_i]), "Slide 10 Table 3 Created YoY wrong")
    chk(_ctxt(t, 2, 4) == fmt_delta(cp[cur], cp[prev_i]), "Slide 10 Table 3 Completed MoM wrong")
    chk(_ctxt(t, 2, 5) == fmt_delta(cp[cur], cp[yr_i]), "Slide 10 Table 3 Completed YoY wrong")
    v_cur, v_prev, v_yr = cp[cur] - cr[cur], cp[prev_i] - cr[prev_i], cp[yr_i] - cr[yr_i]
    chk(_ctxt(t, 3, 4) == plain_delta(v_cur - v_prev), "Slide 10 Table 3 Variance MoM wrong")
    chk(_ctxt(t, 3, 5) == plain_delta(v_cur - v_yr), "Slide 10 Table 3 Variance YoY wrong")

    # ================= SPEAKER NOTES (PART D, 7 Sep 2026) =================
    # Real incident that motivated this section: the July AND August decks
    # both still carried JUNE's speaker notes byte-for-byte (populate_deck
    # never touched notes_slide at all). Kevin reads these aloud when
    # presenting, so he read June's figures in both July and August.
    # LIMITS (stated here, not just in a comment further down): these checks
    # can prove the notes were CHANGED and reference the right month/figures
    # - they CANNOT verify the prose is factually correct. Content
    # correctness is Lauren's judgement call, checked by the separate,
    # mandatory Codex numeric-accuracy pass described in KPI_RUN_SOP.md, not
    # by this script.
    base_notes = getattr(prs, "_kpi_base_notes", None)
    cur_month_name = MONTH_FULL[month - 1]
    combined_text = []
    for si in sorted(EXPECTED_NOTES_SLIDES):
        sl = prs.slides[si]
        txt = sl.notes_slide.notes_text_frame.text.strip() if sl.has_notes_slide else ""
        combined_text.append(txt)
        if notes_required:
            chk(bool(txt), f"NOTES: Slide {si + 1} speaker notes are empty.")
            if base_notes is not None:
                chk(txt != base_notes.get(si, "").strip(),
                    f"NOTES: Slide {si + 1} speaker notes are byte-identical to the "
                    f"base deck's notes for this slide - not updated for "
                    f"{cur_month_name} {year}.")
    if not notes_required:
        print("  validate_deck NOTE: notes_required=False - speaker-notes content "
              "checks run in non-blocking mode (self-test coverage of a month "
              "whose notes aren't drafted yet; build_month always uses "
              "notes_required=True).")
    else:
        chk(cur_month_name in "\n".join(combined_text),
            f"NOTES: {cur_month_name!r} does not appear anywhere in the Slide "
            f"2-10 speaker notes - looks stale (best-effort: cannot verify "
            f"prose content, only that the current month is referenced "
            f"somewhere across them).")

        # Best-effort, per-slide figure freshness: ADVISORY ONLY (printed,
        # does not fail the build). Fires when the PREVIOUS period's
        # headline number is present in a slide's notes and the CURRENT one
        # is not. Deliberately non-blocking, not just "best-effort" in name:
        # empirically confirmed to false-positive on genuine, correct,
        # Lauren-approved prose - the real August Slide 7 notes discuss the
        # "65 to 75 percent" amber KPI band, and 65 also happens to be
        # July's (unrelated) Incident-Other headline count. Hard-failing on
        # that coincidence would block a deck that is factually right, which
        # is worse than the gap this section closes. Kept as a printed
        # signal for human review, per the task's own "(best-effort)"
        # framing - the month-name check above is the hard-fail layer for
        # staleness; this is a hint layer on top of it.
        def _num_in(text, n):
            return re.search(rf"(?<!\d){re.escape(str(n))}(?!\d)", text) is not None

        def _fresh(si, label, cur_val, prev_val):
            sl2 = prs.slides[si]
            txt = sl2.notes_slide.notes_text_frame.text if sl2.has_notes_slide else ""
            cur_s, prev_s = str(cur_val), str(prev_val)
            if _num_in(txt, prev_s) and not _num_in(txt, cur_s):
                print(f"  validate_deck ADVISORY (non-blocking): Slide {si + 1} notes "
                      f"mention last period's {label} figure ({prev_s}) but not this "
                      f"month's ({cur_s}) - worth a human glance, not a build failure.")

        s2_cur = sum(_hs_vol(hs_current, s) for s in ("Cority", "Odyssey", "IRIS", "DSE"))
        s2_prev = sum(_hs_vol(hs_prev, s) for s in ("Cority", "Odyssey", "IRIS", "DSE"))
        _fresh(1, "H&S volume total", s2_cur, s2_prev)

        s3_cur = sum(v[0] for v in hs_current.get("slide3_bands", {}).values())
        s3_prev = sum(v[0] for v in hs_prev.get("slide3_bands", {}).values())
        _fresh(2, "time-to-resolve total", s3_cur, s3_prev)

        s4_cur = sum(pxd["slide4_categories"][k][cur] for k in pxd["slide4_categories"])
        s4_prev_hl = sum(pxd["slide4_categories"][k][prev_i] for k in pxd["slide4_categories"])
        _fresh(3, "PXD total", s4_cur, s4_prev_hl)

        s6_cur = sum(_band_counts(pxd["slide6_bands"], cur).values())
        s6_prev = sum(_band_counts(pxd["slide6_bands"], prev_i).values())
        _fresh(5, "Service Request total", s6_cur, s6_prev)

        s7_cur = sum(_band_counts(pxd["slide7_bands"], cur).values())
        s7_prev = sum(_band_counts(pxd["slide7_bands"], prev_i).values())
        _fresh(6, "Incident-Other total", s7_cur, s7_prev)

        _fresh(7, "average acceptance days",
               f"{pxd['slide8_values'][cur]:.1f}", f"{pxd['slide8_values'][prev_i]:.1f}")
        _fresh(8, "average completion days",
               f"{pxd['slide9_values'][cur]:.1f}", f"{pxd['slide9_values'][prev_i]:.1f}")
        _fresh(9, "Created total", pxd["slide10_created"][cur], pxd["slide10_created"][prev_i])
        _fresh(9, "Completed total", pxd["slide10_completed"][cur], pxd["slide10_completed"][prev_i])

    # ================= CROSS-SLIDE RECONCILIATION =================
    s5t4_total = _cint(find_table(prs.slides[4], "Table 4"), 11, 1)
    s7_band_total = sum(_band_counts(pxd["slide7_bands"], cur).values())
    s5t6 = find_table(prs.slides[4], "Table 6")
    s5t6_total = _cint(s5t6, len(s5t6.rows) - 1, 1)
    s4t5 = find_table(prs.slides[3], "Table 5")
    s4_sr_cur = _cint(s4t5, 1, 3)
    s4_io_cur = _cint(s4t5, 2, 3)
    s4_total_cur = _cint(s4t5, 5, 3)
    sr_src_total = sum(v[0] for v in pxd["slide5_service_request"].values())
    analy3 = pxd["slide9_completed_tasks"]
    s10_completed_cur = _cint(find_table(prs.slides[9], "Table 3"), 2, 3)

    # R1 (exact)
    chk(s5t4_total == s7_band_total,
        f"R1 FAILED: Slide 5 Table 4 Total ({s5t4_total}) != Slide 7 current-month "
        f"band-count total ({s7_band_total}). These are the same task population "
        f"shown two ways and must be identical every month.")
    # R2 (exact, three-way)
    chk(s5t6_total == s4_sr_cur == sr_src_total,
        f"R2 FAILED: Slide 5 Table 6 Total ({s5t6_total}), Slide 4 'Service Request' "
        f"cur ({s4_sr_cur}), Service-Request source total ({sr_src_total}) must all be equal.")
    # R-cur (exact)
    chk(s4_total_cur == analy3[cur],
        f"R-cur FAILED: Slide 4 Table 5 Total cur ({s4_total_cur}) != 'Tasks Completed "
        f"by HRIS Analy3' Completed Tasks for the current month ({analy3[cur]}).")
    # D3 (registered differ-by-design, but bounded to +/-1 on historical cols)
    for ci, idx, name in ((1, yr_i, "yr"), (2, prev_i, "prev")):
        s4v = _cint(s4t5, 5, ci)
        chk(abs(s4v - analy3[idx]) <= 1,
            f"D3 EXCEEDED: Slide 4 Table 5 Total ({name}) {s4v} vs Analy3 {analy3[idx]} "
            f"differ by more than the registered +/-1 tolerance.")

    # Backstop: enumerate every repeated metric on the deck. A group whose
    # values disagree must be governed by a registry entry (R = must-equal
    # and already checked above; D = differ-by-design). A disagreeing group
    # with governed_by=None means a repeated figure was added to the deck
    # without being registered -> fail and name it. (Generic "any equal
    # number across 11 slides" discovery is deliberately not attempted: it
    # false-positives on incidental collisions. New repeated metrics are
    # added here AND to docs/reference/incident-other-reconciliation.md.)
    known_d = {d[0] for d in RECONCILIATION_DIFFER_BY_DESIGN}
    repeated_metrics = {
        "Incident - Other (current month)": {
            "governed_by": "D1",
            "values": {"Slide 4 trend": s4_io_cur, "Slide 5 Table 4": s5t4_total,
                       "Slide 7 bands": s7_band_total},
        },
        "Service Request (current month)": {
            "governed_by": "R2",
            "values": {"Slide 4 trend": s4_sr_cur, "Slide 5 Table 6": s5t6_total,
                       "SR source": sr_src_total},
        },
        "Completed PXD tasks (current month)": {
            "governed_by": "R-cur",
            "values": {"Slide 4 Total": s4_total_cur, "Analy3": analy3[cur]},
        },
        "Current-month PXD disposition count": {
            "governed_by": "D2",
            "values": {"Slide 4 Total (completed)": s4_total_cur,
                       "Slide 10 Completed (incl. cancelled/rejected)": s10_completed_cur},
        },
    }
    for name, meta in repeated_metrics.items():
        distinct = set(meta["values"].values())
        gb = meta["governed_by"]
        if len(distinct) > 1 and gb is None:
            chk(False,
                f"BACKSTOP FAILED: repeated metric {name!r} has disagreeing values "
                f"{meta['values']} and no reconciliation-registry entry governs it. "
                f"Add an R (must-equal) or D (differ-by-design) entry to "
                f"docs/reference/incident-other-reconciliation.md and this dict.")
        if len(distinct) > 1 and gb not in known_d and not gb.startswith("R"):
            chk(False,
                f"BACKSTOP FAILED: repeated metric {name!r} disagrees {meta['values']} "
                f"and its registry code {gb!r} is not a recognised R/D entry.")

    if failures:
        head = f"validate_deck: {len(failures)} FAILURE(S) for {MONTH_FULL[month - 1]} {year}"
        print("\n" + "!" * len(head))
        print(head)
        print("!" * len(head))
        for f in failures:
            print("  - " + f)
        err = DeckValidationError(head)
        err.failures = list(failures)   # for programmatic assertions (tampering tests)
        raise err
    print(f"validate_deck: PASS ({MONTH_FULL[month - 1]} {year}) - structural manifest + "
          f"Total-row sweep; per-category source trace (Slides 4 & 5); H&S source match "
          f"(Slides 2 & 3); row sums / percentages / % columns / deltas / pie==table; "
          f"chart-array chain (Slides 8-10); speaker notes updated + month-referenced "
          f"(Slides 2-10{', notes_required=False' if not notes_required else ''}); "
          f"cross-slide registry R1, R2, R-cur exact; D1-D4 registered.")


def build_month(year, month, out_path=None, chart_dir=None, prev_hs=None, notes_path=None):
    """Top-level entry point: build one month's KPI Presentation end to end
    from its own Source Data folder, using the previous month's own
    finished deck as the base (the real monthly process - see memory/
    kpi-presentation-source-and-rebuild-poc.md).

    prev_hs: optional pre-extracted dict (from extract_hs) to use as the
    prior month's H&S figures, for when the prior month's own Source Data
    folder isn't available. If not given, it's read live from the prior
    month's own H&S doc - real carried-forward data, not invented, per the
    module docstring's KNOWN GAP note.

    notes_path: optional explicit path to the month's speaker-notes markdown
    (defaults to notes_path_for(year, month), i.e. `KPI Presentation -
    Handover/notes/speaker-notes-{year}-{month:02d}.md`). Speaker notes are
    a mandatory part of the deliverable (PART D, 7 Sep 2026) - Kevin reads
    them aloud, and the confirmed production bug was that July's and
    August's decks both still carried June's notes verbatim. If the file
    doesn't exist, the build stops here rather than silently shipping stale
    or empty notes; Lauren drafts it (content), this script only places it."""
    excel_path, hs_path = find_source_files(year, month)
    pxd = extract_pxd(excel_path)
    hs_current = extract_hs(hs_path)

    notes, resolved_notes_path = load_month_notes(year, month, notes_path)
    if notes is None:
        raise FileNotFoundError(
            f"speaker notes for {MONTH_FULL[month - 1]} {year} not found at "
            f"{resolved_notes_path!r}. Speaker notes are part of the KPI "
            f"deliverable, not optional polish - Kevin reads them aloud when "
            f"presenting. Lauren drafts '## Slide N' sections for slides 2-10 "
            f"in that file (content - see KPI_RUN_SOP.md); this script will "
            f"not build without it."
        )

    if prev_hs is None:
        py, pm = prev_ym(year, month)
        _, prev_hs_path = find_source_files(py, pm)
        prev_hs = extract_hs(prev_hs_path)

    py, pm = prev_ym(year, month)
    base_deck = deck_path(py, pm)
    if not os.path.exists(base_deck):
        raise FileNotFoundError(
            f"base deck (previous month's finished deck) not found: {base_deck!r} - "
            "the real monthly process copies this forward; it must exist before a new month can be built."
        )

    if out_path is None:
        out_dir = month_dir(year, month)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"KPI presentation - {MONTH_FULL[month - 1]} {year}.pptx")
    if chart_dir is None:
        chart_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"charts_{year}_{month:02d}")

    month_label = f"{MONTH_FULL[month - 1]} {year}"
    prs = populate_deck(base_deck, pxd, hs_current, prev_hs, month_label, chart_dir, out_path, year, month, notes=notes)

    # HARDENED BLOCKING GATE (HANDOVER Part C): validate the freshly built
    # deck before it is written. On any failure, no deck is left at out_path
    # (a .REJECTED copy is saved for inspection) and the exception propagates
    # so __main__ exits non-zero.
    try:
        validate_deck(prs, pxd, hs_current, prev_hs, year, month)
    except DeckValidationError:
        rejected = out_path + ".REJECTED"
        try:
            prs.save(rejected)
            print(f"  validation failed - NO deck written to {out_path}")
            print(f"  rejected copy saved for inspection: {rejected}")
        except Exception:
            pass
        raise

    prs.save(out_path)
    print("written", out_path)
    return out_path


def set_cell_like(shape, text):
    para = shape.text_frame.paragraphs[0]
    if para.runs:
        para.runs[0].text = text
        for extra in para.runs[1:]:
            extra.text = ""
    else:
        para.text = text


def _diff_all_tables(rebuilt_path, reference_path, skip_slides=(), skip_tables=()):
    """Cell-by-cell diff of every table in every slide between two decks.
    Returns a list of (slide_i, table_name, row, col, got, expected)
    mismatches. Slides 8/9/10's Picture 2 (chart image) is intentionally
    not compared here - the real reference deck still carries the original
    pasted screenshot, not a matplotlib rebuild, so a byte/pixel diff there
    is expected and meaningless; the picture-swap mechanism itself was
    already SHA1-verified separately (memory/kpi-presentation-assembly-gap.md)."""
    a = Presentation(rebuilt_path)
    b = Presentation(reference_path)
    mismatches = []
    for si, (sa, sb) in enumerate(zip(a.slides, b.slides)):
        if si in skip_slides:
            continue
        tables_a = {sh.name: sh.table for sh in sa.shapes if sh.has_table}
        tables_b = {sh.name: sh.table for sh in sb.shapes if sh.has_table}
        for name, ta in tables_a.items():
            if (si, name) in skip_tables:
                continue
            tb = tables_b.get(name)
            if tb is None:
                mismatches.append((si + 1, name, None, None, "table missing in reference", None))
                continue
            for ri, (ra, rb) in enumerate(zip(ta.rows, tb.rows)):
                for ci, (ca, cb) in enumerate(zip(ra.cells, rb.cells)):
                    if ca.text != cb.text:
                        mismatches.append((si + 1, name, ri, ci, ca.text, cb.text))
    return mismatches


def _check_chart(path, slide_i, expected):
    """expected: {category: (value, tolerance)}."""
    prs = Presentation(path)
    chart = next(sh.chart for sh in prs.slides[slide_i].shapes if sh.has_chart)
    plot = chart.plots[0]
    cats = list(plot.categories)
    vals = dict(zip(cats, list(plot.series[0].values)))
    results = []
    for cat, (exp, tol) in expected.items():
        got = vals.get(cat)
        got_f = got if got is not None else 0.0
        ok = abs(got_f - exp) <= tol
        results.append((f"slide{slide_i + 1} chart {cat!r}", got, exp, ok))
    return results


if __name__ == "__main__":
    # ---- Self-test: rebuild June 2026 from its own Source Data and check
    # every figure against the real, known-correct June deck. This is the
    # gate before trusting this script on a real July run.
    SCRATCH = os.path.dirname(os.path.abspath(__file__))
    june_src = r"C:\Users\admin\OneDrive - Nexus365\Functional Analysis Team Monthly Statistics\2026\06 Jun\Source Data"
    excel_path = os.path.join(june_src, "HR_Systems_Functional_Team_Monthly_Report_Excel - 202607010715.xlsx")
    hs_path = os.path.join(june_src, "Health and Safety Systems Support Statistics - 202607010600.docx")

    pxd = extract_pxd(excel_path)
    hs = extract_hs(hs_path)

    checks = [
        ("slide4 Service Request Jun26", pxd["slide4_categories"]["Service Request"][-1], 150),
        ("slide4 Change Jun26", pxd["slide4_categories"]["Change"][-1], 15),
        ("slide8 Jun26 avg acceptance", pxd["slide8_values"][-1], 0.4),
        ("slide9 Jun26 avg completion", pxd["slide9_values"][-1], 1.4),
        ("slide10 created Jun26", pxd["slide10_created"][-1], 347),
        ("slide10 completed Jun26", pxd["slide10_completed"][-1], 322),
        # ADR-0001: Slide 5 Table 4 Total & % base = the source month total
        # (77), NOT the old "trimmed" 68. The circulated June deck carried
        # the same defect - see IO_ORACLE / HANDOVER Part A4.
        ("slide5 incident-other total (source month total, ADR-0001)",
         pxd["slide5_incident_other_total"], 77),
        ("hs slide2 Cority", hs["slide2_volumes"]["Cority - Occupational Health Management Service"][0], 17),
        ("hs slide3 Same Day", hs["slide3_bands"]["Same Day"][0], 13),
    ]
    print("=== Self-test part 1: extraction against known June 2026 figures ===")
    all_pass = True
    for label, got, expected in checks:
        ok = got == expected
        all_pass &= ok
        print(f"  {'PASS' if ok else 'FAIL'}: {label} = {got} (expected {expected})")

    # ---- Part 1b: Slide 5 Table 4 mapping (ADR-0001) vs the corrected June
    # oracle - every named row + the computed "Other" row + the Total.
    print("\n=== Self-test part 1b: Slide 5 Table 4 mapping vs ADR-0001 June oracle ===")
    io_june = pxd["slide5_incident_other"]
    for label, want in IO_ORACLE[(2026, 6)].items():
        got = (pxd["slide5_incident_other_total"] if label == "__total__"
               else io_june.get(label, (None,))[0])
        ok = got == want
        all_pass &= ok
        print(f"  {'PASS' if ok else 'FAIL'}: June Table 4 {label} = {got} (expected {want})")

    # ---- Part 2: full-deck assembly. Rebuild June end to end from May's
    # own finished deck as base (the real monthly process), then diff every
    # table cell against the real June deck - ground truth for tables (see
    # memory/kpi-presentation-assembly-gap.md; unlike charts, the real
    # deck's tables are trustworthy, so a cell-for-cell match here is a
    # meaningful correctness proof, not a tautology).
    print("\n=== Self-test part 2: full deck assembly (native chart writes, ")
    print("    slide 2/3/6/7/10 tables, H&S carry-forward, blank-row fix) ===")
    real_june = deck_path(2026, 6)
    test_out = os.path.join(SCRATCH, "assembly_selftest_v2.pptx")
    test_charts = os.path.join(SCRATCH, "charts_selftest")
    try:
        built_path = build_month(2026, 6, out_path=test_out, chart_dir=test_charts)
        # (4, "Table 4") is skipped from the reference diff on purpose: the
        # real June deck carries the pre-ADR-0001 defect (Total 68, no
        # "Other" row), so it is not valid ground truth for this table. It
        # is checked against the corrected IO_ORACLE below instead.
        mismatches = _diff_all_tables(
            built_path, real_june, skip_slides={7, 8, 9},
            skip_tables={(4, "Table 6"), (4, "Table 4")},
        )
        # Slides 8/9/10 (index 7/8/9) contain Picture 2 (chart image, not
        # comparable - see _diff_all_tables docstring) alongside their KPI
        # threshold tables, which ARE comparable - diff those specifically.
        for si, table_name in ((7, "Table 11"), (8, "Table 10"), (9, "Table 3")):
            a = Presentation(built_path).slides[si]
            b = Presentation(real_june).slides[si]
            ta = next(sh.table for sh in a.shapes if sh.has_table and sh.name == table_name)
            tb = next(sh.table for sh in b.shapes if sh.has_table and sh.name == table_name)
            for ri, (ra, rb) in enumerate(zip(ta.rows, tb.rows)):
                for ci, (ca, cb) in enumerate(zip(ra.cells, rb.cells)):
                    if ca.text != cb.text:
                        mismatches.append((si + 1, table_name, ri, ci, ca.text, cb.text))

        # Slide 5, Table 6 needs a role-based comparison, not row-index
        # zip: our rebuild legitimately has one fewer row than the real
        # deck (the real live deck still carries the un-fixed blank row -
        # Kevin's manual deletion, memory/kpi-presentation-layout-fixes.md,
        # was only ever applied to a separate rebuild-TEST file, never the
        # live deck itself). Compare the 6 category rows by index (unaffected
        # by the row count difference) and the Total row by its role (last
        # row in each table), not by matching absolute index.
        ta6 = next(sh.table for sh in Presentation(built_path).slides[4].shapes
                   if sh.has_table and sh.name == "Table 6")
        tb6 = next(sh.table for sh in Presentation(real_june).slides[4].shapes
                   if sh.has_table and sh.name == "Table 6")
        for ri in range(7):  # header + 6 categories, same position in both
            for ci, (ca, cb) in enumerate(zip(ta6.rows[ri].cells, tb6.rows[ri].cells)):
                if ca.text != cb.text:
                    mismatches.append((5, "Table 6", ri, ci, ca.text, cb.text))
        for ci, (ca, cb) in enumerate(zip(list(ta6.rows)[-1].cells, list(tb6.rows)[-1].cells)):
            if ca.text != cb.text:
                mismatches.append((5, "Table 6 (Total row, by role)", -1, ci, ca.text, cb.text))

        # Slide 5, Table 4: checked against the corrected ADR-0001 oracle,
        # NOT the (defective) real June deck. HANDOVER Part A4: the June
        # oracle for this table changes from 68 to 77 - that is the fix.
        t4b = next(sh.table for sh in Presentation(built_path).slides[4].shapes
                   if sh.has_table and sh.name == "Table 4")
        io_labels = [d for d, _ in INCIDENT_OTHER_NAMED] + ["Other"]
        for ri, label in enumerate(io_labels, start=1):
            want = str(IO_ORACLE[(2026, 6)][label])
            got = t4b.rows[ri].cells[1].text.strip()
            if got != want:
                mismatches.append((5, "Table 4 (vs ADR-0001 oracle)", ri, 1, got, want))
        tot_got = t4b.rows[11].cells[1].text.strip()
        if tot_got != str(IO_ORACLE[(2026, 6)]["__total__"]):
            mismatches.append((5, "Table 4 (vs ADR-0001 oracle)", 11, 1, tot_got,
                               str(IO_ORACLE[(2026, 6)]["__total__"])))

        # One known, disclosed deviation from the real deck - not a bug,
        # filtered out of the strict diff rather than silently left in: the
        # 0.01-point rounding-methodology gap on slide 7's "LESS THAN 5
        # DAYS" Jun26 cell (see NOTE printed below) - exact count division
        # vs. the real deck's own unreconcilable rounding.
        rounding_gap = {(7, "Table 5", 2, 5)}
        mismatches = [mm for mm in mismatches if (mm[0], mm[1], mm[2], mm[3]) not in rounding_gap]

        if mismatches:
            all_pass = False
            print(f"  FAIL: {len(mismatches)} table cell mismatch(es) vs real June deck:")
            for si, name, ri, ci, got, exp in mismatches:
                print(f"    slide{si} {name} row{ri} col{ci}: got {got!r}, expected {exp!r}")
        else:
            print("  PASS: every table cell across all 11 slides matches the real June deck exactly")

        # Chart checks: the real deck's own chart values are NOT trustworthy
        # ground truth (4 of 5 native charts were confirmed stale/pass-through
        # against independently-verified June figures during this build - see
        # HANDOVER.md). So chart checks assert against independently
        # hand-computed percentages from the same already-verified counts
        # above (17/38 Cority, 150/313 Service Request, etc.), not against
        # the real deck's chart content.
        chart_checks = []
        chart_checks += _check_chart(built_path, 1, {"Cority": (17 / 38 * 100, 0.01), "Odyssey": (5 / 38 * 100, 0.01), "IRIS": (16 / 38 * 100, 0.01)})
        chart_checks += _check_chart(built_path, 2, {"Same Day": (13 / 32 * 100, 0.01), "6+ Days": (12 / 32 * 100, 0.01)})
        chart_checks += _check_chart(built_path, 3, {"Service Request": (150 / 313 * 100, 0.01), "Change": (15 / 313 * 100, 0.01)})
        chart_checks += _check_chart(built_path, 5, {"Same Day": (112 / 150 * 100, 0.01)})
        chart_checks += _check_chart(built_path, 6, {"Same Day": (49 / 77 * 100, 0.01)})
        for label, got, exp, ok in chart_checks:
            all_pass &= ok
            print(f"  {'PASS' if ok else 'FAIL'}: {label} = {got} (expected {exp:.2f})")

        # Known, disclosed 0.01%-level rounding-methodology ambiguity (see
        # populate_deck's slide 6/7 comment) - checked separately with a
        # wider tolerance and explicitly flagged, not silently folded into
        # the strict table diff above.
        t7 = find_table(Presentation(built_path).slides[6], "Table 5")
        less5_jun = t7.rows[2].cells[5].text
        print(f"  NOTE (flagged, not a failure): slide 7 'LESS THAN 5 DAYS' Jun26 = {less5_jun!r}; "
              f"real deck shows '87.02%' - exact count division (67/77) gives 87.01%, a 0.01-point "
              f"rounding-methodology difference that doesn't resolve to one clean rule from the "
              f"available source data. See HANDOVER.md (registry D4).")

        # ---- Part 3: hardened BLOCKING gate against a freshly built June
        # deck. build_month() above already ran validate_deck() inline before
        # saving (a failure there would have raised and been caught below);
        # this rebuilds in-memory and re-runs the gate explicitly for a
        # visible self-test line. It must be the in-memory Presentation from
        # populate_deck (it carries prs._kpi_chart_series for the FIX 4
        # chart-array chain), not a reload from disk.
        _, prev_hs_path_june = find_source_files(2026, 5)
        prev_hs_june = extract_hs(prev_hs_path_june)
        june_notes, _ = load_month_notes(2026, 6)
        try:
            _june_prs = populate_deck(
                deck_path(2026, 5), pxd, hs, prev_hs_june, "June 2026",
                os.path.join(SCRATCH, "charts_selftest_p3"), test_out, 2026, 6,
                notes=june_notes,
            )
            validate_deck(_june_prs, pxd, hs, prev_hs_june, 2026, 6)
            print("  PASS: validate_deck(June, freshly built in-memory) - all checks")
        except DeckValidationError as e:
            all_pass = False
            print(f"  FAIL: validate_deck(June) - {e}")
    except Exception as e:
        all_pass = False
        print(f"  FAIL: full-deck assembly raised {type(e).__name__}: {e}")

    # ---- Part 4: August 2026 as a SECOND known-good self-test month
    # (HANDOVER Part C3.4). Fresh end-to-end build from July's deck; the
    # hardened gate runs inline in build_month(); then Slide 5 Table 4 is
    # checked against the ADR-0001 August oracle and the Part B captions are
    # confirmed present. Scratch output only - never the OneDrive archive.
    print("\n=== Self-test part 4: fresh August 2026 build + hardened gate ===")
    aug_out = os.path.join(SCRATCH, "assembly_selftest_august.pptx")
    aug_charts = os.path.join(SCRATCH, "charts_selftest_august")
    try:
        aug_path = build_month(2026, 8, out_path=aug_out, chart_dir=aug_charts)
        print("  PASS: build_month(2026, 8) completed - validate_deck() ran inline and passed")
        aug_prs = Presentation(aug_path)
        t4a = next(sh.table for sh in aug_prs.slides[4].shapes
                   if sh.has_table and sh.name == "Table 4")
        io_labels = [d for d, _ in INCIDENT_OTHER_NAMED] + ["Other"]
        for ri, label in enumerate(io_labels, start=1):
            want = str(IO_ORACLE[(2026, 8)][label])
            got = t4a.rows[ri].cells[1].text.strip()
            ok = got == want
            all_pass &= ok
            print(f"  {'PASS' if ok else 'FAIL'}: Aug Table 4 {label} = {got} (expected {want})")
        tot_got = t4a.rows[11].cells[1].text.strip()
        ok = tot_got == str(IO_ORACLE[(2026, 8)]["__total__"])
        all_pass &= ok
        print(f"  {'PASS' if ok else 'FAIL'}: Aug Table 4 Total = {tot_got} "
              f"(expected {IO_ORACLE[(2026, 8)]['__total__']})")
        ok = tot_got == "61" and t4a.rows[10].cells[0].text.strip() == "Other" \
            and t4a.rows[10].cells[1].text.strip() == "2"
        all_pass &= ok
        print(f"  {'PASS' if ok else 'FAIL'}: Aug Slide 5 Table 4 shows Total 61 / 'Other' row = 2")
        cap = next((sh for sh in aug_prs.slides[4].shapes if sh.name == "IncidentOtherScopeCaption"), None)
        ptr = next((sh for sh in aug_prs.slides[3].shapes if sh.name == "IncidentOtherPointer"), None)
        ok = cap is not None and ptr is not None and "61" in cap.text_frame.text
        all_pass &= ok
        print(f"  {'PASS' if ok else 'FAIL'}: Slide 5 scope caption + Slide 4 pointer text boxes present")
    except DeckValidationError as e:
        all_pass = False
        print(f"  FAIL: August build BLOCKED by validate_deck - {e}")
    except Exception as e:
        all_pass = False
        print(f"  FAIL: August build raised {type(e).__name__}: {e}")
    finally:
        for pth in (aug_out, aug_out + ".REJECTED"):
            if os.path.exists(pth):
                try:
                    os.remove(pth)
                except OSError:
                    pass

    print("\n" + ("ALL PASS" if all_pass
                  else "SOME FAILED - do not trust this script on real data yet"))
    sys.exit(0 if all_pass else 1)
