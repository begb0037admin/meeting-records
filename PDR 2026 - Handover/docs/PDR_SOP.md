# PDR — Prep & Run SOP

> Trigger phrases: **"prep PDR"**, **"prep [Name]'s PDR"**
> First built 14 Sep 2026 across the 2026 PDR round (Kevin, Michael O'Sullivan, James Salas Guillen, Asta Palmer). This is the repeatable process — see `docs/HANDOVER.md` in this same folder for the session-by-session build history and open gaps.

## Steps

### 1. Check the person's real prior-year transcript first — before anything else

Before building the flow doc, check `C:\Users\admin\OneDrive - Nexus365\Kevin Lelitte - Transcribed Files\` for that person's actual prior-year PDR **meeting transcript** — not just their review-form docx. The transcript is a genuinely richer source than the review-form summary: it's the real conversation, not the written-up version, and it survives even when the review-form docx itself is blocked (see the SharePoint/Edu-permission gap in `docs/HANDOVER.md`).

Filename pattern is roughly `YYYY__MMDD_<name>_PDR.docx`, but it isn't perfectly consistent — search flexibly. The real Michael file has a typo, `Micharl` not `Michael`. Confirmed present as of 14 Sep 2026:
- `2025__0912_james_PDR.docx`
- `2025__0917_Kevin_PDR.docx`
- `2025__0922_Asta_PDR.docx`
- `2025__0930_Micharl_PDR.docx`

These are `.docx` files but not Oxford template documents — `python-docx`'s normal `Document(path).paragraphs` API reads them fine (unlike the canonical guide itself, see `docs/reference/README.md`).

### 2. Confirm the meeting date and the Desktop folder

Each person gets a folder under `D:\OneDrive - lelitte.com\Desktop\PDR 2026\<Person Name>\` — one subfolder per person, this is the standing convention (set 13–14 Sep 2026, do not drop a PDR file flat on the Desktop). Confirm the actual scheduled date/time live (Granola, calendar, or command-centre task) before naming the file — don't assume it hasn't moved.

### 3. Build the single flow doc

One file per person: `PDR Review Form - DD-MMM-YYYY.md`, saved into their Desktop folder. This is a script-style markdown document to run the meeting from directly — not a reference doc, not a form with blank fields to fill in later. Structure follows Oxford's real six-stage PDR Conversation Guide exactly (see `docs/reference/`):

1. Workload & wellbeing
2. Performance / progress
3. Values
4. Personal development & career aspirations
5. Working together
6. Agree actions and close (with live checkboxes)

For each section: weave in real, dated content as context, then give natural, bolded, sayable questions — never invented. Real content sources, in rough priority order:
- That person's own 2026 self-review (if they've submitted one)
- Their prior-year transcript, pulled per Step 1 — frame explicitly as **last year's discussion**, for genuine comparison, not as this year's content
- Dated, real activity from `begb0037admin/work-inbox` and `begb0037admin/command-centre` (read-only cross-reference, standing rule for every brief — see Lauren's `AGENT.md`)
- Granola meeting records, where available

**Never invent PDR content.** If a section genuinely has nothing to draw on — no 2026 self-review, no usable prior-year material, nothing dated from work-inbox/command-centre — say so explicitly in the file (e.g. "No 2026 self-review content confirmed for this section yet — ask directly") and keep to the plain standard guide questions only. A flagged gap is always better than a plausible-sounding invention.

If Kevin is the reviewee (his own PDR), frame the whole document as prep for being asked these questions, in second person ("you"), not as a script for asking someone else — the guide is explicit that either side uses the same six stages.

### 4. Run the meeting from the one file

The flow doc is the whole meeting script — open it and go, top to bottom, Section 6 actions captured live in the checkboxes rather than reconstructed afterwards.

### 5. Post-meeting: Manager Summary from the Granola transcript

Once the meeting's happened and a Granola recording exists, draft the Manager Summary from that transcript — not from the flow doc, which was prep, not a record of what was actually said. This is a separate step, done after, and lands in that person's own `PDR Review Form - DD-MMM-YYYY.docx` (the official review form) once Kevin's reviewed the real recording. Don't attempt this before the Granola recording is actually available — flag as pending rather than guessing at what was likely said.

### 6. Once a person's PDR is closed, stop editing it

A closed PDR (Manager Summary drafted, form finalised) is done — don't reopen or edit either the `.md` flow doc or the `.docx` review form for a closed person, even to add newly-found prior-year context. If something materially relevant turns up later, note it separately rather than touching the closed files.

## File naming
- Flow doc: `PDR 2026/<Person Name>/PDR Review Form - DD-MMM-YYYY.md` (date = meeting date)
- Once closed: same folder also gets the official `PDR Review Form - DD-MMM-YYYY.docx`

## Data sources
| Source | What it feeds |
|--------|---------------|
| `Kevin Lelitte - Transcribed Files` (local OneDrive, see Step 1) | Real prior-year PDR discussion, for genuine year-over-year comparison |
| Person's own 2026 self-review (docx, when submitted) | This year's real content |
| `begb0037admin/work-inbox`, `begb0037admin/command-centre` (read-only) | Dated, real 2026 activity to ground Section 2 (and elsewhere) |
| Granola | Meeting records; the post-meeting Manager Summary source |
| `docs/reference/PDR Conversation Guide - PDR Refresh - 22.05.2024 v1.docx` | The canonical six-stage structure itself |

## Known gotchas
- Oxford SharePoint access for the written 2025 review-form docx files (as opposed to the transcripts, which live locally and aren't SharePoint-gated) can be blocked by the Edu-identity permission gap — see `docs/HANDOVER.md` for full detail and the "Kevin drops the file manually" workaround.
- The canonical guide's own text needs raw XML extraction, not `python-docx` paragraphs — see `docs/reference/README.md`.
- Generated flow docs are, by exception, committed to this repo (unlike the usual ephemeral-output rule for generated HTML briefs/decks) — Kevin's explicit instruction, 14 Sep 2026, because these are small, durable, hand-authored-style documents rather than large generated output.
