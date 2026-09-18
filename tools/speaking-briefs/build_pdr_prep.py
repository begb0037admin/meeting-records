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
# UPDATE 14 Sep 2026: Michael O'Sullivan's PDR moved to TODAY (his own
# email this morning, not a scheduled reschedule notice — see his block
# below), and Kevin needed that one done first. Reauth got the mail domain
# working (confirmed via real message/body reads) but SharePoint/calendar
# stayed broken across several rounds, then flapped again after briefly
# working, then a token-rotation collision was root-caused and fixed, then
# attachment-content fetch (as opposed to search/body reads, which work
# fine) hit its own distinct failure modes — a timeout, then a transient
# 404, then a genuine HTTP 403 on the signed download URL for the 2025 doc
# specifically. Full connector incident trail: begb0037admin/drew memory,
# files dated 13-14 Sep 2026 (search "oauth-reauth", "reflapped",
# "cross-machine-root-cause", "still-broken-after-cross-machine-fix",
# "mail-domain-independently-healthy"). Michael's section below now has his
# real, complete 2026 self-review (mail domain succeeded); his 2025 doc is
# confirmed to exist and is precisely named but its content is still
# unreachable (the 403, not the earlier OAuth issue) — flagged accordingly,
# not silently dropped. Kevin/James/Asta's sections are unchanged from
# 13 Sep and still carry the original OAuth-blocked placeholders — pick
# those up next once Michael's meeting is done.
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
#
# UPDATE 14 Sep 2026 (second pass, later same day): Kevin's/James's/Asta's
# sections filled in for real. Drew ran one bounded, mail-domain-only
# connector pass (SharePoint deliberately not touched — confirmed broken
# again that same morning, oauth_token_invalid_grant): James's PDR date was
# FOUND (three 25 Aug 2026 emails: Kevin's booking mail, the invite, and
# James's own acceptance) — Monday 21 Sep 2026, 12:00-1:00pm, resolving the
# 13 Sep "not found" gap and clearing before his confirmed 25-28 Sep annual
# leave. Kevin's and Asta's 2025 review docs were both confirmed to exist
# (found by name/date/size via mail search) but their actual text remained
# unreachable — a distinct download-layer failure (WinError 10061, then
# HTTP 403 for Kevin's; WinError 10061 then a Codex-side retry-policy
# refusal for Asta's), not the original SharePoint OAuth issue. Asta's real
# stored filename also turned out to have no "2025" in it ("Asta Palmer -
# PDR Review.docx"). James's own 2025 doc was not attempted this pass (one
# bounded pass, per pacing rules) — still carries the original generic
# OAuth-blocked flag, now known be be possibly a different failure mode.
# Full record: begb0037admin/drew, memory/codex-m365-mail-attachment-
# download-winerror-10061-14sept.md.

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


def recap_2025_block(name, docx_name, blocked_reason=None):
    reason = blocked_reason or (
        f"<b>Blocked</b> &mdash; source document &ldquo;{docx_name}&rdquo; is unreachable this "
        "session (Oxford M365 connector OAuth reauth required, see flag above). Nothing below is invented or "
        "inferred from memory; rerun this build once the connector is reauthenticated to populate this "
        "table for real.")
    return f"""<div class="table-wrap card">
        <table>
          <thead><tr><th>Achieved</th><th>Not achieved / carried forward</th><th>Notes</th></tr></thead>
          <tbody>
            <tr><td colspan="3">{reason}</td></tr>
          </tbody>
        </table>
      </div>"""


