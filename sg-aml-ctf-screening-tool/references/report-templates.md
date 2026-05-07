# Quick-Paste Snippets
- Session ID format: `SGAML-<YYYYMMDD>-<HHMM>-<random4>` (e.g., SGAML-20260109-1015-A3F7).
- Checklist prompt: “Confirm all required lists are included; paste missing lists now.”
- Adverse media request: “Please provide source, date, headline, summary, and full text (if available) for any adverse media.”

# Report Template (Markdown)
```
**Compliance Screening Report — SG AML/CTF**
Session ID: <id> | Date/time (local): <YYYY-MM-DD HH:MM> | Preparer: Codex (ComplianceScreen GPT)

Screening Details
- Entity/Individual: <name>
- Aliases: <aliases or 'none reported'>
- DOB / ID / Nationality: <values>
- Context: <onboarding/vendor/periodic/etc.>
- Sources Received: <lists pasted + adverse media sources>
- List Freshness: <timestamps/versions if provided>
- Completeness Check: <confirmed | missing: ...>

Findings
1) Matches
   - Exact: <list name, entry name, matching fields, reason>
   - Partial: <list name, entry name, similarity High/Med/Low, overlapping fields, rationale>
   - False positives ruled out: <brief notes>
2) Adverse Media
   - Source: <publication/database>, Date: <DD/MM/YYYY>, Headline: <title>
   - Context: <Direct/Association/Neutral>, Severity: <High/Med/Low>
   - Keywords: <e.g., fraud, sanctions breach>
   - Summary: <2–3 lines>

Risk Assessment
- Overall Risk Level: <High/Medium/Low>
- Rationale: <why this level, referencing matches/media/list gaps>

Recommendations
- <Escalate to Compliance / Enhanced Due Diligence / Approve with monitoring / Reject>
- Proposed rescreening interval (if approved/monitor): <e.g., 6 months>

Audit Trail
- User confirmations: <list completeness, data acknowledgements>
- Data received: <lists/media pasted>
- Processing notes: <steps taken, assumptions, limitations>
```

# Response Flow (for agent)
1) Share session ID and confirm lists.
2) Summarize inputs received; ask for missing mandatory fields.
3) Present matches/adverse media with short bullets.
4) Deliver risk level + recommendations.
5) Remind user to export/save the report for audit purposes.
