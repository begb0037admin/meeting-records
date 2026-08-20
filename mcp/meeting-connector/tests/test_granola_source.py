import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from meeting_context import granola_source
from meeting_context.granola_source import (
    extract_summary, find_latest_meeting, select_latest_matching_note,
)

FIXTURE_PATH = (
    Path(__file__).resolve().parent.parent / "fixtures" / "granola-notes-sample.json"
)


def _load_fixture() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


class GranolaKeywordMatchingTests(unittest.TestCase):
    """Pure-function tests, no network. This is the genuinely new logic --
    see granola_source.py's module docstring for why it differs from
    work-inbox's proven Phase 3.7b matcher."""

    def test_latest_matching_note_wins_over_earlier_match(self):
        # Two notes both match "HR Systems Roadmap"; the newer one must win
        # even though it is NOT first in the list -- this is the actual
        # behaviour change from work-inbox's first-best-score matcher.
        notes = [
            {"id": "old", "title": "HR Systems Roadmap — 03/07", "created_at": "2026-07-03T06:40:29Z"},
            {"id": "new", "title": "HR Systems Roadmap — 14/08", "created_at": "2026-08-14T06:40:29Z"},
        ]
        result = select_latest_matching_note(notes, "HR Systems Roadmap")
        self.assertEqual(result["id"], "new")

    def test_typo_title_still_matches_via_two_keyword_threshold(self):
        # Real observed case, live API, 19 Aug 2026: a note titled
        # "HR Systems Roadmpa 03/07" (Granola's own typo, not ours) must
        # still match "HR Systems Roadmap" -- it shares 2 keywords ("hr",
        # "systems"), meeting the min(2, len(pattern_kw)) threshold even
        # though "roadmpa" != "roadmap".
        notes = [{"id": "typo", "title": "HR Systems Roadmpa 03/07", "created_at": "2026-07-03T06:40:29Z"}]
        result = select_latest_matching_note(notes, "HR Systems Roadmap")
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "typo")

    def test_unrelated_titles_do_not_match(self):
        notes = [
            {"id": "unrelated", "title": "Sickness Absence Survey working group", "created_at": "2026-08-18T10:05:50Z"},
        ]
        self.assertIsNone(select_latest_matching_note(notes, "HR Systems Roadmap"))

    def test_single_shared_keyword_false_positive_is_rejected(self):
        # Codex review finding, 19 Aug 2026: a bare >=1 threshold let a
        # NEWER unrelated note beat the actual older Roadmap note purely
        # on one shared token ("HR"), because selection ranks by recency
        # among matches. The 2-keyword threshold must reject this.
        notes = [
            {"id": "roadmap_older", "title": "HR Systems Roadmap — 03/07", "created_at": "2026-07-03T06:40:29Z"},
            {"id": "false_positive_newer", "title": "HR Operations update", "created_at": "2026-08-18T09:00:00Z"},
        ]
        result = select_latest_matching_note(notes, "HR Systems Roadmap")
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "roadmap_older")

    def test_cross_meeting_type_false_positive_is_rejected(self):
        # Real live bug, 20 Aug 2026: querying get_latest_granola_meeting
        # with "HR Systems Managers Meeting" (a genuinely distinct,
        # real Granola note series -- confirmed live: "HR Systems Managers
        # Meeting 24/06", "29/04", "15/04" all exist) wrongly returned the
        # 3 July "HR Systems Roadmap" note instead, because the flat
        # min(2, len(pattern_kw)) floor let "hr"+"systems" alone satisfy a
        # 4-keyword pattern. Caught by hand before it reached Kevin (the
        # real answer was verified by pulling the raw note list directly),
        # then fixed here: a 4-keyword pattern now requires 3 shared
        # keywords, so "hr"+"systems" alone (2) is correctly rejected.
        notes = [
            {"id": "roadmap_note", "title": "HR Systems Roadmpa 03/07", "created_at": "2026-07-03T06:40:29Z"},
            {"id": "real_managers_meeting", "title": "HR Systems Managers Meeting 24/06", "created_at": "2026-06-24T08:12:12Z"},
        ]
        result = select_latest_matching_note(notes, "HR Systems Managers Meeting")
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "real_managers_meeting")

    def test_cross_meeting_type_false_positive_rejected_even_when_only_candidate(self):
        # Same bug, isolated further: even with NO real Managers Meeting
        # note present at all, the Roadmap note must not be returned as a
        # false-positive match for a "HR Systems Managers Meeting" query --
        # the correct result is no match, not a wrong match.
        notes = [
            {"id": "roadmap_note", "title": "HR Systems Roadmpa 03/07", "created_at": "2026-07-03T06:40:29Z"},
        ]
        result = select_latest_matching_note(notes, "HR Systems Managers Meeting")
        self.assertIsNone(result)

    def test_missing_id_or_title_is_skipped_not_crashed_on(self):
        notes = [
            {"title": "HR Systems Roadmap — 14/08", "created_at": "2026-08-14T06:40:29Z"},  # no id
            {"id": "no-title", "created_at": "2026-08-14T06:40:29Z"},  # no title
            "not-even-a-dict",
        ]
        self.assertIsNone(select_latest_matching_note(notes, "HR Systems Roadmap"))

    def test_no_notes_returns_none(self):
        self.assertIsNone(select_latest_matching_note([], "HR Systems Roadmap"))

    def test_empty_pattern_returns_none(self):
        notes = [{"id": "x", "title": "HR Systems Roadmap — 14/08", "created_at": "2026-08-14T06:40:29Z"}]
        self.assertIsNone(select_latest_matching_note(notes, ""))

    def test_non_string_title_and_created_at_do_not_crash(self):
        # Codex review finding, 19 Aug 2026, pass 2: a malformed API
        # response with a non-string title/created_at (e.g. numbers) must
        # not raise TypeError/AttributeError deep inside matching/sorting.
        notes = [{"id": "weird", "title": 12345, "created_at": 20260814}]
        # "12345" shares no keywords with "HR Systems Roadmap" -- correctly
        # no match, but critically: no exception either.
        self.assertIsNone(select_latest_matching_note(notes, "HR Systems Roadmap"))
        # A non-string title that DOES coerce to matching text must still work.
        notes2 = [{"id": "weird2", "title": "HR Systems Roadmap 14/08", "created_at": 20260814}]
        result = select_latest_matching_note(notes2, "HR Systems Roadmap")
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "weird2")


