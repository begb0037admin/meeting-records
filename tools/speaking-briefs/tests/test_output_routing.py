import ast
import builtins
import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from output_routing import resolve_output_dir, resolve_output_subdir


BRIEF_CHROME_PATH = Path(__file__).resolve().parents[1] / "brief_chrome.py"


class FixedDate:
    def strftime(self, _format):
        return "21-09-2026"


class OutputRoutingWriteTests(unittest.TestCase):
    def _load_write_brief_output(self, scratch, meetings):
        source = BRIEF_CHROME_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(BRIEF_CHROME_PATH))
        function_node = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "write_brief_output"
        )
        namespace = {
            "datetime": FixedDate,
            "os": os,
            "SCRATCH": str(scratch),
            "MEETINGS_DIR": str(meetings),
            "__file__": str(BRIEF_CHROME_PATH),
        }
        exec(
            compile(
                ast.Module(body=[function_node], type_ignores=[]),
                str(BRIEF_CHROME_PATH),
                "exec",
            ),
            namespace,
        )
        return namespace["write_brief_output"]

    def _remove_sibling_from_sys_path(self):
        sibling_dir = str(BRIEF_CHROME_PATH.parent)
        while sibling_dir in sys.path:
            sys.path.remove(sibling_dir)
        sys.modules.pop("output_routing", None)

    def test_write_brief_output_routes_and_same_day_rerun_overwrites(self):
        with tempfile.TemporaryDirectory(dir=BRIEF_CHROME_PATH.parents[2]) as temp_dir:
            root = Path(temp_dir)
            scratch = root / "scratch"
            meetings = root / "meetings"
            write_brief_output = self._load_write_brief_output(scratch, meetings)
            self._remove_sibling_from_sys_path()

            first_path = write_brief_output(
                "first version", "HR Systems Roadmap", date=FixedDate()
            )
            expected_path = (
                meetings
                / "HR Systems Roadmap"
                / "HR Systems Roadmap - 21-09-2026.html"
            )
            self.assertEqual(Path(first_path), expected_path)
            self.assertEqual(expected_path.read_text(encoding="utf-8"), "first version")

            second_path = write_brief_output(
                "updated version", "HR Systems Roadmap", date=FixedDate()
            )
            self.assertEqual(Path(second_path), expected_path)
            self.assertEqual(expected_path.read_text(encoding="utf-8"), "updated version")
            self.assertEqual(
                list((meetings / "HR Systems Roadmap").glob("*.html")),
                [expected_path],
            )

    def test_write_brief_output_import_error_falls_back_with_warning(self):
        with tempfile.TemporaryDirectory(dir=BRIEF_CHROME_PATH.parents[2]) as temp_dir:
            root = Path(temp_dir)
            scratch = root / "scratch"
            meetings = root / "meetings"
            write_brief_output = self._load_write_brief_output(scratch, meetings)
            self._remove_sibling_from_sys_path()

            real_import = builtins.__import__

            def missing_routing_module(name, *args, **kwargs):
                if name == "output_routing":
                    raise ImportError("simulated missing output_routing")
                return real_import(name, *args, **kwargs)

            captured = io.StringIO()
            with contextlib.redirect_stdout(captured), mock.patch(
                "builtins.__import__", missing_routing_module
            ):
                final_path = write_brief_output(
                    "fallback version", "A newly invented meeting", date=FixedDate()
                )

            expected_path = (
                meetings
                / "Reference and Other"
                / "A newly invented meeting - 21-09-2026.html"
            )
            self.assertEqual(Path(final_path), expected_path)
            self.assertTrue(expected_path.is_file())
            self.assertEqual(expected_path.read_text(encoding="utf-8"), "fallback version")
            warning = captured.getvalue()
            self.assertIn("WARNING", warning)
            self.assertIn("output_routing", warning)
            self.assertIn("Reference and Other", warning)


