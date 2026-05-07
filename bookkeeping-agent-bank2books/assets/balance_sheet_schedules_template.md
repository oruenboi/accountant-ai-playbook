# Balance Sheet Supporting Schedules

- **Entity:** {{entity_name}}
- **As Of:** {{statement_date}}
- **Prepared By:** {{prepared_by}}

## Cash & Cash Equivalents Reconciliation
| Bank Account | Statement Ending Balance | Book Balance | Reconciling Items | Variance | Notes |
|--------------|-------------------------|--------------|-------------------|----------|-------|
| {{bank_account_name}} | {{statement_balance}} | {{book_balance}} | {{reconciling_items}} | {{cash_variance}} | {{cash_notes}} |
| **Total Cash** | **{{total_statement_cash}}** | **{{total_book_cash}}** |  | **{{total_cash_variance}}** | |

## Accounts Receivable Aging
| Customer | 0-30 Days | 31-60 Days | 61-90 Days | 90+ Days | Total | Notes |
|----------|----------|-----------|-----------|----------|-------|-------|
| {{customer_name}} | {{age_0_30}} | {{age_31_60}} | {{age_61_90}} | {{age_90_plus}} | {{customer_total}} | {{customer_notes}} |
| **Totals** | **{{total_0_30}}** | **{{total_31_60}}** | **{{total_61_90}}** | **{{total_90_plus}}** | **{{total_ar}}** | |

## Accounts Payable Aging
| Vendor | 0-30 Days | 31-60 Days | 61-90 Days | 90+ Days | Total | Notes |
|--------|----------|-----------|-----------|----------|-------|-------|
| {{vendor_name}} | {{ap_age_0_30}} | {{ap_age_31_60}} | {{ap_age_61_90}} | {{ap_age_90_plus}} | {{vendor_total}} | {{vendor_notes}} |
| **Totals** | **{{ap_total_0_30}}** | **{{ap_total_31_60}}** | **{{ap_total_61_90}}** | **{{ap_total_90_plus}}** | **{{total_ap}}** | |

## Fixed Assets Rollforward
| Category | Beginning Balance | Additions | Disposals | Depreciation | Ending Balance | Notes |
|----------|------------------|-----------|----------|--------------|---------------|-------|
| {{asset_category}} | {{asset_begin}} | {{asset_additions}} | {{asset_disposals}} | {{asset_depreciation}} | {{asset_ending}} | {{asset_notes}} |
| **Totals** | **{{total_asset_begin}}** | **{{total_asset_additions}}** | **{{total_asset_disposals}}** | **{{total_asset_depreciation}}** | **{{total_asset_ending}}** | |

## Loans & Debt Schedule
| Lender | Principal Balance | Interest Rate | Maturity Date | Current Portion | Long-Term Portion | Notes |
|--------|-------------------|---------------|---------------|-----------------|-------------------|-------|
| {{lender_name}} | {{loan_balance}} | {{interest_rate}} | {{loan_maturity}} | {{current_portion}} | {{long_term_portion}} | {{loan_notes}} |
| **Totals** | **{{total_loan_balance}}** |  |  | **{{total_current_portion}}** | **{{total_long_term_portion}}** | |

## Additional Notes
- **Link to Source Files:** {{supporting_documents_link}}
- **Reviewer:** {{reviewer_name}}
- **Review Date:** {{review_date}}
