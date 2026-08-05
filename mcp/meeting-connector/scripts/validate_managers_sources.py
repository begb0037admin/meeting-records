"""Validate the non-circular Managers source chain without the benchmark."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from meeting_context.core import GitHubReader, SourceError
from meeting_context.managers import file_paths, previous_managers_path
from meeting_context.roadmap_export import export as export_roadmap


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "managers-meeting-2026-06-24.json"


def structured(result):
    if result.structuredContent is not None:
        return result.structuredContent
    return json.loads(result.content[0].text)


async def validate() -> None:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    refs = fixture["refs"]
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(ROOT)
    environment["MEETING_CONTEXT_INBOX_REF"] = refs["workInboxRef"]
    environment["MEETING_CONTEXT_TASKS_REF"] = refs["commandCentreRef"]
    environment["MEETING_CONTEXT_ROADMAP_REF"] = refs["roadmapRef"]
    environment["MEETING_CONTEXT_MEETING_RECORDS_REF"] = refs[
        "meetingRecordsRef"
    ]
    parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "meeting_context.managers_server_no_roadmap"],
        env=environment,
    )
    async with stdio_client(parameters) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            listed = await session.list_tools()
            tool_names = sorted(tool.name for tool in listed.tools)
            expected = sorted([
                "get_source_health",
                "get_inbox_briefing",
                "get_command_centre_tasks",
                "get_previous_managers_prep",
                "get_latest_roadmap_prep",
            ])
            if tool_names != expected:
                raise RuntimeError(f"Unexpected tool surface: {tool_names}")
            if "refresh_outlook_work_inbox" in tool_names:
                raise RuntimeError("Outlook refresh must not be exposed")

            health = structured(await session.call_tool(
                "get_source_health", {}
            ))
            briefing = structured(await session.call_tool(
                "get_inbox_briefing", {}
            ))
            tasks = structured(await session.call_tool(
                "get_command_centre_tasks",
                {"include_done": True, "limit": 100},
            ))
            roadmap_prep = structured(await session.call_tool(
                "get_latest_roadmap_prep",
                {"meeting_date": fixture["meetingDate"]},
            ))

    roadmap = export_roadmap(refs["roadmapRef"])
    reader = GitHubReader()
    previous_status = "none-before-target"
    try:
        previous_managers_path(
            file_paths(reader, "meeting-records", refs["meetingRecordsRef"]),
            fixture["meetingDate"],
        )
        previous_status = "unexpectedly-present"
    except SourceError:
        pass
    if previous_status != "none-before-target":
        raise RuntimeError("Fixture unexpectedly exposes a previous Managers brief")
    if roadmap_prep["recordDate"] != "2026-06-22":
        raise RuntimeError("Latest Roadmap prep before target is not 22 June")
    if any(
        value["status"] != "available"
        for key, value in health["sources"].items()
        if key != "granola"
    ):
        raise RuntimeError("A pinned GitHub source is unavailable")

    print(json.dumps({
        "status": "passed",
        "fixtureId": fixture["fixtureId"],
        "tools": tool_names,
        "outlookRefreshToolExposed": False,
        "benchmarkWithheld": True,
        "briefingSnapshotDate": briefing["snapshotDate"],
        "taskCount": tasks["count"],
        "activeRoadmapItemCount": roadmap["activeItemCount"],
        "latestRoadmapPrepDate": roadmap_prep["recordDate"],
        "previousManagersBrief": previous_status,
        "granolaStillRequired": fixture["requiredGranolaMeeting"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(validate())
