from brief_chrome import SCRATCH, e, render_page, write_brief_output

# ---- PDR (Performance Development Review) 2026 prep pack. First build of
#      this meeting type — no prior build_*.py script covers it. One prep
#      doc per person (Kevin's own PDR as reviewee, plus Michael O'Sullivan,
#      James Salas Guillen, and Asta Palmer as reviewees with Kevin as
#      reviewer), same shape as build_sk_1on1.py's agenda-point cards, but
#      repurposed as "discussion theme" cards since there's no prior
#      meeting outcome to carry forward for this meeting type.
#
# CRITICAL, READ BEFORE TRUSTING ANYTHING BELOW: the two sources this brief
# most needed — last year's "<Name> - PDR Review 2025.docx" for each of the
# four people, and the official PDR Toolkit SharePoint site
# (unioxfordnexus.sharepoint.com/sites/ADMN-PDRToolkit) — are BOTH
# genuinely unreachable this session, not merely unchecked. Drew ran a
# read-only Codex M365 connector lookup (13 Sep 2026) against both Kevin's
# Oxford Edu identity and his personal identity; every attempt on both
# identities returned the same explicit Microsoft error
# (TRIGGER_REAUTHENTICATION / oauth_token_invalid_grant) — an expired/
# invalid OAuth grant, not a quota issue, not a "not built" architecture
# gap (SharePoint and Calendar connectors are confirmed attached). Nothing
# was written, sent, or modified in that lookup. Full record:
# https://github.com/begb0037admin/drew/blob/main/memory/codex-m365-connector-oauth-reauth-required-13sept.md
# Fix needed: Kevin reauthenticates the M365 connector in the ChatGPT/Codex
# desktop session(s) (both accounts hit this independently) — a one-time
# sign-in only he can do, not a workaround. Once fixed, rerun this same
# lookup and rebuild this pack — the 2025-recap and SharePoint-toolkit
# sections below are placeholders, not "nothing to report."
#
# Sources actually available and used, verified live 13 Sep 2026:
#   - Kevin's own Google Calendar: "Kevin's PDR Review 2026", Tue 16 Sep
#     2026, 15:00-16:00 UK — the only PDR calendar entry connector-side
#     access could reach (Google Calendar, not Oxford Outlook). Its own
#     description references "Kevin Lelitte - PDR Review 2025.docx" — file
#     not present in Kevin's connected Google Drive, and separately
#     unreachable via the blocked Oxford connector.
#   - begb0037admin/command-centre, data/tasks.json, task
#     task-1787645383808 ("Book PDR sessions with Simon Burford and the FA
#     team") — the one live, dated record of this year's actual PDR
#     scheduling activity, built up from real Oxford-mailbox content Aug-Sep
#     2026. This is the authoritative source for what's confirmed/pending
#     below; nothing in it was invented or extrapolated.
#   - begb0037admin/command-centre, data/tasks.json, full task list —
#     cross-referenced by name (Michael O'Sullivan / James Salas Guillen /
#     Asta Palmer / Simon Burford) for live, current workload context to
#     ground each person's "themes to cover" section in real, dated
#     activity rather than generic PDR boilerplate.
#   - begb0037admin/work-inbox — briefing.json, needs_reply.json,
#     triage_ledger.json, drafted_replies.json, inbox_suggestions.json all
#     checked for "pdr"/"PDR" (Drew's lookup); nothing beyond what's already
#     summarised in the command-centre task above.
#
# NOT checked: Granola (not attempted this session — the PDR-specific gap
# was the Oxford connector, not Granola; worth a follow-up check before this
# pack is treated as complete).

PDR_TRACKER_URL = ("https://unioxfordnexus.sharepoint.com/:x:/r/sites/"
                    "HumanResources-HRSystems-HRSystemsManagementTeam/Shared%20Documents/"
                    "HR%20Systems%20Management%20Team/HR%20Systems%20PDR%20Completion%202026.xlsx"
                    "?d=w2e1b829d370d4c1f877cec77aec7bffb&csf=1&web=1&e=GoiKEZ")
PDR_TOOLKIT_URL = "https://unioxfordnexus.sharepoint.com/sites/ADMN-PDRToolkit/SitePages/Home.aspx"