class GranolaSummaryExtractionTests(unittest.TestCase):
    """Same fallback order as work-inbox's proven Phase 3.7b, confirmed
    against a real live detail response 19 Aug 2026 (no bare `summary` key
    was present at all -- only summary_text/summary_markdown)."""

    def test_string_summary_used_directly(self):
        self.assertEqual(extract_summary({"summary": "Plain text summary."}), "Plain text summary.")

    def test_dict_summary_prefers_text_field(self):
        self.assertEqual(
            extract_summary({"summary": {"text": "From text field.", "content": "ignored"}}),
            "From text field.",
        )

    def test_falls_back_to_summary_text_when_summary_absent(self):
        detail = {"summary_text": "Fallback via summary_text.", "summary_markdown": "**md**"}
        self.assertEqual(extract_summary(detail), "Fallback via summary_text.")

    def test_falls_back_to_summary_markdown_last(self):
        detail = {"summary_markdown": "**only markdown**"}
        self.assertEqual(extract_summary(detail), "**only markdown**")

    def test_no_summary_anywhere_returns_empty_string(self):
        self.assertEqual(extract_summary({}), "")

    def test_non_string_summary_fields_do_not_crash(self):
        # Codex review finding, 19 Aug 2026, pass 2: a numeric summary_text
        # (malformed API response) must not raise AttributeError from a
        # bare .strip() call on a non-string value.
        self.assertEqual(extract_summary({"summary_text": 12345}), "12345")
        self.assertEqual(extract_summary({"summary": 6789}), "6789")
        self.assertEqual(extract_summary("not even a dict"), "")


