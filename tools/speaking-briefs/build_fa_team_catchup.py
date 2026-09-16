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
#      Framing correction #1, same day: Kevin presents items himself in this
#      meeting where the source supports it -- he is not being briefed by
#      others by default. Item 3 is Kevin's own work, presented by him as
#      normal.
#
#      Framing correction #2, same day, SUPERSEDES the item-1 framing above:
#      the standing-agenda slot has NO fixed owner -- Kevin assigns who
#      presents it each time, case by case. Today it's James, because Kevin
#      is on annual leave this afternoon -- confirmed via Work Inbox
#      `calFull` (an all-day "Kevin - Annual Leave" entry plus a specific
#      12:30 "Kevin A/L (pm)" item today), which the shorter `calTomorrow`
#      field used in the first pass didn't surface, causing that pass to get
#      the who's-presenting direction backwards twice in a row (first "James
#      covering for Kevin," then "Kevin covering for James" -- both wrong;
#      real answer is "no fixed owner, James assigned today"). Item 1's Say
#      field is now a note FOR Kevin about what to expect from James, not a
#      first-person line for Kevin to say, since he isn't the one presenting
#      it today.
#
#      Item 2 (patch release notes) was checked for the same backwards-
#      framing risk and found to be a genuinely different pattern: the
#      calendar entry's own wording has Michael as the designated lead "for
#      next 6 months," not a rotating slot -- "Kevin standing in for Michael"
#      holds up. Real patch content itself (what's changing, what it
#      affects) was searched for across Work Inbox, Command Centre, and
#      OneDrive and not found anywhere beyond the calendar entry's own
#      generic description -- flagged plainly in the item rather than
#      guessed at, plus an explicit ask to Asta for support in the room
#      since she'd normally hold the working detail here.
#
#      Kevin's three requested focus areas, verified against real sources
#      (not inferred) rather than taken at face value -- see each item's
#      "what"/"status" for exactly what was confirmed vs not:
#        1. Standing agenda, James presenting today (Kevin assigns
#           case-by-case) -- confirmed a real recurring tracked-items slide
#           exists (19 Aug transcript refers to "the standard agenda slide"
#           directly), but no capture since 19 Aug to confirm today's actual
#           content -- flagged as stale, not guessed.
#        2. Fortnightly patch release notes, Kevin presenting for Michael --
#           confirmed as a real, separate 11:30 calendar slot today, but the
#           actual patch content itself could not be found in Work Inbox,
#           Command Centre, OneDrive, or Granola -- only the calendar entry's
#           own generic description exists. Flagged as a genuine gap, not
#           invented; added an explicit ask to Asta for support.
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
    {"id": "1", "title": "Standing agenda &mdash; James presenting today, Kevin assigns case-by-case", "pill": "onhold",
     "what": "There's no fixed owner for the standing-agenda slot &mdash; Kevin assigns who presents it each time, case by case. Today he's assigned it to James, because Kevin is on annual leave this afternoon (confirmed via Work Inbox calFull: an all-day \"Kevin - Annual Leave\" entry today plus a specific 12:30 \"Kevin A/L (pm)\" calendar item &mdash; this wasn't visible in the shorter calTomorrow view used in an earlier pass, which is why that pass got the framing backwards). The standing agenda itself is a real, recurring tracked-items slide &mdash; confirmed via the 19&nbsp;Aug transcript's own reference to \"the standard agenda slide.\" Last real content captured: Azure Security Groups (largely done, ready to remove from the slide), Letter Templates (on hold pending Michelle's return from leave), GLAM leave/absence workstreams, and a payroll/availability watch item.",
     "status": "<b>No FA Team Catch-up outcome captured in Granola since 19&nbsp;Aug</b> &mdash; nearly a month's gap. Today's actual current slide content isn't independently confirmed; James will be presenting from the last known real state unless he has something newer.",
     "say": "Note for Kevin, not a speaking line &mdash; James is presenting this one today, not you. Just listen for whether anything's moved since the 19&nbsp;Aug state (Azure Security Groups, Letter Templates, GLAM workstreams, payroll watch)."},
    {"id": "2", "title": "Fortnightly patch release notes &mdash; Kevin presenting, standing in for Michael", "pill": "raise",
     "what": "Michael is the designated lead for this fortnightly patch release review \"for next 6 months\" (the calendar entry's own wording, not a rotating case-by-case slot like item&nbsp;1) &mdash; Kevin is presenting it today on Michael's behalf. Real, separate calendar slot today (11:30): \"check HR Systems impact and implementation dependencies before next release date.\" <b>The actual patch content itself &mdash; what's changing in this release and what it affects &mdash; could not be located</b> after checking Work Inbox (briefing.json, no \"release notes\"/\"PeopleXD release\" hits beyond the calendar entry itself), Command Centre (tasks.json, no hits), OneDrive (searched for patch/release-note documents, found nothing current), and Granola (no note exists for this review series). Not guessing at content that isn't sourced.",
     "status": "Kevin hasn't run one of these in a while and doesn't have the underlying document. Presenting without it unless it surfaces before the meeting.",
     "say": "I'm covering the patch release review for Michael today, but I genuinely don't have the notes document in front of me from anything I can pull. Asta, I'd appreciate your support on this one &mdash; it's been a while since I've run through these and you'll hold more of the working detail than I do right now."},
    {"id": "3", "title": "PXD UDF HESA update &mdash; Kevin's own update", "pill": "new",
     "what": "Kevin's own REF 2029 HESA UDF work with Nathan Kirwan &mdash; already flagged urgent in the HR Systems Managers Meeting brief (deadline Thu 17&nbsp;Sept). Since that item was added, Command Centre shows real, dated movement: Nathan has matched the UDF template structure to the data items, and Kevin has given technical guidance on the Contract ID column and confirmed the current UDF template download is needed.",
     "status": "<b>Genuinely more current than the Managers Meeting brief's version</b> (which only had \"last confirmed correct 10&nbsp;Sept\") &mdash; per Command Centre task t2609141649162, dated <b>15&nbsp;Sept</b> (yesterday): Nathan re-confirmed the team is on track for delivery. Upload deadline Thursday 17&nbsp;Sept, ahead of the wider FA-works deadline Friday 18&nbsp;Sept. A separate \"PXD HESA UDF\" calendar slot exists tomorrow, 17&nbsp;Sept 12:00.",
     "say": "Update from me on the HESA UDF &mdash; Nathan's confirmed the template structure matches and we're on track for Thursday's upload."},
]


