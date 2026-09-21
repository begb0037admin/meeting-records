# Authors the pending-draft payload (content only) for meeting.lelitte.co.uk hs-roadmap 2026-09-21.
import json, hashlib, datetime
from author_content import SAY  # reuses the authored say lines (re-runs author_content, harmless)

BRIEF = "Full brief: OneDrive - Nexus365\\Meetings\\Meetings\\Health and Safety Roadmap\\Health and Safety Roadmap - 21-09-2026.html"

def src(*pairs):
    return [{"kind": k, "ref": r} for k, r in pairs]

items = [
 dict(itemId="itm_hs_iris_golive", title="IRIS enhancements go live, night of Mon 28 Sept", tone="update", priority=1,
  detail="Date decided: night of Mon 28 Sept (plan row 2 Completed; Granola 14/09; Command Centre logs Kevin confirming 18 Sept). EcoOnline have no sandbox, changes go straight to production. EcoOnline remove access and make the changes on the night; James and Kevin test Tue 29 Sept; access restored after sign-off.\n\nPlan status (file saved 15 Sept): guidance updates and IRIS report updates due 19 Sept are Not started; test plans due 21 Sept Not started. Chris is on leave until Tue 22 Sept (Work Inbox absences). Pre-go-live comms to users Tue 22 Sept. James away Fri 25 to Mon 28 Sept, back 29th.\n\nOpen question: the plan does not cite HSB references. HSB030, HSB031, HSB062, HSB096 look like the set (EcoOnline started 27 Aug); HSB017 (supervisor name/email relocation, On hold) is in the Nov 2025 change request but may not be included. Confirm the change list.\n\n" + BRIEF,
  speakerNoteSeed="The IRIS changes go live the night of Monday 28 September. EcoOnline have no test environment, so it is production only. I want the exact change list confirmed against the HSB references, and to know where the guidance updates and test plan stand while Chris is away until tomorrow.",
  sources=src(("workbook","HSB030"),("workbook","HSB031"),("workbook","HSB062"),("workbook","HSB096"),("iris-plan","IRIS Enhancement Work - September 2026"),("granola","not_11HR2RMim2Hkbj"),("command-centre","t2608271801020"))),
 dict(itemId="itm_hs_iris_handover", title="IRIS testing handover: 21 Sept (plan) or Thu 24 Sept (14 Sept meeting)?", tone="decision-needed", priority=1,
  detail="Plan row 11 (testing handover, James and Kevin) says Mon 21 Sept. The 14 Sept meeting agreed an internal handover with Chris, James and Kevin around Thu 24 Sept, because James is away from Fri 25 Sept. No calendar entry seen. Test plan (Chris, plan row 10) due 21 Sept, Not started at the 15 Sept save. Debrief with EcoOnline: plan Wed 30 Sept, 14 Sept meeting said the day after go-live (29 Sept); James to email Amanda Bracks copying Joanne Grant, not confirmed sent.",
  speakerNoteSeed="The plan says the testing handover is today, but on 14 September we agreed Thursday 24th because James is away from the 25th. I want one date in the diary today, and the test plan from Chris before then.",
  sources=src(("iris-plan","rows 10, 11, 22"),("granola","not_11HR2RMim2Hkbj"))),
 dict(itemId="itm_hs_hsb096", title="HSB096 Supervisor notification: is it signed off?", tone="raise", priority=1,
  detail="Workbook (24/08/2026): Brian has signed off the change, risk assessment completed, change to be coordinated with supplier once RA signed by Brian. Command Centre (15 Sept): Chris asks Kevin to check the GDPR risk with Brian on the supervisor notification email content. Expected delivery was 11 Sept, now passed. Establish which is current and whether it is in the 28 Sept set.",
  speakerNoteSeed=SAY["HSB096"], sources=src(("workbook","HSB096"),("command-centre","t2609082321250"))),
 dict(itemId="itm_hs_hsb085", title="HSB085 Safety Officers report", tone="update", priority=2,
  detail="In progress, Chris, due 30 Sept. Only note: 24/08/2026 'Chase for a response'. Possibly linked to the plan's 'Update reports on IRIS' step (due 19 Sept, Not started at the 15 Sept save); that link is my inference.",
  speakerNoteSeed=SAY["HSB085"], sources=src(("workbook","HSB085"),("iris-plan","row 9"))),
 dict(itemId="itm_hs_cority_pjp", title="Cority consultancy: primary job position rules (HSB075/076)", tone="update", priority=1,
  detail="PO went through 24 Aug (workbook). Cority scoping and statement-of-work call 14 Sept (Granola 10:29): priority 1 is the primary job position rules (19 nightly rules, inconsistent results, custom rules clash with an out-of-the-box rule); priority 2 compliance reports. SMS integration dropped from scope. Next call Mon 5 Oct 11:30; week of 28 Sept kept clear. Actions from the call (owners not stated): send prod/test URLs to Scott, share business rule details and ticket numbers, pass the Azure app IT guide to central IT, Kevin to request a test plan. 'Scott' appears only in Granola. Owner of HSB075/076 is James in the workbook; Marie on the 20 Aug brief.",
  speakerNoteSeed=SAY["HSB075"], sources=src(("workbook","HSB075"),("workbook","HSB076"),("granola","not_Kr3cDdaQJmbav6"))),
 dict(itemId="itm_hs_cority_teams", title="Outlook/Teams integration and the Teams licence (HSB028)", tone="decision-needed", priority=1,
  detail="The statement of work covers Outlook only (10 hrs). Teams needs a Remote Expert licence, about $5,000 a year on a quote from around a year ago (Granola). The 23 Mar funding request (4,500 pounds, signed off by Marie Cooksey) was described as a one-off development charge. The Azure app needs central IT; another client took three months. Sophie Levy (Cority) to resolve the Teams licence question before work starts.",
  speakerNoteSeed=SAY["HSB028"], sources=src(("workbook","HSB028"),("granola","not_Kr3cDdaQJmbav6"),("funding-request","23 Mar 2026"))),
 dict(itemId="itm_hs_status_align", title="Workbook status: HSB002 compliance reporting and HSB040 SMS reminders", tone="decision-needed", priority=2,
  detail="HSB002 is On hold (Marie), last note 6 July 'Provisional funding secured. Awaiting approval from APC'. The 23 Mar funding request included the health surveillance compliance data fix and the 14 Sept Cority scope treats compliance reports as priority 2, so the workbook status looks stale. HSB040 SMS reminders is On hold; Rob Green de-scoped it 17 Aug (appointment reminders improved DNA rate) and SMS integration left the SOW on 14 Sept. Agree the statuses; Lauren has not written to the workbook.",
  speakerNoteSeed=SAY["HSB002"] + " " + SAY["HSB040"], sources=src(("workbook","HSB002"),("workbook","HSB040"),("granola","not_Kr3cDdaQJmbav6"))),
 dict(itemId="itm_hs_shsms", title="Strategic Health and Safety Modular System evaluation (DTP1334)", tone="fyi", priority=2,
  detail="Helen Harbour emailed 16 Sept that the first stage of supplier evaluation and moderation is complete, with shortlisting outcome and next steps. Work Inbox holds only the opening line, so the outcome is not visible to Lauren; read the email directly. Command Centre (21 Aug) next steps: Entra ID admin guide (target 11 Sept handover to Brian), aggregate evaluator scores, resourcing meeting with Simon and Marie before the 25 Sept revised roadmap deadline. No later evidence found.",
  speakerNoteSeed="For awareness: the first stage of the supplier evaluation is complete and Helen has sent the shortlisting outcome. I am reading it today and will bring next steps back.",
  sources=src(("work-inbox","Helen Harbour 16 Sept"),("command-centre","t2608171727070"))),
 dict(itemId="itm_hs_hsb079", title="HSB079 Retention and purge rules: no owner", tone="raise", priority=2,
  detail="Must Have, Not started, unassigned. Start date 1 Jul 2026 in the workbook. Only note: 04/03/26 Rob Green emailed asking how retention periods are managed on Cority; business rules needed to archive, purge and delete records.",
  speakerNoteSeed=SAY["HSB079"], sources=src(("workbook","HSB079"))),
 dict(itemId="itm_hs_hsb050", title="HSB050 Smart notes: pursue or park", tone="decision-needed", priority=2,
  detail="With supplier, owner Kevin. Cority position 8 June (Command Centre t002): intended feature, enhancement not on roadmap, early access needs Premium Support. Workbook last note 6 July: on hold until the funding work. t002 is marked done but its own log ends on two open TODOs: chase Cority for a firm date; decide whether to pursue via sales/account route or accept as a known limitation.",
  speakerNoteSeed=SAY["HSB050"], sources=src(("workbook","HSB050"),("command-centre","t002"))),
 dict(itemId="itm_hs_bau", title="Cority BAU queue: HSB061, HSB088, HSB089, HSB097, HSB025", tone="update", priority=3,
  detail="HSB061 duplicates: about 80 cleared by 24 Aug, automated monthly merge working. HSB088 immunisation recalls: now On hold (was In progress on the 20 Aug brief), no reason logged, 1 of 75 rules done. HSB089 Med Students dashboard: expected 31 Aug, Not started, only note is GW emailed 15 July. HSB097 outstanding questionnaires report: Not started, no comments (appears newly added). HSB025 Odyssey monthly returns prompts: Not started since reporting issues resolved 16 Mar. All James-owned. Closed since 20 Aug: HSB073 Cardinus feed (delivered 20 Aug), HSB087 chase-email suppression (delivered 25 Aug).",
  speakerNoteSeed="Quick pass on the Cority queue: duplicates are being cleared by the monthly merge, immunisation recalls has moved to On hold with no reason, and the Med Students dashboard is past its 31 August date. James, is any of this stuck?",
  sources=src(("workbook","HSB061"),("workbook","HSB088"),("workbook","HSB089"),("workbook","HSB097"),("workbook","HSB025"))),
 dict(itemId="itm_hs_actions", title="Carried-forward actions to confirm or close", tone="update", priority=3,
  detail="From 6 July, no evidence of closure found: Kevin to follow up with the safety office on the ticket-raising process; Kevin and Simon resourcing session (Oct resource and squad model, ahead of 25 Sept roadmap deadline); Chris to find why dosimetry was not taken forward in Odyssey; communicate paused roadmap items to stakeholders. From 14 Sept: James to email Amanda Bracks (copy Joanne Grant); Chris to build test plan; book internal handover meeting; Kevin to ask Lindsay Hale about SH SMS sessions. Done: initial IRIS comms on Teams (plan row 4). Nothing removed without Kevin's confirmation.",
  speakerNoteSeed="Let's confirm which of the carried-forward actions from July and 14 September are done, so nothing sits open by default.",
  sources=src(("meeting-records","H&S Roadmap 6 Jul"),("granola","not_11HR2RMim2Hkbj"))),
]
for i, it in enumerate(items, start=1):
    it["position"] = i
    it["status"] = "open"
generated = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
payload = dict(meetingId="hs-roadmap", date="2026-09-21", items=items, generatedAt=generated,
  sourceLabel="Lauren draft 21 Sept: H&S workbook copy (saved 14 Sept), IRIS plan (15 Sept), Granola 14/09, Work Inbox/Command Centre to 18 Sept",
  sourceDigest="sha256:" + hashlib.sha256(json.dumps(items, sort_keys=True).encode()).hexdigest())
json.dump(payload, open("pending_hs_2026-09-21.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("items", len(items), "max detail", max(len(i["detail"]) for i in items))
