# Meeting Prep Intake — Phase 1

Private Cloudflare Worker and static interface for creating immutable meeting-intake records. GitHub remains the only durable store; the browser never has a GitHub credential. Revisions create a new `*.revision-<timestamp>.json` record with `supersedes`; the client must provide the latest Contents API SHA, so a stale revision is rejected instead of overwriting anything.

## Deploy preparation (do not deploy from this build)

1. In `meeting-prep-intake/`, run `wrangler secret put GITHUB_PAT`. Use a fine-grained token limited to Contents read/write for `begb0037admin/meeting-records` only.
2. Set `ALLOWED_ORIGIN` as a Worker environment variable to the exact deployed origin, for example `https://meeting-prep.example.org`; `GITHUB_PAT` is the only secret.
3. Deploy with `wrangler deploy` only after review.
4. In Cloudflare Zero Trust, add an **Access Application** for that exact deployed hostname and a policy allowing only Kevin’s approved identity; leave the Worker origin behind that application. This is the one required manual Access configuration step.

Phase 2/3 integration points are intentionally marked in the UI and Worker. There is no chat, voice, extraction, file upload, Outlook, Graph, COM, or SharePoint access in Phase 1.

## Tests

`node --test test/worker.test.mjs` exercises schema validation, carry-forward selection, and immutable/revision GitHub write behaviour with a mocked Contents API. The renderer can be smoke-tested with the synthetic fixture in `test/fixtures/` once the existing `brief_chrome.py` font/crest scratch assets are available.
