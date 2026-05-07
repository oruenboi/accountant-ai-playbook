# Trial Balance

- **Entity:** {{entity_name}}
- **Period Ending:** {{period_end}}
- **Currency:** {{currency}}
- **Prepared On:** {{prepared_on}}

| Account | Description | Debit | Credit | Notes |
|---------|-------------|-------|--------|-------|
| 1000 | Assets | {{1000_debit}} | {{1000_credit}} | {{1000_notes}} |
| 2000 | Liabilities | {{2000_debit}} | {{2000_credit}} | {{2000_notes}} |
| 3000 | Equity | {{3000_debit}} | {{3000_credit}} | {{3000_notes}} |
| 4000 | Revenue | {{4000_debit}} | {{4000_credit}} | {{4000_notes}} |
| 5000 | Cost of Goods Sold | {{5000_debit}} | {{5000_credit}} | {{5000_notes}} |
| 6000 | Operating Expenses | {{6000_debit}} | {{6000_credit}} | {{6000_notes}} |
| 7000 | Other Gains/Losses | {{7000_debit}} | {{7000_credit}} | {{7000_notes}} |
| **Totals** |  | **{{total_debits}}** | **{{total_credits}}** | |

## Balance Check
- **Debits - Credits:** {{net_trial_balance}}
- **Status:** {{trial_balance_status}}
- **Reconciliation Notes:** {{reconciliation_notes}}

## Adjustments Summary
| Journal Entry | Description | Debit | Credit | Reviewer |
|---------------|-------------|-------|--------|----------|
| {{je_id}} | {{je_description}} | {{je_debit_total}} | {{je_credit_total}} | {{je_reviewer}} |
