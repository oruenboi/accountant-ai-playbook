---
name: sg-aml-ctf-screening-tool
description: Screen individuals or entities against pasted AML/CTF regulatory lists and adverse media using ComplianceScreen GPT; use when asked to confirm list completeness, identify exact/partial matches, score risk, and generate a compliance-ready report with an audit trail.
---
# SG AML/CTF Screening Tool

Purpose-built workflow for running sanctions/terrorism screening with user-pasted regulatory lists and adverse media. Optimized for Singapore requirements, but adaptable when additional lists are supplied.

## Quick Start
- Gather structured intake (see `references/checklists.md` ➜ Intake template).
- Confirm required lists are present; if any are missing, request paste and log omissions/confirmations.
- Assign a session ID (e.g., `SGAML-<YYYYMMDD>-<HHMM>-<random4>`), echo it in all replies.
- Run matching: exact first, then partial/alias matching with similarity labels (High ≥0.85, Medium 0.7–0.84, Low <0.7). Note any obvious false positives.
- Review adverse media pasted by user; classify mention type (Direct/Association/Neutral) and severity (High/Medium/Low) using keywords in `references/checklists.md`.
- Score overall risk (High/Medium/Low) with rationale tied to findings and list recency.
- Produce the report using `references/report-templates.md` and include completeness + sources.
- Remind the user to save/export the report for audit and to validate list freshness dates.

## Workflow Details
- **Intake & Variations**: Capture full name, aliases, DOB/ID, nationality, and context (customer/onboarding/vendor/etc.). Expand obvious transliterations or punctuation variants.
- **Completeness Check**: Present the required Singapore lists (see Required Lists in `references/checklists.md`). Ask: “Confirm all required lists are included; paste any missing ones now.” Record “confirmed” vs “missing <list>”.
- **Matching Logic**:
  - Normalize names (casefold, trim honorifics), compare exact; then fuzzy (Levenshtein/Jaro-Winkler conceptual) to label High/Medium/Low similarity.
  - For list rows with multiple fields, highlight which fields matched (name, DOB, nationality, address, passport).
  - Flag duplicate hits across lists; consolidate into a single hit with provenance.
- **Adverse Media**:
  - Request source, date, headline, summary, and full text if not provided.
  - Tag keywords (financial crime, sanctions breach, terrorism, proliferation, corruption, cybercrime). Use the adverse keyword list in `references/checklists.md`.
  - Classify context (Direct/Association/Neutral) and severity (High/Medium/Low).
- **Risk Assessment**:
  - High: confirmed sanctions hit; strong adverse media implying illicit activity; multiple Medium hits.
  - Medium: partial match with supporting attributes or soft adverse media; list gaps.
  - Low: no matches and clean media.
- **Reporting & Audit**:
  - Use the report template; include session ID, timestamps, inputs, findings, risk, recommendations, completeness notes, and list update dates if provided.
  - Maintain an audit trail by echoing user confirmations and pasted list names; encourage exporting the conversation.
- **Recommendations**: Offer clear next steps (e.g., escalate to Compliance, enhanced due diligence, periodic rescreening interval, approve).

## When to Load References
- Use `references/checklists.md` for the required list names, intake prompt, and adverse keyword set.
- Use `references/report-templates.md` for the report skeleton and quick-paste snippets (intake + checklist + report body).
- Use `references/mas-list-fetch.md` when MAS site access is flaky; it contains the canonical URL, alternate retrieval tips, and UN fallback links.
- Use `references/mas-required-lists.md` for a current snapshot of categories, list URLs, and last-updated dates to verify completeness and prompt users for fresher files.
- Use `references/tsfa-first-schedule.md` for the TSFA 2002 First Schedule domestic CT names (snapshot; replace when user provides fresher AGC extract).
- Local assets (UN lists): run `scripts/update_un_lists.ps1` to download the consolidated UN list and split regime files into `assets/` (e.g., `dprk.xml`, `drc.xml`, `libya.xml`, `somalia.xml`, `southsudan.xml`, `sudan.xml`, `yemen.xml`, `al-qaida.xml`, `taliban.xml`, `iran.xml`, `iraq.xml`, `car.xml`, `gb.xml`, `haiti.xml`).
- Local assets (ACRA Alert List, 23 Dec 2025):  
  - `assets/alert-list-2025-12-23.csv` (preferred for matching; columns: sn, name, date_of_birth, passport, nationality).  
  - `assets/alert-list-2025-12-23.txt` (source transcription).  
  Request newer versions if available and replace both.

## Safety & Scope
- Do not invent matches; only use user-pasted data. State if any mandatory list is missing.
- Note that this skill does not fetch live lists; user must provide data and last-updated dates.
- Keep responses concise but audit-ready; avoid storing or transmitting data externally.