class GranolaFindLatestMeetingTests(unittest.TestCase):
    """Network-touching orchestrator, tested by replaying one real recorded
    response shape (fixtures/granola-notes-sample.json) -- never hits the
    live API in tests."""

    def setUp(self):
        self.fixture = _load_fixture()

    def _fake_fetch_notes_page(self, api_key, *, created_after=None, cursor=None):
        if cursor:
            self.assertEqual(cursor, "fixture-cursor-page2")
            return self.fixture["page2"]
        self.assertIsNotNone(created_after)
        return self.fixture["page1"]

    def _fake_fetch_note_detail(self, api_key, note_id):
        self.assertEqual(note_id, "not_fixture_roadmap_recent")
        return self.fixture["detail"]

    def test_finds_latest_matching_note_across_pages_and_returns_summary(self):
        with patch.object(granola_source, "fetch_notes_page", side_effect=self._fake_fetch_notes_page), \
             patch.object(granola_source, "fetch_note_detail", side_effect=self._fake_fetch_note_detail):
            result = find_latest_meeting(
                "HR Systems Roadmap", api_key="fixture-key", lookback_days=120
            )
        self.assertEqual(result["status"], "found")
        # The 14 Aug note must win over the 3 Jul typo'd note found on page 2.
        self.assertEqual(result["noteId"], "not_fixture_roadmap_recent")
        self.assertEqual(result["createdAt"], "2026-08-14T06:40:29.259Z")
        self.assertIn("Fixture summary text", result["summary"])
        self.assertEqual(result["notesScanned"], 5)

    def test_no_api_key_returns_unavailable_without_any_network_call(self):
        with patch.object(granola_source, "fetch_notes_page") as fake_fetch:
            result = find_latest_meeting("HR Systems Roadmap", api_key="")
        fake_fetch.assert_not_called()
        self.assertEqual(result["status"], "unavailable")

    def test_pattern_with_no_match_in_fixture_returns_no_match(self):
        with patch.object(granola_source, "fetch_notes_page", side_effect=self._fake_fetch_notes_page), \
             patch.object(granola_source, "fetch_note_detail") as fake_detail:
            result = find_latest_meeting(
                "Nonexistent Meeting Type", api_key="fixture-key", lookback_days=120
            )
        fake_detail.assert_not_called()
        self.assertEqual(result["status"], "no_match")
        self.assertEqual(result["notesScanned"], 5)

    def test_granola_error_during_listing_returns_error_status(self):
        def _raise(*args, **kwargs):
            raise granola_source.GranolaError("simulated failure")

        with patch.object(granola_source, "fetch_notes_page", side_effect=_raise):
            result = find_latest_meeting("HR Systems Roadmap", api_key="fixture-key")
        self.assertEqual(result["status"], "error")
        self.assertIn("simulated failure", result["reason"])

    def test_malformed_response_during_listing_returns_error_not_a_crash(self):
        # Codex review finding, 19 Aug 2026: only HTTPError/URLError were
        # caught before -- a malformed (non-dict) page must not raise an
        # unhandled exception up into the MCP tool caller.
        with patch.object(granola_source, "fetch_notes_page", return_value="not a dict"):
            result = find_latest_meeting("HR Systems Roadmap", api_key="fixture-key")
        self.assertEqual(result["status"], "error")

    def test_max_pages_cap_reached_reports_incomplete_scan_not_no_match(self):
        # Codex review finding, 19 Aug 2026: hitting the page-cap safety
        # limit before reaching the lookback boundary must be distinguished
        # from a genuine, fully-scanned absence.
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        always_more_page = {
            "notes": [
                {"id": "recent", "title": "Sickness Absence Survey working group", "created_at": now_iso}
            ],
            "hasMore": True,
            "cursor": "keeps-going-forever",
        }
        with patch.object(granola_source, "fetch_notes_page", return_value=always_more_page):
            result = find_latest_meeting(
                "HR Systems Roadmap", api_key="fixture-key", lookback_days=120, max_pages=3
            )
        self.assertEqual(result["status"], "no_match_incomplete_scan")
        self.assertEqual(result["notesScanned"], 3)
        self.assertIn("safety cap", result["reason"])

    def test_absurd_lookback_days_is_clamped_not_a_crash(self):
        # Codex review finding, 19 Aug 2026, pass 3: an out-of-range
        # lookback_days (an MCP parameter an LLM caller supplies) used to
        # raise OverflowError from timedelta() before any structured
        # status could be returned.
        empty_page = {"notes": [], "hasMore": False, "cursor": None}
        with patch.object(granola_source, "fetch_notes_page", return_value=empty_page):
            result = find_latest_meeting(
                "HR Systems Roadmap", api_key="fixture-key", lookback_days=10**100
            )
        self.assertIn(result["status"], ("no_match", "no_match_incomplete_scan"))
        self.assertEqual(result["lookbackDays"], 3650)

    def test_non_list_notes_field_is_an_error_not_a_confirmed_absence(self):
        # Codex review finding, 19 Aug 2026, pass 3: a malformed "notes": {}
        # was silently coerced to [] and reported as a confirmed "no_match"
        # -- that is an API contract violation, not a real absence.
        malformed_page = {"notes": {}, "hasMore": True, "cursor": "x"}
        with patch.object(granola_source, "fetch_notes_page", return_value=malformed_page):
            result = find_latest_meeting("HR Systems Roadmap", api_key="fixture-key")
        self.assertEqual(result["status"], "error")

    def test_invalid_created_at_cannot_win_over_a_valid_older_match(self):
        # Codex review finding, 19 Aug 2026, pass 3: _as_text() alone
        # prevented a crash but let an invalid created_at sort as if
        # comparable, letting it incorrectly win latest-note selection
        # over a genuinely valid, real (older) timestamp. Uses a
        # non-ISO garbage string here specifically -- a bare compact date
        # like "20260814" is actually a VALID ISO 8601 basic-format date
        # once datetime.fromisoformat() is the validator (pass 4), so it
        # is not a usable "invalid" example any more; see
        # test_impossible_calendar_timestamp_is_rejected for the
        # impossible-calendar-value case instead.
        page = {
            "notes": [
                {"id": "invalid_date", "title": "HR Systems Roadmap — bad date", "created_at": "not-a-real-timestamp"},
                {"id": "valid_older", "title": "HR Systems Roadmap — 03/07", "created_at": "2026-07-03T06:40:29Z"},
            ],
            "hasMore": False,
            "cursor": None,
        }

        def fake_detail(api_key, note_id):
            self.assertEqual(note_id, "valid_older")
            return {"summary_text": "ok"}

        with patch.object(granola_source, "fetch_notes_page", return_value=page), \
             patch.object(granola_source, "fetch_note_detail", side_effect=fake_detail):
            result = find_latest_meeting("HR Systems Roadmap", api_key="fixture-key")
        self.assertEqual(result["status"], "found")
        self.assertEqual(result["noteId"], "valid_older")

    def test_non_object_detail_response_is_an_error_not_found(self):
        # Codex review finding, 19 Aug 2026, pass 3: a malformed non-object
        # detail response (e.g. a bare list) was reported as "found" with
        # a silently empty summary, misrepresenting an unavailable outcome
        # as successfully captured.
        with patch.object(granola_source, "fetch_notes_page", side_effect=self._fake_fetch_notes_page), \
             patch.object(granola_source, "fetch_note_detail", return_value=[]):
            result = find_latest_meeting("HR Systems Roadmap", api_key="fixture-key")
        self.assertEqual(result["status"], "error")

    def test_found_with_no_summary_content_reports_has_summary_false(self):
        # Codex review finding, 19 Aug 2026, pass 4: a real note can be
        # genuinely found and matched but have no usable summary content
        # (e.g. Granola never generated one) -- "found" is still correct
        # (the note itself was really located), but the caller needs a
        # signal that there is nothing substantive to report.
        with patch.object(granola_source, "fetch_notes_page", side_effect=self._fake_fetch_notes_page), \
             patch.object(granola_source, "fetch_note_detail", return_value={"id": "not_fixture_roadmap_recent"}):
            result = find_latest_meeting("HR Systems Roadmap", api_key="fixture-key")
        self.assertEqual(result["status"], "found")
        self.assertEqual(result["summary"], "")
        self.assertFalse(result["hasSummary"])

    def test_found_with_summary_content_reports_has_summary_true(self):
        result = self._run_full_fixture_lookup()
        self.assertEqual(result["status"], "found")
        self.assertTrue(result["hasSummary"])

    def _run_full_fixture_lookup(self):
        with patch.object(granola_source, "fetch_notes_page", side_effect=self._fake_fetch_notes_page), \
             patch.object(granola_source, "fetch_note_detail", side_effect=self._fake_fetch_note_detail):
            return find_latest_meeting("HR Systems Roadmap", api_key="fixture-key", lookback_days=120)

    def test_malformed_list_member_does_not_falsely_signal_past_cutoff(self):
        # Codex review finding, 19 Aug 2026, pass 4: the previous
        # count-based comparison (len(in_range) < len(notes)) treated a
        # malformed entry's exclusion the same as a genuine past-cutoff
        # exclusion, which could truncate pagination early and miss a real
        # match sitting on a later page. A malformed entry mixed into an
        # otherwise-complete, still-in-range page must NOT stop pagination.
        page1 = {
            "notes": [
                {"id": "recent_unrelated", "title": "Sickness Absence Survey", "created_at": "2026-08-18T10:00:00Z"},
                None,  # malformed member, must be skipped, not treated as a cutoff signal
                {"id": "no_date", "title": "Some other meeting"},  # missing created_at entirely
            ],
            "hasMore": True,
            "cursor": "fixture-page-2-with-real-match",
        }
        page2 = {
            "notes": [
                {"id": "real_match", "title": "HR Systems Roadmap — 14/08", "created_at": "2026-08-14T06:40:29Z"},
            ],
            "hasMore": False,
            "cursor": None,
        }

        def fake_fetch(api_key, *, created_after=None, cursor=None):
            return page2 if cursor == "fixture-page-2-with-real-match" else page1

        def fake_detail(api_key, note_id):
            self.assertEqual(note_id, "real_match")
            return {"summary_text": "ok"}

        with patch.object(granola_source, "fetch_notes_page", side_effect=fake_fetch), \
             patch.object(granola_source, "fetch_note_detail", side_effect=fake_detail):
            result = find_latest_meeting("HR Systems Roadmap", api_key="fixture-key")
        self.assertEqual(result["status"], "found")
        self.assertEqual(result["noteId"], "real_match")

    def test_impossible_calendar_timestamp_is_rejected(self):
        # Codex review finding, 19 Aug 2026, pass 4: a digit-shape-only
        # regex accepted impossible timestamps like "2099-99-99T99:99:99Z".
        # datetime.fromisoformat() does genuine calendar validation.
        notes = [
            {"id": "impossible_date", "title": "HR Systems Roadmap — bad", "created_at": "2099-99-99T99:99:99Z"},
            {"id": "valid", "title": "HR Systems Roadmap — 03/07", "created_at": "2026-07-03T06:40:29Z"},
        ]
        result = select_latest_matching_note(notes, "HR Systems Roadmap")
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "valid")


if __name__ == "__main__":
    unittest.main()
