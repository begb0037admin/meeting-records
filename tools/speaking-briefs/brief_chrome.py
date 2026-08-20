"""
Shared chrome for all speaking-brief artifacts: Oxford brandbar, live clock +
meeting stopwatch, dual-month calendar, and the two-grid layout system
(top-grid: flag / clock / at-a-glance-style summary / calendar, all on one
shared 3-column backbone; item-grid: card tiles below).

Every meeting brief (Roadmap, Managers Meeting, H&S Roadmap, 1-1s, FA
Catch-up, project meetings) imports this instead of redefining the chrome,
so a fix or design change made once (e.g. the tile-alignment fix, the
stopwatch) propagates to every brief automatically.
"""
import base64, html, os
from datetime import datetime

SCRATCH = r"C:\Users\admin\AppData\Local\Temp\claude\C--Users-admin\75a25187-c549-45b9-ab8d-623015c16c47\scratchpad"

# Kevin's real Desktop -- NOT C:\Users\admin\Desktop (a known, confirmed
# gotcha; that path is not where OneDrive syncs the visible Desktop folder
# to). Every finished brief's HTML is written here as the durable, final
# deliverable, per Kevin's instruction (20 Aug 2026) that these briefs must
# not live only in scratchpad. See write_brief_output() below.
DESKTOP = r"D:\OneDrive - lelitte.com\Desktop"


def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def e(s):
    return html.escape(str(s), quote=False) if s else ""


FONT_400 = b64(fr"{SCRATCH}\inter-400.woff2")
FONT_600 = b64(fr"{SCRATCH}\inter-600.woff2")
FONT_700 = b64(fr"{SCRATCH}\inter-700.woff2")
FONT_800 = b64(fr"{SCRATCH}\inter-800.woff2")
CREST = b64(fr"{SCRATCH}\oxford-crest.jpg")

PILL_LABEL = {
    "overdue": "Overdue", "atrisk": "At risk", "onhold": "On hold", "ontrack": "On track",
    "info": "Update", "raise": "Raise", "resolved": "Resolved", "new": "New",
}

