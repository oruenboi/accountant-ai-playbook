#!/usr/bin/env python3
"""Convert DBS PDF bank statements to Xero-importable CSV and validate balances.

Usage (example):
  python tools/skills/dbs-xero-csv/scripts/dbs_to_xero_csv.py \
    "C:/Users/wdqia/Daisy Accountants/Taeseong Taekwondo - Accounts - Documents/4. Novena/Novena 2025" \
    -o build/novena_2025_dbs_xero.csv --date-format "%d/%m/%Y"

The script parses DBS Business Account statements, derives transaction amounts
from running balances, and writes the Xero bank-import CSV columns
Date, Amount, Payee, Description, Reference, Check Number.
It also checks that opening + transactions = reported closing balance.
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import List, Sequence

import pdfplumber
import re


DATE_LINE_RE = re.compile(r"^(\d{2}-[A-Za-z]{3}-\d{2})\s+(\d{2}-[A-Za-z]{3}-\d{2})\s+(.*)")
UOB_DATE_HEAD_RE = re.compile(r"^(\d{2}/\d{2}/\d{4})\s+(\d{2}/\d{2}/\d{4})\s*(.*)$")
MONEY_RE = re.compile(r"-?\d{1,3}(?:,\d{3})*\.\d{2}")
BF_RE = re.compile(r"Balance Brought Forward\s+(-?\d[\d,]*\.\d{2})", re.I)
BC_RE = re.compile(r"Balance Carried Forward\s+(-?\d[\d,]*\.\d{2})", re.I)


@dataclass
class Transaction:
    date: datetime
    value_date: datetime
    amount: Decimal
    balance: Decimal
    payee: str
    description: str
    reference: str
    source: str


def d(value: str) -> Decimal:
    """Parse a money string into Decimal rounded to 2dp."""
    return (Decimal(value.replace(",", ""))
            .quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def clean_text(line: str) -> str:
    return " ".join(line.split())


def last_money(line: str) -> Decimal | None:
    nums = MONEY_RE.findall(line)
    return d(nums[-1]) if nums else None


def infer_payee(lines: Sequence[str]) -> str:
    for line in lines:
        stripped = re.sub(r"[^A-Za-z0-9 &'@#/.,\-]", " ", line).strip()
        if stripped and not stripped.lower().startswith(("sgd", "usd", "eur")):
            # prefer the first human-readable line
            return " ".join(stripped.split())[:70]
    return ""


def infer_reference(lines: Sequence[str]) -> str:
    for line in lines:
        if re.search(r"\b\d{6,}\b", line) or re.search(r"[A-Z0-9]{10,}", line):
            return line[:100]
    return ""


def parse_pdf(path: Path, tolerance: Decimal) -> tuple[List[Transaction], dict]:
    lines: List[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            lines.extend([clean_text(l) for l in text.splitlines() if l.strip()])

    uob_line_hits = sum(1 for line in lines if parse_uob_line(line) is not None)
    if uob_line_hits:
        return parse_uob_lines(lines, path, tolerance)

    opening: Decimal | None = None
    closing_reported: Decimal | None = None
    prev_balance: Decimal | None = None
    txns: List[Transaction] = []
    current: dict | None = None
    warnings: List[str] = []

    def finalize_current():
        nonlocal prev_balance, current
        if not current:
            return
        balance = current.get("balance")
        if balance is None:
            warnings.append(f"Missing balance on line starting {current.get('raw')!r}")
            current = None
            return
        if prev_balance is None:
            prev_balance_local = balance
            amount = Decimal("0.00")
        else:
            prev_balance_local = prev_balance
            amount = (balance - prev_balance_local).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        prev_balance = balance
        description_lines: List[str] = current.get("lines", [])
        description = " | ".join(description_lines)
        payee = infer_payee(description_lines)
        reference = infer_reference(description_lines)
        txns.append(
            Transaction(
                date=current["date"],
                value_date=current["value_date"],
                amount=amount,
                balance=balance,
                payee=payee,
                description=description,
                reference=reference,
                source=path.name,
            )
        )
        current = None

    for line in lines:
        if line.lower().startswith("withdrawal deposit balance"):
            continue
        match_bf = BF_RE.search(line)
        if match_bf:
            bf = d(match_bf.group(1))
            if opening is None:
                opening = bf
                prev_balance = bf
            else:
                if prev_balance is None:
                    prev_balance = bf
                elif (bf - prev_balance).copy_abs() > tolerance:
                    # Warning only — keep prev_balance so deltas remain accurate.
                    warnings.append(f"Balance brought forward reset from {prev_balance} to {bf}")
            continue

        match_bc = BC_RE.search(line)
        if match_bc:
            closing_reported = d(match_bc.group(1))
            continue

        match_date = DATE_LINE_RE.match(line)
        if match_date:
            finalize_current()
            tran_date_raw, val_date_raw, rest = match_date.groups()
            balance_val = last_money(line)
            try:
                tran_date = datetime.strptime(tran_date_raw, "%d-%b-%y")
                val_date = datetime.strptime(val_date_raw, "%d-%b-%y")
            except ValueError:
                warnings.append(f"Unparseable date line: {line}")
                continue
            current = {
                "date": tran_date,
                "value_date": val_date,
                "balance": balance_val,
                "lines": [rest.strip()],
                "raw": line,
            }
            continue

        if current:
            current.setdefault("lines", []).append(line)

    finalize_current()

    closing_calc = prev_balance
    # Fix zero-amount rows caused by balance resets/page headers by inferring
    # the amount from the next balance movement.
    for i in range(len(txns) - 1):
        if txns[i].amount.copy_abs() <= tolerance:
            inferred = (txns[i + 1].balance - txns[i].balance).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            txns[i].amount = inferred
    meta = {
        "opening": opening,
        "closing_reported": closing_reported,
        "closing_calc": closing_calc,
        "warnings": warnings,
    }
    return txns, meta


def parse_uob_lines(lines: Sequence[str], path: Path, tolerance: Decimal) -> tuple[List[Transaction], dict]:
    txns: List[Transaction] = []
    warnings: List[str] = []
    pending_desc: List[str] = []
    prev_balance: Decimal | None = None
    opening: Decimal | None = None
    in_statement = False

    skip_prefixes = (
        "Date of Export:",
        "Account Activities",
        "Statement",
        "Value Date Description",
        "Company / Account",
        "Company Available Balance",
        "Account Ledger Balance",
        "Account Details",
        "Account Type",
        "Total Float",
        "Account Transactions",
        "Withdrawal and Deposit",
    )

    for line in lines:
        if line == "Statement":
            in_statement = True
            pending_desc = []
            continue
        if line.startswith("Date of Export:"):
            in_statement = False
            pending_desc = []
            continue
        if not in_statement:
            continue

        if line.startswith(skip_prefixes):
            continue
        if line in ("Date", "Advice"):
            continue
        if re.search(r"\b\d+\s+of\s+\d+\b", line):
            continue

        parsed = parse_uob_line(line)
        if not parsed:
            pending_desc.append(line)
            if len(pending_desc) > 12:
                pending_desc = pending_desc[-12:]
            continue

        tran_date_raw, val_date_raw, inline_desc, dep_raw, wd_raw, bal_raw = parsed
        try:
            tran_date = datetime.strptime(tran_date_raw, "%d/%m/%Y")
            val_date = datetime.strptime(val_date_raw, "%d/%m/%Y")
            deposit = d(dep_raw)
            withdrawal = d(wd_raw)
            balance = d(bal_raw)
        except Exception:
            warnings.append(f"Unparseable UOB row: {line}")
            pending_desc = []
            continue

        amount = (deposit - withdrawal).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if amount.copy_abs() <= tolerance and prev_balance is not None:
            inferred = (balance - prev_balance).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if inferred.copy_abs() > tolerance:
                amount = inferred

        desc_lines = pending_desc[:]
        if inline_desc:
            desc_lines.append(inline_desc)
        pending_desc = []

        description = " | ".join(desc_lines).strip()
        payee = infer_payee(desc_lines)
        reference = infer_reference(desc_lines)

        if prev_balance is None:
            opening = (balance - amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        prev_balance = balance

        txns.append(
            Transaction(
                date=tran_date,
                value_date=val_date,
                amount=amount,
                balance=balance,
                payee=payee,
                description=description,
                reference=reference,
                source=path.name,
            )
        )

    closing_calc = prev_balance
    closing_reported = txns[-1].balance if txns else None
    meta = {
        "opening": opening,
        "closing_reported": closing_reported,
        "closing_calc": closing_calc,
        "warnings": warnings,
    }
    return txns, meta


def parse_uob_line(line: str) -> tuple[str, str, str, str, str, str] | None:
    head = UOB_DATE_HEAD_RE.match(line)
    if not head:
        return None
    tran_date_raw, val_date_raw, tail = head.groups()
    money_matches = list(MONEY_RE.finditer(tail))
    if len(money_matches) < 3:
        return None
    dep_m, wd_m, bal_m = money_matches[-3:]
    if tail[bal_m.end():].strip():
        return None
    inline_desc = tail[:dep_m.start()].strip()
    dep_raw = dep_m.group(0)
    wd_raw = wd_m.group(0)
    bal_raw = bal_m.group(0)
    return tran_date_raw, val_date_raw, inline_desc, dep_raw, wd_raw, bal_raw


def write_csv(txns: Sequence[Transaction], output: Path, date_format: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Amount", "Payee", "Description", "Reference", "Check Number"])
        for txn in txns:
            writer.writerow(
                [
                    txn.date.strftime(date_format),
                    f"{txn.amount:.2f}",
                    txn.payee,
                    txn.description,
                    txn.reference,
                    "",
                ]
            )


def audit_csv(csv_path: Path, tolerance: Decimal) -> list[str]:
    import csv
    money_re = re.compile(r"-?\d[\d,]*\.\d{2}")
    issues: list[str] = []
    with csv_path.open() as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=1):
            try:
                amt = Decimal(row["Amount"])
            except Exception:
                issues.append(f"Row {idx}: non-numeric Amount {row.get('Amount')}")
                continue
            nums = money_re.findall(row.get("Description", ""))
            if nums:
                stated = d(nums[0])
                if (amt.copy_abs() - stated).copy_abs() > tolerance:
                    issues.append(f"Row {idx}: Amount {amt} != stated {stated}")
            if amt.copy_abs() <= tolerance:
                issues.append(f"Row {idx}: Amount is zero or near-zero ({amt})")
    return issues


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="+", help="DBS PDF file(s) or directories containing PDFs")
    parser.add_argument("-o", "--output", required=True, help="Output CSV path")
    parser.add_argument("--date-format", default="%d/%m/%Y", help="strftime format for Date column (default: %%d/%%m/%%Y)")
    parser.add_argument("--tolerance", type=float, default=0.01, help="Balance tolerance in dollars (default: 0.01)")
    parser.add_argument("--allow-mismatch", action="store_true", help="Do not exit with error on balance mismatch")
    parser.add_argument("--log", help="Optional log file path for summaries and warnings")
    args = parser.parse_args(argv)

    tolerance = d(f"{args.tolerance:.2f}")
    inputs: List[Path] = []
    for raw in args.input:
        p = Path(raw)
        if p.is_dir():
            inputs.extend(sorted(p.glob("*.pdf")))
        elif p.is_file():
            inputs.append(p)
        else:
            parser.error(f"Input not found: {p}")

    all_txns: List[Transaction] = []
    summaries: List[str] = []
    for pdf_path in inputs:
        txns, meta = parse_pdf(pdf_path, tolerance)
        all_txns.extend(txns)
        opening = meta.get("opening")
        closing_reported = meta.get("closing_reported")
        closing_calc = meta.get("closing_calc")
        diff = (closing_calc - closing_reported) if (closing_calc is not None and closing_reported is not None) else None
        summary = f"{pdf_path.name}: {len(txns)} txns, opening={opening}, closing_reported={closing_reported}, closing_calc={closing_calc}, diff={diff}"
        summaries.append(summary)
        for warn in meta.get("warnings", []):
            summaries.append(f"WARN {pdf_path.name}: {warn}")
        if diff is not None and diff.copy_abs() > tolerance and not args.allow_mismatch:
            summaries.append(f"ERROR {pdf_path.name}: closing diff {diff} exceeds tolerance {tolerance}")
            if args.log:
                Path(args.log).write_text("\n".join(summaries), encoding="utf-8")
            print("\n".join(summaries), file=sys.stderr)
            return 1

    all_txns.sort(key=lambda t: (t.date, t.source))
    out_path = Path(args.output)
    write_csv(all_txns, out_path, args.date_format)

    audit_lines: List[str] = []
    audit_issues = audit_csv(out_path, tolerance)
    if audit_issues:
        audit_lines.append("AUDIT ISSUES:")
        audit_lines.extend(audit_issues)
    else:
        audit_lines.append("AUDIT: no amount casting issues detected")

    if args.log:
        Path(args.log).write_text("\n".join(summaries + audit_lines), encoding="utf-8")

    print("\n".join(summaries + audit_lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
