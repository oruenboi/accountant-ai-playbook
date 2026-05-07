
# Bank Statement to Financial Statement Workflow

This document captures the end-to-end process the bookkeeping agent follows to transform raw bank statements into the Markdown outputs located in `templates/` (Profit & Loss, Balance Sheet, Trial Balance, General Ledger, and Balance Sheet schedules).

## 0. Preconditions
- Chart of Accounts (COA) defined and stored so every transaction can map to an `account_id`.
- Secure storage locations configured for raw statements, parsed transactions, ledger entries, and rendered reports.
- Workflow orchestrator/state machine available to move each statement packet through the stages below.

## 1. Statement Intake
- **Inputs:** PDFs, CSVs, OFX files, or API payloads from bank portals or email inboxes.
- **Actions:**
  - Fetch statements on a schedule, checksum the files, tag them with account/period metadata.
  - Save the immutable copy in `raw_statement_store` and emit a `statement_ingested` event plus URI.
- **Outputs:** Metadata record (bank, account, period, currency, file hash) + blob reference.

## 2. Parsing & Normalization
- **Inputs:** Statement metadata + blob reference.
- **Actions:**
  - Detect format, run OCR when needed, extract line items and balances.
  - Normalize into the canonical transaction schema: `date`, `description`, `amount`, `currency`, `balance`, `source_statement_id`, `reference_page`.
  - Capture parser confidence and validation totals (e.g., sum of debits/credits equals statement change).
- **Outputs:** Structured transactions stored in `parsed_transactions` with full provenance for audit.

## 3. Enrichment & Classification
- **Inputs:** Parsed transactions + COA mapping tables + vendor knowledge base.
- **Actions:**
  - Deduplicate overlapping statement windows.
  - Enhance descriptions (detect vendor, customer, tax category) and attach tags/classes.
  - Map each transaction to a COA account (`coa_account_id`) using deterministic rules + LLM fallback for ambiguous cases; flag low-confidence mappings for reviewer queue.
- **Outputs:** Classified transactions ready for reconciliation.

## 4. Reconciliation
- **Inputs:** Classified transactions + current ledger balances.
- **Actions:**
  - Match statement opening/closing balances to ledger cash accounts.
  - Identify timing differences (outstanding checks, deposits in transit) and create reconciling items.
  - Surface breaks that exceed tolerance for human investigation.
- **Outputs:** Reconciled transaction set with reconciliation status and adjusting entries list.

## 5. Ledger Posting
- **Inputs:** Reconciled transactions + adjusting entries.
- **Actions:**
  - Convert each transaction into double-entry journal entries (`journal_entry_id`, debits, credits, memo, source links).
  - Enforce COA validation, period locks, and approval rules before committing to the ledger store.
- **Outputs:** Ledger entries appended to the general ledger; each references the originating statement transaction for traceability.

## 6. Trial Balance Assembly
- **Inputs:** Ledger snapshot for the reporting period.
- **Actions:**
  - Aggregate debits and credits by account to produce the Trial Balance.
  - Run integrity checks (debits = credits, retained earnings roll-forward, prior-period comparison).
- **Outputs:** Trial Balance data feeding `templates/trial_balance_template.md`.

## 7. Financial Statement Generation
- **Inputs:** Trial Balance + supporting schedules data.
- **Actions:**
  - Populate:
    - `templates/profit_and_loss_template.md` using TB accounts 4000–7000.
    - `templates/balance_sheet_template.md` using TB accounts 1000–3000.
    - `templates/general_ledger_template.md` using detailed ledger entries per account.
    - `templates/balance_sheet_schedules_template.md` using reconciliation outputs (cash), AR/AP aging, fixed asset roll-forward, and loan data.
  - Insert metadata (entity, period, preparer, source references) and calculated metrics (gross margin, net income, balance check).
- **Outputs:** Filled Markdown statements ready for reviewer delivery or PDF export.

## 8. QA & Review
- **Inputs:** Filled Markdown statements + QA rules.
- **Actions:**
  - Automated checks: Assets = Liabilities + Equity, Net Income flows to Equity, cash schedule equals BS cash, etc.
  - Produce variance analysis vs. prior period and highlight anomalies.
  - Route exceptions to human reviewers with source links.
- **Outputs:** Approved statements plus review notes.

## 9. Distribution & Archival
- Store the final Markdown/PDF outputs alongside their source statement IDs and ledger snapshot IDs.
- Notify stakeholders and archive supporting artifacts for audit (e.g., zipped package of Markdown + raw statement references).

## Quick Reference Flow
1. Ingest statement → 2. Parse/OCR → 3. Enrich & classify → 4. Reconcile → 5. Post to ledger → 6. Build trial balance → 7. Render PL/BS/TB/GL/schedules → 8. QA/review → 9. Distribute & archive.

Keep this document updated as new agents or reports are added so onboarding teammates know how bank data traverses the system.