BLOCKER_FLAG_PARAGRAPHS = [
    "<b>Last year's PDR review document and the official PDR Toolkit are both blocked, not empty.</b> "
    "Drew ran a read-only Codex M365 connector lookup today against both your Oxford (Edu) and personal "
    "identities; every attempt on both hit the same explicit Microsoft error &mdash; an expired/invalid "
    "OAuth grant (<code>TRIGGER_REAUTHENTICATION</code>), not a missing feature. SharePoint and Calendar "
    "connectors are confirmed attached &mdash; they're just unreadable until reauthenticated. Nothing was "
    "written, sent, or changed anywhere during the attempt.",
    "<b>Fix needed from you specifically:</b> reauthenticate the Microsoft&nbsp;365 connector in the "
    "ChatGPT/Codex desktop session(s) &mdash; both accounts hit this independently, so likely both need it. "
    "Once done, this pack can be rebuilt with the real 2025 recap and the current PDR Toolkit process/"
    "timeline filled in &mdash; same script, same sources, just re-run.",
    "Everything below that <i>is</i> filled in comes from your own Google Calendar (personal, not Oxford) "
    "and from live, dated command-centre/work-inbox cross-reference &mdash; real facts, not inferred ones. "
    "Where something isn't confirmed, it's left flagged rather than guessed.",
]


def render_theme(t):
    return f'''
  <article class="item card">
    <header class="item-head">
      <span class="item-id">{t["id"]}</span>
      <h3 class="item-title">{t["title"]}</h3>
      <span class="pill pill-{t["pill"]}">{ {"raise":"Raise","onhold":"Ongoing","info":"Update","overdue":"Blocked","resolved":"Confirmed","new":"New for 2026","atrisk":"Flag"}[t["pill"]] }</span>
      <p class="item-owner">{t["category"]}</p>
    </header>
    <p class="item-desc">{t["desc"]}</p>
    <blockquote><span class="say-label">Say this</span><p>&ldquo;{t["say"]}&rdquo;</p></blockquote>
  </article>'''


def recap_2025_block(name, docx_name):
    return f"""<div class="table-wrap card">
        <table>
          <thead><tr><th>Achieved</th><th>Not achieved / carried forward</th><th>Notes</th></tr></thead>
          <tbody>
            <tr><td colspan="3"><b>Blocked</b> &mdash; source document &ldquo;{docx_name}&rdquo; is unreachable this
            session (Oxford M365 connector OAuth reauth required, see flag above). Nothing below is invented or
            inferred from memory; rerun this build once the connector is reauthenticated to populate this
            table for real.</td></tr>
          </tbody>
        </table>
      </div>"""


def build_person(slug, display_name, meeting_label, date_status_html, glance_rows, themes,
                  scheduling_risk_html, docx_name, extra_conflict_html=""):
    items_html = "\n".join(render_theme(t) for t in themes)

    sections = f"""
  <h2>2025 recap <span class="h2-sub">What was achieved, what wasn't, what carries forward</span></h2>
  {recap_2025_block(display_name, docx_name)}

  <h2>Themes to cover for 2026 <span class="h2-sub">Grounded in live, dated command-centre/work-inbox activity, not generic PDR boilerplate</span></h2>
  <div class="item-grid">
{items_html}
  </div>

  <h2 class="h2-warn">Risks and dependencies</h2>
  <p class="body-loose">{scheduling_risk_html}</p>
  <p class="body-loose">The <a href="{PDR_TRACKER_URL}">HR Systems PDR Completion 2026 tracker</a> (SharePoint) is
  the central record for booking status across the whole FA team &mdash; also currently unreadable via the
  connector for the same OAuth reauth reason, so its live status couldn't be corroborated directly this session;
  the command-centre task above is the freshest available proxy for it.</p>

  <h2>Unresolved conflicts</h2>
  <div class="risk-block">
    <p class="risk-head">2025 PDR review document and PDR Toolkit both unreachable (OAuth reauth required)</p>
    <p class="body-loose">See the flag at the top of this brief for the full detail. This is a genuine, named
    blocker (Drew's connector lookup, 13&nbsp;Sep 2026) &mdash; not something left unchecked.</p>
  </div>
  {extra_conflict_html}
"""

    footnote = f"""<div class="footnote">
    Prepared 13 Sep 2026 &middot; Sources: Kevin's own Google Calendar (PDR entry, personal account only &mdash;
    Oxford calendar unreachable this session), command-centre/data/tasks.json (task-1787645383808 and full task
    list, cross-referenced by name), work-inbox (briefing.json/needs_reply.json/triage_ledger.json/
    drafted_replies.json/inbox_suggestions.json &mdash; checked, nothing further found). Oxford OneDrive/SharePoint
    (2025 PDR review docs, PDR Toolkit site, PDR Completion 2026 tracker) genuinely blocked this session &mdash;
    see flag. Granola not checked this session &mdash; worth a follow-up before treating this as complete.<br>
    Draft only &mdash; not committed to meeting-records, not sent or shared with anyone. Rebuild once the Oxford
    connector is reauthenticated to fill in the blocked sections for real.<br>
    Branding: command-centre/BRANDING.md v2.0 (4 Jul 2026) &mdash; Oxford Navy, Inter, canonical crest. Template
    shared with the other speaking briefs via brief_chrome.py.
  </div>"""

    html_out = render_page(
        title=f"PDR 2026 — {display_name}",
        app_name=f"PDR 2026 — {display_name}",
        kicker="Speaking Brief &middot; Draft",
        h1=f"PDR 2026 — {display_name}",
        meta_spans=[
            f"<b>Meeting</b> {meeting_label}",
            f"<b>Date/time</b> {date_status_html}",
            "<b>Status</b> Draft — not yet approved",
        ],
        flag_label="Before anything else",
        flag_paragraphs=BLOCKER_FLAG_PARAGRAPHS,
        glance_label="At a glance",
        glance_sub="Confirmed facts only — see flag for what's blocked",
        glance_table_html=glance_rows,
        sections_html=sections,
        footnote_html=footnote,
    )
    write_brief_output(html_out, f"PDR 2026 - {display_name}")


