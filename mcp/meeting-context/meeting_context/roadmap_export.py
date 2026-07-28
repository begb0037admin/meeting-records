"""Export all formal active Roadmap fields as one read-only JSON bundle."""

from __future__ import annotations

import argparse
import json

from .core import GitHubReader, OWNER, SOURCES, read_roadmap
from .managers import active_roadmap_items, latest_commit


def export(ref: str) -> dict:
    reader = GitHubReader()
    repo, path = SOURCES["roadmap"]
    blob = reader.blob(repo, path, ref)
    active = active_roadmap_items(read_roadmap(blob.content, limit=200))
    formal = [
        {
            "id": item.get("id"),
            "activity": item.get("activity"),
            "lead": item.get("lead"),
            "team": item.get("team"),
            "deadline": item.get("deadline"),
            "lastReviewed": item.get("lastReviewed"),
            "status": item.get("status"),
            "statusDetails": item.get("statusDetails"),
        }
        for item in active
    ]
    return {
        "source": f"github:{OWNER}/{repo}/{path}@{ref}",
        "blobSha": blob.sha,
        **latest_commit(reader, repo, path, ref),
        "activeItemCount": len(formal),
        "items": formal,
        "readOnly": True,
        "selectionRequirement": "Assess every item and retain include/exclude reason.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref", default="main")
    args = parser.parse_args()
    print(json.dumps(export(args.ref), ensure_ascii=False))


if __name__ == "__main__":
    main()
