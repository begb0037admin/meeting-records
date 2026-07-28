from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def load(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fail(errors: list[str], warnings: list[str]) -> int:
    print(json.dumps({
        "status": "failed",
        "valid": False,
        "errors": errors,
        "warnings": warnings,
    }, ensure_ascii=False))
    return 1


def validate(result: dict[str, Any], profile: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    required_keys = (
        "status", "workflowId", "meetingType", "meetingDate", "draftState",
        "sourceManifest", "roadmapAssessment", "spokenSummary", "draftMarkdown",
        "blockers", "warnings", "nextStep",
    )
    for key in required_keys:
        if key not in result:
            errors.append(f"Missing result key: {key}")

    if errors:
        return errors, warnings

    if result["workflowId"] != profile["workflowId"]:
        errors.append("Result workflowId does not match the selected profile")
    if result["meetingType"] != profile["canonicalMeetingType"]:
        errors.append("Result meetingType does not match the selected profile")
    if result["draftState"] != "draft":
        errors.append("Result draftState must remain draft")
    if result["status"] not in {"completed", "blocked"}:
        errors.append("Result status must be completed or blocked")

    sources = {
        item.get("sourceId"): item
        for item in result.get("sourceManifest", [])
        if isinstance(item, dict) and item.get("sourceId")
    }
    for source_id in profile["requiredSources"]:
        source = sources.get(source_id)
        if source is None:
            errors.append(f"Required source is absent from manifest: {source_id}")
        elif result["status"] == "completed" and source.get("status") in {
            "unavailable", "empty", "not-required"
        }:
            alternatives = profile.get("sourceAlternatives", {}).get(
                source_id, []
            )
            accepted = [
                alternative for alternative in alternatives
                if sources.get(alternative, {}).get("status") not in {
                    None, "unavailable", "empty", "not-required"
                }
            ]
            if not accepted:
                errors.append(
                    f"Completed result cannot omit required source: {source_id}"
                )
            else:
                warnings.append(
                    f"{source_id} was replaced by approved source: "
                    f"{accepted[0]}"
                )

    if result["status"] == "blocked":
        if not result.get("blockers"):
            errors.append("Blocked result must identify at least one blocker")
        return errors, warnings

    draft = result.get("draftMarkdown", "")
    requirements = profile["outputRequirements"]
    word_count = len(re.findall(r"\b[\w'’-]+\b", draft))
    if word_count < requirements["minimumDraftWords"]:
        errors.append(
            f"Draft is too thin: {word_count} words; "
            f"minimum is {requirements['minimumDraftWords']}"
        )

    for heading in requirements["requiredHeadings"]:
        if not re.search(rf"(?im)^#+\s+.*{re.escape(heading)}", draft):
            errors.append(f"Missing required heading: {heading}")

    agenda_items = re.findall(r"(?im)^###\s+(?:\d+[.)]\s+)?(.+)$", draft)
    if len(agenda_items) < requirements["minimumAgendaItems"]:
        errors.append(
            f"Only {len(agenda_items)} agenda-style sections found; "
            f"minimum is {requirements['minimumAgendaItems']}"
        )

    say_this_count = len(re.findall(r"(?i)\*\*Say this:\*\*", draft))
    minimum_scripts = requirements["minimumAgendaItems"] + 2
    if say_this_count < minimum_scripts:
        errors.append(
            f"Only {say_this_count} exact speaker-note blocks found; "
            f"minimum is {minimum_scripts}"
        )

    for field in requirements["agendaItemFields"]:
        if field.casefold() not in draft.casefold():
            errors.append(f"Draft does not demonstrate required agenda field: {field}")

    active = [
        item for item in result.get("roadmapAssessment", [])
        if isinstance(item, dict) and item.get("active") is True
    ]
    if not active:
        errors.append("No active Roadmap items were assessed")
    for item in active:
        if not str(item.get("reason", "")).strip():
            errors.append(f"Roadmap item {item.get('itemId')} has no selection reason")
        if item.get("included") and not item.get("destination"):
            errors.append(f"Included Roadmap item {item.get('itemId')} has no destination")

    if not result.get("spokenSummary", "").strip():
        errors.append("spokenSummary is empty")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", required=True)
    parser.add_argument("--profile", required=True)
    args = parser.parse_args()

    try:
        result = load(args.result)
        profile = load(args.profile)
    except Exception as exc:
        return fail([f"Unable to load validation input: {exc}"], [])

    errors, warnings = validate(result, profile)
    if errors:
        return fail(errors, warnings)

    print(json.dumps({
        "status": "passed",
        "valid": True,
        "errors": [],
        "warnings": warnings,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
