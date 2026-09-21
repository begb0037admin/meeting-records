# Content authoring only (data, no rendering logic). Writes content.json for the generator Codex writes.
import json

SAY = {
 "HSB030": "Incident classification and the near-miss field: EcoOnline got in touch on 27 August to start. As far as I can tell this is in the 28 September go-live. Chris is away today, so James, can you confirm the exact list of changes going in?",
 "HSB031": "DSO Review layout: same position as HSB030, EcoOnline started on 27 August and I read it as part of 28 September. I'd like the final change list confirmed against the HSB references.",
 "HSB062": "Field rename to 'Incident Review Findings': same EcoOnline start on 27 August, small change. Just confirming it's in the same release.",
 "HSB096": "Supervisor notification wording: the workbook says Brian signed it off and the risk assessment is done, but Chris's 15 September email asks me to check the GDPR point with Brian. Which is current, and is this in the 28 September set? Delivery date of 11 September has passed.",
 "HSB085": "Safety Officers report: due 30 September, and the only note is 'chase for a response' on 24 August. Is this still on track, and is it part of the 'update reports on IRIS' step in the go-live plan?",
 "HSB075": "Primary job position, inactive clients: PO went through on 24 August and the scoping call with Cority was on 14 September. Their read is that 19 nightly business rules give inconsistent results because our custom rules clash with an out-of-the-box one. Next call is 5 October, 11:30. Owner in the workbook is now James; it was Marie on the last brief, so I just want to confirm that's intended.",
 "HSB076": "Primary job position, active clients: same Cority project and same scoping call. The active-client fault is the NULL Clearance Status blocking the rules. Same 5 October follow-up.",
 "HSB002": "Compliance reporting: the workbook still says On hold, waiting for APC approval since 6 July. But the 14 September Cority call treated compliance reports as priority 2 inside the funded work, and the March funding request included the health surveillance compliance data fix. Can we agree the status is stale and update it?",
 "HSB028": "Outlook and Teams: the statement of work only covers Outlook. Teams needs a Remote Expert licence, roughly $5,000 a year on Cority's quote from a year ago, and the March funding request was a one-off 4,500 pounds. Sophie needs to resolve that before work starts. Separately, central IT need to build the Azure app, and another client took three months.",
 "HSB040": "SMS reminders: Rob Green de-scoped it on 17 August because appointment reminders have improved the DNA rate, and SMS integration also came out of the 14 September statement of work as a third-party dependency. Can we agree this is not proceeding rather than leave it On hold?",
 "HSB061": "Duplicate records: about 80 cleared by 24 August and the automated monthly merge is in place and working. Any movement since, and is the 27 July question about me picking it up still live?",
 "HSB079": "Retention and purge rules: a Must Have, Not started, and it has no owner. The only note is Rob Green's 4 March email. I need us to name an owner today.",
 "HSB050": "Smart notes: still with Cority. Their position on 8 June was that it is an intended feature and an enhancement not on their roadmap, with early access needing Premium Support. My own open items are to chase for a date and decide whether we pursue it or accept the limitation. I'd like a decision.",
 "HSB088": "Immunisation recall auto-population: it was In progress on the 20 August brief and is now On hold, with no note saying why. One of 75 rules was done in March. Is this parked on purpose?",
 "HSB089": "Med Students dashboard: expected delivery was 31 August and it hasn't started. The only note is that GW was emailed on 15 July. Has anything come back?",
 "HSB097": "New report for outstanding health surveillance questionnaires: Not Started, James, no comments yet. I'd like to know whether it goes into the Cority consultancy hours or the BAU queue.",
 "HSB025": "Odyssey monthly returns prompts: the reporting issues were resolved on 16 March and it has been Not Started since. Is anything stopping James picking it up?",
}
ORDER = ["HSB030","HSB031","HSB062","HSB096","HSB085","HSB075","HSB076","HSB002","HSB028","HSB040","HSB061","HSB079","HSB050","HSB088","HSB089","HSB097","HSB025"]
PILL = {"HSB030":"ontrack","HSB031":"ontrack","HSB062":"ontrack","HSB096":"overdue","HSB085":"ontrack","HSB075":"ontrack","HSB076":"ontrack","HSB002":"onhold","HSB028":"ontrack","HSB040":"onhold","HSB061":"ontrack","HSB079":"new","HSB050":"info","HSB088":"onhold","HSB089":"overdue","HSB097":"new","HSB025":"new"}
PILL_TEXT = {"onhold":"On hold","new":"Not started","overdue":"Overdue","ontrack":"In progress","info":"With supplier"}

