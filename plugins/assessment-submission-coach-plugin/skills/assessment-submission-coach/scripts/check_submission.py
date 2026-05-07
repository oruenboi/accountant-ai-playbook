#!/usr/bin/env python3
"""Lightweight completeness check for Agentic AI Foundations submissions."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_PATTERNS = {
    "Section 1 / LO1": [
        r"workflow",
        r"pain point",
        r"frequency",
        r"average time|time per run",
        r"success metric|target improvement|roi",
    ],
    "Section 2 / LO2": [
        r"\.codex-plugin/plugin\.json",
        r"skill\.md",
        r"duo|discover|understand|output",
        r"normal",
        r"messy",
        r"edge case",
    ],
    "Section 3 / LO3": [
        r"mini-app|app",
        r"input screen",
        r"output screen",
        r"validation",
        r"error state|handled error",
    ],
    "Section 4 / LO4": [
        r"trigger",
        r"condition|branch",
        r"workflow diagram|diagram",
        r"run log|successful run",
        r"failure alert|alert",
    ],
    "Section 5 / LO5": [
        r"agent task",
        r"non-goal|non-goals",
        r"tool permission|tool limit",
        r"action limit",
        r"approval|human-in-the-loop",
    ],
    "Section 6 / LO6": [
        r"dummy|anonymized|anonymised",
        r"pdpa|personal data|confidential",
        r"api key|credential|token|secret",
        r"least[- ]privilege",
        r"attestation",
    ],
}

SECRET_HINTS = [
    r"sk-[A-Za-z0-9_-]{20,}",
    r"api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_-]{12,}",
    r"password\s*[:=]",
    r"token\s*[:=]\s*['\"]?[A-Za-z0-9_-]{12,}",
]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_submission.py <draft-file.md|txt>")
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}")
        return 2

    text = path.read_text(encoding="utf-8", errors="replace")
    lowered = text.lower()
    missing: list[str] = []

    for section, patterns in REQUIRED_PATTERNS.items():
        for pattern in patterns:
            if not re.search(pattern, lowered, re.IGNORECASE):
                missing.append(f"{section}: missing evidence keyword `{pattern}`")

    safety_flags = []
    for pattern in SECRET_HINTS:
        if re.search(pattern, text, re.IGNORECASE):
            safety_flags.append(f"Possible exposed secret matching `{pattern}`")

    if not missing and not safety_flags:
        print("Status: READY FOR HUMAN REVIEW")
        print("No obvious completeness gaps or secret patterns found.")
        return 0

    print("Status: NEEDS WORK")
    if missing:
        print("\nMissing or weak evidence:")
        for item in missing:
            print(f"- {item}")

    if safety_flags:
        print("\nSafety flags:")
        for item in safety_flags:
            print(f"- {item}")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