CSS_BASE = r"""
  @font-face { font-family: 'Inter'; font-style: normal; font-weight: 400; font-display: swap; src: url(data:font/woff2;base64,__FONT_400__) format('woff2'); }
  @font-face { font-family: 'Inter'; font-style: normal; font-weight: 600; font-display: swap; src: url(data:font/woff2;base64,__FONT_600__) format('woff2'); }
  @font-face { font-family: 'Inter'; font-style: normal; font-weight: 700; font-display: swap; src: url(data:font/woff2;base64,__FONT_700__) format('woff2'); }
  @font-face { font-family: 'Inter'; font-style: normal; font-weight: 800; font-display: swap; src: url(data:font/woff2;base64,__FONT_800__) format('woff2'); }

  :root {
    --navy: #002147; --bg: #f5f7fb; --card: #ffffff; --sidebar-width: 340px;
    --navy-soft: #1b3a63; --ink: #1a2430; --ink-soft: #56607a; --ink-faint: #8791a6;
    --line: #e2e6f0; --line-strong: #cbd2e3;
    --overdue: #a3271f; --overdue-bg: #fbe9e7;
    --atrisk: #92600a; --atrisk-bg: #fbf0dc;
    --onhold: #5c6478; --onhold-bg: #eceef4;
    --ontrack: #14663f; --ontrack-bg: #e2f3ea;
    --info: #1b3a63; --info-bg: #e6ecf5;
    --shadow: 0 1px 2px rgba(0,33,71,0.05), 0 6px 20px rgba(0,33,71,0.06);
    --grid-gap: 1.6rem;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --navy: #0a1f38; --bg: #0d1420; --card: #141d2c; --navy-soft: #17385e;
      --ink: #e8ecf4; --ink-soft: #aab3c8; --ink-faint: #717c93;
      --line: #253046; --line-strong: #33405c;
      --overdue: #ef8f7f; --overdue-bg: #2d1a17; --atrisk: #e0b25a; --atrisk-bg: #2c2413;
      --onhold: #a3acc2; --onhold-bg: #1c2436; --ontrack: #6fc998; --ontrack-bg: #142a1f;
      --info: #8fb2e0; --info-bg: #17263d;
      --shadow: 0 1px 2px rgba(0,0,0,0.3), 0 6px 24px rgba(0,0,0,0.4);
    }
  }
  :root[data-theme="dark"] {
    --navy: #0a1f38; --bg: #0d1420; --card: #141d2c; --navy-soft: #17385e;
    --ink: #e8ecf4; --ink-soft: #aab3c8; --ink-faint: #717c93;
    --line: #253046; --line-strong: #33405c;
    --overdue: #ef8f7f; --overdue-bg: #2d1a17; --atrisk: #e0b25a; --atrisk-bg: #2c2413;
    --onhold: #a3acc2; --onhold-bg: #1c2436; --ontrack: #6fc998; --ontrack-bg: #142a1f;
    --info: #8fb2e0; --info-bg: #17263d;
    --shadow: 0 1px 2px rgba(0,0,0,0.3), 0 6px 24px rgba(0,0,0,0.4);
  }
  :root[data-theme="light"] {
    --navy: #002147; --bg: #f5f7fb; --card: #ffffff; --navy-soft: #1b3a63;
    --ink: #1a2430; --ink-soft: #56607a; --ink-faint: #8791a6;
    --line: #e2e6f0; --line-strong: #cbd2e3;
    --overdue: #a3271f; --overdue-bg: #fbe9e7; --atrisk: #92600a; --atrisk-bg: #fbf0dc;
    --onhold: #5c6478; --onhold-bg: #eceef4; --ontrack: #14663f; --ontrack-bg: #e2f3ea;
    --info: #1b3a63; --info-bg: #e6ecf5;
    --shadow: 0 1px 2px rgba(0,33,71,0.05), 0 6px 20px rgba(0,33,71,0.06);
  }

  * { box-sizing: border-box; }
  html, body { margin: 0; background: var(--bg); color: var(--ink); font-family: 'Inter', -apple-system, "Segoe UI", sans-serif; }
  ::selection { background: var(--navy); color: #fff; }
  a { color: var(--navy-soft); }
  a:focus-visible, [tabindex]:focus-visible, summary:focus-visible { outline: 2px solid var(--navy-soft); outline-offset: 2px; }

  .brandbar { background: var(--navy); padding: 18px clamp(20px, 3vw, 48px) 16px; }
  .sidebar-logo { display: flex; align-items: center; gap: 14px; }
  .sidebar-crest { width: 64px; height: 64px; object-fit: contain; flex-shrink: 0; }
  .sidebar-brand-text { display: inline-flex; flex-direction: column; }
  .sb-univ-of { font-size: 9px; font-weight: 400; letter-spacing: 0.30em; text-transform: uppercase; color: rgba(255,255,255,0.70); line-height: 1.5; white-space: nowrap; }
  .sb-oxford { font-size: 22px; font-weight: 800; letter-spacing: 0.03em; text-transform: uppercase; color: #fff; line-height: 1.1; white-space: nowrap; }
  .sb-app-name { font-size: 10.5px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: rgba(255,255,255,0.85); margin-top: 3px; }

  .page { max-width: 1680px; margin: 0 auto; padding: 1.8rem clamp(16px, 3vw, 48px) 4rem; }

  .doc-title-row { margin-bottom: 1.4rem; }
  .doc-kicker { font-size: 11px; font-weight: 700; letter-spacing: 0.09em; text-transform: uppercase; color: var(--navy-soft); margin: 0 0 0.4rem; }
  h1 { font-size: clamp(1.5rem, 1.6vw + 1rem, 1.9rem); line-height: 1.2; margin: 0 0 0.6rem; font-weight: 800; color: var(--ink); text-wrap: balance; letter-spacing: -0.01em; }
  .meta-row { display: flex; flex-wrap: wrap; gap: 0.35rem 1.4rem; font-size: 0.85rem; color: var(--ink-soft); font-weight: 500; }
  .meta-row b { color: var(--ink); font-weight: 700; }

  /* Top section: brief (left) + live clock/calendar (right), built on the SAME
     3-column / var(--grid-gap) backbone as .item-grid below, so column
     boundaries run straight down the page unbroken. Row-matched so each
     right tile is always exactly as tall as its left-hand counterpart. */
  .top-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    grid-auto-rows: auto;
    gap: var(--grid-gap);
    margin-bottom: 0.5rem;
  }
  .flag { grid-column: span 2; margin: 0; }
  .glance { grid-column: span 2; min-width: 0; }
  .clock-card { grid-column: span 1; }
  .cal-card { grid-column: span 1; }

  .clock-card { display: flex; align-items: stretch; padding: 0; }
  .clock-half, .stopwatch-half { flex: 1 1 50%; min-width: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 1rem 0.9rem; text-align: center; }
  .clock-half { border-right: 1px solid var(--line); }
  .clock-time { font-size: 1.7rem; font-weight: 800; color: var(--navy); font-variant-numeric: tabular-nums; letter-spacing: 0.01em; line-height: 1.1; }
  .clock-date { font-size: 0.7rem; font-weight: 600; color: var(--ink-faint); margin-top: 0.35rem; text-transform: uppercase; letter-spacing: 0.04em; }

  .stopwatch-label { font-size: 9.5px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink-faint); margin: 0 0 0.35rem; }
  .stopwatch-time { font-size: 1.7rem; font-weight: 800; color: var(--ink); font-variant-numeric: tabular-nums; letter-spacing: 0.01em; line-height: 1.1; }
  .stopwatch-time.running { color: var(--navy); }
  .stopwatch-btn {
    margin-top: 0.55rem; border: none; border-radius: 999px; padding: 0.32rem 1rem;
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase;
    cursor: pointer; background: var(--navy); color: #fff; transition: background 0.15s ease;
  }
  .stopwatch-btn:hover { background: var(--navy-soft); }
  .stopwatch-btn.is-running { background: var(--overdue); }
  .stopwatch-reset {
    margin-top: 0.35rem; border: none; background: none; cursor: pointer;
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.03em; color: var(--ink-faint);
    text-decoration: underline; text-underline-offset: 2px; padding: 0.15rem;
  }
  .stopwatch-reset:hover { color: var(--ink-soft); }
  @media (max-width: 420px) {
    .clock-card { flex-direction: column; }
    .clock-half { border-right: none; border-bottom: 1px solid var(--line); }
  }

  .cal-card { display: flex; flex-direction: column; padding: 1rem 1.1rem; overflow: hidden; }
  .cal-months { display: flex; flex-direction: column; justify-content: space-evenly; flex: 1; gap: 1.15rem; }
  /* Divider moved to the BOTTOM inset edge of every non-last month (was the
     TOP edge of every non-first month). Visually it's the same single line
     at each month boundary, but anchoring it to the top of the block above
     means the .cal-months flex gap (already read live by the JS fit-
     calculation via getComputedStyle().rowGap) is what sits between the
     divider and the next label — so widening that gap buys breathing room
     without adding any height to a specific month's own box. Still a
     zero-height box-shadow, still doesn't touch the adaptive month-count
     measurement (which renders/measures a single, divider-free month). */
  .cal-month:not(:last-child) { box-shadow: inset 0 -1px 0 0 var(--line); }
  .cal-month-label { font-size: 0.82rem; font-weight: 700; color: var(--ink); margin: 0 0 0.9rem; text-align: center; }
  .cal-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 1px; }
  .cal-dow { font-size: 8.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.03em; color: var(--ink-faint); text-align: center; padding: 2px 0 5px; }
  .cal-day { font-size: 10.5px; text-align: center; padding: 4px 1px; color: var(--ink-soft); font-variant-numeric: tabular-nums; line-height: 1; }
  .cal-day.blank { visibility: hidden; }
  .cal-day.today { background: var(--navy); color: #fff; font-weight: 700; border-radius: 4px; }

  @media (max-width: 1100px) {
    .top-grid { grid-template-columns: 1fr; }
    .flag, .glance, .clock-card, .cal-card { grid-column: span 1; }
  }

  .flag { background: var(--overdue-bg); border: 1px solid color-mix(in srgb, var(--overdue) 35%, transparent); border-left: 4px solid var(--overdue); border-radius: 8px; padding: 1rem 1.3rem; display: flex; flex-direction: column; justify-content: center; }
  .flag-label { font-size: 11px; font-weight: 700; letter-spacing: 0.09em; text-transform: uppercase; color: var(--overdue); margin: 0 0 0.5rem; }
  .flag p { margin: 0 0 0.55rem; font-size: 0.92rem; line-height: 1.5; color: var(--ink); }
  .flag p:last-child { margin-bottom: 0; }

  h2 { font-size: 0.95rem; font-weight: 700; letter-spacing: 0.01em; margin: 2.2rem 0 0.85rem; color: var(--ink); display: flex; align-items: baseline; gap: 0.6rem; flex-wrap: wrap; }
  h2 .h2-sub { font-size: 11px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--ink-faint); }

  /* Section headings that flag something needing attention (e.g. "Risks and
     dependencies") get their own treatment — amber, larger, a left tab —
     so they don't read as just another neutral section label. */
  h2.h2-warn { color: var(--atrisk); font-size: 1.08rem; padding-left: 0.7rem; border-left: 3px solid var(--atrisk); }
  h2.h2-warn .h2-sub { color: color-mix(in srgb, var(--atrisk) 65%, var(--ink-faint)); }

  /* "At a glance" as one card with an internal label, same pattern as .flag,
     so its box top lines up exactly with the calendar's box top. */
  .glance { display: flex; flex-direction: column; padding: 0; }
  .glance-head { padding: 1rem 1.3rem 0.7rem; }
  .glance-label { font-size: 11px; font-weight: 700; letter-spacing: 0.09em; text-transform: uppercase; color: var(--navy-soft); margin: 0 0 0.3rem; }
  .glance-sub { font-size: 11px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--ink-faint); margin: 0; }
  .glance .table-wrap { flex: 1; max-width: none; border-radius: 0 0 10px 10px; }

  .card { background: var(--card); border: 1px solid var(--line); border-radius: 10px; box-shadow: var(--shadow); }

  .table-wrap { overflow-x: auto; border-radius: 10px; max-width: 980px; }
  table { width: 100%; border-collapse: collapse; font-size: 0.87rem; }
  thead th { text-align: left; font-size: 10.5px; font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase; color: var(--ink-faint); padding: 0.8rem 0.9rem; border-bottom: 1px solid var(--line-strong); white-space: nowrap; background: color-mix(in srgb, var(--navy) 3%, var(--card)); }
  tbody td { padding: 0.7rem 0.9rem; border-bottom: 1px solid var(--line); vertical-align: top; color: var(--ink); }
  tbody tr:last-child td { border-bottom: none; }
  td.idcell { font-weight: 700; color: var(--navy-soft); font-variant-numeric: tabular-nums; white-space: nowrap; }
  td.datecell { font-variant-numeric: tabular-nums; white-space: nowrap; color: var(--ink-soft); }

  .pill { display: inline-block; font-size: 10.5px; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; padding: 0.26rem 0.58rem; border-radius: 999px; white-space: nowrap; }
  .pill-overdue, .pill-raise { background: var(--overdue-bg); color: var(--overdue); }
  .pill-atrisk, .pill-new { background: var(--atrisk-bg); color: var(--atrisk); }
  .pill-onhold { background: var(--onhold-bg); color: var(--onhold); }
  .pill-ontrack, .pill-resolved { background: var(--ontrack-bg); color: var(--ontrack); }
  .pill-info { background: var(--info-bg); color: var(--info); }

  /* Item grid — same 3-column / var(--grid-gap) backbone as .top-grid above,
     so column boundaries line up exactly. Fixed (not auto-fit) so a short
     final row leaves a genuine blank cell instead of stretching to fill it.
     align-items left at default (stretch) so every card in a row shares the
     same bottom edge. */
  .item-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--grid-gap); }
  @media (max-width: 1100px) {
    .item-grid { grid-template-columns: 1fr; }
  }

  .item { padding: 1.1rem 1.25rem 1.25rem; }
  .item-head { display: flex; flex-direction: column; align-items: flex-start; gap: 0.32rem; margin-bottom: 1rem; }
  .item-id { display: block; font-weight: 700; color: var(--navy-soft); font-size: 0.78rem; font-variant-numeric: tabular-nums; letter-spacing: 0.03em; }
  .item-title { display: block; font-size: 1.05rem; font-weight: 700; color: var(--ink); margin: 0; line-height: 1.3; }
  .item-head .pill { margin: 0.05rem 0 0.1rem; }
  .item-owner { display: block; font-size: 0.82rem; color: var(--ink-faint); margin: 0; font-variant-numeric: tabular-nums; }
  .item-desc { font-size: 0.86rem; color: var(--ink-soft); margin: 0 0 0.8rem; line-height: 1.5; padding-bottom: 0.8rem; border-bottom: 1px solid var(--line); }

  .last-update { background: color-mix(in srgb, var(--navy) 4%, var(--bg)); border-radius: 8px; padding: 0.65rem 0.85rem; margin: 0 0 0.8rem; }
  .lu-label { display: block; font-size: 9.5px; font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase; color: var(--navy-soft); margin-bottom: 0.3rem; }
  .last-update p { margin: 0; font-size: 0.87rem; color: var(--ink); line-height: 1.45; }

  .item-current { font-size: 0.87rem; line-height: 1.5; color: var(--ink-soft); margin: 0 0 0.9rem; }
  .cur-label { display: block; font-size: 9.5px; font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase; color: var(--ink-faint); margin-bottom: 0.3rem; }

  blockquote { margin: 0 0 0.9rem; padding: 0.75rem 0.95rem; background: color-mix(in srgb, var(--navy) 5%, var(--bg)); border-left: 3px solid var(--navy); border-radius: 6px; }
  blockquote .say-label { display: block; font-size: 9.5px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--navy-soft); margin-bottom: 0.3rem; }
  blockquote p { margin: 0; font-size: 0.89rem; color: var(--ink); font-style: italic; line-height: 1.48; }

  details.expand { border-top: 1px dashed var(--line-strong); padding-top: 0.6rem; }
  details.expand summary {
    cursor: pointer; list-style: none; font-size: 0.8rem; font-weight: 700; color: var(--navy-soft);
    display: flex; align-items: center; gap: 0.4rem; letter-spacing: 0.02em;
    padding: 0.3rem 0; user-select: none;
  }
  details.expand summary::-webkit-details-marker { display: none; }
  details.expand .chev { transition: transform 0.15s ease; font-size: 0.7rem; }
  details.expand[open] .chev { transform: rotate(180deg); }
  @media (prefers-reduced-motion: reduce) { details.expand .chev { transition: none; } }

  .expand-body { padding: 0.7rem 0 0.1rem; font-size: 0.86rem; color: var(--ink-soft); }
  .expand-body h4 { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--ink-faint); margin: 1rem 0 0.5rem; }
  .expand-body h4:first-child { margin-top: 0; }
  .expand-body .count { font-weight: 500; text-transform: none; letter-spacing: 0; }
  .expand-body .empty { font-style: italic; color: var(--ink-faint); margin: 0; }

  p.impact { font-size: 0.86rem; line-height: 1.5; color: var(--ink-soft); margin: 0 0 0.9rem; }
  p.impact .fact-k { display: block; font-size: 9.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: var(--ink-faint); margin-bottom: 0.3rem; }

  .facts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.6rem 1rem; margin-bottom: 0.4rem; }
  .fact { font-size: 0.82rem; }
  .fact-k { display: block; font-size: 9.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--ink-faint); margin-bottom: 0.15rem; }
  .fact-v { color: var(--ink); }

  ul.update-log { list-style: none; margin: 0; padding: 0; border-left: 2px solid var(--line-strong); }
  ul.update-log li { position: relative; padding: 0 0 0.75rem 1rem; }
  ul.update-log li::before { content: ''; position: absolute; left: -5px; top: 0.35rem; width: 8px; height: 8px; border-radius: 50%; background: var(--navy-soft); }
  ul.update-log .u-date { display: block; font-size: 0.72rem; font-weight: 700; color: var(--navy-soft); font-variant-numeric: tabular-nums; margin-bottom: 0.1rem; }
  ul.update-log .u-text { display: block; font-size: 0.85rem; color: var(--ink); line-height: 1.45; }

  ul.next-steps { margin: 0; padding-left: 1.1rem; }
  ul.next-steps li { font-size: 0.85rem; color: var(--ink); line-height: 1.5; margin-bottom: 0.35rem; }

  ul.ask-list { margin: 0; padding-left: 1.1rem; }
  ul.ask-list li { font-size: 0.85rem; color: var(--ink); line-height: 1.5; margin-bottom: 0.35rem; }

  p.body-loose { font-size: 0.92rem; line-height: 1.58; color: var(--ink-soft); max-width: 980px; }
  p.body-loose b { color: var(--ink); }

  /* Reusable "risk block": a labelled sub-section (heading + body copy +
     optional bullet list of IDs), so a Risks/dependencies section with
     several distinct points reads as separated blocks, not one wall of text. */
  .risk-block { max-width: 980px; margin-bottom: 1.4rem; padding-bottom: 1.4rem; border-bottom: 1px solid var(--line); }
  .risk-block:last-child { margin-bottom: 0; padding-bottom: 0; border-bottom: none; }
  .risk-head { font-size: 0.95rem; font-weight: 700; color: var(--ink); margin: 0 0 0.5rem; }
  .risk-block .body-loose { margin: 0 0 0.6rem; }
  .risk-block .body-loose:last-child { margin-bottom: 0; }
  ul.risk-list { list-style: none; margin: 0 0 0.6rem; padding: 0; display: flex; flex-direction: column; gap: 0.5rem; }
  ul.risk-list li { font-size: 0.89rem; line-height: 1.5; color: var(--ink-soft); padding-left: 1rem; border-left: 2px solid var(--line-strong); }
  ul.risk-list li b { color: var(--ink); font-variant-numeric: tabular-nums; }

  .footnote { margin-top: 2.4rem; padding: 1rem 1.2rem; font-size: 0.75rem; color: var(--ink-faint); line-height: 1.7; border-top: 1px solid var(--line); max-width: 980px; }

  @media (max-width: 560px) {
    .brandbar { padding: 14px 14px 12px; }
    .sb-oxford { font-size: 19px; }
    .sidebar-crest { width: 48px; height: 48px; }
    .page { padding: 1.4rem 0.9rem 3rem; }
    .item-head { flex-direction: column; align-items: flex-start; gap: 0.25rem; }
  }
  @media print {
    body { background: #fff; }
    .card, .item { box-shadow: none; break-inside: avoid; }
    details.expand { display: block; }
    details.expand summary { display: none; }
  }
"""

