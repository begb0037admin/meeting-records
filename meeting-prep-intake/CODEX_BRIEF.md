# Brief: Meeting Prep Intake — visual redesign

**Repo:** `begb0037admin/meeting-records`, path `meeting-prep-intake/` (Cloudflare Worker + static site, served at https://meeting.lelitte.co.uk/)
**Branch:** `drew/meeting-prep-intake-branding-redesign` (existing work-in-progress branch — build on it, don't start fresh)
**Files primarily affected:** `meeting-prep-intake/public/style.css`, `meeting-prep-intake/public/index.html` (or equivalent template), `meeting-prep-intake/public/app.js` where markup is generated client-side.

**Visual spec:** https://claude.ai/artifact/2GCf7EJoyFkibFEj6SHAyj — a design canvas mockup showing the target pill/colour system, built from the real `style.css` tokens already in the repo. Treat this as the literal spec for the pill system specifically; the rest of this brief covers everything else.

**Design reference site (for general layout/card/pill language):** https://pxd.lelitte.co.uk/ — HRIS Launcher. Match its card shadow, pill shape, and section-heading treatment, not its content.

**Branding standard:** `begb0037admin/command-centre/BRANDING.md` v2.0 — Oxford Navy `#002147`, Inter font, 340px navy sidebar, 80px crest, exact CSS values given there.

## Non-negotiable process rule

**Codex implements. The reviewing agent (Drew) only reviews, verifies, and checkpoints — never writes the diff itself, no exceptions for "trivial" changes.** This is canonical in `agent-commons/operating-model/COORDINATOR_AND_CODEX_POLICY.md` §3a and `SESSION_PROTOCOL.md` §9. Every change in this brief, however small, goes through Codex as the implementer.

## What's wrong right now, and what "done" looks like

### 1. Every clickable action button must be a pill — zero exceptions
Kevin's rule, stated plainly: **"Any button click that does something should be a pill."** Not a curated list — audit the entire page for every element that performs an action (not a text input, not a `<select>`, not a static label) and convert it. This includes, at minimum:
- `Create recurring definition`
- `Add agenda item`
- `Remove`
- `Add to detail` (per agenda item, next to the update-line input)
- `Suggest speaker note`
- `Send`, `Mic`, `Listen`, `Attach reply to detail` (Ask Lauren chat panel)
- `Choose File`, `Extract`, `Attach selected sheets to detail` (source material / Excel extraction panel)
- `Submit locked intake`
- The `Draft workspace` status badge (this is a status indicator, not an action — but should carry the same pill visual language)
- Any tone tags (`Update`, `Raise`, `FYI`, `Decision needed`) — already partially pill-styled, keep consistent

Pill shape, per the repo's own existing `.pill` CSS class (already defined in `style.css` — reuse and extend it, don't reinvent): `border: none`, `border-radius: 20px`, `padding: 8px 18px` (or slightly more for primary/final actions), solid pastel fill, no border of any kind, no left-accent bar, no drop shadow on the pill itself.

### 2. Colour-code pills by functional section, not just tone
Kevin wants distinct, reused colours per functional category so the eye can group actions at a glance. Existing `.pill-teal/.pill-blue/.pill-coral/.pill-green/.pill-amber` classes in `style.css` are the base palette — extend with one more (e.g. violet) as needed. Suggested mapping (see the design canvas for the worked example):
- **Navy** (`pill-navy`, solid `#002147`, white text) — primary/structural actions: `Add agenda item`, `Submit locked intake`
- **Coral** (existing `.pill-coral`) — destructive: `Remove`
- **Violet** (new) — Step 1 / meeting-context actions: `Create recurring definition`
- **Blue** (existing `.pill-blue`) — update-line actions: `Add to detail`
- **Amber** (existing `.pill-amber`) — speaker-note actions: `Suggest speaker note`
- **Teal** (existing `.pill-teal`) — Ask Lauren / assistant actions: `Send`, `Mic`, `Listen`, `Attach reply to detail`
- **Green** (existing `.pill-green`) — source-material actions: `Choose File`, `Extract`, `Attach selected sheets to detail`

Each pill should carry a small inline SVG icon (never emoji) representing its action, sized ~15-16px, alongside the label text.

### 3. Zero colored border-lines anywhere, on anything
This was raised and "fixed" multiple times but kept resurfacing on different elements — audit **every** element, not just item cards: status/error banners (`.message.ok`, `.message.error`), item cards, the "Request failed" banner, anything else. No `border-left`, no accent bar, anywhere on the page. Confirm via `getComputedStyle` in a real browser check, not by eyeballing a screenshot — that's how this got missed repeatedly.

### 4. Spacing — everything needs to breathe
Round 1 of this redesign silently dropped the original `label { margin: 0.7rem 0 }` rule, making every stacked field in every item card cramped (zero vertical margin between label and field, between field groups). Restore generous vertical rhythm: real margin between every label and its input, and between stacked field groups (Title → Tone/Priority → update-line → Detail → Speaker-note seed). Increase overall card padding too — content should not sit tight against card edges.

### 5. Card / section structure — match pxd's actual anatomy
- Cards: white background, `border-radius: 16px`, a real visible box-shadow (pxd's stronger "pop" value, not a flat/subtle one) so tiles/cards visually lift off the page background.
- Section headings (`Step 1 / Meeting context`, `Step 2 / Agenda items`, final lock step) should sit on the plain page background, NOT trapped inside the same card as the form fields below them — pxd's own headings float free, with independent cards underneath. This was fixed in round 3; verify it's still correct.
- Section-to-section visual separation should read naturally from this structure (heading + rule, then a gap, then the next card) — no extra divider element needed.

### 6. Full-page verification screenshots required before any handback
Every round of this redesign needs: (a) a genuine top-to-bottom full-page screenshot (not a cropped viewport, not a fragment), (b) at least one detail crop of a filled-in item card showing the pill system, (c) labelled clearly as "Meeting Prep Intake" (this repo has a SEPARATE speaking-brief output template that looks similar — do not confuse the two, and do not touch or re-render the Speaking Brief template as a side effect of testing this one).

### 7. Approval gate
Standard for this repo: no merge, no push to `main`, until Kevin has seen real screenshots and given his own direct, explicit approval. Screenshot-and-wait is not optional and isn't satisfied by an agent's own claim that something looks right.

## Verification standard
Every claim of "fixed" must be checked directly (computed styles in a real rendered page, actual screenshots, `npm test` if present) — not taken on Codex's own self-report. This repo has already had two false "reviewed: PASS" self-claims from Codex during this same redesign; the reviewing agent must independently re-verify every round, every time.
