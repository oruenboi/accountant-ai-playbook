$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $here
$fixtures = Join-Path $root "assets\\fixtures"
$outDir = Join-Path $root "smoke_output"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$python = "python"
$converter = Join-Path $here "convert_to_md.py"

$inputs = @("sample.docx","sample.pdf","sample.html","sample.csv","sample.txt") | ForEach-Object { Join-Path $fixtures $_ }

Write-Host "Running smoke conversion to $outDir..."
& $python $converter @inputs --out-dir $outDir --media-dir (Join-Path $outDir "media") --ocr --legal-normalize --meta-citation "SMOKE-TEST" --toc

if ($LASTEXITCODE -eq 0) {
  Write-Host "Smoke conversion completed." -ForegroundColor Green
} else {
  Write-Host "Smoke conversion failed with exit code $LASTEXITCODE" -ForegroundColor Red
}