SCRIPT_BASE = r"""
(function () {
  var DOW = ['Mon','Tue','Wed','Thu','Fri']; // working-week calendar — no Sat/Sun
  var MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  var DAY_NAMES = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];

  function pad(n) { return n < 10 ? '0' + n : '' + n; }

  function tickClock() {
    var now = new Date();
    var timeEl = document.getElementById('liveClock');
    var dateEl = document.getElementById('liveDate');
    if (timeEl) timeEl.textContent = pad(now.getHours()) + ':' + pad(now.getMinutes()) + ':' + pad(now.getSeconds());
    if (dateEl) dateEl.textContent = DAY_NAMES[now.getDay()] + ' ' + now.getDate() + ' ' + MONTHS[now.getMonth()] + ' ' + now.getFullYear();
  }

  // Working-week only (Mon-Fri) — Sat/Sun are skipped entirely, not just
  // dimmed, per Kevin's instruction (1 Aug 2026): these are meeting-prep
  // calendars, weekends aren't relevant. Since the 5-day grid divides evenly
  // into a week, skipping weekend days mid-stream still keeps every Monday
  // starting a fresh row with no extra bookkeeping.
  function buildMonth(year, month, todayY, todayM, todayD) {
    var first = new Date(year, month, 1);
    var daysInMonth = new Date(year, month + 1, 0).getDate();
    var firstDow = (first.getDay() + 6) % 7; // Monday-first, 0=Mon .. 6=Sun
    var leadBlanks = firstDow < 5 ? firstDow : 0; // month starting on a weekend collapses to the first Monday's row

    var html = '<p class="cal-month-label">' + MONTHS[month] + ' ' + year + '</p>';
    html += '<div class="cal-grid">';
    for (var i = 0; i < 5; i++) html += '<span class="cal-dow">' + DOW[i] + '</span>';
    for (var b = 0; b < leadBlanks; b++) html += '<span class="cal-day blank">&nbsp;</span>';
    for (var d = 1; d <= daysInMonth; d++) {
      var dow = (firstDow + d - 1) % 7;
      if (dow >= 5) continue; // Saturday/Sunday
      var isToday = (year === todayY && month === todayM && d === todayD);
      var cls = 'cal-day' + (isToday ? ' today' : '');
      html += '<span class="' + cls + '">' + d + '</span>';
    }
    html += '</div>';
    return html;
  }

  // Fills whatever vertical space the calendar tile has been given (it's
  // grid-stretched to match the "at a glance" tile's height, which grows as
  // more items are added) with as many consecutive months as actually fit,
  // starting from the current month — 1 when the tile is short, more as it
  // grows, rather than a fixed count that leaves dead space or overflows.
  function buildCalendars() {
    var now = new Date();
    var y = now.getFullYear(), m = now.getMonth(), d = now.getDate();
    var container = document.getElementById('calMonths');
    var card = container ? container.closest('.cal-card') : null;
    if (!container || !card) return;

    function monthHtml(offset) {
      var total = m + offset;
      var yy = y + Math.floor(total / 12);
      var mm = ((total % 12) + 12) % 12;
      return '<div class="cal-month">' + buildMonth(yy, mm, y, m, d) + '</div>';
    }

    // Render one month to measure its natural height, then work out how
    // many (plus inter-month gaps) fit inside the tile's actual height.
    container.innerHTML = monthHtml(0);
    var monthH = container.firstElementChild.offsetHeight;
    var gapPx = parseFloat(getComputedStyle(container).rowGap || getComputedStyle(container).gap || '0') || 0;
    var available = card.clientHeight - (parseFloat(getComputedStyle(card).paddingTop) || 0) - (parseFloat(getComputedStyle(card).paddingBottom) || 0);

    var count = monthH > 0 ? Math.floor((available + gapPx) / (monthH + gapPx)) : 1;
    count = Math.max(1, Math.min(count, 6));

    var html = '';
    for (var i = 0; i < count; i++) html += monthHtml(i);
    container.innerHTML = html;
  }

  tickClock();
  buildCalendars();
  setInterval(tickClock, 1000);

  // Meeting stopwatch — counts up, start/stop toggle, reset. Purely local
  // to this viewing of the page; nothing is persisted or sent anywhere.
  (function () {
    var timeEl = document.getElementById('stopwatchTime');
    var btnEl = document.getElementById('stopwatchBtn');
    var resetEl = document.getElementById('stopwatchReset');
    if (!timeEl || !btnEl || !resetEl) return;

    var elapsedMs = 0;
    var startedAt = null;
    var intervalId = null;

    function fmt(ms) {
      var totalSec = Math.floor(ms / 1000);
      var h = Math.floor(totalSec / 3600);
      var m = Math.floor((totalSec % 3600) / 60);
      var s = totalSec % 60;
      return pad(h) + ':' + pad(m) + ':' + pad(s);
    }

    function render() {
      var current = elapsedMs + (startedAt ? (Date.now() - startedAt) : 0);
      timeEl.textContent = fmt(current);
    }

    function start() {
      startedAt = Date.now();
      intervalId = setInterval(render, 1000);
      btnEl.textContent = 'Stop';
      btnEl.classList.add('is-running');
      timeEl.classList.add('running');
    }

    function stop() {
      elapsedMs += Date.now() - startedAt;
      startedAt = null;
      clearInterval(intervalId);
      btnEl.textContent = 'Start';
      btnEl.classList.remove('is-running');
      timeEl.classList.remove('running');
      render();
    }

    btnEl.addEventListener('click', function () {
      if (startedAt) stop(); else start();
    });

    resetEl.addEventListener('click', function () {
      if (startedAt) stop();
      elapsedMs = 0;
      render();
    });

    render();
  })();
})();
"""

