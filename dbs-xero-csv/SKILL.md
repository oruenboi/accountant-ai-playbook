---
name: dbs-xero-csv
description: Convert DBS business account PDF statements to Xero bank-import CSV using the Xero template columns, validate opening/closing balances by recomputing transactions, flag mismatches, and emit an audit summary. Trigger when importing DBS (business/SME) statements into Xero or when a Xero CSV bank-import file with balance checks is requested.
---

# DBS -> Xero CSV Skill

Use this skill whenever a user needs to import DBS bank statements into Xero via the CSV bank-import template and wants balance-checked output plus an audit log.

## Workflow
1. Identify inputs
   - DBS PDF statements (monthly) from the client folder.
   - Xero CSV template columns: `Date,Amount,Payee,Description,Reference,Check Number`.
2. Run converter
   - Script: `tools/skills/dbs-xero-csv/scripts/dbs_to_xero_csv.py`
   - Example: `python tools/skills/dbs-xero-csv/scripts/dbs_to_xero_csv.py "C:/path/NOV Dec 2025.pdf" -o build/nov_dec_2025_xero.csv --date-format "%d/%m/%Y" --log build/nov_dec_2025.log`
   - Accepts multiple PDFs or a directory; auto-sorts by transaction date.
3. Balance & casting checks
   - Script derives amounts from running balance deltas (inflow positive, outflow negative).
   - Validates `opening + sum(amounts) = closing_reported` within tolerance (default S$0.01). Fails unless `--allow-mismatch` is set.
   - Auto-fixes zero/blank amounts by inferring from adjacent balances.
4. Audit report output
   - The `--log` file captures per-PDF summary: txn count, opening, closing_reported, closing_calc, diff, and all warnings (balance resets, missing balance lines).
   - After conversion, scan the CSV for any zero or non-numeric amounts and cross-check stated amounts in descriptions; if issues exist, append them to the same log.
5. Review outputs
   - CSV ready for Xero manual import (matches template header).
   - Log is the audit report to attach for review.
6. Troubleshooting
   - If “closing diff exceeds tolerance”: inspect log; check OCR noise, missing pages, non-SGD currency.
   - Use `--allow-mismatch` to force output but still capture warnings.
   - Change `--date-format` for locale (e.g., `%m/%d/%Y`).

## Notes & Assumptions
- Currency: SGD only.
- Amount sign: from balance movement; inflow positive, outflow negative.
- Payee/Reference are heuristic; light manual clean-up may be needed.
- Template reference: `StatementImportTemplate.en-US (43).csv`.

## Useful commands
- Single file: `python tools/skills/dbs-xero-csv/scripts/dbs_to_xero_csv.py "C:/.../NOV Dec 2025.pdf" -o build/nov_dec_2025_xero.csv --log build/nov_dec_2025.log`
- Whole folder: `python tools/skills/dbs-xero-csv/scripts/dbs_to_xero_csv.py "C:/.../Novena 2025" -o build/novena_2025_xero.csv --log build/novena_2025.log`
- Allow mismatch: add `--allow-mismatch`.
