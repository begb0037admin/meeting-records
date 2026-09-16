# Meeting Prep Intake

Private Cloudflare Worker and static interface for creating immutable meeting-intake records. GitHub remains the only durable store; the browser never has a GitHub credential. Revisions create a new `*.revision-<timestamp>.json` record with `supersedes`; the client must provide the latest Contents API SHA, so a stale revision is rejected instead of overwriting anything.

**Phase 1** (merged, live at `meeting.lelitte.co.uk`): meeting picker, agenda-item workspace, carry-forward, and the immutable GitHub submission gateway.

**Phase 2** (merged, live): per-item Lauren chat (`/api/chat`) backed by a dedicated `CHAT_KV` namespace keyed by `draftId:itemId`, and Workers AI voice routes (`/api/voice/stt`, `/api/voice/tts`). Chat is never durable on its own — Kevin can click "Attach reply to detail" to append a Lauren reply into the Detail field before it is submitted.

**Phase 3** (merged, live): per-item `.xlsx` upload/extraction (`/api/extract`) with extension/signature/macro/size rejection, bounded sheet previews (no formula evaluation), and sheet selection that can be attached into Detail. The raw upload is never persisted; only a bounded preview lives in `CHAT_KV` for one hour.

**Field-simplification change** (16 Sept 2026, folded into the Phase 3 PR): the browser no longer shows a separate "Confirmed context" field. Kevin's real workflow has no unverified-vs-confirmed distinction — everything pasted into Detail (an email, a transcript) is already a verified source, so a second field asking him to re-enter the same content was pure duplicate data entry. The client now submits `confirmedContext` equal to `detail` automatically; the backend schema and Lauren's chat payload shape are unchanged (`confirmedContext` is still a required string on `/api/intakes/submit` and is still sent to `/api/chat`), only the browser UI and what the user has to type changed. "Attach selected sheets to detail" (Excel extraction) now appends into Detail the same way.

**Phase 4** (merged, live): `/api/speaker-notes/candidate` — given an item's title/tone/detail/confirmedContext and any selected extraction sheets, Lauren proposes one candidate spoken line for the Speaker-note seed field, using the same tone-prefix conventions as chat. Stateless (no KV/GitHub write); the "Suggest speaker note" button overwrites the visible Speaker-note seed field only, for Kevin to review/edit before submitting. Style is sourced from and kept in sync with the canonical [`meeting-records/styles/speaker-note-style.md`](https://github.com/begb0037admin/agent-commons/blob/main/meeting-records/styles/speaker-note-style.md) in `begb0037admin/agent-commons`, alongside that repo's `memory/kevin-email-drafting-style.md` — not a locally-diverging copy of style guidance. This is the last of the four phases in the original build proposal (§14).

## Deploy preparation (do not deploy from this build)

1. In `meeting-prep-intake/`, run `wrangler secret put GITHUB_PAT`. Use a fine-grained token limited to Contents read/write for `begb0037admin/meeting-records` only.
2. Run `wrangler secret put ANTHROPIC_API_KEY` for Lauren chat; never commit either secret.
3. Run `wrangler kv namespace create CHAT_KV` once and paste its returned ID into `wrangler.toml` in place of the documented placeholder.
4. Set `ALLOWED_ORIGIN` as a Worker environment variable to the exact deployed origin, for example `https://meeting-prep.example.org`.
5. Deploy with `wrangler deploy` only after review.
6. In Cloudflare Zero Trust, add an **Access Application** for that exact deployed hostname and a policy allowing only Kevin’s approved identity; leave the Worker origin behind that application. This is the one required manual Access configuration step. (As of the Phase 1 deploy, Kevin explicitly asked for this to be reversed on the live `meeting.lelitte.co.uk` hostname — see `CHECKPOINT.md`'s "Access provisioned, then explicitly removed" entry before assuming this step should run again without checking with him first.)

All four phases from the original build proposal are now built and live. There is still no Outlook, Graph, COM, or SharePoint access anywhere in this tool, and no Cloudflare Access gate in front of `meeting.lelitte.co.uk` — a deliberate, Kevin-confirmed decision recorded in `CHECKPOINT.md`.

## Tests

`node --test test/worker.test.mjs` exercises schema validation, carry-forward selection, immutable/revision GitHub write behaviour, chat/voice, `.xlsx` extraction safety, and speaker-note candidate generation, all against a mocked Contents/Anthropic API. The renderer can be smoke-tested with the synthetic fixture in `test/fixtures/` once the existing `brief_chrome.py` font/crest scratch assets are available.
