from brief_chrome import render_page, write_brief_output

# ---- Ad hoc supplier scoping meeting: Oxford Holiday Records Reports —
#      Access Group (PeopleXD Insight Reporting), Fri 18 Sep 2026, 14:00-15:00.
#      Attendees: Kevin Lelitte, Simon Burford, Marie Cooksey (Head of HR
#      Systems) (Oxford); Conor O'Shea, Alan Quirke (Access Group).
#
# Source: content already drafted and confirmed with Kevin earlier the same
# day, built from the Athena Artuso (10 Jun) and Ann-Marie Topliss (12 Jun)
# email thread re: Holiday Records Duty / PeopleXD Insight Reporting quote.
# Kevin sent the revised specification and field-list workbook to Conor
# ahead of this meeting so Access can assess scope against them.

DECISIONS = [
    "Confirm the field-list workbook is explicitly in scope, not just the three report titles in the quote.",
    "Ask Access to map every requested field to its source, calculation, report logic, and any unavailable data.",
    "Confirm whether the 4 days covers build, configuration, testing, refinements and deployment &mdash; or only initial build.",
    "Agree report grain and keys: person, appointment, leave year, payroll period (matters for multi-appointment staff).",
    "Resolve overlap for variable-hours employees: Report 1 = leave position, Report 2 = accrual/holiday-pay trail.",
    "Agree UAT acceptance criteria, named testers, test data, sign-off date.",
    "Obtain updated quote, delivery timetable, named consultant availability.",
]

QUESTIONS = [
    "Does the quoted scope cover the field-list workbook?",
    "Which fields come direct from PeopleXD vs need configuration/calculation/payroll data/unavailable?",
    "Can the reports use person + appointment ID consistently for multi-appointment staff?",
    "What exactly will Access build and test in the 4 consultancy days?",
    "What UAT scenarios and acceptance criteria do they propose before live deployment?",
]

UAT_SCENARIOS = [
    "Part-time, term-time and variable-hours employees",
    "Multiple appointments and non-standard departmental leave years",
    "Starter/leaver or a change in hours",
    "Long-service and additional-annual-leave adjustments",
    "Ordinary, sickness and family-leave carry-over",
    "Standard casual vs rolled-up eligible casual worker",
    "Termination with payment in lieu, and with over-taken leave",
]


def li(items):
    return "\n".join(f"          <li>{x}</li>" for x in items)


REPORTS_TABLE = """<div class="table-wrap card">
        <table>
          <thead><tr><th>#</th><th>Report</th><th>Confirm Access can show</th></tr></thead>
          <tbody>
            <tr><td class="idcell">1</td><td>Annual Leave Record by Person and Leave Year</td><td>Entitlement, booked/taken/remaining leave, and carry-over by person and appointment. Ask specifically about different departmental leave years, part-time/term-time treatment, long-service leave, and carry-over reason/expiry.</td></tr>
            <tr><td class="idcell">2</td><td>Holiday Pay and Accrual Record for Variable-Hours and Casual Arrangements</td><td>Clearly distinguishes variable-hours employees, standard casual workers, and rolled-up holiday-pay eligible casual workers. Hours worked, accrual rate, accrued and taken leave, holiday pay, payment date, and payroll reference/pay code.</td></tr>
            <tr><td class="idcell">3</td><td>Holiday Pay in Lieu on Termination</td><td>Entitlement to leaving date, leave taken, untaken balance, rate used, payment/deduction value, and payroll evidence.</td></tr>
          </tbody>
        </table>
      </div>"""

