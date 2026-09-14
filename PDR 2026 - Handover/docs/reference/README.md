# Reference — PDR Conversation Guide

`PDR Conversation Guide - PDR Refresh - 22.05.2024 v1.docx` is Oxford's official PDR (Performance Development Review) conversation guide, copied here 14 Sep 2026 from Kevin's Downloads folder (`C:\Users\admin\Downloads\`) at his request, as the canonical source for the six-stage structure every PDR flow doc in this repo is built around:

1. Check in on workload and wellbeing
2. Performance / progress
3. Values
4. Personal development & career aspirations
5. Working together
6. Agree actions and close

The guide states explicitly that either party — manager or colleague — uses the same six stages; that's why Kevin's own PDR flow doc (`PDR 2026/Kevin Lelitte/`) is framed as reviewee prep using the identical structure, not a different one.

## Extraction gotcha — read before trying to pull text out of this file again

`python-docx`'s normal `Document(path).paragraphs` API returns **nothing** for this file — the guide's real content only surfaces through the raw `word/document.xml` inside the `.docx` zip, reading the `w:t` text runs directly. This was hit and worked around when the guide was first used to build the three flow docs (James, Asta, Kevin) on 14 Sep 2026. If a future session needs to re-extract this file's text, don't assume `python-docx` paragraphs will work — unzip and read the XML directly, or use a tool that handles Oxford's template markup correctly.

This is distinct from the separate, unrelated SharePoint/Codex-connector access gap affecting the *2025 review-form docx* files for Kevin and Asta (see `PDR 2026 - Handover/docs/HANDOVER.md`) — this guide file itself has no access problem, it was a local Downloads file all along.
