
# Depreciation Policy

This policy defines how the bookkeeping agent should depreciate fixed assets captured from bank statements (e.g., the FY2023 workspace renovation). Apply it to all assets once they are capitalized into account 1400 and surfaced in the financial statement templates.

## 1. Asset Classes & Useful Lives

| Asset Class | Description | Useful Life | Residual Value | Notes |
|-------------|-------------|-------------|----------------|-------|
| Leasehold Improvements | Renovations, fit-outs, and permanent changes to rented space. | 3 years (36 months) | 0 | Applies to the SGD 11,654 workspace renovation paid 16 Jun 2023. |
| Furniture & Fixtures | Chairs, shelving, other office fixtures. | 5 years (60 months) | 0 | Add when such assets are capitalized. |
| Equipment & Machines | Production equipment, specialty tools. | 4 years (48 months) | 0 | Placeholder; update when assets arise. |

Adjust useful lives if tax guidance or client instructions differ, but document deviations in this file and in `workflow.md`.

## 2. Depreciation Method
- Use straight-line depreciation with a monthly cadence.
- Convention: place assets in service on the first day of the month following the payment date unless the client provides exact in-service dates. For the 16 Jun 2023 renovation, start depreciation on 1 Jul 2023.
- Monthly depreciation formula:
  - `monthly_expense = asset_cost / useful_life_months`
  - Example (renovation): 11,654 / 36 = 323.72 per month (rounded to two decimals).

## 3. Journals & Accounts
- Standard entry: `Dr 6700 Depreciation Expense (or 6500 if no dedicated account)` / `Cr 1410 Accumulated Depreciation`.
- Tag each journal with:
  - `asset_id` or description ("Leasehold Improvements - Jun 2023 Renovation").
  - Service month (e.g., 2023-07) for audit traceability.
- Lock the depreciation schedule once posted to avoid double-counting.

## 4. Integration with Workflow
1. **Parsing/Classification** - when a large capital outlay is detected, mark it as a fixed asset candidate and route for approval before moving to ledger posting.
2. **Ledger Posting** - capitalized cost goes to account 1400 (debit) with offsetting credit to cash; simultaneously create an amortization schedule based on the table above.
3. **Trial Balance & Reporting** - ensure:
   - P&L picks up depreciation expense in 6700 (or the configured account).
   - Balance Sheet shows asset cost in 1400 and accumulated depreciation in 1410; net book value flows into the B/S templates.
   - Balance Sheet schedules include a fixed-asset rollforward with columns for additions, depreciation, and ending balance.
4. **QA Agent** - verify cumulative depreciation <= asset cost and that net book value matches 1400 - 1410 before reports are released.

## 5. Implementation Checklist
- [ ] Add automated schedule generator that starts depreciation the month after `in_service_date` and stops when useful life completes or asset is disposed.
- [ ] Update P&L template usage so depreciation expense appears under Operating Expenses (use 6700 by default).
- [ ] Update `workflow.md` Step 5/6 to mention depreciation postings.
- [ ] Capture policy metadata (method, life, convention) in configuration so agents can retrieve it programmatically.

Keep this document in sync with client instructions. When new asset classes or lives are introduced, append them to the table and inform the classification/posting agents.
