# Balance Sheet

- **Entity:** {{entity_name}}
- **As Of:** {{statement_date}}
- **Currency:** {{currency}}
- **Prepared By:** {{prepared_by}}

## Snapshot
- **Total Assets:** {{total_assets}}
- **Total Liabilities:** {{total_liabilities}}
- **Total Equity:** {{total_equity}}
- **Balance Check (Assets - Liabilities - Equity):** {{balance_check}}

## Assets
### Current Assets
| Account | Description | Ending Balance | Prior Balance | Variance | Notes |
|---------|-------------|----------------|---------------|----------|-------|
| 1100 | Cash & Cash Equivalents | {{1100_current}} | {{1100_prior}} | {{1100_variance}} | {{1100_notes}} |
| 1200 | Accounts Receivable | {{1200_current}} | {{1200_prior}} | {{1200_variance}} | {{1200_notes}} |
| 1300 | Prepaid Expenses | {{1300_current}} | {{1300_prior}} | {{1300_variance}} | {{1300_notes}} |
| **Total Current Assets** |  | **{{total_current_assets}}** | **{{total_current_assets_prior}}** | **{{total_current_assets_variance}}** | |

### Non-Current Assets
| Account | Description | Ending Balance | Prior Balance | Variance | Notes |
|---------|-------------|----------------|---------------|----------|-------|
| 1400 | Fixed Assets | {{1400_current}} | {{1400_prior}} | {{1400_variance}} | {{1400_notes}} |
| 1410 | Accumulated Depreciation | {{1410_current}} | {{1410_prior}} | {{1410_variance}} | {{1410_notes}} |
| **Total Non-Current Assets** |  | **{{total_non_current_assets}}** | **{{total_non_current_assets_prior}}** | **{{total_non_current_assets_variance}}** | |

> **Total Assets:** {{total_assets}}

## Liabilities
### Current Liabilities
| Account | Description | Ending Balance | Prior Balance | Variance | Notes |
|---------|-------------|----------------|---------------|----------|-------|
| 2100 | Accounts Payable | {{2100_current}} | {{2100_prior}} | {{2100_variance}} | {{2100_notes}} |
| 2200 | Credit Cards / Lines | {{2200_current}} | {{2200_prior}} | {{2200_variance}} | {{2200_notes}} |
| 2300 | Accrued Expenses | {{2300_current}} | {{2300_prior}} | {{2300_variance}} | {{2300_notes}} |
| **Total Current Liabilities** |  | **{{total_current_liabilities}}** | **{{total_current_liabilities_prior}}** | **{{total_current_liabilities_variance}}** | |

### Long-Term Liabilities
| Account | Description | Ending Balance | Prior Balance | Variance | Notes |
|---------|-------------|----------------|---------------|----------|-------|
| 2400 | Loans Payable | {{2400_current}} | {{2400_prior}} | {{2400_variance}} | {{2400_notes}} |
| **Total Long-Term Liabilities** |  | **{{total_long_term_liabilities}}** | **{{total_long_term_liabilities_prior}}** | **{{total_long_term_liabilities_variance}}** | |

> **Total Liabilities:** {{total_liabilities}}

## Equity
| Account | Description | Ending Balance | Prior Balance | Variance | Notes |
|---------|-------------|----------------|---------------|----------|-------|
| 3100 | Owner's Equity | {{3100_current}} | {{3100_prior}} | {{3100_variance}} | {{3100_notes}} |
| 3200 | Retained Earnings | {{3200_current}} | {{3200_prior}} | {{3200_variance}} | {{3200_notes}} |
| **Total Equity** |  | **{{total_equity}}** | **{{total_equity_prior}}** | **{{total_equity_variance}}** | |

## Balance Verification
- **Check:** Assets ({{total_assets}}) = Liabilities ({{total_liabilities}}) + Equity ({{total_equity}})
- **Variance:** {{balance_check}}
- **Notes on Variance:** {{balance_notes}}

## Narrative Commentary
{{narrative_commentary}}