# ---------------------------------------------------------------------------
# Kevin (reviewee) — reviewer presumed Simon Burford, unconfirmed (Oxford
# calendar unreachable to verify organizer/attendee list directly).
build_person(
    slug="kevin",
    display_name="Kevin Lelitte",
    meeting_label="Kevin's own 2026 PDR review (reviewee) — reviewer presumed Simon Burford, unconfirmed",
    date_status_html="<b>Confirmed</b> Tue 16 Sep 2026, 15:00&ndash;16:00 UK (Kevin's own Google Calendar, "
                      "\"Kevin's PDR Review 2026\")",
    glance_rows="""<table><thead><tr><th>Item</th><th>Status</th></tr></thead><tbody>
      <tr><td>Date/time</td><td><span class="pill pill-resolved">Confirmed</span> 16 Sep, 15:00-16:00 UK</td></tr>
      <tr><td>Reviewer</td><td><span class="pill pill-overdue">Blocked</span> presumed Simon Burford, not verified</td></tr>
      <tr><td>2025 review doc</td><td><span class="pill pill-overdue">Blocked</span> OAuth reauth required</td></tr>
      <tr><td>Simon's own PDR</td><td><span class="pill pill-onhold">Ongoing</span> still unbooked per command-centre</td></tr>
      </tbody></table>""",
    themes=[
        {"id": "1", "title": "Team delivered through repeated absence-coverage gaps",
         "pill": "new", "category": "Leadership / capacity",
         "desc": "Multiple documented periods this year with no meaningful first-line HR Systems cover "
                 "(w/c 6 Jul, 13 Jul gap, end-July with Michael/Beth/Simon/Sarah all out simultaneously), "
                 "overlapping Kevin's own July leave.",
         "say": "I want to talk about how the team held together through several genuine cover gaps this "
                "year, including while I was out myself — what that showed about resilience and where it "
                "needs shoring up."},
        {"id": "2", "title": "SHSMS dedicated resource ask", "pill": "onhold", "category": "Workload advocacy",
         "desc": "Raised the case for dedicated project resource (not BAU capacity) for the H&S Management "
                 "System evaluation/implementation; sent formal position to Marie and Simon 3 Jul.",
         "say": "I made the case in writing for dedicated SHSMS resource back in July — I want to revisit "
                "whether that's actually been resourced or is still riding on BAU capacity."},
        {"id": "3", "title": "Roadmap ownership", "pill": "info", "category": "Delivery",
         "desc": "Per the 27 Aug roadmap alignment pass, Kevin leads 3 active roadmap rows directly (all "
                 "proposed status) — worth a concrete review of what's moved since.",
         "say": "I want to walk through my own live roadmap rows and where they actually stand."},
    ],
    scheduling_risk_html="No risk identified with Kevin's own slot — it's confirmed. The open risk is entirely "
                          "on the reviewer/process side: who's reviewing, and against what documented 2025 "
                          "baseline, given the docx is currently unreachable.",
    docx_name="Kevin Lelitte - PDR Review 2025.docx",
)

