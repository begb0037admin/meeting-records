from __future__ import annotations

import re
from datetime import date
from typing import Any
from urllib.parse import quote

from .core import GitHubReader, OWNER, SourceError


ACTIVE_EXCLUSIONS = {"complete", "removed", "not delivered"}


def latest_commit(reader: GitHubReader, repo: str, path: str, ref: str) -> dict[str, str]:
    payload = reader._api(
        f"repos/{OWNER}/{repo}/commits?path={quote(path, safe='/')}"
        f"&sha={quote(ref, safe='')}&per_page=1"
    )
    if not payload:
        raise SourceError(f"No commit history for {repo}/{path}@{ref}")
    return {
        "commitSha": payload[0]["sha"],
        "recordDate": payload[0]["commit"]["committer"]["date"],
    }


def file_paths(reader: GitHubReader, repo: str, ref: str) -> list[str]:
    payload = reader._api(
        f"repos/{OWNER}/{repo}/git/trees/{quote(ref, safe='')}?recursive=1"
    )
    if payload.get("truncated"):
        raise SourceError(f"Truncated GitHub tree for {repo}@{ref}")
    return [
        item["path"] for item in payload.get("tree", [])
        if item.get("type") == "blob"
    ]


def dated_path(
    paths: list[str],
    *,
    prefix: str,
    cutoff: str,
    exclude_cutoff: bool = False,
) -> tuple[str, str]:
    target = date.fromisoformat(cutoff)
    pattern = re.compile(
        rf"^Meeting Reviews/{re.escape(prefix)} — (\d{{2}})-(\d{{2}})\.md$"
    )
    candidates: list[tuple[date, str]] = []
    for path in paths:
        match = pattern.match(path)
        if not match:
            continue
        candidate = date(target.year, int(match.group(2)), int(match.group(1)))
        if candidate > target or (exclude_cutoff and candidate == target):
            continue
        candidates.append((candidate, path))
    if not candidates:
        raise SourceError(f"No {prefix} record exists before cutoff {cutoff}")
    record_date, path = max(candidates)
    return path, record_date.isoformat()


def previous_managers_path(paths: list[str], meeting_date: str) -> tuple[str, str]:
    return dated_path(
        paths,
        prefix="HR Systems Managers Meeting",
        cutoff=meeting_date,
        exclude_cutoff=True,
    )


def latest_roadmap_path(paths: list[str], meeting_date: str) -> tuple[str, str]:
    return dated_path(
        paths,
        prefix="HR Systems Roadmap",
        cutoff=meeting_date,
    )


def active_roadmap_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        item for item in items
        if str(item.get("status") or "").casefold() not in ACTIVE_EXCLUSIONS
    ]
