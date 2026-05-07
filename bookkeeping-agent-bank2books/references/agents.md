
# Agent Operating Guide

This guide describes how each agent in the bookkeeping pipeline should use the shared files and templates within this repository. The end goal is to transform raw bank statements into reconciled ledgers and Markdown-based financial statements.

## Shared Resources
- `workflow.md` – canonical description of the end-to-end process. Every agent should align its inputs/outputs with the steps documented there.
- `templates/` – Markdown skeletons for Profit & Loss, Balance Sheet, Trial Balance, General Ledger detail, and Balance Sheet schedules. Agents responsible for rendering reports must populate the `{{placeholders}}` with actual values.
- Chart of Accounts – defined within the code base; all posting/classification logic must reference the COA IDs embedded in the templates (e.g., 1100 Cash, 4100 Operating Revenue).

## Agent Responsibilities

### 1. Statement Intake Agent
- Pulls raw bank statements (PDF/CSV/OFX/API) and records metadata.
- Stores the immutable files in the raw statement store and emits references consumed downstream.
- Must log each ingestion in accordance with Step 1 of `workflow.md` so later agents have traceable inputs.

### 2. Parsing Agent
- Consumes statement metadata/URIs, performs OCR or structured parsing, and emits normalized transactions.
- Writes structured output into the `parsed_transactions` store along with provenance fields described in Step 2 of `workflow.md`.
- Flags low-confidence extractions for human review before they move to classification.

### 3. Enrichment & Classification Agent
- Deduplicates overlapping statements, enhances descriptions, and maps each transaction to a COA account.
- Uses deterministic mapping tables first, then calls LLM helpers only when rules fail.
- Outputs enriched transactions with `coa_account_id`, `tags`, and confidence scores (Step 3).

### 4. Reconciliation Agent
- Compares classified transactions to the ledger’s cash accounts, ensuring opening/closing balances tie to statements.
- Produces reconciliation artifacts (outstanding items, timing differences) that will later populate the cash schedule within `templates/balance_sheet_schedules_template.md`.
- Generates adjusting entries when needed and routes unresolved breaks for review (Step 4).

### 5. Ledger Posting Agent
- Converts reconciled transactions plus adjustments into double-entry journal entries stored in the ledger database.
- Enforces COA validation, period locks, and link-backs to source statement IDs, as outlined in Step 5.
- Provides a ledger snapshot ID for the Reporting Agent to use.

### 6. Trial Balance Agent
- Aggregates the ledger snapshot into debits/credits per account to build the period’s trial balance (Step 6).
- Supplies totals to `templates/trial_balance_template.md`, ensuring debits equal credits before releasing data downstream.

### 7. Reporting Agent
- Reads the approved trial balance, ledger detail, and reconciliation schedules to populate all Markdown templates:
  - `templates/profit_and_loss_template.md` – fill revenue/COGS/OpEx sections and narrative commentary.
  - `templates/balance_sheet_template.md` – insert asset/liability/equity balances and balance-check metrics.
  - `templates/general_ledger_template.md` – loop per active account to embed transaction tables.
  - `templates/balance_sheet_schedules_template.md` – add cash reconciliations, AR/AP aging, fixed-asset rollforward, and loan schedules.
- Writes the rendered Markdown files to the designated output location or bundles them for delivery (Step 7).

### 8. QA & Review Agent
- Runs automated validations (Assets = Liabilities + Equity, Net Income flows to Retained Earnings, cash schedule ties to BS, etc.).
- Annotates the Markdown files with review notes or produces a summary checklist for approvers (Step 8).
- Blocks distribution if any template fails validation or is missing required sections.

### 9. Distribution Agent
- Packages finalized Markdown (and optional PDF exports) with references to the originating statement IDs and ledger snapshot IDs.
- Archives outputs per Step 9 of `workflow.md` and notifies stakeholders.

## Implementation Notes
- All agents must store intermediate artifacts with the IDs referenced in `workflow.md` to keep the lineage intact.
- Markdown templates should be treated as source-of-truth formats; downstream systems can convert them to PDFs or HTML as needed.
- When updating templates or the workflow, ensure this guide stays in sync so agents know which files to touch.