pre_grid = """
  <h2>Live this week &mdash; IRIS enhancements go live night of Monday 28 September <span class="h2-sub">Source: Chris's IRIS Enhancement Work project plan (file last saved 15 Sept) &middot; H&amp;S Roadmap Granola note 14 Sept &middot; Command Centre / Work Inbox as at Fri 18 Sept</span></h2>
  <div class="table-wrap card">
  <table class="fixed-grid">
    <colgroup><col style="width:36%"><col style="width:13%"><col style="width:17%"><col style="width:34%"></colgroup>
    <thead><tr><th>Step</th><th>Owner</th><th>When</th><th>Status found</th></tr></thead>
    <tbody>
      <tr><td>Update guidance material (DSO Review; supervisor investigations) and update IRIS reports</td><td>Chris</td><td>Due Sat 19 Sept</td><td>Plan shows <b>Not started</b> at the 15 Sept save. Two other guidance documents are marked Completed. Nothing later seen.</td></tr>
      <tr><td>Write test plans (from Chris's change-list email)</td><td>Chris</td><td>Due today, Mon 21 Sept</td><td>Plan shows <b>Not started</b>. Chris is on leave until Tue 22 Sept.</td></tr>
      <tr><td>Testing handover</td><td>James &amp; Kevin</td><td>Plan: Mon 21 Sept<br>14 Sept meeting: Thu 24 Sept</td><td><b>Dates conflict.</b> The plan row still says 21 Sept; the meeting agreed an internal handover with Chris, James and Kevin around Thu 24 Sept because James is away from Fri 25 Sept. No calendar entry for it seen.</td></tr>
      <tr><td>Pre-go-live comms to IRIS users (SHEOx Teams channel)</td><td>Chris</td><td>Tue 22 Sept</td><td>Plan says Tue 22 Sept, one week before go-live. Chris is on leave until Tue 22 Sept (Work Inbox absences), which fits that date.</td></tr>
      <tr><td>Access for system users removed; enhancements made in production</td><td>EcoOnline</td><td>Night of Mon 28 Sept</td><td>EcoOnline have no sandbox or test environment, so changes go straight to production. Date decided (plan row 2 Completed, &ldquo;night of 28/09/2026&rdquo;). Command Centre logs Kevin confirming it on 18 Sept.</td></tr>
      <tr><td>Testing of enhancements; access restored once signed off; guidance published; users and Safety Office told</td><td>James &amp; Kevin (testing); Chris (comms)</td><td>Tue 29 Sept</td><td>James is away Fri 25 to Mon 28 Sept and back on the 29th. The 14 Sept meeting kept it minimal so two people can cover it.</td></tr>
      <tr><td>Debrief / catch-up with EcoOnline</td><td>James</td><td>Plan: Wed 30 Sept<br>14 Sept meeting: day after go-live (29 Sept)</td><td>James to email Amanda Bracks (EcoOnline), copying Joanne Grant (Success Manager). Not confirmed sent. EcoOnline review meeting also requested for Fri 9 Oct, 13:30 or later (Command Centre task t2608271801020).</td></tr>
    </tbody>
  </table>
  </div>

  <h2>Cority consultancy &mdash; scoped 14 September <span class="h2-sub">Granola note 14 Sept 10:29 &middot; workbook comments &middot; 23 Mar funding request</span></h2>
  <div class="risk-block">
    <p class="body-loose">The PO went through on 24 Aug (workbook). A Cority scoping and statement-of-work call took place on 14 Sept (Granola, 10:29), after the workbook was last saved, so its outcome isn't logged there yet. Funded work follows the 23 Mar request for &pound;4,500: primary job position fix (HSB075/076), health surveillance compliance data fix (HSB002), Outlook/Teams integration (HSB028) and SMS reminders (HSB040).</p>
    <ul class="risk-list">
      <li><b>Scope now:</b> SMS integration dropped (third-party dependency). Remaining: 10 hrs Outlook/Teams integration, 10 hrs functional consultancy (primary job position rules, then compliance reports). Health surveillance reminder emails only if hours remain.</li>
      <li><b>Priority 1, primary job position:</b> 19 nightly business rules give inconsistent results; custom rules clash with an out-of-the-box rule; no HR feed for this field, Cority rules alone decide it.</li>
      <li><b>Priority 2, compliance reports:</b> depends on priority 1; the clearance certificate table has no ID linking to the parent SEG.</li>
      <li><b>Outlook/Teams:</b> the statement of work only covers Outlook. Teams needs a Remote Expert licence, about $5,000 a year on a quote from around a year ago. The Azure app needs central IT; another client took three months.</li>
      <li><b>Next call:</b> Mon 5 Oct, 11:30. The week of 28 Sept is kept clear because of the IRIS go-live.</li>
      <li><b>Actions from the call, owners not stated in the note:</b> send production and test URLs to Scott; share business rule details and ticket numbers with Scott; pass the Azure app IT guide to central IT; settle the Teams licence question with Sophie; Kevin to request a test plan and test structure from Cority.</li>
    </ul>
    <p class="body-loose">Speaker check: Sophie is Sophie Levy (Cority Account Executive), confirmed in Command Centre and the funding request. &ldquo;Scott&rdquo; appears only in Granola and could not be corroborated elsewhere.</p>
  </div>

  <h2>Strategic Health and Safety Modular System evaluation (DTP1334) <span class="h2-sub">Work Inbox / Command Centre as at Fri 18 Sept</span></h2>
  <div class="risk-block">
    <p class="body-loose">Helen Harbour emailed on 16 Sept that the first stage of supplier evaluation and moderation is complete, with shortlisting outcome and next steps. Work Inbox holds only the opening line of that email, so the outcome itself is <b>not visible to me</b> &mdash; please read the email directly. Work Inbox triage marked it &ldquo;reply within 48hrs&rdquo; but did not flag it as needing a reply.</p>
    <p class="body-loose">Command Centre (t2608171727070, 21 Aug) recorded three next steps: chase the Entra ID team on the admin guide (target 11 Sept handover to Brian), aggregate evaluator scores, and a resourcing meeting with Simon and Marie on the October resource and squad model ahead of a <b>25 Sept</b> revised roadmap deadline. No later evidence of any of the three was found.</p>
  </div>

  <h2>Other Cority items in flight <span class="h2-sub">Command Centre as at Fri 18 Sept &middot; not backlog items</span></h2>
  <div class="risk-block">
    <ul class="risk-list">
      <li><b>Urgent Cority support call #11707051 / Incident 11706988</b> &mdash; forwarded by Chris on 4 Sept, assigned to Kevin's team. Latest entry (7 Sept): Gillian Wilson responded, investigation underway. No later update seen. (t2609020705201)</li>
      <li><b>Cority employee import (SFTP) errors</b> &mdash; logged 28 Aug and 4 Sept. The 4 Sept task is marked done; the parent task t030 is still open and parked. No later import result seen.</li>
    </ul>
    <p class="body-loose">Command Centre's auto-appended action lines often cite an unrelated email in brackets; the action wording above is used, not the bracketed citation.</p>
  </div>
"""

