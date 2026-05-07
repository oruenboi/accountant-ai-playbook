# General Ledger Detail

- **Entity:** {{entity_name}}
- **Period:** {{period_start}} to {{period_end}}
- **Currency:** {{currency}}

## Instructions
1. Repeat the ledger detail table for each account that has activity.
2. Ensure transactions are sorted by date and reference the originating source (bank, journal entry, adjustment).
3. Running balance should respect the account's normal balance (debit or credit).

## Account {{account_id}} - {{account_name}}
| Date | JE / Reference | Description | Debit | Credit | Running Balance | Source |
|------|----------------|-------------|-------|--------|-----------------|--------|
| {{txn_date}} | {{journal_entry_id}} | {{txn_description}} | {{txn_debit}} | {{txn_credit}} | {{running_balance}} | {{source_link}} |

### Account Summary
- **Beginning Balance:** {{beginning_balance}}
- **Total Debits:** {{account_total_debits}}
- **Total Credits:** {{account_total_credits}}
- **Ending Balance:** {{ending_balance}}
- **Reviewer Notes:** {{account_notes}}

> Repeat the "Account" and "Account Summary" blocks for all applicable accounts.
