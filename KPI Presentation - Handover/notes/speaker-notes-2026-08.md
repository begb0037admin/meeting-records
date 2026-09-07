# Speaker notes — August 2026 KPI Presentation

Authored by Lauren (content), drafted 7 Sep 2026. Voice, length, and per-slide
structure matched to the established pattern across March–June 2026 (the
July and August decks had been silently carrying June's notes forward
unchanged — see `docs/decisions/` / HANDOVER for the process-gap writeup).
Every figure below is cross-checked against the built August 2026 deck's own
tables and the underlying source data — see the cross-check table in
`docs/sessions/2026-08-KPI-run.md`. Slides 1 and 11 carry no notes, matching
every month since March.

Standing lines carried forward from prior months, updated where the
underlying fact has changed: H&S "still building the dataset" (Slide 2),
"not sitting idle with us — waiting on customer/third party" (Slide 3),
WFM-complete / settled BAU footprint (Slide 5), small-team-no-slack /
capacity-not-performance (Slides 6, 7, 10), "consistently green throughout
2026" (Slide 8), the fixed historical peak-trend anchors — Feb 2025 8.3
days, Oct 2025 6.5, Jan 2026 4.1 — reused every month regardless of the
chart's rolling 15-month window (Slide 9).

Format note: parsed by `build_kpi_presentation.py`'s `load_month_notes()` —
`## Slide N` headers (1-based slide number), body is the exact speaker-notes
text for that slide. Do not add slides 1 or 11.

## Slide 2

For H&S – in August we handled 23 tasks in total, down eight on July's 31. Cority fell from 17 to 11, IRIS from 9 to 5, and Odyssey rose from 5 to 7. DSE recorded no activity again this month. This month-to-month shuffling between the three systems is natural variation – occupational health work tends to be reactive and unpredictable rather than following a consistent pattern. As you know we're still building the dataset for H&S, so the trend will become clearer as the year goes on.

## Slide 3

Looking at how quickly H&S tasks were resolved – 27 tasks were completed in August, down from 41 in July. The 6+ day band is back to being the largest at 14 tasks, 51.9% of the total, up from 46.3% in July. Same-day resolution fell to 8 tasks (29.6%), next-day to 1, and 3–5 days to 4. As always, the 6+ day cases are mostly tasks waiting on the customer for information, or on a third party to respond – they're not sitting idle with us. With overall H&S volume this low, one or two long-running cases move these percentages around a lot.

## Slide 4

August came in at 504 PXD tasks across all categories, up from 418 in July. Year-on-year that's 504 against 288 in August 2025 – a 75 percent increase, so volume is well ahead of where we were twelve months ago. Service requests drove almost all of the movement, up from 246 to 368. Incident – Other went the other way, down from 100 to 66. HR Self Service was broadly flat at 53, and Change ticked up from 16 to 17. Volumes across these categories keep moving month to month; we'll keep tracking the pattern.

## Slide 5

Looking at where the work came from. On service requests, Manager Self Service was again the single biggest category at nearly half the total, 48 percent at 177 tasks. Work Group followed at 86 and Add New Shift Type at 64. Together those three account for around 89 percent of all service request work. With the WFM project complete and all departments live, these volumes are a settled picture of BAU support – the ongoing operational footprint of a fully deployed system, and a useful baseline for what WFM support looks like month to month.

On the incident side, this table shows last month's non-self-service incident tasks by service category – 61 in total. People Management led at 31, with Time and Attendance at 18; together those two account for around 80 percent of the reactive work. The rest is spread thinly across Data Protection, Work Groups, Payroll and a handful of one-off categories, grouped here as "Other". Note this 61 is a narrower cut than the Incident – Other figure on the previous slide, which uses a different Ivanti grouping over a rolling window – the caption on the slide explains the difference. With WFM fully live, this is the level of ongoing demand we should expect to carry each month.

## Slide 6

Service requests stayed strong in August, though the five-day measure slipped. Same or next day came in at 83 percent – down a little on July's 87, but still comfortably above the 75 percent green threshold. Less than five days was 91 percent, down from July's 99.6, which puts it into the amber band this month rather than green. 239 of the 368 service requests were completed on the day they came in. Holding these numbers on a small team is still worth acknowledging – the dip on the five-day measure tracks the jump in service request volume, from 246 last month to 368.

## Slide 7

Incident completion times remain a mixed picture. Same or next day came in at 73.8 percent – back inside the 65 to 75 percent amber band, a small step down from July's 75.4, which had just tipped into green. Less than five days improved to 88.5 percent, up from July's 78.5, but still short of the 90 percent amber threshold, so it stays red. Incident – Other tasks can be complex – cases where it takes longer to pin down the root cause. With the team also handling 368 service requests this month, the time available for that investigative work gets squeezed. Seven tasks ran to six or more days. It seems like a small number, but on a small team with no slack, it's about capacity, not performance.

## Slide 8

Task acceptance time was 0.2 days in August, down from 1.0 in July, and a long way better than the 1.7 days we were at this time last year. Tasks are typically being picked up the same day they come in – well inside the green threshold. This metric has been consistently green throughout 2026. A clean result, and a positive reflection of the team.

## Slide 9

Average completion time was 1.8 days in August, essentially flat on July's 1.9, and well below the 3.5-day green threshold. A year ago, in August 2025, the average was 3.7 days, so the twelve-month improvement remains solid. To put the trajectory in context: the peak we recorded was 8.3 days in February 2025, then 6.5 in October, 4.1 in January 2026. We came down to a low of 1.4 in June, and we've held around 1.8 to 1.9 since. If the balance of work shifts – more Change tasks, more complex incident work returning at scale – the average will move up again. But the direction over the past year is genuinely strong.

## Slide 10

In August the team completed 518 tasks against 491 created – a positive variance of 27, recovering from July's negative 22. Year on year, both figures are well up: 177 more tasks created than in August 2025 and 220 more completed, increases of 56 and 74 percent. So volume and throughput are both running well ahead of last year. To reiterate, the team operating at this level still has no headroom – there's no capacity to absorb a sustained spike in demand. This month's positive variance is welcome, but the margin the team works on can move either way, as July showed.
