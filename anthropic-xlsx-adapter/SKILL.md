---
name: anthropic-xlsx-adapter
description: Use when a workflow needs to align spreadsheet handling with the official Anthropic xlsx skill without redistributing Anthropic proprietary materials. Covers Windows/Codex environment assumptions for reading, editing, validating, and producing .xlsx, .xlsm, .csv, and .tsv files.
---

# Anthropic XLSX Adapter

## Purpose
Provide local environment guidance for spreadsheet workflows while pointing users to the official Anthropic xlsx skill as an external reference.

This repository does not include or modify Anthropic's xlsx skill files. Review the upstream license before installing or copying any external skill materials.

## Official Reference
- Source: https://github.com/anthropics/skills/tree/main/skills/xlsx
- License: see the upstream `LICENSE.txt` in that folder.

## Environment Notes
- Prefer the Codex bundled Python runtime when available.
- Use `pandas` for tabular analysis, cleanup, joins, pivots, and CSV/TSV conversion.
- Use `openpyxl` when preserving workbook structure, formulas, styles, sheets, and cell-level formatting matters.
- Use LibreOffice only when formulas or rendering need recalculation outside Excel.
- Keep client data out of committed fixtures unless it has been anonymized and approved for sharing.

## Workflow
1. Inspect workbook structure, sheets, named ranges, formulas, and formatting before editing.
2. Preserve existing templates and formatting conventions unless the user asks for a redesign.
3. Use formulas inside the workbook for values that should remain dynamic.
4. Validate output by reopening the workbook and checking formulas, totals, dates, sheet names, hidden rows/columns, and expected formatting.
5. For accounting work, document data sources, assumptions, and any manual adjustments in a visible notes sheet or adjacent comments.

## Review Checklist
- No formula errors such as `#REF!`, `#DIV/0!`, `#VALUE!`, or `#NAME?`.
- Date, currency, percentage, and zero formats are consistent.
- Protected sheets, hidden tabs, and formulas are preserved unless intentionally changed.
- Workpapers include clear source references and reviewer notes.
- No client-identifiable data is added to reusable examples.
