from brief_chrome import SCRATCH, e, render_page, write_brief_output

# ---- Organisational Structure Update - August 2026 - Walk through
#      One-off ad hoc meeting brief (Kevin / Anna Gilbert, 15 Sep 2026,
#      13:30-14:00). Anna is covering for Katherine Corr (unavailable) as
#      the person who can answer content/decision questions on the Trinity
#      Term 2026 Change Schedule. Anthony Kong (HR Systems) handles PeopleXD
#      technical checks separately and is not part of this meeting.
#
# CONTENT SOURCE: all five questions, the closed-items list, and the
# parked/not-for-today items were fully worked through and verified by
# Kevin against the source workbook in the session that requested this
# brief (15 Sep 2026) -- NOT re-derived here. Source workbook: "Organisational
# Structure (Trinity Term 2026 FINAL CORRECTED).xlsx", Change Schedule tab.
# Core scope: Change Schedule rows 8-24 and 111-136 only.
#
# Work Inbox / Command Centre cross-reference (read-only, per standing
# scope) -- checked live 15 Sep 2026 against begb0037admin/work-inbox
# data/briefing.json and begb0037admin/command-centre data/tasks.json.
# Both repos track this as one live thread ("URGENT -- Organisational Structure Update - August 2026 - FINAL"),
# action log entries dated through today (15 Sep 2026). This corroborates
# rather than changes Question 1 (B8 code) -- Anthony Kong's 15 Sep finding
# ("B8 was costing a department code prior to the August 2026 Organisation
# Structure") and Anna Gilbert's 14/15 Sep relay of Sally Vine's findings are
# both already reflected in Kevin's own verified question text below.


QUESTIONS = [
    {
        "id": "1",
        "title": "B8 code (row 16) — reactivate or fresh code?",
        "pill": "raise",
        "owner": "Anna Gilbert",
        "desc": "Sally Vine (HAF, Physiology/Anatomy/Genetics) says B8 is actively used across PXD/Oracle/X5 and should stay that way. Cross-reference: Anthony Kong separately confirmed (15 Sep) that B8 was costing a department code prior to the August 2026 Organisation Structure — corroborates, doesn't change, this question.",
        "say": "Sally says B8 is actively used across PXD, Oracle and X5 and should stay that way — do we reactivate the old B8 for Centre for Neural Circuits and Behaviour, or still assign a fresh code?",
    },
    {
        "id": "2",
        "title": "Target completion date",
        "pill": "info",
        "owner": "Anna Gilbert",
        "desc": "October is a busy month for Anna's team — need a realistic target for this batch.",
        "say": "When do you need this batch done by — realistically November or December, given how busy October is?",
    },
    {
        "id": "3",
        "title": "Colour key — confirm what green vs grey mean",
        "pill": "info",
        "owner": "Anna Gilbert",
        "desc": "Working theory: green = data still relevant, grey = original data of something being deleted. Needs Anna's confirmation before relying on it for anything downstream.",
        "say": "Can you confirm what green vs grey mean in the Change Schedule? My working theory is green = data still relevant, grey = original data of something being deleted.",
    },
    {
        "id": "4",
        "title": "40-character limit — which field, and shortened names",
        "pill": "raise",
        "owner": "Anna Gilbert",
        "desc": "Nine rows have an Entity Full Name over 40 characters: rows 8, 19, 119, 126, 127, 130, 133, 135, 136. Need to confirm which field is actually capped — Entity Name or Entity Full Name — and, if it's Entity Full Name, agree a shortened name for each of the nine rows.",
        "say": "Which field has the 40-character limit — Entity Name or Entity Full Name? Nine rows are over 40 characters on Entity Full Name — rows 8, 19, 119, 126, 127, 130, 133, 135, 136 — if that's the capped field, what shortened name should we use for each?",
    },
    {
        "id": "5",
        "title": "Pay-admin codes on the 16 new subsidiary companies",
        "pill": "raise",
        "owner": "Anna Gilbert",
        "desc": "Rows 111–136 (16 new subsidiary companies) are Level 2 entities, not Level 3 departments. Only three rows in today's scope actually create departments: A7 (row 9), 8H40 (row 11), B8 (row 16).",
        "say": "The 16 new subsidiary companies at rows 111 to 136 are Level 2 entities, not Level 3 departments — do they each need a DEP/DIV pay-admin code the way a new department does, or does that rule only apply to the three department-level creates: A7 row 9, 8H40 row 11, and B8 row 16?",
    },
]


def render_question(q):
    return f'''
  <article class="item card">
    <header class="item-head">
      <span class="item-id">{q["id"]}</span>
      <h3 class="item-title">{q["title"]}</h3>
      <span class="pill pill-{q["pill"]}">{ {"raise": "Raise", "info": "Update"}[q["pill"]] }</span>
      <p class="item-owner">Ask {q["owner"]}</p>
    </header>

    <p class="item-desc">{q["desc"]}</p>

    <blockquote><span class="say-label">Say this</span><p>&ldquo;{q["say"]}&rdquo;</p></blockquote>
  </article>'''


ITEMS_HTML = "\n".join(render_question(q) for q in QUESTIONS)

