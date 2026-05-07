---
name: bookkeeping-agent-bank2books
description: Transform raw bank statements (PDF/CSV/OFX/API payloads) into reconciled ledgers and Markdown financial statements using the Bank2Books pipeline. Use when you need to ingest and parse statements, classify to the COA, reconcile cash, post journals, build trial balances, and render P&L/Balance Sheet/Trial Balance/GL/schedules/cash-flow outputs with the provided templates and depreciation rules.
---

# Bookkeeping Agent — Bank2Books

## Quick Purpose
Turn raw bank statements into reconciled ledgers and Markdown financial statements using the nine-stage Bank2Books pipeline. Follow the staged checklist below, then render the provided templates and run QA before distribution.

## Workflow Snapshot (1 → 9)
1) Intake: fetch statements, checksum, tag bank/account/period, store immutable copy, emit metadata. 2) Parse: OCR/parse to canonical txn schema with provenance. 3) Enrich/Classify: dedupe, enrich descriptions, map to COA with confidences. 4) Reconcile: tie to cash opening/closing balances; create reconciling items. 5) Post: generate double-entry journals with links back to source IDs. 6) Trial Balance: aggregate debits/credits; ensure debits = credits. 7) Report: populate P&L/BS/TB/GL/schedules/cash-flow templates. 8) QA: balance checks, roll-forwards, prior-period variances. 9) Distribute: package Markdown/PDF with source IDs and archive.

## How to Work a Packet
- **Prereqs:** Ensure COA IDs are known; configure storage for raw → parsed → ledger → outputs; keep the statement URI handy.
- **Run stages in order**; if skipping, document why inside the packet notes.
- **Low-confidence or ambiguous mappings**: pause at Stage 3; surface for human review before reconciliation.
- **Reconciliation rules:** opening/closing cash must match statement; outstanding items go to the cash schedule block in `assets/balance_sheet_schedules_template.md`.
- **Ledger posting:** enforce period locks and COA validation; include `source_statement_id` and `reference_page` on each journal line.

## Rendering the Financials
- Use the Markdown skeletons in `assets/` (see Resource Map). Copy the template, then replace `{{placeholders}}` with computed values and narrative.
- Keep table structures intact; mark unused sections as `Not Applicable` rather than deleting.
- Calculated links: net income feeds retained earnings; assets must equal liabilities + equity; cash schedule should tie to BS cash and statement movement.

## Fixed-Asset & Depreciation Rules
- Capitalize fixed-asset spend to 1400; credit cash. Start straight-line depreciation on the first day of the month after payment unless an in-service date is provided.
- Default lives/residuals are in `references/depreciation_policy.md`; journal pattern: Dr 6700 Depreciation Expense / Cr 1410 Accumulated Depreciation.
- Populate the fixed-asset rollforward inside `assets/balance_sheet_schedules_template.md` and ensure cumulative depreciation ≤ cost.

## QA & Delivery Checklist
- Debits = credits in the trial balance; BS balances; cash schedule ties; retained earnings rollforward correct.
- Every rendered statement cites entity, period, currency, preparer, source IDs (statement + ledger snapshot).
- Package Markdown (and optional PDF exports) with references back to source statement IDs; archive per Stage 9.

## Resource Map
- references/workflow.md — full step-by-step pipeline; load when uncertain about a stage.
- references/agents.md — responsibilities per agent role; use to hand off or segment tasks.
- references/depreciation_policy.md — asset lives, conventions, journal patterns.
- references/templates_readme.md — quick notes on when to use each template.
- assets/*.md — report skeletons: profit_and_loss, balance_sheet, trial_balance, general_ledger, balance_sheet_schedules, cash_flow_statement. Copy then fill; keep placeholders unless not applicable.
