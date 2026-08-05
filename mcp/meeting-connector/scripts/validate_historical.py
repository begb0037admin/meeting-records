"""Exercise the actual stdio protocol against the archived 24 June 2026 sources."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


REFS = {
    "inbox_ref": "1dded7a99ed3",
    "tasks_ref": "019dd2497c69",
    "roadmap_ref": "f16a11ac3377",
    "meeting_ref": "main",
}


def structured(result):
    if result.structuredContent is not None:
        return result.structuredContent
    return json.loads(result.content[0].text)


async def validate() -> None:
    root = Path(__file__).resolve().parents[1]
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(root)
    parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "meeting_context.server"],
        env=environment,
    )
    async with stdio_client(parameters) as streams:
        async with ClientSession(*streams) as session:
            print("validate: initialize", file=sys.stderr, flush=True)
            await session.initialize()
            print("validate: list tools", file=sys.stderr, flush=True)
            listed = await session.list_tools()
            tool_names = sorted(tool.name for tool in listed.tools)
            expected = sorted([
                "get_source_health", "get_inbox_briefing", "get_command_centre_tasks",
                "get_roadmap_items", "get_previous_meeting_prep", "refresh_outlook_work_inbox",
            ])
            if tool_names != expected:
                raise RuntimeError(f"Unexpected tool surface: {tool_names}")

            print("validate: source health", file=sys.stderr, flush=True)
            health = structured(await session.call_tool("get_source_health", REFS))
            print("validate: briefing", file=sys.stderr, flush=True)
            briefing = structured(await session.call_tool("get_inbox_briefing", {"ref": REFS["inbox_ref"]}))
            print("validate: tasks", file=sys.stderr, flush=True)
            tasks = structured(await session.call_tool(
                "get_command_centre_tasks",
                {"ref": REFS["tasks_ref"], "query": "SHSMS", "include_done": True},
            ))
            print("validate: roadmap", file=sys.stderr, flush=True)
            roadmap = structured(await session.call_tool(
                "get_roadmap_items",
                {"ref": REFS["roadmap_ref"], "query": "HR Reporting", "limit": 10},
            ))
            print("validate: meeting", file=sys.stderr, flush=True)
            meeting = structured(await session.call_tool("get_previous_meeting_prep", {"ref": "main"}))

            summary = {
                "status": "passed",
                "proofOfConcept": "archived-material-only",
                "meeting": "HR Systems Managers Meeting — 24 June 2026",
                "tools": tool_names,
                "sourceStatuses": {
                    name: value["status"] for name, value in health["sources"].items()
                },
                "briefingSnapshotDate": briefing["snapshotDate"],
                "matchingTaskCount": tasks["count"],
                "matchingRoadmapCount": roadmap["count"],
                "previousPrepCharacters": len(meeting["markdown"]),
                "outlookRefreshed": briefing["outlookRefreshed"],
                "published": False,
            }
            print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(validate())
