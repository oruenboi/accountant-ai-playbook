---
name: document-to-md
description: Convert documents (pdf, docx/doc, rtf/odt, html/htm, epub, pptx, xlsx/csv/tsv, images via OCR, txt/md) into Markdown for agent use; trigger when asked to normalize files to .md while preserving structure, tables, and embedded media where possible.
---
# Document-to-MD

## Overview
Guides conversion of supplied documents into Markdown optimized for downstream processing. Prefers Pandoc for structure and media extraction, with Python fallbacks (pdfplumber, python-docx, pandas, pytesseract) so conversions stay workable even when Pandoc or GUI apps are missing.

## Quick Start
- Install tools if missing: `pip install pandoc pypandoc pdfplumber python-docx beautifulsoup4 pillow pytesseract pdf2image pandas`; Windows binaries: `choco install tesseract poppler` (ensure on PATH).
- Convert with media extraction: `python scripts/convert_to_md.py input.docx --media-dir media_out`.
- Batch convert to a folder: `python scripts/convert_to_md.py docs/* --out-dir converted`.
- Metadata is added automatically (source path, timestamp, converter flags). Skip with `--no-meta` if needed.
- Table of Contents auto-inserts for long docs (default ≥120 lines with ≥3 headings); force with `--toc` or disable with `--no-toc` / adjust with `--toc-threshold 80`.
- Legal-friendly cleanup: `--legal-normalize` converts `(a)` bullets to dash bullets, unwraps broken lines, highlights currency amounts, reformats `"Term" means ...` into definition bullets, and cleans spacing. Useful for statutes/contracts with heavy nesting.
- Extra metadata: `--meta-date-in-force 2025-06-09`, `--meta-made-on 2025-05-05`, `--meta-citation F014.001.0048.V1`, `--meta-source-url https://...` to embed legal citations/URLs.
- Scanned PDFs or photos: add `--ocr` to enable OCR fallback.
- If Pandoc output looks sparse, rerun with `--ocr` (PDF) or check `references/conversion_matrix.md` for the best path per format.

## Format Playbook
- **DOCX/DOC/ODT/RTF**: Use Pandoc with `--extract-media <dir>` to keep images; fallback uses python-docx (text only; tables flattened).
- **PDF**: Try Pandoc first; if result is short/empty, rerun with `--ocr` (needs pdf2image + pytesseract). Without OCR, fallback pdfplumber text only—figures not preserved.
- **HTML/HTM/EPUB**: Pandoc preferred; fallback strips scripts/styles and keeps readable text.
- **PPTX**: Pandoc can pull slide text/notes; for better fidelity export to PDF then reconvert.
- **XLSX/CSV/TSV**: Pandoc renders tables; fallback uses pandas to emit Markdown tables (index dropped).
- **Images (PNG/JPG/TIF/GIF/BMP)**: OCR via pytesseract; add page headers manually if multiple images represent pages.
- **TXT/MD**: Read and normalize to UTF-8; wrap is left untouched.

## Using scripts/convert_to_md.py
- Accepts multiple input paths; writes `<stem>.md` beside the source unless `--out-dir` is set.
- `--media-dir` extracts embedded media for formats Pandoc supports (docx/odt/rtf/html/pptx/pdf when available).
- Metadata header fields: `source`, `original_extension`, `converted_at`, `converter`, `used_pandoc`, `ocr_used`, `heading_count`, `line_count`, optional `media_dir`. Disable with `--no-meta`.
- TOC control: auto when long; `--toc` forces, `--no-toc` disables, `--toc-threshold N` tunes length trigger.
- Legal normalization flag: `--legal-normalize` (bullet cleanup, unwrap, currency bold, definition bullets).
- Optional metadata injections: `--meta-date-in-force`, `--meta-made-on`, `--meta-citation`, `--meta-source-url`.
- Returns non-zero exit code if any file fails; logs steps to stderr for transparency.

## Bundled resources
- `scripts/install_deps_win.ps1` — one-shot dependency install (pandoc, tesseract, poppler, Python libs).
- `scripts/smoke_convert.ps1` — runs conversions on fixtures with media + TOC + OCR + legal normalize to `smoke_output/`.
- `scripts/gen_fixtures.py` — regenerates tiny fixture set in `assets/fixtures/`.
- `scripts/legal_postcheck.py` — checks a converted `.md` for wrapped bullets, heading count, and unbolded currency.
- Fixtures in `assets/fixtures/`: `sample.docx`, `sample.pdf`, `sample.html`, `sample.csv`, `sample.txt`.
- References: `references/legal_normalization_examples.md`, `references/dependencies_win.md`, `references/toc_edgecases.md`, `references/conversion_matrix.md`.

## Validation and Packaging
- Run a quick syntax check: `python -m compileall scripts`.
- Package for distribution with the skill-creator tooling, e.g., `python <skill-creator-path>/scripts/package_skill.py skills/document-to-md`.
- Keep this SKILL.md concise (<500 lines) and prune unused resources; current references live in `references/conversion_matrix.md`.
