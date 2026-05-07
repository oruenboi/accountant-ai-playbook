
# Financial Statement Templates

The `templates` directory contains Markdown skeletons that the bookkeeping agent can fill when producing reports from parsed bank and ledger data. Each template expects the agent to substitute the `{{placeholders}}` with actual values or narrative text.

## Template Overview

1. **profit_and_loss_template.md** – Structures the income statement with revenue, COGS, operating expenses, other income/expenses, and commentary.
2. **balance_sheet_template.md** – Covers assets, liabilities, equity, and includes a balance verification block.
3. **trial_balance_template.md** – Summarizes debit/credit totals per account class and highlights adjustments.
4. **general_ledger_template.md** – Provides a per-account ledger detail table plus running balance summary.
5. **balance_sheet_schedules_template.md** – Supplies supporting schedules for cash, receivables, payables, fixed assets, and debt.
6. **cash_flow_statement_template.md** – Provides operating/investing/financing sections plus cash reconciliation for period-over-period analysis.


## Usage Notes

- Populate metadata fields (entity, period, preparer) before inserting financial figures.
- Keep numeric values formatted consistently (e.g., currency with thousand separators) to simplify downstream rendering.
- Preserve the Markdown table structures so reviewers can scan or export them without reformatting.
- When a section is not applicable, explicitly state `Not Applicable` instead of removing the block so the review checklist remains complete.
