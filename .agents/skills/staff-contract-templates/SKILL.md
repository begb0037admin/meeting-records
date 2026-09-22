---
name: staff-contract-templates
description: Apply controlled, approved updates to Staff Contract Templates from their supporting reference files. Use when the user asks to update a template file, including URL, text, wording, or other local template changes.
metadata:
  short-description: Update and verify Staff Contract Templates
---

# Staff Contract Templates

Use this skill when Kevin asks to update a Staff Contract Template.

## Intake location

Use only this local folder; it is deliberately outside the public `meeting-records` Git repository:

`C:\Users\admin\OneDrive - Nexus365\Meetings\Meetings\Staff Contract Templates\`

- `Input\` holds the current template to update and its authoritative supporting reference file or files.
- `Output\` receives the new dated copy and an HTML verification report.

Do not use files in Downloads as an input once the intake folder exists. Do not commit templates, outputs, or contract content to Git.

## Required workflow

1. Identify one target template and the authoritative supporting reference file or files in `Input\`. Stop and report any missing or ambiguous input.
2. Extract only the approved changes from the supporting material. This can include links, text, wording, or other local template amendments. Do not make unapproved editorial, formatting, policy, or structural changes.
3. Copy the template to `Output\` using a dated filename. Never overwrite, save, rename, or alter the input template.
4. Apply the approved changes while preserving all other content, fields, formatting, mail-merge behaviour, and macro storage.
5. Verify the output before reporting success:
   - Word opens the copy and its Word-document structure is valid.
   - Every requested change is present in the correct visible and functional location.
   - Superseded text, links, or wording are absent where the approved change requires their replacement.
   - The macro/VBA streams in the output are byte-identical to the input template when the input contains macros.
   - State clearly if an end-to-end macro run cannot be tested because of a missing local dependency. Never run the macro on the input or deliverable.
6. Write a short dated HTML verification report in `Output\` beside the updated copy, including the input names, approved-change count, preservation results, and any testing limitation.

## Completion standard

Report the output path and concise verification result. If anything does not pass, leave the input untouched, do not present the output as ready, and state the exact blocker.
