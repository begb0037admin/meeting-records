# Task: build the 21 Sep 2026 Health and Safety Roadmap brief generator (scratchpad only)

You are the lead implementer. Work ONLY inside this directory (the working root). Do not read or write anywhere else. Do not touch any OneDrive path. Do not modify `brief_chrome.py`, `content.json`, `build_hs_roadmap_orig.py`, or `hs_workflow_copy.xlsx`.

## Files present
- `brief_chrome.py` : shared template (render_page, e, write_brief_output, SCRATCH, MEETINGS_DIR). Already repointed; leave it alone. No CSS changes anywhere.
- `build_hs_roadmap_orig.py` : the reference generator from the repo. Reuse its `render_updates` and `render_item` logic and its item-card markup exactly (facts grid, last-update block, say-this blockquote, collapsible history). It hardcodes ITEMS/PILL/SAY; replace those with data-driven inputs.
- `hs_workflow_copy.xlsx` : a COPY of the shared H&S workbook. Read-only input. Sheet "Backlog Items": header row is row 3, data starts row 4, only rows where "Ref Num" is non-empty.
- `content.json` : authored content. Keys: title, app_name, kicker, h1, meta_spans (list of HTML strings), flag_label, flag_paragraphs (list of HTML strings), pre_grid_html, grid_heading_html, item_order (list of refs), pill (ref->pill key), pill_text (pill key->label), say (ref->plain text), post_grid_html, footnote_html. HTML strings are authored and must be inserted raw. `say` values are plain text and must go through `e()`. The token `{{GENERATED}}` appears in meta_spans and footnote_html; replace it at run time with a Europe/London timestamp like `Mon 21 Sep 2026, 08:05 BST` (use zoneinfo, `%a %d %b %Y, %H:%M %Z`).

## Deliverable 1: `extract_hs_items.py`
Reads `hs_workflow_copy.xlsx` (openpyxl, `data_only=True`) and writes `hs-items.json`, a dict keyed by Ref Num. Map by HEADER NAME using only the FIRST occurrence of each header (the sheet has duplicate "T Shirt Size" and "Status" helper columns further right; ignore those). Fields per item:
`item_name` (Item Name), `system` (System), `type` (Type of Request), `moscow` (MoSCoW rating:), `tshirt` (T Shirt Size), `owner` (Owner, stripped, None if blank), `start` (Start Date), `exp_delivery` (Expected Delivery Date), `delivered` (Delivered Date), `osm` (OSM Reference, as string), `detail` (Detail), `benefit` (Expected benefit), `status` (Status), `updates`.
Dates that are datetimes become `%d %b %Y` strings (e.g. `02 Mar 2026`); cells that are already strings (some are like `24/10/2025`) stay as stripped strings; empty becomes None.
`updates` is a list of `[date, text]` pairs in the order they appear in the "Comment/Updates" cell (newest first). Parse line by line: a line matching `^\s*(\d{1,2}/\d{1,2}/\d{2,4})\s*[-:–]*\s*(.*)$` starts a new entry with that date; a non-empty line that does not match is a continuation appended (with a space) to the previous entry's text; non-empty lines appearing before any dated line become their own entry with the date string `undated`. Duplicate Ref Num (HSB069 appears twice): keep the first under its ref, store the second as `HSB069_dup`.
Print the count of items and the count per status.

## Deliverable 2: `build_hs_roadmap_2026-09-21.py`
Adapt `build_hs_roadmap_orig.py`:
- Load `hs-items.json` and `content.json` from this directory (use paths relative to the script file).
- Render one card per ref in `content["item_order"]` using the orig `render_item` markup, with pill = `content["pill"][ref]`, pill label from `content["pill_text"]`, say text from `content["say"][ref]` (escaped). Keep the orig fact fields. Validate up front: every ref in item_order exists in hs-items.json and has a pill and a say entry; otherwise raise a clear error.
- Build an "At a glance" section: `<h2>At a glance <span class="h2-sub">{n} featured items</span></h2>` then `<div class="table-wrap card"><table class="fixed-grid">` with a `<colgroup>` (widths 9%, 47%, 12%, 12%, 20%), header Ref / Item / System / Owner / Status, one row per featured ref (Ref cell class `idcell`, Status cell a `pill pill-<key>` span).
- SECTIONS = `pre_grid_html` + at-a-glance section + `grid_heading_html` + `<div class="item-grid">` + all cards + `</div>` + `post_grid_html`.
- FOOTNOTE = `footnote_html`.
- Call `render_page(title=..., app_name=..., kicker=..., h1=..., meta_spans=..., flag_label=..., flag_paragraphs=..., sections_html=SECTIONS, footnote_html=FOOTNOTE)` with values from content.json (after `{{GENERATED}}` substitution), then `write_brief_output(html_out, "Health and Safety Roadmap", date=datetime(2026, 9, 21))`.
- If the environment variable `HS_BRIEF_TEST=1` is set, set `brief_chrome.MEETINGS_DIR` to `os.path.join(brief_chrome.SCRATCH, "out_test")` BEFORE calling write_brief_output, so a test run never touches OneDrive. Without that variable it writes normally (the parent will do the real run).
- Import brief_chrome as a module (`import brief_chrome`, then `from brief_chrome import e, render_page, write_brief_output`) so the override above works.

## Verification you must do
1. `python extract_hs_items.py` then `HS_BRIEF_TEST=1 python build_hs_roadmap_2026-09-21.py`.
2. Confirm the output HTML exists under `out_test`, contains all 17 refs from item_order, contains no literal `{{GENERATED}}`, and that the item-card count equals 17.
3. Confirm you did not write outside this directory and did not touch `hs_workflow_copy.xlsx` (compare its size 96651 bytes before/after).
Finish with a short report: files created, commands run, results, any deviation from this spec.
