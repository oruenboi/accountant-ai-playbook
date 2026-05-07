# Requires: Administrator for choco installs
choco install -y pandoc tesseract poppler
python -m pip install --upgrade pip
python -m pip install pandoc pypandoc pdfplumber python-docx beautifulsoup4 pillow pytesseract pdf2image pandas fpdf2
Write-Host "Dependencies installed. If Tesseract isn't on PATH, set pytesseract.pytesseract.tesseract_cmd accordingly."
