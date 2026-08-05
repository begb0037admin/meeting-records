import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_PATH = (
    ROOT / ".agents" / "skills" / "chatGPT-meeting-prep-voice" /
    "scripts" / "validate-meeting-result.py"
)
PROFILE_PATH = (
    ROOT / ".agents" / "skills" / "chatGPT-meeting-prep-voice" /
    "profiles" / "managers-meeting.json"
)
SPEC = importlib.util.spec_from_file_location("meeting_result_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)
PROFILE = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))


def complete_draft() -> str:
    item = """
### {number}. Project {number}

**Purpose:** Important project purpose.
**Relevant history:** Supported history and earlier position.
**Owner and team:** Kevin and the FA team.
**Current position:** Current evidence-based position.
**Management relevance:** Management awareness is required.
**Deadline or milestone:** 31 August 2026.
**Risk or dependency:** Supplier dependency.
**Kevin's position:** Proceed with a controlled plan.
**Ask of the room:** Support the escalation.

**Say this:**
*"I want to bring this item to the group's attention and agree the next step."*

**Likely questions:**
- What changed?

**Supported answers:**
- The latest Roadmap outcome supports this position.

**Proposed next step:** Kevin will confirm the plan.
**Sources and freshness:** Roadmap and latest meeting outcome, dated and checked.
"""
    items = "\n".join(item.format(number=i) for i in range(1, 7))
    padding = " ".join(["Supported management context."] * 150)
    return f"""# HR Systems Managers Meeting — 24/06

## Source and freshness summary

All required sources checked.

## Opening

**Say this:**
*"I want to work through the key management items and agree support."*

## Agenda items

{items}

## Risks and dependencies

Supplier, capacity and deadline risks are set out above. {padding}

## Decisions and support required

Management support is required.

## Unresolved conflicts

None.

## Closing

**Say this:**
*"I will confirm the agreed actions and bring back any unresolved points."*
"""


def valid_result() -> dict:
    sources = [
        {
            "sourceId": source_id,
            "source": source_id,
            "status": "used",
            "recordDate": "2026-06-23",
            "retrievedAt": "2026-07-28T10:00:00Z",
            "notes": "Fixture source",
        }
        for source_id in PROFILE["requiredSources"]
    ]
    return {
        "status": "completed",
        "workflowId": "managers-meeting-draft",
        "meetingType": "HR Systems Managers Meeting",
        "meetingDate": "2026-06-24",
        "draftState": "draft",
        "sourceManifest": sources,
        "roadmapAssessment": [
            {
                "itemId": str(i),
                "itemName": f"Item {i}",
                "active": True,
                "included": i <= 6,
                "reason": "Management relevance" if i <= 6 else "Stable",
                "destination": "Agenda items" if i <= 6 else None,
            }
            for i in range(1, 9)
        ],
        "spokenSummary": "A complete draft is ready.",
        "draftMarkdown": complete_draft(),
        "blockers": [],
        "warnings": [],
        "nextStep": "Review the draft.",
    }


class MeetingResultValidationTests(unittest.TestCase):
    def test_complete_result_passes(self):
        errors, _ = validator.validate(valid_result(), PROFILE)
        self.assertEqual(errors, [])

    def test_thin_result_fails(self):
        result = valid_result()
        result["draftMarkdown"] = "# Managers Meeting\n\nOne line."
        errors, _ = validator.validate(result, PROFILE)
        self.assertTrue(any("too thin" in error for error in errors))
        self.assertTrue(any("Missing required heading" in error for error in errors))

    def test_required_roadmap_outcome_cannot_be_unavailable(self):
        result = valid_result()
        for source in result["sourceManifest"]:
            if source["sourceId"] == "latest-roadmap-outcome-granola":
                source["status"] = "unavailable"
        errors, _ = validator.validate(result, PROFILE)
        self.assertTrue(any("latest-roadmap-outcome-granola" in error for error in errors))

    def test_manual_recap_can_replace_missing_granola_outcome(self):
        result = valid_result()
        for source in result["sourceManifest"]:
            if source["sourceId"] == "latest-roadmap-outcome-granola":
                source["status"] = "unavailable"
        result["sourceManifest"].append({
            "sourceId": "manual-roadmap-recap",
            "source": "Kevin-provided manual recap",
            "status": "used",
            "recordDate": "2026-06-22",
            "retrievedAt": "2026-07-28T10:00:00Z",
            "notes": "Explicit fallback supplied by Kevin.",
        })
        errors, warnings = validator.validate(result, PROFILE)
        self.assertEqual(errors, [])
        self.assertTrue(any("manual-roadmap-recap" in item for item in warnings))

    def test_empty_manual_recap_cannot_replace_missing_granola(self):
        result = valid_result()
        for source in result["sourceManifest"]:
            if source["sourceId"] == "latest-roadmap-outcome-granola":
                source["status"] = "unavailable"
        result["sourceManifest"].append({
            "sourceId": "manual-roadmap-recap",
            "source": "Kevin-provided manual recap",
            "status": "empty",
            "recordDate": "2026-06-22",
            "retrievedAt": "2026-07-28T10:00:00Z",
            "notes": "No substantive recap supplied.",
        })
        errors, _ = validator.validate(result, PROFILE)
        self.assertTrue(any(
            "latest-roadmap-outcome-granola" in error for error in errors
        ))

    def test_blocked_result_requires_blocker(self):
        result = valid_result()
        result["status"] = "blocked"
        result["draftMarkdown"] = ""
        errors, _ = validator.validate(result, PROFILE)
        self.assertTrue(any("Blocked result" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