SECTIONS = f"""
  <h2>What's proposed <span class="h2-sub">Three reports named in the Access quote (12 Jun)</span></h2>
  {REPORTS_TABLE}

  <h2>Decisions to get in this meeting</h2>
  <ul class="next-steps">
{li(DECISIONS)}
  </ul>

  <h2>Five questions to ask Access</h2>
  <ul class="ask-list">
{li(QUESTIONS)}
  </ul>

  <h2>Suggested UAT scenarios <span class="h2-sub">Ask Access to demonstrate each before sign-off</span></h2>
  <ul class="next-steps">
{li(UAT_SCENARIOS)}
  </ul>

  <h2 class="h2-warn">Risks to raise</h2>
  <div class="risk-block">
    <p class="body-loose">The specification depends on fields that may not be consistently available upstream: worker category, holiday model, departmental leave year, carry-over reason, payroll transaction/pay-code reference, and rolled-up eligibility.</p>
  </div>
  <div class="risk-block">
    <p class="body-loose">The three reports do not fully solve regular-overtime holiday-pay treatment for fixed-hours employees.</p>
  </div>
  <div class="risk-block">
    <p class="body-loose">The reports alone do not evidence six-year retention, retrievability, or GDPR controls.</p>
  </div>
  <div class="risk-block">
    <p class="body-loose">For salaried staff, leave-to-pay linkage may remain indirect &mdash; holiday pay is normally embedded in salary.</p>
  </div>
  <div class="risk-block">
    <p class="body-loose">Payment in lieu must show the calculation basis, not only the amount, and must also cover over-taken leave deductions.</p>
  </div>

  <h2>What you want to leave with</h2>
  <ul class="next-steps">
    <li>A confirmed list of fields that are in scope.</li>
    <li>A written gap/assumption list for anything not available.</li>
    <li>Confirmation whether the quote needs changing.</li>
    <li>A delivery and UAT timetable, including named owners.</li>
  </ul>

  <h2>If they start discussing individual fields in detail</h2>
  <blockquote><span class="say-label">Say this</span><p>&ldquo;Let's record that as either 'available as standard', 'available with configuration', or 'not currently available', then confirm whether it affects scope, cost or UAT.&rdquo;</p></blockquote>

  <h2>Closing question</h2>
  <blockquote><span class="say-label">Say this</span><p>&ldquo;Can we leave today with the field lists confirmed as the acceptance baseline, a gap log for anything PeopleXD cannot supply, and an updated quote and timetable for UAT and live delivery?&rdquo;</p></blockquote>
"""

FOOTNOTE_HTML = """<div class="footnote">
    Prepared 18 Sep 2026 &middot; Sources: Athena Artuso email 10 Jun 2026 (Holiday Records Duty &mdash; proposed reports), Ann-Marie Topliss email 12 Jun 2026 (PeopleXD Insight Reporting &mdash; Quote Request), revised three-report specification and field-list workbook (sent to Conor O'Shea ahead of this meeting).<br>
    Ad hoc meeting prep &mdash; not one of the standing meeting-records workflows.
  </div>"""

html_out = render_page(
    title="Oxford Holiday Records Reports — Access Group Scoping",
    app_name="Holiday Records Reports — Access Group",
    kicker="Speaking Brief &middot; Ad hoc &middot; Scoping meeting",
    h1="Oxford Holiday Records Reports — Access Group Scoping Call",
    meta_spans=[
        "<b>Date</b> Friday 18 September 2026, 14:00&ndash;15:00",
        "<b>Attendees</b> Kevin Lelitte, Simon Burford, Marie Cooksey (Head of HR Systems) &middot; Conor O'Shea, Alan Quirke (Access Group)",
        "<b>Quote</b> Access Group quotation of 12 Jun 2026 &middot; 4 consultancy days (2.5 Payroll + 1.5 WFM)",
    ],
    flag_label="Opening position",
    flag_paragraphs=[
        "We have a detailed Oxford-specific specification and field lists for the three reports, sent to Conor ahead of today. Before proceeding, confirm these are the build and acceptance baseline, that every field is available from PeopleXD/payroll, and that the quotation still covers the work.",
        "The June quote's 14-day validity (from 12 Jun) has lapsed &mdash; assume it needs reissuing or reconfirming.",
    ],
    sections_html=SECTIONS,
    footnote_html=FOOTNOTE_HTML,
)

write_brief_output(html_out, "Holiday Records Reports - Access Group Scoping")