# ---------------------------------------------------------------------------
# Michael O'Sullivan
build_person(
    slug="michael",
    display_name="Michael O'Sullivan",
    meeting_label="Kevin reviewing Michael O'Sullivan's 2026 PDR",
    date_status_html="<b>Unresolved</b> originally Fri 18 Sep, Michael requested a reschedule 30 Aug (leave + "
                      "annual-leave-year-end) &mdash; no new date recorded anywhere as of the last note, 9 Sep",
    glance_rows="""<table><thead><tr><th>Item</th><th>Status</th></tr></thead><tbody>
      <tr><td>Date/time</td><td><span class="pill pill-overdue">Unresolved</span> 18 Sep declined, no new date yet</td></tr>
      <tr><td>2025 review doc</td><td><span class="pill pill-overdue">Blocked</span> OAuth reauth required</td></tr>
      <tr><td>Current workload signal</td><td><span class="pill pill-new">High</span> central to Clinical Pay Uplift, WFM, PeopleXD config</td></tr>
      </tbody></table>""",
    themes=[
        {"id": "1", "title": "Clinical Pay Uplift — testing lead", "pill": "resolved", "category": "Delivery",
         "desc": "Confirmed live 27 Jul per meeting-records; Michael led the testing workstream.",
         "say": "Clinical Pay Uplift went live 27 July with you leading testing — that's a real, dateable "
                "delivery worth naming explicitly."},
        {"id": "2", "title": "DTP1092 / Company 90 &ndash; UOXU/UOXC refresh approach", "pill": "onhold",
         "category": "Systems", "desc": "Owns confirming the refresh approach for Company 90 integration "
         "testing (command-centre t2608071801052), alongside the wider REF2029/College-staff-into-PXD workstream.",
         "say": "How's the Company 90 refresh approach landed — are we clean on UOXU vs UOXC now?"},
        {"id": "3", "title": "38-day balance leave scheme — advisory role", "pill": "info", "category": "Advisory",
         "desc": "Advising on GLAM joining the 38-day balance departments scheme and reviewing the wider "
                 "implementation timeline (command-centre t2608111507360, t2608121801280).",
         "say": "Your read on the 38-day balance rollout and GLAM's position in it has been useful — I want "
                "to make sure that's recognised, not just absorbed as background work."},
        {"id": "4", "title": "Repeatedly flagged as highest-risk single point of absence", "pill": "atrisk",
         "category": "Capacity / risk", "desc": "Named directly in the SK 1-1 brief as the highest-risk "
         "absence given his central role across clinical pay uplift, OSPS pension changes, WFM lead, and "
         "PeopleXD config queries.",
         "say": "You've been flagged more than once this year as a single point of failure for several "
                "workstreams at once — I want to talk about whether that's sustainable and what backup "
                "looks like."},
    ],
    scheduling_risk_html="Michael's PDR date is genuinely unresolved — he asked to move off 18 Sep on 30 Aug "
                          "and nothing since confirms a replacement date. This needs resolving before this "
                          "brief is usable for an actual sitting.",
    docx_name="Michael O'Sullivan - PDR Review 2025.docx",
)