class OutputRoutingTests(unittest.TestCase):
    def test_routing_cases(self):
        cases = {
            "SK 1-1": "1-1s",
            "HR Systems Managers Meeting": "HR Systems Managers Meeting",
            "HR Systems Roadmap": "HR Systems Roadmap",
            "Health and Safety Roadmap": "Health and Safety Roadmap",
            "FA Team Catch-up": "FA Team Catch-ups",
            "Holiday Records Reports - Access Group Scoping": "Working Groups and Scoping Calls",
            "Organisational Structure Walkthrough": "Working Groups and Scoping Calls",
            "Monthly Standing Agenda - September 2026": "Monthly Standing Agenda",
            "Kevin - Michael 1-1": "1-1s",
            "Simon 1-1 - September": "1-1s",
            "Sickness Absence Review": "Working Groups and Scoping Calls",
            "Holiday Records Review": "Working Groups and Scoping Calls",
            "Oxford Holiday Records": "Working Groups and Scoping Calls",
            "Organisational Structure Review": "Working Groups and Scoping Calls",
            "Codex dashboard review": "Tooling Reviews",
            "Command Centre review": "Tooling Reviews",
            "Needs Response review": "Tooling Reviews",
            "Work Inbox review": "Tooling Reviews",
            "Weekly Granola Review - September": "Reference and Other",
        }
        for brief_name, expected in cases.items():
            with self.subTest(brief_name=brief_name):
                subdir, matched = resolve_output_subdir(brief_name)
                self.assertEqual(subdir, expected)
                self.assertTrue(matched)

    def test_pdr_person_folders_preserve_names(self):
        for person in (
            "Kevin Lelitte",
            "Michael O'Sullivan",
            "James Salas Guillen",
            "Asta Palmer",
            "New Person",
        ):
            with self.subTest(person=person):
                subdir, matched = resolve_output_subdir(f"PDR 2026 - {person}")
                self.assertEqual(subdir, os.path.join("PDR 2026", person))
                self.assertTrue(matched)

    def test_unmatched_uses_fallback_and_warns(self):
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            subdir, matched = resolve_output_subdir("A newly invented meeting")
            self.assertEqual(subdir, "Reference and Other")
            self.assertFalse(matched)

            output_dir = resolve_output_dir("C:\\meetings", "A newly invented meeting")

        warning = captured.getvalue()
        self.assertIn("WARNING", warning)
        self.assertIn("A newly invented meeting", warning)
        self.assertIn("Reference and Other", warning)
        self.assertTrue(output_dir.endswith(os.path.join("Reference and Other")))

    def test_traversal_attempts_are_sanitised(self):
        attempts = {
            r"PDR 2026 - ..\evil": os.path.join("PDR 2026", "--evil"),
            "PDR 2026 - ../evil": os.path.join("PDR 2026", "--evil"),
            "PDR 2026 - C:/temp/<Person>": os.path.join("PDR 2026", "C--temp--Person-"),
            "PDR 2026 - Name.. ": os.path.join("PDR 2026", "Name-"),
        }
        for brief_name, expected in attempts.items():
            with self.subTest(brief_name=brief_name):
                subdir, matched = resolve_output_subdir(brief_name)
                self.assertEqual(subdir, expected)
                self.assertTrue(matched)
                self.assertNotIn("..", subdir)

    def test_resolve_output_dir_is_absolute_and_not_root(self):
        meetings_dir = os.path.abspath(tempfile.gettempdir())
        output_dir = resolve_output_dir(meetings_dir, "HR Systems Roadmap")
        self.assertTrue(os.path.isabs(output_dir))
        self.assertNotEqual(os.path.normcase(output_dir), os.path.normcase(meetings_dir))
        self.assertEqual(
            os.path.normcase(output_dir),
            os.path.normcase(os.path.join(meetings_dir, "HR Systems Roadmap")),
        )


if __name__ == "__main__":
    unittest.main()
