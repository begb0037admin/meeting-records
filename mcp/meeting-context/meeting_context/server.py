from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from typing import Any

from mcp.server.fastmcp import FastMCP

from .core import (
    GitHubReader, OWNER, REFRESH_CONFIRMATION, SOURCES, compact_briefing,
    filter_tasks, read_roadmap, require_refresh_confirmation, utc_now,
)


mcp = FastMCP(
    "meeting-context",
    instructions=(
        "Read-only context for meeting preparation. This server never refreshes Outlook, "
        "writes files, edits tasks, commits, pushes, sends, schedules, or publishes."
    ),
)
reader = GitHubReader()


@mcp.tool()
def get_source_health(
    inbox_ref: str = "main",
    tasks_ref: str = "main",
    roadmap_ref: str = "main",
    meeting_ref: str = "main",
) -> dict[str, Any]:
    """Check approved GitHub snapshots and report Granola as external coverage."""
    checks = {}
    for name, ref in (
        ("inbox", inbox_ref), ("tasks", tasks_ref), ("roadmap", roadmap_ref), ("meeting", meeting_ref)
    ):
        repo, path = SOURCES[name]
        try:
            blob = reader.blob(repo, path, ref)
            checks[name] = {
                "status": "available", "repository": f"{OWNER}/{repo}", "path": path,
                "ref": ref, "blobSha": blob.sha,
            }
        except Exception as exc:
            checks[name] = {"status": "unavailable", "repository": f"{OWNER}/{repo}", "path": path, "ref": ref, "error": str(exc)}
    checks["granola"] = {
        "status": os.getenv("MEETING_CONTEXT_GRANOLA_STATUS", "external-not-checked"),
        "notes": "Granola remains Claude's existing connector; this read-only MCP does not impersonate or refresh it.",
    }
    checks["claude"] = {
        "status": "external-reasoning-seat",
        "notes": "Claude is invoked by the Voice launcher and consumes this MCP; it is not replaced by it.",
    }
    return {"checkedAt": utc_now(), "mode": "read-only", "sources": checks}


@mcp.tool()
def get_inbox_briefing(ref: str = "main") -> dict[str, Any]:
    """Read the already-published Work Inbox briefing from GitHub. Never opens or refreshes Outlook.

    Returns the triage sections (urgent, needs, low, fyi), plus today's and
    tomorrow's calendar (calToday, calTomorrow), the full multi-day calendar
    breakdown (calFull), and any reported absences — all passed through with
    the same time/title/sub/summary shape they have in briefing.json.
    """
    repo, path = SOURCES["inbox"]
    payload, blob = reader.json_file(repo, path, ref)
    return compact_briefing(payload, blob)


@mcp.tool()
def get_command_centre_tasks(
    query: str = "",
    tiers: list[str] | None = None,
    include_done: bool = False,
    limit: int = 50,
    ref: str = "main",
) -> dict[str, Any]:
    """Read and filter the GitHub-published Command Centre tasks snapshot."""
    repo, path = SOURCES["tasks"]
    payload, blob = reader.json_file(repo, path, ref)
    tasks = payload if isinstance(payload, list) else payload.get("tasks", [])
    return {
        "source": f"github:{OWNER}/{repo}/{path}@{ref}", "blobSha": blob.sha,
        "count": len(filtered := filter_tasks(tasks, query=query, tiers=tiers, include_done=include_done, limit=limit)),
        "tasks": filtered, "readOnly": True,
    }


@mcp.tool()
def get_roadmap_items(
    query: str = "",
    statuses: list[str] | None = None,
    lead: str = "",
    limit: int = 50,
    ref: str = "main",
) -> dict[str, Any]:
    """Read and filter the Work Tracker sheet from the GitHub-published HR roadmap workbook."""
    repo, path = SOURCES["roadmap"]
    blob = reader.blob(repo, path, ref)
    items = read_roadmap(blob.content, query=query, statuses=statuses, lead=lead, limit=limit)
    return {
        "source": f"github:{OWNER}/{repo}/{path}@{ref}", "blobSha": blob.sha,
        "count": len(items), "items": items, "readOnly": True,
    }


@mcp.tool()
def get_previous_meeting_prep(ref: str = "main") -> dict[str, Any]:
    """Read the archived HR Systems Managers Meeting prep document from meeting-records."""
    repo, path = SOURCES["meeting"]
    blob = reader.blob(repo, path, ref)
    return {
        "source": f"github:{OWNER}/{repo}/{path}@{ref}", "blobSha": blob.sha,
        "markdown": blob.content.decode("utf-8-sig"), "readOnly": True,
    }


@mcp.tool()
def refresh_outlook_work_inbox(confirmation: str) -> dict[str, Any]:
    """Explicitly run the established Outlook-to-Work-Inbox process.

    CONSEQUENTIAL ACTION: this reads Outlook through Windows COM, publishes the
    Work Inbox briefing to GitHub, and may apply the established Command Centre
    task updates. It is never called by normal meeting preparation. There is no
    schedule, polling, or background invocation. To run it, the caller must pass
    the exact confirmation phrase documented by the server.
    """
    require_refresh_confirmation(
        confirmation,
        enabled=os.getenv("MEETING_CONTEXT_ALLOW_OUTLOOK_REFRESH") == "1",
    )
    gh = shutil.which("gh")
    powershell = shutil.which("powershell.exe") or shutil.which("powershell")
    if not gh or not powershell:
        raise RuntimeError("The explicit refresh requires gh and Windows PowerShell on PATH.")
    with tempfile.TemporaryDirectory(prefix="meeting-context-refresh-") as temp:
        checkout = os.path.join(temp, "work-inbox")
        cloned = subprocess.run(
            [gh, "repo", "clone", f"{OWNER}/work-inbox", checkout, "--", "--depth", "1"],
            check=False, capture_output=True, text=True, encoding="utf-8",
        )
        if cloned.returncode:
            raise RuntimeError(cloned.stderr.strip() or "Unable to clone the canonical Work Inbox.")
        launcher = os.path.join(checkout, "Run_Inbox_Briefing.ps1")
        completed = subprocess.run(
            [powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", launcher],
            check=False, capture_output=True, text=True, encoding="utf-8",
            timeout=900,
        )
        if completed.returncode:
            raise RuntimeError(
                "Established Outlook refresh failed. "
                + (completed.stderr.strip() or completed.stdout.strip()[-2000:])
            )
        return {
            "status": "completed",
            "mode": "explicit-manual",
            "publishedByEstablishedProcess": True,
            "automaticRefreshConfigured": False,
            "output": completed.stdout.strip()[-4000:],
        }


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