BRANDBAR = """<div class="brandbar">
  <div class="sidebar-logo">
    <img class="sidebar-crest" src="data:image/jpeg;base64,__CREST__" alt="University of Oxford crest">
    <div class="sidebar-brand-text">
      <span class="sb-univ-of">University of</span>
      <span class="sb-oxford">Oxford</span>
      <span class="sb-app-name">{app_name}</span>
    </div>
  </div>
</div>"""

CLOCK_CARD = """<div class="clock-card card">
      <div class="clock-half">
        <div class="clock-time" id="liveClock">--:--:--</div>
        <div class="clock-date" id="liveDate">&nbsp;</div>
      </div>
      <div class="stopwatch-half">
        <p class="stopwatch-label">Meeting stopwatch</p>
        <div class="stopwatch-time" id="stopwatchTime">00:00:00</div>
        <button type="button" class="stopwatch-btn" id="stopwatchBtn">Start</button>
        <button type="button" class="stopwatch-reset" id="stopwatchReset">Reset</button>
      </div>
    </div>"""

CAL_CARD = """<div class="cal-card card">
      <div class="cal-months" id="calMonths"></div>
    </div>"""


def write_brief_output(html_out, brief_name, date=None):
    """Write a finished speaking-brief HTML page to disk under its final,
    Kevin-facing name: "<brief_name> - DD-MM-YYYY.html" (matches the KPI
    Presentation deck's own naming convention -- Lauren's call, 20 Aug 2026).
    Called once from the bottom of every brief_chrome.py-based build script
    instead of each script hand-rolling its own `open(...).write()` -- one
    shared output point, so the Desktop-write policy only has to be right
    in one place.

    Always writes a SCRATCH copy first (unchanged prior behaviour -- still
    useful in-session, e.g. for Artifact-tool prep), then writes the SAME
    bytes to Kevin's real Desktop as the durable, final deliverable, per
    Kevin's instruction that these briefs must not live only in scratchpad
    (a per-session temp path that gets cleaned up and isn't visible in
    Explorer). Same-day reruns overwrite in place, deliberately -- a brief
    only exists for one meeting per day, so the latest rebuild is always the
    one Kevin wants, not a timestamped pile of near-duplicates from
    redrafting the same meeting's brief across a session.

    If the Desktop path isn't reachable (e.g. a session running on a
    machine/environment without that OneDrive mount), the SCRATCH copy still
    exists and this prints a loud warning instead of silently losing the
    "final" copy.
    """
    d = date or datetime.now()
    fname = f"{brief_name} - {d.strftime('%d-%m-%Y')}.html"

    os.makedirs(SCRATCH, exist_ok=True)
    scratch_path = os.path.join(SCRATCH, fname)
    with open(scratch_path, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"written {scratch_path} ({len(html_out)} chars)")

    try:
        os.makedirs(DESKTOP, exist_ok=True)
        desktop_path = os.path.join(DESKTOP, fname)
        with open(desktop_path, "w", encoding="utf-8") as f:
            f.write(html_out)
        print(f"written {desktop_path} ({len(html_out)} chars) -- final output")
        return desktop_path
    except OSError as ex:
        print(f"WARNING: could not write to Desktop ({DESKTOP}): {ex}")
        print(f"Desktop path not reachable this session -- only the scratchpad copy exists: {scratch_path}")
        print("Copy it to the real Desktop manually, or rerun from a session where that OneDrive path is mounted.")
        return scratch_path