def build_person(slug, display_name, meeting_label, date_status_html, themes,
                  scheduling_risk_html, docx_name, extra_conflict_html="", extra_section_html="",
                  blocked_reason=None, recap_label="2025 recap",
                  recap_sub="What was achieved, what wasn't, what carries forward"):
    items_html = "\n".join(render_theme(t) for t in themes)

    sections = f"""
  <h2>{recap_label} <span class="h2-sub">{recap_sub}</span></h2>
  {recap_2025_block(display_name, docx_name, blocked_reason)}
  {extra_section_html}

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
                          "baseline, given the docx's content is unreachable (though the document itself is "
                          "now confirmed to exist).",
    docx_name="Kevin Lelitte - PDR Review 2025.docx",
    blocked_reason=("<b>Found, not blocked-and-unknown</b> &mdash; Drew's mail-domain connector pass "
                     "(14&nbsp;Sep&nbsp;2026) confirmed a matching email: Kevin's own sent message, "
                     "24&nbsp;Sep&nbsp;2025 12:09:30&nbsp;UTC, subject &ldquo;Kevin - PDR Review&rdquo;, "
                     "132,315-byte attachment. The connector found and identified it correctly, but "
                     "downloading the signed URL to extract the actual text failed &mdash; first "
                     "<code>WinError 10061</code> (connection refused), retry got <code>HTTP 403: "
                     "Forbidden</code> &mdash; a download-layer block, distinct from the earlier SharePoint "
                     "OAuth issue (SharePoint itself wasn't touched this pass). Not re-attempted beyond the "
                     "one retry, per connector-pacing instructions."),
)

# ---------------------------------------------------------------------------
# Michael O'Sullivan — updated 14 Sep 2026, meeting is TODAY. Michael emailed
# his completed 2026 self-review form this morning (09:10:22 BST); full text
# retrieved live via the mail-domain connector (working) — SharePoint/
# calendar domains were not, so the reschedule-to-today date and the 2025
# comparison doc both come from what the mail thread itself revealed, not
# from those blocked domains. See MICHAEL_2026_SUBMISSION below for the
# real, complete extracted content — nothing in it is invented.
MICHAEL_2026_SUBMISSION = """<div class="table-wrap card">
    <p class="body-loose" style="margin-top:0;"><b>Source:</b> Michael's email today, 14 Sep 2026 09:10:22 BST
    (&ldquo;RE: PDR 2026 &ndash; Friday 18 September&rdquo;) &mdash; &ldquo;Ahead of my PDR review this afternoon,
    please find completed form. I've literally just finished this so apologies not to get it back before now.&rdquo;
    Attachment &ldquo;PDR Review Form - 14-SEP-2026.docx&rdquo; (138,258 bytes), full text retrieved live.</p>
    <p class="body-loose"><b>Performance &mdash; looking back:</b> Full-time on the WFM (Workforce Management)
    Project through to March 2026 (project itself ran to April 2026), then transitioned back to BAU Functional
    Analysis &mdash; but WFM kept generating BAU workload (incidents/service requests/queries) even while he was
    meant to be fully allocated to it. Kept contributing to BAU throughout: ~37% of the FA team's incident-related
    tasks completed Sep 2025&ndash;Feb 2026 even while full-time on WFM, rising to a &ldquo;very high
    percentage&rdquo; since formally returning to BAU in March. Operational Support/OSM: <b>79 Change Requests
    completed over the 12 months</b> &mdash; named examples include Clinical Pay Uplift, PeopleXD Oxford Living
    Wage Uplift 2026, several pension/compliance changes (NHS 2015 Scheme, NHS ERRBO, NHS AVC, USS Future
    Service/Career Revalued DB AVC salary exchange), Sickness Absence Return workflow config, WFM Balance Period
    End 2025, Employee Co-Workers Calendar, PeopleXD UK Payroll Year End 2025/26, HESA category defaults, and
    email template updates post website migration. Legacy ownership: corrected/enhanced the PERDEP02 report suite
    (Change #20019074) &mdash; restored Target End Date filtering/MAX_TARGET_END logic, added End of FTC Reason
    fields, applied a new Division parameter consistently. Collaboration cited with Business Change, Training,
    Service/Support Desk, EDU &mdash; specifically the EDU collaboration on Gender Validation for HMRC RTI
    compliance.</p>
    <p class="body-loose"><b>Values:</b> ties back to Professional Services Together (People, Collaboration,
    Quality) via the same WFM/BAU transition narrative.</p>
    <p class="body-loose"><b>Looking forward / development:</b> wants to keep developing within Functional
    Analysis; no specific development ask made; states he's &ldquo;happy in current role&rdquo;; values regular
    feedback; wants more complex changes and more cross-team work.</p>
    <p class="body-loose"><b>Career aspirations:</b> no specific aspiration stated &mdash; again &ldquo;happy in
    current role&rdquo;, wants to keep deepening HR systems expertise, cites the WFM Project as valuable
    groundwork.</p>
    <p class="body-loose" style="margin-bottom:0;"><b>Manager summary section:</b> left blank in the form &mdash;
    that's Kevin's part to complete, expected, not a gap in the submission.</p>
  </div>
  <div class="risk-block" style="margin-top:1.2rem;">
    <p class="risk-head">Comparing to 2025 &mdash; what to check, since the 2025 text itself isn't in this brief</p>
    <p class="body-loose">The 2025 PDR (<code>Michael - PDR Review Form 29SEP2025.docx</code>, confirmed to exist
    as an attachment on Kevin's own 25 Aug email to Michael) couldn't be pulled into this brief &mdash; see the
    2025 recap section above for why. Kevin already has this file in his own sent mail and can open it directly
    in the minutes before the meeting if a side-by-side matters more than this brief's turnaround allowed for.
    Worth checking specifically: (1) did last year's forward-look flag the WFM Project as the big 2026 theme, or
    has it landed as a surprise scale of BAU overlap; (2) was a development ask or career aspiration raised last
    year that this year's &ldquo;happy in current role, no specific ask&rdquo; represents a change from &mdash;
    worth probing gently rather than taking the blank answer at face value; (3) whether the 79-change-request
    volume this year reads as more, less, or about the same as whatever throughput was reported/expected in 2025.</p>
  </div>"""

build_person(
    slug="michael",
    display_name="Michael O'Sullivan",
    meeting_label="Kevin reviewing Michael O'Sullivan's 2026 PDR",
    date_status_html="<b>Confirmed — TODAY</b>, 14 Sep 2026, this afternoon (Michael's own email this morning: "
                      "&ldquo;ahead of my PDR review this afternoon&rdquo;) &mdash; originally booked for 18 Sep, "
                      "rescheduled since; exact time not stated in the email itself, only &ldquo;this "
                      "afternoon&rdquo;",
    themes=[
        {"id": "1", "title": "WFM Project transition back to BAU — dual-loaded all year", "pill": "new",
         "category": "Capacity / delivery", "desc": "His own submission: full-time on WFM to March 2026, but kept "
         "delivering ~37% of FA team's incident work throughout, then a very high share since returning to BAU. "
         "Corroborates the SK&nbsp;1-1 brief's repeated flag of him as highest-risk single point of absence.",
         "say": "The WFM/BAU overlap you've described — nearly 40% of incident work even while notionally "
                "full-time on WFM — is a bigger ask than the project plan probably accounted for. I want to "
                "talk about whether that's sustainable going forward, not just note it as a 2025-26 fact."},
        {"id": "2", "title": "79 Change Requests delivered", "pill": "resolved", "category": "Delivery",
         "desc": "Includes Clinical Pay Uplift, PeopleXD Oxford Living Wage Uplift 2026, multiple NHS/USS "
         "pension compliance changes, Sickness Absence Return workflow config, PeopleXD UK Payroll Year End "
         "2025/26, and more — a real, high-volume delivery record for the year.",
         "say": "79 change requests this year, across some genuinely high-stakes ones — Clinical Pay Uplift, "
                "the payroll year end work — that's a lot to name explicitly rather than let blur into "
                "\"BAU as usual.\""},
        {"id": "3", "title": "PERDEP02 legacy report fix (Change #20019074)", "pill": "info",
         "category": "Technical ownership", "desc": "Restored Target End Date filtering/MAX_TARGET_END logic, "
         "added End of FTC Reason fields, applied a consistent Division parameter — real technical ownership of "
         "an inherited report suite, not just new-build work.",
         "say": "The PERDEP02 fix is a good example of taking ownership of something inherited and broken, "
                "not just building new things — worth naming as its own point."},
        {"id": "4", "title": "Cross-team collaboration — EDU / Gender Validation / HMRC RTI", "pill": "info",
         "category": "Collaboration", "desc": "Specifically cited EDU collaboration on Gender Validation for "
         "HMRC RTI compliance, alongside Business Change, Training, and Service/Support Desk.",
         "say": "The EDU collaboration on HMRC RTI compliance is a good concrete example if we're talking about "
                "cross-team work — worth asking what made that one work well."},
        {"id": "5", "title": "\"Happy in current role\" — no development ask or aspiration stated", "pill": "atrisk",
         "category": "Development", "desc": "Both the development and career-aspiration sections say he's happy "
         "in his current role with no specific ask, though he does want more complex changes and more "
         "cross-team work. Worth probing gently rather than taking at face value, especially given the capacity "
         "strain already flagged above.",
         "say": "You've said you're happy where you are and don't have a specific development ask — I want to "
                "make sure that's genuinely where you're at, not just not wanting to add to an already full "
                "plate. What would \"more complex changes, more cross-team work\" actually look like for you?"},
    ],
    scheduling_risk_html="Confirmed for today — the only open detail is the exact time, which Michael's email "
                          "doesn't state (\"this afternoon\" only). Worth a quick check of the actual invite if "
                          "that matters before walking in.",
    docx_name="Michael - PDR Review Form 29SEP2025.docx",
    blocked_reason=("<b>Found, not blocked-and-unknown</b> &mdash; confirmed to exist as an attachment on "
                     "Kevin's own 25&nbsp;Aug&nbsp;2026 13:17&nbsp;BST sent email to Michael (alongside a blank "
                     "template, <code>PDR Review Form - PDR Refresh - 22.05.2024 v1.docx</code>, not this one). "
                     "The connector found and fetched the message/attachment reference correctly, but extracting "
                     "the actual document text failed twice with <code>HTTP 403: Forbidden</code> on the signed "
                     "download URL &mdash; a distinct failure from the earlier OAuth/timeout issues, looks like a "
                     "connector sandbox restriction on out-of-band binary downloads specifically. Not fixed by a "
                     "further retry. Kevin already has this exact file in his own sent mail if a direct read is "
                     "needed before this afternoon's meeting."),
    extra_section_html=f"""
  <h2>What Michael submitted this morning <span class="h2-sub">Full 2026 self-review, extracted live from his email attachment</span></h2>
  {MICHAEL_2026_SUBMISSION}""",
)

# ---------------------------------------------------------------------------
# James Salas Guillen
build_person(
    slug="james",
    display_name="James Salas Guillen",
    meeting_label="Kevin reviewing James Salas Guillen's 2026 PDR",
    date_status_html="<b>Confirmed</b> Mon 21 Sep 2026, 12:00&ndash;1:00pm UK &mdash; found via mail-domain "
                      "connector search 14 Sep 2026 (three 25 Aug 2026 emails: Kevin's booking mail "
                      "&ldquo;PDR 2026 &ndash; Monday 21 September&rdquo;, the invite &ldquo;James Salas "
                      "Guillen - PDR Review 2026&rdquo;, and James's own &ldquo;Accepted: James Salas "
                      "Guillen - PDR Review 2026&rdquo;) &mdash; not previously found in Google Calendar, "
                      "command-centre, or work-inbox, which is why the 13 Sep pass came up empty",
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
    scheduling_risk_html="Resolved 14 Sep 2026 — booked for Mon 21 Sep 2026, 12:00-1:00pm, accepted by James "
                          "(found via mail-domain connector search after the 13 Sep pass found nothing in "
                          "Google Calendar, command-centre, or work-inbox). No conflict with his confirmed "
                          "25-28 Sep annual leave — the review lands comfortably before it.",
    docx_name="James Salas Guillen - PDR Review 2025.docx",
    blocked_reason=("Not attempted this session &mdash; only Kevin's and Asta's 2025 docs were pulled in the "
                     "14&nbsp;Sep&nbsp;2026 mail-domain pass, per the connector-pacing rule of one bounded "
                     "pass at a time. Kevin's and Asta's own docs were both found to exist but blocked at "
                     "the download layer (<code>WinError 10061</code>/<code>HTTP 403</code>), a different "
                     "failure mode from the original SharePoint OAuth issue this row still names &mdash; "
                     "worth trying James's the same way next pass rather than assuming it's identical."),
)

# ---------------------------------------------------------------------------
# Asta Palmer
build_person(
    slug="asta",
    display_name="Asta Palmer",
    meeting_label="Kevin reviewing Asta Palmer's 2026 PDR",
    date_status_html="<b>Confirmed</b> Fri 25 Sep 2026, 12:00&ndash;1:00pm (corrected from an initial invite "
                      "sent to Asta Siautilaite in error)",
    themes=[
        {"id": "1", "title": "Holiday Records — 3 reports built", "pill": "resolved", "category": "Delivery",
         "desc": "Three holiday-records reports approved; kickoff call with Access Group confirmed for "
                 "2pm Fri 18 Sep 2026, calendar invite still awaited as of the last logged update "
                 "(command-centre t1781204987882, case 69001638).",
         "say": "The three holiday records reports are approved, and the Access Group kickoff call is "
                "locked in for the 18th — good, concrete delivery worth naming."},
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
    docx_name="Asta Palmer - PDR Review.docx",
    blocked_reason=("<b>Found, not blocked-and-unknown</b> &mdash; the real stored filename is "
                     "&ldquo;Asta Palmer - PDR Review.docx&rdquo;, with no &ldquo;2025&rdquo; in it (unlike "
                     "Kevin's/James's/Michael's naming pattern). Drew's "
                     "mail-domain connector pass (14&nbsp;Sep&nbsp;2026) confirmed a matching email: Asta's "
                     "own message to Kevin, 15&nbsp;Sep&nbsp;2025 14:28:52&nbsp;UTC, subject &ldquo;RE: "
                     "Preparing for Your Upcoming PDR&rdquo;, 136,056-byte attachment. Downloading the "
                     "signed URL failed with <code>WinError 10061</code> (connection refused); the retry "
                     "was refused outright by Codex's own internal safety guard as exceeding the one-retry "
                     "pacing limit, not a second network failure. Not re-attempted this session."),
)

print("PDR 2026 prep pack: 4 briefs built (Kevin, Michael O'Sullivan, James Salas Guillen, Asta Palmer).")
