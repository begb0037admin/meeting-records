import unittest

from meeting_context.managers import (
    active_roadmap_items, latest_roadmap_path, previous_managers_path,
)


class ManagersMeetingTests(unittest.TestCase):
    def test_previous_managers_excludes_target(self):
        paths = [
            "Meeting Reviews/HR Systems Managers Meeting — 10-06.md",
            "Meeting Reviews/HR Systems Managers Meeting — 24-06.md",
        ]
        path, record_date = previous_managers_path(paths, "2026-06-24")
        self.assertTrue(path.endswith("10-06.md"))
        self.assertEqual(record_date, "2026-06-10")

    def test_latest_roadmap_respects_meeting_date(self):
        paths = [
            "Meeting Reviews/HR Systems Roadmap — 22-06.md",
            "Meeting Reviews/HR Systems Roadmap — 26-06.md",
            "Meeting Reviews/HR Systems Roadmap — 03-07.md",
        ]
        path, record_date = latest_roadmap_path(paths, "2026-06-24")
        self.assertTrue(path.endswith("22-06.md"))
        self.assertEqual(record_date, "2026-06-22")

    def test_only_active_roadmap_items_are_returned(self):
        items = [
            {"id": 1, "status": "In Progress"},
            {"id": 2, "status": "Complete"},
            {"id": 3, "status": "On Hold"},
            {"id": 4, "status": "Removed"},
        ]
        self.assertEqual(
            [item["id"] for item in active_roadmap_items(items)],
            [1, 3],
        )


if __name__ == "__main__":
    unittest.main()
