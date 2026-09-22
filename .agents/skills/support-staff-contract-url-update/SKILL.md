---
name: support-staff-contract-url-update
description: Update the Support Staff contract template from its tracked-changes reference when the user asks to update the template file. Uses the local Meetings intake folder and preserves the original Word template and its macros.
metadata:
  short-description: Update and verify the Support Staff contract template
---

# Support Staff Contract URL Update

Use this skill when Kevin asks to update the Support Staff contract template.

## Intake location

Use only this local folder; it is deliberately outside the public `meeting-records` Git repository:

`C:\Users\admin\OneDrive - Nexus365\Meetings\Meetings\Support Staff Contract URL Updates\`

- `Input\` must contain exactly the current contract template to update and its tracked-changes/reference document.
- `Output\` receives the new dated copy and its verification report.

Do not use files in Downloads as an input once the intake folder exists. Do not commit templates, outputs, or personal/contract content to Git.

## Required workflow

1. Identify the tracked-changes/reference document and the contract template in `Input\`. Stop and report the missing or ambiguous input if there is not exactly one of each.
2. Extract only the approved old-URL to new-URL replacements from the reference document. Do not make editorial, formatting, or policy changes.
3. Copy the contract template to `Output\` using a dated filename. Never overwrite, save, rename, or alter the input template.
4. Apply every approved URL replacement to both the hyperlink target and its visible field result. Preserve all other document content, fields, formatting, and macro storage.
5. Verify the output before reporting success:
   - Word opens the copy and its Word-document structure is valid.
   - Every approved new URL is present as both a hyperlink target and visible text.
   - None of the approved old URLs remain in those fields.
   - The macro/VBA streams in the output are byte-identical to the input template when the input contains macros.
   - State clearly if an end-to-end macro run cannot be tested because of a missing local dependency. Never run the macro on the input or deliverable.
6. Write a short dated verification report in `Output\` beside the updated copy, including the input names, replacement count, macro-preservation result, and any testing limitation.

## Completion standard

Report the output path and concise verification result. If anything does not pass, leave the input untouched, do not present the output as ready, and state the exact blocker.