grid_heading = """
  <h2>Backlog items &mdash; full context <span class="h2-sub">Must Have + In Progress, plus every James/Kevin-owned active item &middot; 17 of 33 active &middot; full dated comment history &middot; expand for background</span></h2>
"""

post_grid = """
  <h2>Closed since the 20 Aug brief <span class="h2-sub">Shown so nothing drops off silently</span></h2>
  <div class="risk-block">
    <ul class="risk-list">
      <li><b>HSB073</b> &mdash; HR data feed into Cardinus &mdash; now <b>Completed</b>, delivered 20 Aug 2026 (SBS filter implemented and working as expected). It was overdue on the last brief.</li>
      <li><b>HSB087</b> &mdash; Prevent chase emails for health surveillance &mdash; now <b>Completed</b>, delivered 25 Aug 2026. A manual checkbox to exclude reminder emails is live in production; awaiting feedback from Karen Ralph. This settles the SEG-scope question that was open on the last brief.</li>
    </ul>
  </div>

  <h2>Carried-forward actions <span class="h2-sub">6 July outcome and 14 Sept notes &middot; nothing removed &middot; status is what I could find, not confirmed</span></h2>
  <div class="table-wrap card">
  <table class="fixed-grid">
    <colgroup><col style="width:42%"><col style="width:14%"><col style="width:12%"><col style="width:32%"></colgroup>
    <thead><tr><th>Action</th><th>Owner</th><th>From</th><th>Status found</th></tr></thead>
    <tbody>
      <tr><td>Follow up with the safety office on the ticket-raising process (all work pre-raised as a ticket, nothing added during on-site sessions)</td><td>Kevin</td><td>6 Jul</td><td>No evidence of closure found.</td></tr>
      <tr><td>Resourcing session with Simon on October resource and squad model</td><td>Kevin</td><td>6 Jul</td><td>Command Centre 21 Aug: to be scheduled on Simon and Marie's return, ahead of the 25 Sept roadmap deadline. No later evidence.</td></tr>
      <tr><td>Find out why dosimetry was not taken forward in the original Odyssey project</td><td>Chris</td><td>6 Jul</td><td>No evidence of closure found.</td></tr>
      <tr><td>Tell stakeholders what is paused and why once funded changes are confirmed</td><td>Not stated</td><td>6 Jul</td><td>Funding for HSB075/076/028 approved 10 Aug (workbook); no evidence the pauses were communicated.</td></tr>
      <tr><td>Copy Rachel Mitchell (and Naomi Hood if she is on leave) into supplier and procurement correspondence</td><td>Kevin</td><td>6 Jul</td><td>Standing instruction; cannot be verified from the data seen.</td></tr>
      <tr><td>Agree Cority timelines once APC funding confirmed; reply to Sophie about the statement of work</td><td>Kevin</td><td>6 Jul</td><td>Likely overtaken: PO went through 24 Aug and the SOW was reviewed on the 14 Sept call. Confirm and close.</td></tr>
      <tr><td>Email Amanda Bracks to confirm 28 Sept and book the post-go-live catch-up, copying Joanne Grant</td><td>James</td><td>14 Sept</td><td>Not confirmed sent.</td></tr>
      <tr><td>Build the IRIS test plan from the change-list email</td><td>Chris</td><td>14 Sept</td><td>Plan row 10 Not started, due 21 Sept.</td></tr>
      <tr><td>Book the internal IRIS handover meeting (Chris, James, Kevin), around Thu 24 Sept</td><td>Not stated</td><td>14 Sept</td><td>No calendar entry seen.</td></tr>
      <tr><td>Ask Lindsay Hale (Business Change) about optional SH SMS process-map sessions</td><td>Kevin</td><td>14 Sept</td><td>The in-person session was 15 Sept; no evidence Kevin attended or asked.</td></tr>
      <tr><td>Send initial IRIS comms to users on Teams</td><td>Chris</td><td>14 Sept</td><td><b>Done</b> &mdash; plan row 4 Completed 14 Sept.</td></tr>
    </tbody>
  </table>
  </div>

  <h2 class="h2-warn">Decisions and questions for Kevin</h2>
  <div class="risk-block">
    <ul class="risk-list">
      <li><b>Attendance and time.</b> Work Inbox lists H&amp;S Roadmap at 10:00 today with Chris as organiser, but Chris is on leave until Tue 22 Sept (Work Inbox absences list, plus his all-day annual leave entry on 18 Sept). Earlier sittings started around 09:00. James has his PDR review at 12:00. Confirm who is in the room and the start time.</li>
      <li><b>Testing handover date.</b> The plan says 21 Sept; the 14 Sept meeting agreed around 24 Sept. Pick one and get it in the diary before James is away.</li>
      <li><b>HSB096 sign-off.</b> Workbook says Brian signed off (24 Aug); Chris's 15 Sept email asks Kevin to check the GDPR risk with Brian. Establish which is current before 28 Sept.</li>
      <li><b>Teams licence.</b> Roughly $5,000 a year is not covered by the &pound;4,500 one-off funding request. Who takes this to Marie or Sophie, and does Outlook-only go ahead first?</li>
      <li><b>HSB002 status.</b> Workbook says On hold awaiting funding; the Cority scope treats it as funded. Agree the status is stale.</li>
      <li><b>HSB079 has no owner</b> and no movement since 4 March. <b>HSB050</b> smart notes needs a pursue-or-park decision.</li>
      <li><b>Owner on HSB075/076:</b> Marie on the 20 Aug brief, James in the workbook now.</li>
    </ul>
  </div>

  <div class="risk-block">
    <p class="risk-head">The workbook is behind the meetings</p>
    <p class="body-loose">The H&amp;S workbook was last saved on 14 Sept at 09:50 and its newest comment is dated 14 Sept. It does not yet record the 14 Sept IRIS go-live decision (HSB030/031/062 stop at 27 Aug), the outcome of the same-day Cority scoping call (HSB075/076/028 only say the meeting was to take place), or why HSB088 moved to On hold. I have not written to it; the shared file is read-only for me.</p>
  </div>

  <h2>Unresolved conflicts</h2>
  <p class="body-loose"><b>Testing handover:</b> plan 21 Sept vs meeting 24 Sept. <b>HSB096 sign-off:</b> workbook vs 15 Sept email. <b>HSB002:</b> workbook On hold vs Cority scope treating it as funded. <b>Debrief with EcoOnline:</b> plan 30 Sept vs 14 Sept meeting 29 Sept. <b>Granola date slip:</b> the 14 Sept summary says follow-up comms &ldquo;Monday 22nd September&rdquo;; 22 Sept is a Tuesday, and the transcript says next Monday, then moved a day because someone was off on the 21st (Chris is the one on leave that day per Work Inbox). Chris's plan agrees (Tue 22 Sept). <b>Which IRIS changes are in the 28 Sept set:</b> the plan does not cite HSB references. HSB030, HSB031, HSB062 and HSB096 are my inference from matching descriptions and the 27 Aug EcoOnline start; HSB017 (relocate supervisor name and email, On hold) is in the November 2025 change request but its status suggests it may not be included. Please confirm the list.</p>
  <p class="body-loose"><b>Speaker identity:</b> Granola's 14 Sept summary uses &ldquo;Work&rdquo; where the transcript shows James (&ldquo;my update and Kevin's update&rdquo;, &ldquo;I'm off the 25th to the 28th&rdquo;). Read as James. Attendees for 14 Sept were Kevin, James and Chris; Granola's own attendee field only shows the recording account.</p>
"""

