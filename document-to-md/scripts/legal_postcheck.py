#!/usr/bin/env python3
"""
Simple post-conversion checker for legal docs.
Reports:
- Headings count
- Bullets still wrapped across lines
- Currency tokens not bolded
"""
from pathlib import Path
import re
import sys


def find_wrapped_bullets(text: str):
    bullet_re = re.compile(r"^\s*(?:-|\*|\+|\d+\.|\([a-z]\))\s", re.MULTILINE)
    issues = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if bullet_re.match(line):
            # If next line is non-bullet and not blank, likely a wrap
            if i + 1 < len(lines) and lines[i + 1].strip() and not bullet_re.match(lines[i + 1]):
                issues.append((i + 1, line.strip(), lines[i + 1].strip()))
    return issues


def find_unbold_currency(text: str):
    currency_re = re.compile(r"\$[0-9][\d,]*(?:\.\d+)?")
    results = []
    for m in currency_re.finditer(text):
        snippet = text[max(0, m.start() - 15) : m.end() + 15]
        if not text[max(0, m.start() - 2) : m.end() + 2].startswith("**"):
            results.append(snippet.replace("\n", " "))
    return results


def main(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    headings = len(re.findall(r"^#{1,6}\s", text, flags=re.MULTILINE))
    wrapped = find_wrapped_bullets(text)
    unbold = find_unbold_currency(text)

    print(f"File: {path}")
    print(f"Headings: {headings}")
    if wrapped:
        print("\nWrapped bullets needing attention:")
        for line_no, l1, l2 in wrapped[:20]:
            print(f"  line {line_no}: {l1} // {l2}")
    else:
        print("\nNo wrapped bullets detected.")

    if unbold:
        print("\nCurrency not bolded (first 10 snippets):")
        for snip in unbold[:10]:
            print(f"  ...{snip}...")
    else:
        print("\nAll currency tokens appear bolded.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: legal_postcheck.py <converted.md>")
    sys.exit(main(Path(sys.argv[1]).expanduser().resolve()))
