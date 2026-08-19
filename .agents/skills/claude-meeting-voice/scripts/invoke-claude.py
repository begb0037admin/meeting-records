"""Invoke Claude Code with lossless Windows argument and UTF-8 handling."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

def for_claude_schema(value: object) -> object:
    """Translate canonical union types to Claude CLI's strict AJV dialect."""
    if isinstance(value, list):
        return [for_claude_schema(item) for item in value]
    if not isinstance(value, dict):
        return value

    normalized = {
        key: for_claude_schema(item)
        for key, item in value.items()
        if key != "$schema"
    }
    declared_type = normalized.get("type")
    if not isinstance(declared_type, list):
        return normalized

    remainder = {
        key: item for key, item in normalized.items() if key != "type"
    }
    alternatives: list[dict[str, object]] = []
    for type_name in declared_type:
        alternative: dict[str, object] = {"type": type_name}
        if type_name != "null":
            alternative.update(remainder)
        alternatives.append(alternative)
    return {"anyOf": alternatives}


def main() -> int:
    # Windows' default stdout/stderr encoding is the legacy system code page
    # (e.g. cp1252) when not attached to a real UTF-8 console, even though
    # this module's own docstring promises "lossless ... UTF-8 handling".
    # subprocess.run() below correctly decodes the child `claude` process's
    # output as UTF-8, but re-encoding it back out via a cp1252 sys.stdout
    # then raises UnicodeEncodeError on any character outside that legacy
    # code page (confirmed live 19 Aug 2026: a genuine "→" arrow
    # character in a real drafted result crashed this exact write). Python
    # 3.7+ supports reconfiguring the already-open stream's encoding
    # in place, restoring the UTF-8 guarantee the docstring already claims.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument("--claude", required=True)
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--mcp-config", required=True, type=Path)
    parser.add_argument("--name", required=True)
    parser.add_argument("--prompt-file", required=True, type=Path)
    parser.add_argument("--allowed-tools", required=True)
    args = parser.parse_args()

    schema = for_claude_schema(
        json.loads(args.schema.read_text(encoding="utf-8-sig"))
    )
    schema_argument = json.dumps(schema, separators=(",", ":"), ensure_ascii=False)
    prompt = args.prompt_file.read_text(encoding="utf-8-sig")

    command = [
        args.claude,
        "--print",
        "--output-format",
        "json",
        "--json-schema",
        schema_argument,
        "--permission-mode",
        "dontAsk",
        "--tools",
        "Read",
        "--allowedTools",
        args.allowed_tools,
        "--disallowedTools",
        "Bash,Write,Edit,NotebookEdit,WebFetch,WebSearch",
        "--setting-sources",
        "user,project,local",
        "--mcp-config",
        str(args.mcp_config),
        "--effort",
        "medium",
        "--name",
        args.name,
        prompt,
    ]
    completed = subprocess.run(
        command,
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.stdout:
        sys.stdout.write(completed.stdout)
    if completed.stderr:
        sys.stderr.write(completed.stderr)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