# ---------------------------------------------------------------------------
# James Salas Guillen
build_person(
    slug="james",
    display_name="James Salas Guillen",
    meeting_label="Kevin reviewing James Salas Guillen's 2026 PDR",
    date_status_html="<b>Not found</b> &mdash; no PDR calendar entry or command-centre/work-inbox record of a "
                      "booked date exists anywhere checked; confirm directly whether one has been arranged",
    glance_rows="""<table><thead><tr><th>Item</th><th>Status</th></tr></thead><tbody>
      <tr><td>Date/time</td><td><span class="pill pill-overdue">Not found</span> no record of a booked session</td></tr>
      <tr><td>2025 review doc</td><td><span class="pill pill-overdue">Blocked</span> OAuth reauth required</td></tr>
      <tr><td>Scheduling constraint</td><td><span class="pill pill-atrisk">Flag</span> annual leave 25-28 Sep confirmed</td></tr>
      </tbody></table>""",
    themes=[
        {"id": "1", "title": "Cority — SFTP feed, applicant import, ongoing ownership", "pill": "new",
         "category": "Systems ownership", "desc": "Owns/co-owns several live Cority H&S system issues this "
         "year: the 22 Jun SFTP production feed error (t030), the urgent Aug applicant-data-import file "
         "thread with Simon Burford (t2608111331410).",
         "say": "Cority's had several live incidents on your plate this year — SFTP feed, the applicant "
                "import file — I want to talk through what that's shown about the system and your ownership "
                "of it."},
        {"id": "2", "title": "DTP1334 SHSMS Evaluation", "pill": "onhold", "category": "Evaluation",
         "desc": "Reviewing Helen Harbour's briefing and weightings for the H&S Management System evaluation "
                 "(t029); also involved in the SHMS Tender final session (t2608171727070).",
         "say": "Where's your read landed on the SHSMS evaluation weightings?"},
        {"id": "3", "title": "IRIS/IEX incident change timing coordination", "pill": "info",
         "category": "Coordination", "desc": "Confirming IRIS/IEX incident change timings with Amanda "
         "(command-centre t2608271801020).",
         "say": "How's the IRIS/IEX timing coordination with Amanda going?"},
    ],
    scheduling_risk_html="No PDR date could be found for James in any source checked — this needs confirming "
                          "directly rather than assumed booked. Separately, command-centre shows James's "
                          "annual leave confirmed for 25-28 Sep — worth checking against whatever date is "
                          "eventually set.",
    docx_name="James Salas Guillen - PDR Review 2025.docx",
)

# ---------------------------------------------------------------------------
# Asta Palmer
build_person(
    slug="asta",
    display_name="Asta Palmer",
    meeting_label="Kevin reviewing Asta Palmer's 2026 PDR",
    date_status_html="<b>Confirmed</b> Fri 25 Sep 2026, 12:00&ndash;1:00pm (corrected from an initial invite "
                      "sent to Asta Siautilaite in error)",
    glance_rows="""<table><thead><tr><th>Item</th><th>Status</th></tr></thead><tbody>
      <tr><td>Date/time</td><td><span class="pill pill-resolved">Confirmed</span> 25 Sep, 12:00-1:00pm</td></tr>
      <tr><td>2025 review doc</td><td><span class="pill pill-overdue">Blocked</span> OAuth reauth required</td></tr>
      <tr><td>Roadmap ownership</td><td><span class="pill pill-atrisk">Flag</span> leads zero active roadmap rows structurally</td></tr>
      </tbody></table>""",
    themes=[
        {"id": "1", "title": "Holiday Records — 3 reports built", "pill": "resolved", "category": "Delivery",
         "desc": "Three holiday-records reports approved and awaiting scheduling (command-centre "
                 "t1781204987882, case 69001638).",
         "say": "The three holiday records reports are approved and just waiting on scheduling — good, "
                "concrete delivery worth naming."},
        {"id": "2", "title": "Team calendar config investigation", "pill": "onhold", "category": "Systems",
         "desc": "Investigating a team calendar config issue jointly with Michael and Simon "
                 "(command-centre t2608071801051).",
         "say": "How's the team calendar config issue landed — anything still open there?"},
        {"id": "3", "title": "HR Reporting SSO Migration (Roadmap 179)", "pill": "onhold",
         "category": "Systems", "desc": "Associated with the Managed Desktop SSO migration workstream "
         "(t033), currently parked.",
         "say": "SSO migration is parked at the moment — worth checking whether that's still the right call "
                "or just stalled."},
        {"id": "4", "title": "Visibility gap: leads zero active roadmap rows", "pill": "atrisk",
         "category": "Recognition", "desc": "The 27 Aug roadmap alignment pass found Asta leads zero active "
         "roadmap rows — structural, because her work sits under other leads' rows rather than a reflection "
         "of her actual contribution.",
         "say": "I noticed the roadmap doesn't show you leading anything directly, even though you're "
                "clearly doing real work across several rows — I want to make sure that's not a recognition "
                "gap in how the roadmap's structured."},
    ],
    scheduling_risk_html="Asta's date is confirmed and corroborated by two independent command-centre entries "
                          "(27 Aug and 2 Sep) — no risk identified.",
    docx_name="Asta Palmer - PDR Review 2025.docx",
)

print("PDR 2026 prep pack: 4 briefs built (Kevin, Michael O'Sullivan, James Salas Guillen, Asta Palmer).")