CLOSED_TABLE = """<div class="table-wrap card">
        <table>
          <thead><tr><th>Item</th><th>Resolution</th><th>Confirmed by</th></tr></thead>
          <tbody>
            <tr><td>KB (row 12) and AU (row 15)</td><td>Only two parent changes in rows 8–24</td><td>Anna, by email</td></tr>
            <tr><td>Row 20 (CC)</td><td>Blank new-parent field is intentional — name-only change</td><td>Anna, by email</td></tr>
            <tr><td>Oxuniprint (XU row 129 / XP rows 123–124)</td><td>Only XU (row 129) should be created; XP should not — nets to no-op</td><td>Anna, by email</td></tr>
            <tr><td>Rows 10 and 17 (HESA codes)</td><td>Don't touch PeopleXD — nothing to build</td><td>Anthony Kong</td></tr>
            <tr><td>PERSUP11 Active Hierarchy report</td><td>Saved as pre-change baseline</td><td>—</td></tr>
          </tbody>
        </table>
      </div>"""

PARKED_TABLE = """<div class="table-wrap card">
        <table>
          <thead><tr><th>Item</th><th>Why parked</th><th>Owner</th></tr></thead>
          <tbody>
            <tr><td>Row 12 (KB) — whether anyone active needs moving before the parent change to PAD</td><td>Anthony's PeopleXD technical check to complete separately</td><td>Anthony Kong</td></tr>
            <tr><td>Colleges &amp; Societies / REF structure (Company 90, St Cross / Kellogg / Reuben)</td><td>Separate workstream, not today's scope</td><td>Nathan &amp; Simon</td></tr>
          </tbody>
        </table>
      </div>"""

SECTIONS = f"""
  <h2>Five questions for Anna <span class="h2-sub">Agenda core &middot; Change Schedule rows 8–24 and 111–136 only</span></h2>
  <div class="item-grid">
{ITEMS_HTML}
  </div>

  <h2>Already closed — agreed background, not re-asked</h2>
  {CLOSED_TABLE}

  <h2>Not for today — parked / different owners</h2>
  {PARKED_TABLE}

  <h2 class="h2-warn">Cross-reference note</h2>
  <p class="body-loose">Work Inbox and Command Centre were checked live (15&nbsp;Sep 2026) — both track this as one live thread (&ldquo;URGENT &mdash; Organisational Structure Update &mdash; August 2026 &mdash; FINAL&rdquo;), with action-log entries dated through today. This corroborates Question&nbsp;1 (Anthony Kong's 15&nbsp;Sep B8 finding, Anna's 14/15&nbsp;Sep relay of Sally Vine's findings) rather than adding anything new beyond what's already reflected in the question above.</p>

"""

FOOTNOTE_HTML = """<div class="footnote">
    Prepared 15 Sep 2026 for the 13:30–14:00 walkthrough with Anna Gilbert (covering for Katherine Corr). Content — the five questions, closed items, and parked items — verified by Kevin directly against the source workbook this session, not re-derived here.<br>
    Source: "Organisational Structure (Trinity Term 2026 FINAL CORRECTED).xlsx", Change Schedule tab. Cross-referenced (read-only) against begb0037admin/work-inbox data/briefing.json and begb0037admin/command-centre data/tasks.json, 15 Sep 2026 — see Cross-reference note above.<br>
    Branding: command-centre/BRANDING.md v2.0 — Oxford Navy, Inter, canonical crest. Template shared with the other speaking briefs via brief_chrome.py.
  </div>"""

html_out = render_page(
    title="Organisational Structure Update — Walk through",
    app_name="Org Structure Walkthrough",
    kicker="Speaking Brief &middot; Ad hoc",
    h1="Organisational Structure Update — August 2026 — Walk through",
    meta_spans=[
        "<b>Date</b> Tuesday 15 September 2026, 13:30&ndash;14:00",
        "<b>Attendees</b> Kevin Lelitte; Anna Gilbert (covering for Katherine Corr)",
        "<b>Status</b> Draft &mdash; content verified by Kevin, presentation only",
    ],
    flag_label="Before anything else",
    flag_paragraphs=[
        "Anna Gilbert is covering for Katherine Corr today &mdash; confirmed by Anna's own 11&nbsp;Sep email. Anna is the person who can answer content/decision questions on the Change Schedule.",
        "Core scope for today is Change Schedule <b>rows 8&ndash;24 and 111&ndash;136 only</b>. Anthony Kong (HR Systems) handles PeopleXD technical checks (active people, moves) separately &mdash; he is not part of today's meeting. Colleges/REF structure (Company&nbsp;90, St&nbsp;Cross/Kellogg/Reuben) is a separate parked workstream with Nathan and Simon &mdash; not today.",
        "Work Inbox / Command Centre cross-reference (checked live, 15&nbsp;Sep): both track this as one live thread &mdash; see Cross-reference note below for what that corroborates.",
        "Tell me if anything below is wrong or out of date and I'll correct it.",
    ],
    sections_html=SECTIONS,
    footnote_html=FOOTNOTE_HTML,
)

write_brief_output(html_out, "Organisational Structure Walkthrough")
