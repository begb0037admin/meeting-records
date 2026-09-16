from datetime import datetime
from brief_chrome import SCRATCH, e, render_page, write_brief_output

# ---- FA Team Catch-up. FIRST BUILD of this meeting type, 16 Sept 2026 --
#      next in the planned rollout order after SK 1-1 (per
#      tools/speaking-briefs/README.md: "FA Team Catch-up (Wed/Fri) is next
#      and should be able to follow it closely" from build_sk_1on1.py).
#
#      Format note: built using the compact What/Status/Say table shape
#      (# | Item | What/Status | Say this) rather than build_sk_1on1.py's
#      full item-card shape -- that compact format was requested and
#      approved by Kevin the same day, on the Managers Meeting brief, after
#      explicit feedback that the full-card shape read too noisy. Using the
#      already-proven, already-approved shape for a brand new meeting type
#      rather than starting from the older card pattern.
#
#      Date/time confirmed LIVE, not assumed: Work Inbox data/briefing.json
#      (pulled 16 Sept) calTomorrow field (captured from the 15 Sept pull,
#      i.e. today's real schedule) shows "FA Team Daily Catchup" at 09:30
#      today, Wednesday 16 Sept 2026. Cross-checked against Granola: real
#      "FA Team Catch-up" notes exist (11 Aug, 19 Aug) confirming this is a
#      genuine recurring series with its own name in Granola even though
#      Work Inbox's calendar auto-labels it generically as "Daily Catchup" --
#      same meeting, two different naming conventions. NOTE: despite
#      Lauren's own AGENT.md/README describing this as "twice-weekly
#      (Wed/Fri)", the live calendar shows a DAILY 09:30 slot -- that
#      description looks stale/imprecise and is flagged for correction in
#      memory, not silently carried forward as fact here.
#
#      No FA Team Catch-up outcome has been captured in Granola since
#      19 Aug 2026 -- essentially a month's gap before today's sitting.
#      Everything below is flagged accordingly: real per the 19 Aug capture
#      where that's the best available source, explicitly marked unconfirmed
#      where nothing more current exists.
#
#      Framing correction, same day: Kevin presents all three items himself
#      in this meeting -- he is not being briefed/updated by James or
#      Michael. Items 1 and 2 are Kevin STANDING IN to present slots James
#      and Michael normally own (per Kevin's own account of today's
#      arrangement -- not independently confirmed via calendar/absence data,
#      which doesn't show either of them absent today, but this is Kevin
#      describing his own day directly, not an intermediary's claim). Item 3
#      is Kevin's own work, presented by him as normal.
#
#      Kevin's three requested focus areas, verified against real sources
#      (not inferred) rather than taken at face value -- see each item's
#      "what"/"status" for exactly what was confirmed vs not:
#        1. Standing agenda, Kevin presenting for James -- confirmed a real
#           recurring tracked-items slide exists (19 Aug transcript refers to
#           "the standard agenda slide" directly), but no capture since
#           19 Aug to confirm today's actual content -- flagged as stale, not
#           guessed.
#        2. Fortnightly patch release notes, Kevin presenting for Michael --
#           confirmed as a real, separate 11:30 calendar slot today, but the
#           actual patch content itself could not be found in Work Inbox,
#           Command Centre, or Granola -- only the calendar entry's own
#           generic description exists. Flagged as a genuine gap, not
#           invented.
#        3. PXD UDF HESA update, Kevin's own -- confirmed real and materially more
#           current than the version already in the Managers Meeting brief:
#           Command Centre task t2609141649162 (dated 15 Sept, yesterday)
#           shows Nathan has since matched the UDF template structure to
#           data items and the team is confirmed on track; Kevin gave
#           technical guidance on the Contract ID column and template
#           download. A separate "PXD HESA UDF" calendar slot exists
#           tomorrow, 17 Sept 12:00 -- the same day as the upload deadline
#           already flagged urgent in the Managers Meeting brief.

ITEMS = [
    {"id": "1", "title": "Standing agenda &mdash; Kevin presenting, standing in for James", "pill": "onhold",
     "what": "James normally owns and presents the standing-agenda slot; Kevin is presenting it today on James's behalf (per Kevin's own account &mdash; not independently confirmed via calendar/absence data, which doesn't show James absent today, but this is Kevin's own description of today's arrangement, not an intermediary's claim). The standing agenda itself is a real, recurring tracked-items slide &mdash; confirmed via the 19&nbsp;Aug transcript's own reference to \"the standard agenda slide.\" Last real content captured: Azure Security Groups (largely done, ready to remove from the slide), Letter Templates (on hold pending Michelle's return from leave), GLAM leave/absence workstreams, and a payroll/availability watch item.",
     "status": "<b>No FA Team Catch-up outcome captured in Granola since 19&nbsp;Aug</b> &mdash; nearly a month's gap. Today's actual current slide content isn't independently confirmed; presenting from the last known real state.",
     "say": "I'm covering the standing agenda for James today &mdash; last I've got is the 19&nbsp;Aug state, so flag anything that's actually moved since."},
    {"id": "2", "title": "Fortnightly patch release notes &mdash; Kevin presenting, standing in for Michael", "pill": "raise",
     "what": "Michael normally leads this fortnightly patch release review; Kevin is presenting it today on Michael's behalf (per Kevin's own account, same basis as item&nbsp;1). Real, separate calendar slot today (11:30): \"leading patch release review for next 6 months; check HR Systems impact and implementation dependencies before next release date.\"",
     "status": "<b>Actual patch release notes content not found</b> in Work Inbox, Command Centre, or Granola &mdash; only the calendar entry's own generic description exists. Presenting without the underlying document unless it surfaces before the meeting.",
     "say": "I'm covering the patch release review for Michael today, but I don't actually have the notes document in front of me from anything I can pull &mdash; need to get hold of it live or defer the detail."},
    {"id": "3", "title": "PXD UDF HESA update &mdash; Kevin's own update", "pill": "new",
     "what": "Kevin's own REF 2029 HESA UDF work with Nathan Kirwan &mdash; already flagged urgent in the HR Systems Managers Meeting brief (deadline Thu 17&nbsp;Sept). Since that item was added, Command Centre shows real, dated movement: Nathan has matched the UDF template structure to the data items, and Kevin has given technical guidance on the Contract ID column and confirmed the current UDF template download is needed.",
     "status": "<b>Genuinely more current than the Managers Meeting brief's version</b> (which only had \"last confirmed correct 10&nbsp;Sept\") &mdash; per Command Centre task t2609141649162, dated <b>15&nbsp;Sept</b> (yesterday): Nathan re-confirmed the team is on track for delivery. Upload deadline Thursday 17&nbsp;Sept, ahead of the wider FA-works deadline Friday 18&nbsp;Sept. A separate \"PXD HESA UDF\" calendar slot exists tomorrow, 17&nbsp;Sept 12:00.",
     "say": "Update from me on the HESA UDF &mdash; Nathan's confirmed the template structure matches and we're on track for Thursday's upload."},
]


