"""Direct Granola REST API integration for meeting-connector.

Ports the proven fetch/auth/parsing plumbing from work-inbox's
`fetch_inbox.py` Phase 3.7b -- confirmed live in production since 4 July
2026, closed and marked "do not modify" in that repo's own HANDOVER.md.
This module is an independent implementation; it does not import or
depend on work-inbox at runtime, and work-inbox's own copy is left
untouched.

What is genuinely ported as-is (same auth header, same two endpoints,
same summary-field fallback order -- all previously debugged live against
real API responses on 3-4 July 2026):

- `Authorization: Bearer <GRANOLA_API_KEY>` on every call.
- `GET /v1/notes?created_after=<ISO8601>` to list notes, and
  `GET /v1/notes/{id}?include=transcript` for detail -- the
  `?include=transcript` parameter is required or the API returns no
  usable summary content at all.
- Summary extraction fallback order: `summary` (string or dict) ->
  `summary_text` -> `summary_markdown`. A live probe of the real API on
  19 August 2026 found no bare `summary` key on any note at all in the
  current API version -- only `summary_text`/`summary_markdown` -- so the
  first branch is now purely defensive/forward-compatible, matching
  work-inbox's own comment about why the fallback exists.

What is genuinely NEW, not ported (see `select_latest_matching_note`):
work-inbox's matcher answers "which note best matches THIS ALREADY-KNOWN
calendar item's title", scored by keyword overlap within a short (10 day)
lookback, first-best-score wins. meeting-connector needs a different
question answered: "what is the single LATEST note matching a RECURRING
MEETING-TYPE title pattern" (e.g. "HR Systems Roadmap") over a much
longer horizon -- Kevin has had real 7+ week meeting gaps, so several
same-pattern-titled notes can exist across the lookback window, and the
selection must be by actual note recency, not by which one happens to
score highest or appear first.

Read-only. Every function below only ever issues HTTP GET.
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.parse import quote

GRANOLA_API_BASE = "https://public-api.granola.ai/v1"

# Kevin has had real single meeting-type gaps of 7+ weeks (see
# voice-workflows/PROGRAMME_STATUS.md, 1 Aug 2026: no HR Systems Roadmap
# meeting captured in Granola between 3 Jul and 1 Aug). 120 days gives
# comfortable headroom above any gap observed so far without scanning
# indefinitely.
DEFAULT_LOOKBACK_DAYS = 120

# Safety cap on pagination. The live API returns ~10 notes/page; 12 pages
# (~120 notes) comfortably covers a 120-day lookback for this mailbox's
# real note volume (confirmed live: 19 August 2026's most recent 20 notes
# already reached back to 2 July) while guaranteeing this can never loop
# indefinitely if `hasMore` were ever stuck true.
MAX_PAGES = 12


class GranolaError(RuntimeError):
    """Raised for a genuine Granola API failure (auth, network, HTTP error)."""


def is_configured() -> bool:
    """True if GRANOLA_API_KEY is present in this process's environment."""
    return bool(os.environ.get("GRANOLA_API_KEY"))


