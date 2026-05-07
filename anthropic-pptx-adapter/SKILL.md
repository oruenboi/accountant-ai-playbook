---
name: anthropic-pptx-adapter
description: Use when a workflow needs to align presentation handling with the official Anthropic pptx skill without redistributing Anthropic proprietary materials. Covers Windows/Codex environment assumptions for reading, editing, creating, and visually checking .pptx decks.
---

# Anthropic PPTX Adapter

## Purpose
Provide local environment guidance for presentation workflows while pointing users to the official Anthropic pptx skill as an external reference.

This repository does not include or modify Anthropic's pptx skill files. Review the upstream license before installing or copying any external skill materials.

## Official Reference
- Source: https://github.com/anthropics/skills/tree/main/skills/pptx
- License: see the upstream `LICENSE.txt` in that folder.

## Environment Notes
- Prefer the Codex bundled Node.js runtime for JavaScript-based deck generation helpers.
- Use Python extraction tools for reading slide text and notes when a text summary is enough.
- Use LibreOffice or PowerPoint-compatible rendering for final visual QA when layout matters.
- For accounting and advisory decks, prioritize dense, scannable analysis over marketing-style filler.

## Workflow
1. Determine whether the task is read-only extraction, template editing, or new deck creation.
2. If editing an existing deck, inspect slide masters, layouts, theme fonts, colors, speaker notes, and embedded charts before changing content.
3. Preserve the client's branding and template conventions unless explicitly asked to refresh the design.
4. Render the final deck to images or PDF and check every slide visually.
5. Confirm charts, numbers, source notes, page numbers, and section labels match the underlying support.

## Review Checklist
- No placeholder text remains.
- Text does not overflow or overlap with shapes, charts, or footers.
- Slide titles, section labels, source notes, and chart labels are readable.
- Financial figures reconcile to the source schedule or management account pack.
- The file opens cleanly in PowerPoint-compatible software.
