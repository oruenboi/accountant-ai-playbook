# AGM Data Intake + Field Mapping (Auto-Fill First)

Use this checklist before drafting AGM documents. Extract all available data from provided files and pre-fill drafts. Ask user only for fields marked **Critical Missing**.

## 1) Source Priority
1. Current-year ACRA BizProfile (latest date)
2. Current-year Financial Statements (FS)
3. Prior AGM/AR documents (if provided)
4. User instructions in chat

If two sources conflict, use the newest dated source and state the assumption.

## 2) Extracted Company Facts
- Company legal name
- UEN
- Registered office address
- FYE date
- Last AGM date (context only)
- Last AR date (context only)
- Directors in office
- Shareholders and holdings
- Audit status (audited / unaudited exempt)

## 3) Document-by-Document Required Fields

## A. Notice of AGM
- Company name (auto-fill)
- UEN (auto-fill)
- Registered office (auto-fill)
- Notice date (auto-fill from user statement "today" or system date)
- AGM date (auto-fill from user instruction)
- AGM time (**Critical Missing if absent**)
- AGM venue (default to registered office unless overridden)
- Chair name (default to a director if not specified)
- Agenda clauses (conditional per rules file)
- Proxy lodgement deadline (AGM datetime minus 48 hours)

## B. Proxy Form
- Company name/UEN (auto-fill)
- AGM date/time/venue (time may be Critical Missing)
- Resolution list (conditional)
- Lodgement deadline datetime (auto-calc)

## C. Board Resolution to Convene AGM
- Board approval date (notice date unless specified)
- Directors list/signatories (auto-fill from BizProfile)
- AGM datetime/venue
- Approval of FS for tabling
- Authority clause for filing/follow-up

## D. AGM Minutes (client-ready draft)
- Meeting date/time/venue
- Chair (default to first active director unless instructed)
- Attendance default:
  - If exactly 2 shareholders and no proxy instructions: "Both members present in person"
  - Otherwise: "Members present in person and/or by proxy as recorded"
- Resolution outcomes default: "carried unanimously" (mark as draft assumption)
- End time (**Critical Missing if user requires final signed version**)

## 4) Critical Missing Fields (ask only if still missing)
Ask in one compact question pack:
1. AGM time
2. Venue confirmation (registered office or different venue)
3. Chairperson (default acceptable?)
4. Include directors' remuneration resolution? (Yes/No)
5. Include director re-election resolution? (Yes/No)

## 5) Quality Gate (must pass before sending)
- No unresolved placeholders where data exists
- Names match BizProfile spelling exactly
- UEN/date consistency across all documents
- Proxy deadline correctly computed
- Conditional clauses included/excluded correctly
- Add assumptions note when defaults were used