def render_page(title, app_name, kicker, h1, meta_spans, flag_label, flag_paragraphs,
                 glance_label, glance_sub, glance_table_html,
                 sections_html, footnote_html):
    """Assemble one full brief page from the shared chrome + a section's worth
    of caller-supplied HTML (item-grid, risks, footnote, etc.)."""
    meta_html = "".join(f"<span>{m}</span>" for m in meta_spans)
    flag_html = "".join(f"<p>{p}</p>" for p in flag_paragraphs)
    css = CSS_BASE.replace("__FONT_400__", FONT_400).replace("__FONT_600__", FONT_600) \
        .replace("__FONT_700__", FONT_700).replace("__FONT_800__", FONT_800)
    brandbar = BRANDBAR.replace("__CREST__", CREST).format(app_name=e(app_name))

    return f"""<title>{e(title)}</title>
<style>{css}</style>

{brandbar}

<div class="page">

  <div class="doc-title-row">
    <p class="doc-kicker">{kicker}</p>
    <h1>{h1}</h1>
    <div class="meta-row">{meta_html}</div>
  </div>

  <div class="top-grid">
    <div class="flag">
      <p class="flag-label">{flag_label}</p>
      {flag_html}
    </div>

    {CLOCK_CARD}

    <div class="glance card">
      <div class="glance-head">
        <p class="glance-label">{glance_label}</p>
        <p class="glance-sub">{glance_sub}</p>
      </div>
      <div class="table-wrap">
        {glance_table_html}
      </div>
    </div>

    {CAL_CARD}
  </div>

  {sections_html}

  {footnote_html}

</div>

<script>{SCRIPT_BASE}</script>
"""
