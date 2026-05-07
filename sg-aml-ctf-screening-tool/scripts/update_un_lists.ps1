# Downloads the UN consolidated sanctions list and splits it into regime-specific XML files.
param(
    [string]$BaseDir = "$(Split-Path $PSScriptRoot)",  # skill root
    [string]$ConsolidatedUrl = "https://scsanctions.un.org/resources/xml/en/consolidated.xml"
)

$assets = Join-Path $BaseDir "assets"
if (-not (Test-Path $assets)) { New-Item -ItemType Directory -Path $assets | Out-Null }
$consolidated = Join-Path $assets "consolidated.xml"

Write-Host ("Run started: " + (Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"))
Write-Host "Downloading consolidated list from $ConsolidatedUrl ..."
Invoke-WebRequest -Uri $ConsolidatedUrl -MaximumRedirection 5 -UserAgent "Mozilla/5.0" -OutFile $consolidated
Write-Host "Saved consolidated list to $consolidated"

# Python splitter (uses only stdlib)
$env:UN_LIST_BASE = $assets
$py = @"
import xml.etree.ElementTree as ET, os, collections, copy
base = os.environ["UN_LIST_BASE"]
src = os.path.join(base, "consolidated.xml")
root = ET.parse(src).getroot()
items = collections.defaultdict(lambda: {'IND': [], 'ENT': []})
for elem in root.findall('.//INDIVIDUAL'):
    t = elem.findtext('UN_LIST_TYPE')
    if t:
        items[t.strip()]['IND'].append(copy.deepcopy(elem))
for elem in root.findall('.//ENTITY'):
    t = elem.findtext('UN_LIST_TYPE')
    if t:
        items[t.strip()]['ENT'].append(copy.deepcopy(elem))
for t, data in items.items():
    new_root = ET.Element('CONSOLIDATED_LIST', root.attrib)
    inds = ET.SubElement(new_root, 'INDIVIDUALS')
    ents = ET.SubElement(new_root, 'ENTITIES')
    for e in data['IND']:
        inds.append(e)
    for e in data['ENT']:
        ents.append(e)
    out = os.path.join(base, f"{t.lower()}.xml")
    ET.ElementTree(new_root).write(out, encoding="UTF-8", xml_declaration=True)
print("Split regimes:", ", ".join(sorted(items.keys())))
"@

$tmpPy = [System.IO.Path]::GetTempFileName() + ".py"
Set-Content -Path $tmpPy -Value $py -Encoding UTF8
python $tmpPy
Remove-Item $tmpPy -Force

Write-Host "Done. Regime XML files are in $assets (e.g., dprk.xml, drc.xml, libya.xml, somalia.xml, southsudan.xml, sudan.xml, yemen.xml, al-qaida.xml, taliban.xml, iran.xml, iraq.xml, car.xml, gb.xml, haiti.xml)."
Write-Host ("Run finished: " + (Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"))
