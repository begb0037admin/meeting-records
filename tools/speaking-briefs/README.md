# Speaking-brief template

Generates the HTML that gets published as a Claude Artifact for Kevin to read from live in a meeting: Oxford brandbar, live clock + meeting stopwatch, dual-month calendar (today highlighted), a flagged data-gap warning, an "at a glance" summary table, and a grid of per-item cards with a "say this" line for each.

## Files

- `brief_chrome.py` — shared chrome. Fonts (Inter, self-hosted as base64 WOFF2 to satisfy the Artifact CSP), CSS design tokens (light + dark, `command-centre/BRANDING.md` v2.0 palette), the brandbar, the live clock/stopwatch/calendar widgets and their JS, and the two-grid layout system (`top-grid` and `item-grid` share one 3-column / `--grid-gap` backbone so column boundaries and tile heights line up exactly, top to bottom of the page). Every brief script imports this instead of redefining the chrome — a design fix made once (the tile-alignment fix, the stopwatch) propagates to every brief automatically.
- `build_roadmap.py` — HR Systems Roadmap brief. Reads the Roadmap Master workbook fields (via a separately-generated `roadmap-items.json`) into per-item cards.
- `build_managers_meeting.py` — HR Systems Managers Meeting brief. Agenda-item cards (no Roadmap Master behind it) carried forward from the last captured meeting outcome, cross-checked against overlapping Roadmap items where relevant.

## Not yet built (planned rollout order per Kevin, 1 Aug 2026)

Managers Meeting (done) → H&S Roadmap → SK 1-1 (Simon, incl. leave handovers) → FA Team Catch-up (Wed/Fri) → Team 1-1s (James, Michael, Asta). Roadmap-style meetings (a tracked-items master behind them, e.g. H&S Roadmap, ongoing project meetings like College Staff PeopleXD / OrcID PeopleXD) can likely reuse `build_roadmap.py`'s per-item-card shape directly. 1-1 / team-catch-up style meetings need a different card shape (agenda points, actions, carry-overs) — same chrome, different `render_item`.

## Running a build script

Each script is self-contained except for two binary inputs it expects to find alongside it (not committed here — they're large/generated, not source): `inter-400/600/700/800.woff2` (Inter, subset + WOFF2-converted via `fontTools.subset`) and `oxford-crest.jpg` (the canonical crest referenced in `command-centre/BRANDING.md`). Point `SCRATCH` in `brief_chrome.py` at a working directory containing those, then `python build_roadmap.py` (etc.) writes the finished HTML there, ready to hand to the `Artifact` tool.

Every generated brief is a draft only — nothing here writes to `meeting-records`, publishes, or schedules anything on its own.