footnote = """<div class="footnote">
    Generated {{GENERATED}} for the Monday 21 Sept 2026 sitting (calendar entry 10:00 per Work Inbox refreshed Fri 18 Sept 12:14; time to be confirmed) &middot; Sources: HR Systems Workflow Overview &mdash; Health and Safety Systems.xlsx, &quot;Backlog Items&quot; sheet, read from a scratchpad copy of the live OneDrive file (last saved 14 Sept 09:50; original left untouched); IRIS Enhancement Work &mdash; September 2026 &mdash; Project Plan.xlsx (copy, last saved 15 Sept 13:13); March 2026 Cority funding request and November 2025 IRIS change request (copies); Granola live pull &mdash; H&amp;S Roadmap 14/09, 17/08, 06/07 and the 14 Sept Cority scoping call; Work Inbox and Command Centre read-only, as at Fri 18 Sept (nothing after that date seen; Work Inbox mail bodies are truncated).<br>
    Scoped to Must Have or In Progress items plus every James/Kevin-owned active item (17 of 33 active). The 20 Aug brief featured 12; two of those are now Completed (shown above) and seven are newly featured (HSB028, 030, 031, 040, 062, 096, 097). I cannot see the workbook's earlier state, so I cannot say what changed.<br>
    Draft only &mdash; not committed to meeting-records. Nothing published, sent, or scheduled. Generator script is a scratchpad adaptation of build_hs_roadmap.py, not committed (21 Aug pipeline-review freeze).<br>
    Branding: command-centre/BRANDING.md v2.0 &mdash; Oxford Navy, Inter, canonical crest. Template shared via brief_chrome.py.
  </div>"""

