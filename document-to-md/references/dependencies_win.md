# Windows Dependency Notes

- **Tesseract OCR**: `choco install tesseract` (adds binaries to PATH). If not on PATH, set `pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"`.
- **Poppler (for pdf2image)**: `choco install poppler`. Ensure `poppler/bin` is on PATH or pass `poppler_path` to `convert_from_path`.
- **Python deps (minimal)**:
  ```powershell
  python -m pip install pandoc pypandoc pdfplumber python-docx beautifulsoup4 pillow pytesseract pdf2image pandas fpdf2
  ```
- **Pandoc binary**: download from https://github.com/jgm/pandoc/releases and add to PATH, or install via `choco install pandoc`.

After installing, run the smoke script: `powershell -File scripts/smoke_convert.ps1`.