def _as_text(value: Any) -> str:
    """Coerce a possibly-malformed API field to a plain string. A Codex
    review pass (19 Aug 2026, pass 2) correctly found that a non-string
    but truthy field (e.g. a note `title` or `summary_text` coming back
    as a number from a malformed/unexpected API response) would otherwise
    raise TypeError/AttributeError deep inside `_keywords`/`extract_summary`,
    outside the try/except boundaries in `find_latest_meeting` -- this
    closes that gap at the source rather than trying to guard every call
    site."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def _created_at(note: Any) -> str:
    """Return a note's `created_at` only if it is a genuinely valid ISO
    8601 timestamp, else "". A Codex review pass (19 Aug 2026, pass 3)
    found that `_as_text()` alone prevents a crash but does not stop an
    invalid value (e.g. a bare int like 20260814, or a non-date string)
    from sorting as if it were a valid, comparable date. A follow-up pass
    (pass 4) then found a hand-rolled digit-shape regex was too permissive
    -- it accepted impossible calendar values like "2099-99-99T99:99:99Z".
    `datetime.fromisoformat()` does genuine calendar validation (confirmed
    live: it also correctly parses the real API's actual format, including
    milliseconds and a trailing "Z", e.g. "2026-08-19T14:18:13.671Z").
    An invalid/missing value sorts as "" (lower than any real ISO
    timestamp), so it can never win selection and never passes an
    inclusive `>=` cutoff comparison against a real cutoff string."""
    if not isinstance(note, dict):
        return ""
    value = _as_text(note.get("created_at"))
    if not value:
        return ""
    try:
        datetime.fromisoformat(value)
    except ValueError:
        return ""
    return value


def _keywords(title: Any) -> set[str]:
    """Same normalisation as work-inbox's proven `_granola_keywords`:
    strip DD/MM dates, bare years, dashes/ampersands and punctuation,
    lowercase, tokenise on whitespace. See `select_latest_matching_note`
    for the actual match threshold applied to these keyword sets (a plain
    >=1 threshold, as work-inbox uses, is deliberately NOT used here)."""
    t = re.sub(r"\b\d{1,2}/\d{2}\b", "", _as_text(title))
    t = re.sub(r"\b\d{4}\b", "", t)
    t = re.sub(r"[—\-&]", " ", t)
    t = re.sub(r"[^\w\s]", "", t)
    return set(w.lower() for w in t.split() if len(w) >= 2)


def _http_get(url: str, api_key: str) -> dict[str, Any]:
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {api_key}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        raise GranolaError(
            f"Granola API returned HTTP {exc.code} for {url}"
        ) from exc
    except urllib.error.URLError as exc:
        raise GranolaError(f"Granola API request failed: {exc.reason}") from exc
    try:
        return json.loads(raw.decode())
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise GranolaError(f"Granola API returned invalid JSON for {url}") from exc


def fetch_notes_page(
    api_key: str,
    *,
    created_after: str | None = None,
    cursor: str | None = None,
) -> dict[str, Any]:
    """One page of `GET /v1/notes`. Pass either `created_after` (first
    page) or `cursor` (subsequent pages) -- not both; a live probe of the
    real API (19 Aug 2026) confirmed cursor-only pagination continues
    correctly without re-supplying created_after."""
    if cursor:
        url = f"{GRANOLA_API_BASE}/notes?cursor={quote(cursor, safe='')}"
    elif created_after:
        url = f"{GRANOLA_API_BASE}/notes?created_after={quote(created_after, safe='')}"
    else:
        url = f"{GRANOLA_API_BASE}/notes"
    return _http_get(url, api_key)


def fetch_note_detail(api_key: str, note_id: str) -> dict[str, Any]:
    """`GET /v1/notes/{id}?include=transcript` -- the query param is
    required or the API returns no usable summary field at all (root
    cause of work-inbox's 3 Jul 2026 fix, commit e595218d)."""
    url = f"{GRANOLA_API_BASE}/notes/{quote(note_id, safe='')}?include=transcript"
    return _http_get(url, api_key)


def extract_summary(detail: dict[str, Any]) -> str:
    """Same fallback order as work-inbox's proven Phase 3.7b logic,
    confirmed against a real live detail response on 19 Aug 2026 (which
    had no bare `summary` key at all -- only summary_text/summary_markdown
    were populated): summary (string or dict) -> summary_text ->
    summary_markdown."""
    raw = detail.get("summary") if isinstance(detail, dict) else None
    if isinstance(raw, dict):
        text = _as_text(raw.get("text") or raw.get("content") or "").strip()
    elif raw:
        text = _as_text(raw).strip()
    else:
        text = ""
    if not text and isinstance(detail, dict):
        text = _as_text(
            detail.get("summary_text") or detail.get("summary_markdown") or ""
        ).strip()
    return text


def select_latest_matching_note(
    notes: list[dict[str, Any]], title_pattern: str
) -> dict[str, Any] | None:
    """Pure function, no network -- the genuinely new logic (see module
    docstring). Among `notes` whose title shares enough normalised keywords
    with `title_pattern`, return the one with the latest `created_at` (ISO
    8601 strings sort correctly as plain strings).

    Threshold: requires at least (len(pattern keywords) - 1) shared
    keywords, floored at 1 -- i.e. the note's title may miss at most ONE
    of the pattern's words. A Codex review pass (19 Aug 2026, pass 1)
    flagged that a bare >=1 threshold was too permissive once selection
    prioritises RECENCY among matches rather than best score -- e.g. a
    newer "HR Operations update" note would otherwise beat the actual
    older "HR Systems Roadmap" note on the single shared "hr" token. The
    fix shipped then was a flat min(2, len(pattern_kw)) floor, but that
    was ITSELF found live-broken 20 Aug 2026: it let "HR Systems
    Managers Meeting" (4 keywords: hr, systems, managers, meeting) wrongly
    match "HR Systems Roadmpa 03/07" (shares only "hr"+"systems", 2
    keywords -- meeting the flat floor of min(2,4)=2 despite being a
    genuinely different, real, distinct Granola note series -- confirmed
    live: "HR Systems Managers Meeting 24/06" and "29/04" and "15/04" all
    exist as their own real notes). A flat floor of 2 can never scale with
    how DISTINCTIVE a longer pattern is; "missing at most one word" does:
    for the 3-keyword "HR Systems Roadmap" pattern it still requires 2
    (surviving the real "Roadmpa" typo, which only drops one word), but
    for the 4-keyword "HR Systems Managers Meeting" pattern it now
    correctly requires 3, rejecting the "hr"+"systems"-only false-positive
    match against the Roadmap note.

    Returns None if `title_pattern` normalises to nothing, or no note
    matches."""
    pattern_kw = _keywords(title_pattern)
    if not pattern_kw:
        return None
    required_overlap = max(1, len(pattern_kw) - 1)
    candidates = []
    for note in notes:
        if not isinstance(note, dict) or not note.get("id") or not note.get("title"):
            continue
        overlap = pattern_kw & _keywords(note["title"])
        if len(overlap) >= required_overlap:
            candidates.append(note)
    if not candidates:
        return None
    return max(candidates, key=_created_at)


def find_latest_meeting(
    title_pattern: str,
    *,
    api_key: str | None = None,
    lookback_days: int = DEFAULT_LOOKBACK_DAYS,
    max_pages: int = MAX_PAGES,
) -> dict[str, Any]:
    """Network-touching orchestrator. Paginates the live Granola notes
    list back to `lookback_days`, finds the single latest note matching
    `title_pattern`, fetches its full detail for the summary, and returns
    a compact result. Read-only throughout -- issues GET requests only,
    never writes anything.

    Status values: "unavailable" (no API key in this environment), "error"
    (a genuine Granola API failure or unexpected malformed response),
    "no_match" (fully scanned back to the lookback boundary, no matching
    note found), "no_match_incomplete_scan" (hit the `max_pages` safety
    cap before reaching the lookback boundary or a natural end -- a real
    match may exist further back, this is NOT the same claim as
    "no_match"), "found".
    """
    key = api_key if api_key is not None else os.environ.get("GRANOLA_API_KEY", "")
    if not key:
        return {
            "status": "unavailable",
            "titlePattern": title_pattern,
            "reason": "GRANOLA_API_KEY is not set in this environment.",
        }

    # Clamp lookback_days defensively: this is an MCP tool parameter an LLM
    # caller supplies, not a trusted internal value. A Codex review pass
    # (19 Aug 2026, pass 3) found an out-of-range value (e.g. 10**100)
    # raises OverflowError from timedelta() -- clamping first avoids that
    # regardless of where the computation happens.
    safe_lookback_days = max(1, min(int(lookback_days), 3650))

    all_notes: list[dict[str, Any]] = []
    cursor: str | None = None
    reached_natural_end = False
    try:
        lookback_cutoff = (
            datetime.now(timezone.utc) - timedelta(days=safe_lookback_days)
        ).strftime("%Y-%m-%dT%H:%M:%SZ")

        for _ in range(max_pages):
            page = fetch_notes_page(
                key,
                created_after=None if cursor else lookback_cutoff,
                cursor=cursor,
            )
            if not isinstance(page, dict):
                raise GranolaError("Granola API returned an unexpected (non-object) response.")
            raw_notes = page.get("notes")
            if raw_notes is not None and not isinstance(raw_notes, list):
                # Codex review pass 3: a malformed non-list "notes" field
                # (e.g. {}) must not be silently coerced into "we searched
                # and found nothing" -- that is a genuine API contract
                # violation, not a confirmed absence.
                raise GranolaError("Granola API returned a non-list 'notes' field.")
            notes = raw_notes or []
            if not notes:
                reached_natural_end = True
                break
            # created_after only reliably bounds the FIRST page server-side;
            # once paginating by cursor alone, stop client-side as soon as a
            # genuinely-dated note falls before the cutoff (notes arrive
            # newest-first, so this is a safe early exit, not just an
            # optimisation). A Codex review pass (19 Aug 2026, pass 4)
            # found the previous count-based comparison (len(in_range) <
            # len(notes)) wrongly treated a malformed list member (e.g.
            # None, or a note with an unparseable created_at) as a
            # past-cutoff signal purely because it got excluded for a
            # DIFFERENT reason -- which could truncate pagination early and
            # miss a real match on a later page. Malformed/undated entries
            # are now just skipped; only a genuinely-dated note that is
            # actually before the cutoff sets the stop signal.
            in_range = []
            saw_note_past_cutoff = False
            for note in notes:
                if not isinstance(note, dict):
                    continue
                note_created_at = _created_at(note)
                if not note_created_at:
                    continue
                if note_created_at >= lookback_cutoff:
                    in_range.append(note)
                else:
                    saw_note_past_cutoff = True
            all_notes.extend(in_range)
            if saw_note_past_cutoff or not page.get("hasMore"):
                reached_natural_end = True
                break
            cursor = page.get("cursor")
            if not cursor:
                reached_natural_end = True
                break
            # else: loop continues: reached_natural_end stays False if the
            # `max_pages` cap is hit without ever reaching a natural stop.
    except GranolaError as exc:
        return {"status": "error", "titlePattern": title_pattern, "reason": str(exc)}
    except Exception as exc:  # defensive: never let a malformed response escape unstructured
        return {
            "status": "error",
            "titlePattern": title_pattern,
            "reason": f"Unexpected failure while listing Granola notes: {exc}",
        }

    best = select_latest_matching_note(all_notes, title_pattern)
    if not best:
        result: dict[str, Any] = {
            "status": "no_match" if reached_natural_end else "no_match_incomplete_scan",
            "titlePattern": title_pattern,
            "lookbackDays": safe_lookback_days,
            "notesScanned": len(all_notes),
        }
        if not reached_natural_end:
            result["reason"] = (
                f"Stopped after the {max_pages}-page safety cap without "
                "reaching the lookback boundary; a matching note may exist "
                "further back and this result should not be treated as a "
                "confirmed absence."
            )
        return result

    try:
        detail = fetch_note_detail(key, best["id"])
        if not isinstance(detail, dict):
            # Codex review pass 3: a malformed non-object detail response
            # (e.g. a bare list) must not be reported as "found" with a
            # silently empty summary -- that would let the workflow treat
            # a genuinely unavailable outcome as successfully captured.
            raise GranolaError(
                "Granola API returned an unexpected (non-object) note detail response."
            )
    except GranolaError as exc:
        return {
            "status": "error",
            "titlePattern": title_pattern,
            "reason": str(exc),
            "noteId": best["id"],
            "noteTitle": best.get("title"),
            "createdAt": best.get("created_at"),
        }
    except Exception as exc:  # defensive: same rationale as the listing loop above
        return {
            "status": "error",
            "titlePattern": title_pattern,
            "reason": f"Unexpected failure while fetching Granola note detail: {exc}",
            "noteId": best["id"],
            "noteTitle": best.get("title"),
            "createdAt": best.get("created_at"),
        }

    # detail is guaranteed to be a dict here -- the type check above raises
    # GranolaError (caught, returns status "error") for anything else.
    summary = extract_summary(detail)
    return {
        "status": "found",
        "titlePattern": title_pattern,
        "noteId": best["id"],
        "noteTitle": best.get("title"),
        "createdAt": best.get("created_at"),
        "webUrl": detail.get("web_url"),
        "summary": summary,
        # A Codex review pass (19 Aug 2026, pass 4) noted that "found"
        # with a silently empty summary could read as a captured outcome
        # when there is genuinely nothing to report (e.g. a real note
        # with no generated summary content). The note itself was
        # genuinely found and matched -- that part of "found" is correct
        # -- so this stays a boolean flag rather than a new status value,
        # letting the caller (the launcher's dispatch prompt) decide
        # whether an empty summary should be treated the same as
        # Granola being unavailable for this specific meeting.
        "hasSummary": bool(summary),
        "lookbackDays": safe_lookback_days,
        "notesScanned": len(all_notes),
    }
