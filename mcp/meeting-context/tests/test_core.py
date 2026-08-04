import io
import json
import unittest

from meeting_context.core import (
    GitHubBlob, REFRESH_CONFIRMATION, SourceError, compact_briefing,
    filter_tasks, read_roadmap, require_refresh_confirmation,
)


class MeetingContextCoreTests(unittest.TestCase):
    def test_briefing_is_compact_and_never_claims_refresh(self):
        blob = GitHubBlob("work-inbox", "data/briefing.json", "abc123", "blob1", b"")
        value = compact_briefing(
            {"date": "Tuesday 23 June 2026", "urgent": [{"title": "Cover gap", "from": "Julie"}]},
            blob,
        )
        self.assertEqual(value["snapshotDate"], "Tuesday 23 June 2026")
        self.assertEqual(value["sections"]["urgent"][0]["title"], "Cover gap")
        self.assertFalse(value["outlookRefreshed"])
        self.assertTrue(value["readOnly"])

    def test_briefing_low_section_is_not_dropped(self):
        # Regression test: the sections whitelist used to read payload["waiting"],
        # but briefing.json's low-priority key is actually "low" — so low-priority
        # items were silently dropped. Confirm they now come through.
        blob = GitHubBlob("work-inbox", "data/briefing.json", "abc123", "blob1", b"")
        value = compact_briefing(
            {
                "date": "Tuesday 4 Aug 2026",
                "low": [{"title": "Password expiry notice", "from": "Password Manager", "sub": "..."}],
            },
            blob,
        )
        self.assertIn("low", value["sections"])
        self.assertEqual(len(value["sections"]["low"]), 1)
        self.assertEqual(value["sections"]["low"][0]["title"], "Password expiry notice")
        self.assertNotIn("waiting", value["sections"])

    def test_briefing_passes_through_calendar_and_absences(self):
        blob = GitHubBlob("work-inbox", "data/briefing.json", "abc123", "blob1", b"")
        payload = {
            "date": "Monday 3 Aug 2026",
            "calToday": [
                {"time": "09:30", "title": "FA Team Daily Catchup", "sub": "Kevin Lelitte", "summary": "Standard catchup."}
            ],
            "calTomorrow": [
                {"time": "All day", "title": "Simon out of the office - funeral", "sub": "Simon Burford"}
            ],
            "calFull": [
                {
                    "date": "2026-08-03",
                    "label": "Monday 3 Aug",
                    "isToday": False,
                    "items": [
                        {"time": "09:30", "title": "FA Team Daily Catchup", "sub": "Kevin Lelitte"},
                        {"time": "10:00", "title": "H&S Roadmap", "sub": "Christopher Sanders"},
                    ],
                }
            ],
            "absences": ["Crispin Muncaster - out of office - date unknown"],
        }
        value = compact_briefing(payload, blob)

        self.assertEqual(value["calToday"], [
            {"time": "09:30", "title": "FA Team Daily Catchup", "sub": "Kevin Lelitte", "summary": "Standard catchup."}
        ])
        self.assertEqual(value["calTomorrow"], [
            {"time": "All day", "title": "Simon out of the office - funeral", "sub": "Simon Burford", "summary": None}
        ])
        self.assertEqual(len(value["calFull"]), 1)
        self.assertEqual(value["calFull"][0]["date"], "2026-08-03")
        self.assertEqual(value["calFull"][0]["label"], "Monday 3 Aug")
        self.assertFalse(value["calFull"][0]["isToday"])
        self.assertEqual(len(value["calFull"][0]["items"]), 2)
        self.assertEqual(value["calFull"][0]["items"][1]["title"], "H&S Roadmap")
        self.assertEqual(value["absences"], ["Crispin Muncaster - out of office - date unknown"])

    def test_briefing_calendar_and_absences_default_to_empty(self):
        blob = GitHubBlob("work-inbox", "data/briefing.json", "abc123", "blob1", b"")
        value = compact_briefing({"date": "Tuesday 23 June 2026"}, blob)
        self.assertEqual(value["calToday"], [])
        self.assertEqual(value["calTomorrow"], [])
        self.assertEqual(value["calFull"], [])
        self.assertEqual(value["absences"], [])

    def test_tasks_filter_query_tier_and_done(self):
        tasks = [
            {"id": "1", "title": "SHSMS evaluation", "tier": "week", "done": False},
            {"id": "2", "title": "Closed SHSMS item", "tier": "week", "done": True},
            {"id": "3", "title": "Holiday reports", "tier": "today", "done": False},
        ]
        value = filter_tasks(tasks, query="SHSMS", tiers=["week"])
        self.assertEqual([item["id"] for item in value], ["1"])

    def test_roadmap_reads_work_tracker_without_saving(self):
        from openpyxl import Workbook

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Work Tracker"
        sheet.append([f"h{i}" for i in range(28)])
        row = [None] * 28
        row[0], row[1], row[6], row[19], row[26] = 179, "HR Reporting SSO", "Kevin", "2026-04-30", "In progress"
        sheet.append(row)
        stream = io.BytesIO()
        workbook.save(stream)
        workbook.close()
        items = read_roadmap(stream.getvalue(), query="SSO", lead="Kevin")
        self.assertEqual(items[0]["id"], 179)
        self.assertEqual(items[0]["status"], "In progress")

    def test_outlook_refresh_requires_exact_confirmation(self):
        with self.assertRaises(SourceError):
            require_refresh_confirmation(REFRESH_CONFIRMATION)
        with self.assertRaises(SourceError):
            require_refresh_confirmation("yes", enabled=True)
        require_refresh_confirmation(REFRESH_CONFIRMATION, enabled=True)


if __name__ == "__main__":
    unittest.main()
