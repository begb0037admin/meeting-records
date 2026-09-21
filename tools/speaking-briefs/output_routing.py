"""Route finished speaking briefs into their per-series output folders."""

import os
import re


ROUTES = [
    (re.compile(r"^SK 1-1$", re.IGNORECASE), "1-1s"),
    (re.compile(r"^HR Systems Managers Meeting$", re.IGNORECASE), "HR Systems Managers Meeting"),
    (re.compile(r"^HR Systems Roadmap$", re.IGNORECASE), "HR Systems Roadmap"),
    (re.compile(r"^(Health and Safety|H&S) Roadmap$", re.IGNORECASE), "Health and Safety Roadmap"),
    (re.compile(r"^FA Team Catch-up$", re.IGNORECASE), "FA Team Catch-ups"),
    (
        re.compile(r"^Holiday Records Reports - Access Group Scoping$", re.IGNORECASE),
        "Working Groups and Scoping Calls",
    ),
    (
        re.compile(r"^Organisational Structure Walkthrough$", re.IGNORECASE),
        "Working Groups and Scoping Calls",
    ),
    (
        re.compile(r"^PDR 2026 - (?P<person>.+)$", re.IGNORECASE),
        os.path.join("PDR 2026", "{person}"),
    ),
    (re.compile(r"^Monthly Standing Agenda", re.IGNORECASE), "Monthly Standing Agenda"),
    (
        re.compile(r"^(Kevin - Michael 1-1|Simon 1-1|SK 1-1)", re.IGNORECASE),
        "1-1s",
    ),
    (
        re.compile(r"^(Sickness Absence|Holiday Records|Oxford Holiday Records|Organisational Structure)", re.IGNORECASE),
        "Working Groups and Scoping Calls",
    ),
    (
        re.compile(r"^(Codex dashboard|Command Centre|Needs Response|Work Inbox)", re.IGNORECASE),
        "Tooling Reviews",
    ),
    (re.compile(r"^Weekly Granola Review", re.IGNORECASE), "Reference and Other"),
]

_INVALID_COMPONENT_CHARS = re.compile(r'[\\/:*?"<>|]')


def _sanitise_component(component):
    """Return a safe single directory component."""
    component = _INVALID_COMPONENT_CHARS.sub("-", component)
    while ".." in component:
        component = component.replace("..", "-")
    component = component.rstrip(". ")
    return component or "-"


def _safe_subdir(folder_template, match):
    if "{person}" in folder_template:
        person = _sanitise_component(match.group("person"))
        folder_template = folder_template.format(person=person)

    components = [component for component in re.split(r"[\\/]", folder_template) if component]
    return os.path.join(*(_sanitise_component(component) for component in components))


def resolve_output_subdir(brief_name):
    """Return ``(relative_subfolder, matched)`` for a brief name."""
    for pattern, folder_template in ROUTES:
        match = pattern.match(brief_name)
        if match:
            return _safe_subdir(folder_template, match), True
    return os.path.join("Reference and Other"), False


def resolve_output_dir(meetings_dir, brief_name):
    """Return the absolute output directory for ``brief_name``."""
    subdir, matched = resolve_output_subdir(brief_name)
    output_dir = os.path.abspath(os.path.join(meetings_dir, subdir))
    if not matched:
        print(
            f"WARNING: brief name {brief_name!r} has no routing rule; "
            f"placed in {output_dir!r}."
        )
    return output_dir