def render_row(a):
    return f'''<tr>
            <td class="idcell">{a["id"]}</td>
            <td>{a["title"]} <span class="pill pill-{a["pill"]}">{ {"raise":"Raise","onhold":"Historic — unresolved","info":"Update","overdue":"Overdue","resolved":"Resolved","new":"New"}[a["pill"]] }</span></td>
            <td><b>What:</b> {a["what"]}<br><span class="cur-label">Status</span> {a["status"]}</td>
            <td><span class="say-label">Say</span> &ldquo;{a["say"]}&rdquo;</td>
          </tr>'''


ITEMS_TABLE = "\n".join(render_row(a) for a in ITEMS)

GLANCE_TABLE = """<table>
          <thead><tr><th>ID</th><th>Item</th><th>Type</th></tr></thead>
          <tbody>
            <tr><td class="idcell">1</td><td>Standing agenda (Kevin presenting for James)</td><td><span class="pill pill-onhold">Historic</span></td></tr>
            <tr><td class="idcell">2</td><td>Patch release notes (Kevin presenting for Michael)</td><td><span class="pill pill-raise">Raise</span></td></tr>
            <tr><td class="idcell">3</td><td>PXD UDF HESA update (Kevin's own)</td><td><span class="pill pill-new">New</span></td></tr>
          </tbody>
        </table>"""

SECTIONS = f"""
  <h2>Today's three focus areas <span class="h2-sub">Verified against Work Inbox / Command Centre / Granola, not inferred</span></h2>
  <table>
    <thead><tr><th>#</th><th>Item</th><th>What / Status</th><th>Say this</th></tr></thead>
    <tbody>
{ITEMS_TABLE}
    </tbody>
  </table>

  <h2 class="h2-warn">Gaps, flagged plainly</h2>
  <ul class="body-loose">
    <li>No FA Team Catch-up outcome captured in Granola since 19&nbsp;Aug &mdash; today's real standing-agenda content is not confirmed, only the last capture's.</li>
    <li>The actual fortnightly patch release notes content couldn't be found in any available source &mdash; only the calendar entry's own description.</li>
    <li>Lauren's own README/AGENT.md describes this meeting as "twice-weekly (Wed/Fri)" but the live calendar shows a daily 09:30 slot &mdash; that description looks stale and is being corrected in memory, not treated as fact here.</li>
  </ul>
"""

FOOTNOTE = """<div class="footnote">
    Prepared 16 Sept 2026 for today's 09:30 sitting (first build of this meeting type) &middot; Sources: Work Inbox data/briefing.json (calTomorrow field from the 15 Sept pull, i.e. today's live schedule), Command Centre data/tasks.json (task t2609141649162, dated 15 Sept), Granola "FA Team Catch-up" notes (11 Aug: not_edc9scBKs2Fy0a, 19 Aug: not_HfuqAJkW1IgOZr &mdash; most recent available, nearly a month stale).<br>
    First-time authorized build under the 21 Aug 2026 pipeline-review freeze -- a new meeting type, not an edit to an existing frozen script.<br>
    Branding: command-centre/BRANDING.md v2.0 &mdash; Oxford Navy, Inter, canonical crest. Template shared via brief_chrome.py.
  </div>"""

html_out = render_page(
    title="FA Team Catch-up — 16/09",
    app_name="FA Team Catch-up",
    kicker="Speaking Brief &middot; Draft &middot; First build",
    h1="FA Team Catch-up — 16/09",
    meta_spans=[
        "<b>Meeting</b> Today, Wednesday 16 September 2026, 09:30",
        "<b>Related slot</b> Patch release notes review, 11:30 today (separate calendar entry)",
        "<b>Status</b> First build of this meeting type, 16 Sept 2026",
    ],
    flag_label="Before anything else",
    flag_paragraphs=[
        "First-ever build of this meeting type &mdash; no prior brief or captured outcome doc exists to carry forward from, so everything below is built fresh from live sources.",
        "No FA Team Catch-up has been captured in Granola since 19&nbsp;Aug &mdash; nearly a month's gap. Tell me what's actually on the standing agenda today and I'll correct the record afterwards.",
    ],
    glance_label="At a glance",
    glance_sub="3 focus items, all verified against live sources",
    glance_table_html=GLANCE_TABLE,
    sections_html=SECTIONS,
    footnote_html=FOOTNOTE,
)

write_brief_output(html_out, "FA Team Catch-up", date=datetime(2026, 9, 16))