# Same fixed-grid fix applied to the Managers Meeting brief the same day:
# no standalone # column (numbering folded into the Item cell's own text),
# fixed column widths via <colgroup> with What/Status clearly the widest.
ITEM_COLGROUP = '''<colgroup><col style="width:24%"><col style="width:51%"><col style="width:25%"></colgroup>'''


def render_row(a):
    return f'''<tr>
            <td>{a["id"]}. {a["title"]} <span class="pill pill-{a["pill"]}">{ {"raise":"Raise","onhold":"Historic — unresolved","info":"Update","overdue":"Overdue","resolved":"Resolved","new":"New"}[a["pill"]] }</span></td>
            <td><b>What:</b> {a["what"]}<br><span class="cur-label">Status</span> {a["status"]}</td>
            <td><span class="say-label">Say</span> &ldquo;{a["say"]}&rdquo;</td>
          </tr>'''


ITEMS_TABLE = "\n".join(render_row(a) for a in ITEMS)

GLANCE_TABLE = """<table class="fixed-grid">
          <colgroup><col style="width:70%"><col style="width:30%"></colgroup>
          <thead><tr><th>Item</th><th>Type</th></tr></thead>
          <tbody>
            <tr><td>1. Standing agenda (James presenting today)</td><td><span class="pill pill-onhold">Historic</span></td></tr>
            <tr><td>2. Patch release notes (Kevin presenting for Michael)</td><td><span class="pill pill-raise">Raise</span></td></tr>
            <tr><td>3. PXD UDF HESA update (Kevin's own)</td><td><span class="pill pill-new">New</span></td></tr>
          </tbody>
        </table>"""

SECTIONS = f"""
  <h2>Today's three focus areas <span class="h2-sub">Verified against Work Inbox / Command Centre / Granola, not inferred</span></h2>
  <table class="fixed-grid">
    {ITEM_COLGROUP}
    <thead><tr><th>Item</th><th>What / Status</th><th>Say this</th></tr></thead>
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
    Prepared 16 Sept 2026 for today's 09:30 sitting, corrected same day (first build of this meeting type) &middot; Sources: Work Inbox data/briefing.json calFull field (richer than calTomorrow -- surfaces the all-day "Kevin - Annual Leave" entry and the 12:30 "Kevin A/L (pm)" item that calTomorrow's shorter view missed), Command Centre data/tasks.json (task t2609141649162, dated 15 Sept), Granola "FA Team Catch-up" notes (11 Aug: not_edc9scBKs2Fy0a, 19 Aug: not_HfuqAJkW1IgOZr &mdash; most recent available, nearly a month stale). Patch-content search also checked OneDrive directly -- nothing found beyond the calendar entry's own description.<br>
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
