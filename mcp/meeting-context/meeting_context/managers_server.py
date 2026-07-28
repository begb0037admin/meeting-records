from __future__ import annotations

import os
from typing import Any

from mcp.server.fastmcp import FastMCP

from .core import (
    GitHubReader, OWNER, SOURCES, compact_briefing, filter_tasks, read_roadmap,
    utc_now,
)
from .managers import (
    active_roadmap_items, file_paths, latest_commit, latest_roadmap_path,
    previous_managers_path,
)


mcp = FastMCP(
    "managers-meeting-context",
    instructions=(
        "Draft-only read context for Managers Meeting preparation. "
        "This server has no Outlook refresh or write tool."
    ),
)
reader = GitHubReader()


@mcp.tool()
def get_source_health(
    inbox_ref: str = "main",
    tasks_ref: str = "main",
    roadmap_ref: str = "main",
) -> dict[str, Any]:
    checks: dict[str, Any] = {}
    for name, ref in (
        ("inbox", inbox_ref), ("tasks", tasks_ref), ("roadmap", roadmap_ref)
    ):
        repo, path = SOURCES[name]
        try:
            blob = reader.blob(repo, path, ref)
            checks[name] = {
                "status": "available",
                "repository": f"{OWNER}/{repo}",
                "path": path,
                "ref": ref,
                "blobSha": blob.sha,
                **latest_commit(reader, repo, path, ref),
            }
        except Exception as exc:
            checks[name] = {
                "status": "unavailable",
                "repository": f"{OWNER}/{repo}",
                "path": path,
                "ref": ref,
                "error": str(exc),
            }
    checks["granola"] = {
        "status": os.getenv(
            "MEETING_CONTEXT_GRANOLA_STATUS", "external-must-be-checked"
        ),
        "notes": (
            "Claude must call the approved Granola connector for the actual "
            "latest Roadmap outcome. This MCP does not impersonate it."
        ),
    }
    return {
        "checkedAt": utc_now(),
        "mode": "read-only-draft",
        "outlookRefreshToolExposed": False,
        "sources": checks,
    }


@mcp.tool()
def get_inbox_briefing(ref: str = "main") -> dict[str, Any]:
    repo, path = SOURCES["inbox"]
    payload, blob = reader.json_file(repo, path, ref)
    result = compact_briefing(payload, blob)
    result.update(latest_commit(reader, repo, path, ref))
    return result


@mcp.tool()
def get_command_centre_tasks(
    query: str = "",
    tiers: list[str] | None = None,
    include_done: bool = False,
    limit: int = 200,
    ref: str = "main",
) -> dict[str, Any]:
    repo, path = SOURCES["tasks"]
    payload, blob = reader.json_file(repo, path, ref)
    tasks = payload if isinstance(payload, list) else payload.get("tasks", [])
    filtered = filter_tasks(
        tasks, query=query, tiers=tiers, include_done=include_done, limit=limit
    )
    return {
        "source": f"github:{OWNER}/{repo}/{path}@{ref}",
        "blobSha": blob.sha,
        **latest_commit(reader, repo, path, ref),
        "count": len(filtered),
        "tasks": filtered,
        "readOnly": True,
        "knownLimitation": (
            "Command Centre browser done-state may also exist in localStorage."
        ),
    }


@mcp.tool()
def get_active_roadmap_items(
    query: str = "",
    lead: str = "",
    limit: int = 200,
    ref: str = "main",
) -> dict[str, Any]:
    repo, path = SOURCES["roadmap"]
    blob = reader.blob(repo, path, ref)
    items = active_roadmap_items(
        read_roadmap(blob.content, query=query, lead=lead, limit=limit)
    )
    return {
        "source": f"github:{OWNER}/{repo}/{path}@{ref}",
        "blobSha": blob.sha,
        **latest_commit(reader, repo, path, ref),
        "count": len(items),
        "items": items,
        "readOnly": True,
        "selectionRequirement": "Assess every returned item.",
    }


@mcp.tool()
def get_previous_managers_prep(
    meeting_date: str,
    ref: str = "main",
) -> dict[str, Any]:
    repo = "meeting-records"
    path, record_date = previous_managers_path(
        file_paths(reader, repo, ref), meeting_date
    )
    blob = reader.blob(repo, path, ref)
    return {
        "source": f"github:{OWNER}/{repo}/{path}@{ref}",
        "blobSha": blob.sha,
        **latest_commit(reader, repo, path, ref),
        "recordDate": record_date,
        "markdown": blob.content.decode("utf-8-sig"),
        "readOnly": True,
    }


@mcp.tool()
def get_latest_roadmap_prep(
    meeting_date: str,
    ref: str = "main",
) -> dict[str, Any]:
    repo = "meeting-records"
    path, record_date = latest_roadmap_path(
        file_paths(reader, repo, ref), meeting_date
    )
    blob = reader.blob(repo, path, ref)
    return {
        "source": f"github:{OWNER}/{repo}/{path}@{ref}",
        "blobSha": blob.sha,
        **latest_commit(reader, repo, path, ref),
        "recordDate": record_date,
        "markdown": blob.content.decode("utf-8-sig"),
        "readOnly": True,
    }


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
