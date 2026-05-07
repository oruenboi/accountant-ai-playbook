---
name: anthropic-docx-adapter
description: Use when a workflow needs to align Word document handling with the official Anthropic docx skill without redistributing Anthropic proprietary materials. Covers Windows/Codex environment assumptions for reading, editing, creating, commenting, redlining, and validating .docx files.
---

# Anthropic DOCX Adapter

## Purpose
Provide local environment guidance for Word document workflows while pointing users to the official Anthropic docx skill as an external reference.

This repository does not include or modify Anthropic's docx skill files. Review the upstream license before installing or copying any external skill materials.

## Official Reference
- Source: https://github.com/anthropics/skills/tree/main/skills/docx
- License: see the upstream `LICENSE.txt` in that folder.

## Environment Notes
- Prefer the Codex bundled Node.js runtime for document generation libraries when available.
- Use XML-level editing only when normal document libraries cannot preserve the needed structure.
- Use tracked changes and comments for review workflows when the user needs an audit trail.
- For client-facing accounting and corporate secretarial documents, preserve templates, numbering, headers, footers, and defined terms.

## Workflow
1. Identify whether the task is extraction, generation, template fill, redline, comment, image replacement, or repair.
2. Inspect styles, numbering, sections, headers, footers, tables, bookmarks, comments, and tracked changes before editing.
3. Preserve existing document conventions unless the user asks for a new template or house style.
4. Validate the final file by opening or rendering it and checking layout, page breaks, numbering, tables, references, and comments.
5. For formal documents, review names, dates, company numbers, signing blocks, and statutory references against source documents.

## Review Checklist
- Headings, numbering, tables, headers, footers, and page breaks are intact.
- Comments and tracked changes show the intended author and scope.
- No placeholder fields remain.
- Generated documents open cleanly in Word-compatible software.
- No client-identifiable templates are committed unless approved for community sharing.
