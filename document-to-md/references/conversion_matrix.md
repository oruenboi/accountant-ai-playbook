# Conversion Matrix (Formats → Preferred Path)

- **docx / doc / odt / rtf** — `pandoc` with `--extract-media` → best structure; fallback `python-docx` for text only.
- **pdf** — `pandoc` first; fallback `pdfplumber` for text; enable `--ocr` to use `pdf2image+pytesseract` when pages are images.
- **html / htm** — `pandoc`; fallback BeautifulSoup text extraction.
- **pptx** — `pandoc` (notes + text only); if missing, export slides to PDF then rerun.
- **xlsx / csv / tsv** — `pandoc` to Markdown tables; fallback: open with Python `pandas` and emit `DataFrame.to_markdown()`.
- **images (png/jpg/tif/gif/bmp)** — OCR via `pytesseract`; for multipage TIFF, convert to PDF then re-run if needed.
- **epub** — `pandoc` handles chapters well; fallback: unzip and concatenate XHTML with BeautifulSoup.

## Quick dependency installs (pip)

```bash
pip install pandoc pypandoc pdfplumber python-docx beautifulsoup4 pillow pytesseract pdf2image pandas
```

Windows OCR extras: install Tesseract binary (e.g., https://github.com/UB-Mannheim/tesseract/wiki) and ensure it is on PATH. Poppler is required for `pdf2image` (`choco install poppler`).

## Usage heuristics

- Prefer `--media-dir <path>` whenever images/charts must be preserved (Pandoc writes extracted media to that folder).
- If Pandoc output is sparse, rerun with `--wrap=none` already set, then try `--pdf-engine=ocr` alternatives via `--ocr` flag for image-heavy PDFs.
- When accuracy matters, compare word counts between source and Markdown; rerun with OCR if counts are far apart.
