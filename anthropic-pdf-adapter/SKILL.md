---
name: anthropic-pdf-adapter
description: Use when a workflow needs to align PDF handling with the official Anthropic pdf skill without redistributing Anthropic proprietary materials. Covers Windows/Codex environment assumptions for reading, extracting, splitting, merging, OCR, form filling, and producing PDF files.
---

# Anthropic PDF Adapter

## Purpose
Provide local environment guidance for PDF workflows while pointing users to the official Anthropic pdf skill as an external reference.

This repository does not include or modify Anthropic's pdf skill files. Review the upstream license before installing or copying any external skill materials.

## Official Reference
- Source: https://github.com/anthropics/skills/tree/main/skills/pdf
- License: see the upstream `LICENSE.txt` in that folder.

## Environment Notes
- Prefer the Codex bundled Python runtime for PDF parsing and generation scripts.
- Use structured extraction tools for text and tables before falling back to OCR.
- Use OCR only when pages are scanned or text extraction is incomplete.
- Treat signed documents, identity documents, bank statements, and statutory filings as confidential by default.

## Workflow
1. Classify the PDF as text-based, scanned, form-based, signed, or mixed.
2. Choose the lightest tool that preserves the required fidelity: text extraction, table extraction, page manipulation, OCR, or rendering.
3. For page operations, verify page counts and page ordering before and after processing.
4. For forms, inspect field names and appearance behavior before filling.
5. For final deliverables, open or render the PDF and verify layout, page size, text, tables, signatures, and attachments.

## Review Checklist
- Page count and page order match the request.
- Extracted tables reconcile to visible totals where applicable.
- OCR output is reviewed for names, dates, amounts, and registration numbers.
- Redactions are true redactions, not just visual overlays.
- No confidential source PDFs are committed to reusable examples.
