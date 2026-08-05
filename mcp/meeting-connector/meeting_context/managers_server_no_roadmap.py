"""Managers MCP for sources other than the launcher-exported Roadmap master."""

from __future__ import annotations

import os
from typing import Any

from mcp.server.fastmcp import FastMCP

from . import managers_server as source


mcp = FastMCP(
    "managers-meeting-context",
    instructions=(
        "Draft-only read context. The launcher supplies the formal active "
        "Roadmap JSON separately. No Outlook refresh or write tool exists."
    ),
)

INBOX_REF = os.getenv("MEETING_CONTEXT_INBOX_REF", "main")
TASKS_REF = os.getenv("MEETING_CONTEXT_TASKS_REF", "main")
ROADMAP_REF = os.getenv("MEETING_CONTEXT_ROADMAP_REF", "main")
MEETING_RECORDS_REF = os.getenv(
    "MEETING_CONTEXT_MEETING_RECORDS_REF", "main"
)


@mcp.tool()
def get_source_health(
    inbox_ref: str = INBOX_REF,
    tasks_ref: str = TASKS_REF,
    roadmap_ref: str = ROADMAP_REF,
) -> dict[str, Any]:
    return source.get_source_health(inbox_ref, tasks_ref, roadmap_ref)

@mcp.tool()
def get_inbox_briefing(ref: str = INBOX_REF) -> dict[str, Any]:
    return source.get_inbox_briefing(ref)

@mcp.tool()
def get_command_centre_tasks(
    query: str = "",
    tiers: list[str] | None = None,
    include_done: bool = False,
    limit: int = 100,
    ref: str = TASKS_REF,
) -> dict[str, Any]:
    return source.get_command_centre_tasks(
        query, tiers, include_done, min(limit, 100), ref
    )

@mcp.tool()
def get_previous_managers_prep(
    meeting_date: str,
    ref: str = MEETING_RECORDS_REF,
) -> dict[str, Any]:
    return source.get_previous_managers_prep(meeting_date, ref)

@mcp.tool()
def get_latest_roadmap_prep(
    meeting_date: str,
    ref: str = MEETING_RECORDS_REF,
) -> dict[str, Any]:
    return source.get_latest_roadmap_prep(meeting_date, ref)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