content = dict(
 title="Health and Safety Roadmap — 21/09", app_name="Health and Safety Roadmap",
 kicker="Speaking Brief &middot; Draft", h1="Health and Safety Roadmap — 21/09",
 meta_spans=[
  "<b>Meeting</b> Today, Monday 21 September 2026, 10:00 (per calendar, to be confirmed)",
  "<b>Follow-on from</b> H&amp;S Roadmap 14/09 (Granola-verified)",
  "<b>Generated</b> {{GENERATED}}",
  "<b>Status</b> Draft &mdash; not yet approved"],
 flag_label="Before anything else",
 flag_paragraphs=[
  "The dominant topic is the <b>IRIS enhancements going live on the night of Monday 28 September</b>. The go-live plan and the 14 Sept meeting disagree on the testing handover date, and Chris, who owns the test plan and the comms, is on leave until tomorrow. Details are in the first section below.",
  "The backlog workbook was last saved on 14 Sept, so it does not yet reflect the same-day Cority scoping call or the IRIS go-live decision. Work Inbox and Command Centre data stop at Fri 18 Sept, so anything since the weekend is not seen here. Sources are listed in the footnote.",
  "Featured backlog items: 17 of 33 active (Must Have, In Progress, or owned by James or Kevin). Two earlier featured items, HSB073 and HSB087, are now Completed and are listed separately so they do not disappear."],
 pre_grid_html=pre_grid, grid_heading_html=grid_heading, item_order=ORDER, pill=PILL, pill_text=PILL_TEXT, say=SAY,
 post_grid_html=post_grid, footnote_html=footnote)
json.dump(content, open("content.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(json.dumps(content)))
