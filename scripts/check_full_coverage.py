#!/usr/bin/env python3
"""Run all registered WCT audits and emit CSV, JSON, and Markdown reports."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from wct_sympy.audit import run_full_audit, summary  # noqa: E402
from wct_sympy.models import AuditStatus  # noqa: E402

FIELDS = [
    "equation_id",
    "title",
    "status",
    "expected_status",
    "expectation_matches",
    "audit_mode",
    "value",
    "expected",
    "residual",
    "assumptions",
    "reason",
]


def write_csv(results, path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(result.as_row() for result in results)


def write_json(results, report_summary, path: Path) -> None:
    payload = {
        "summary": report_summary,
        "results": [result.as_row() | {"evidence": dict(result.evidence)} for result in results],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str), encoding="utf-8")


def write_markdown(results, report_summary, path: Path) -> None:
    lines = [
        "# WCT SymPy Full-Corpus Coverage",
        "",
        f"Registered equations: **{report_summary['total']}**",
        f"Registry coverage: **{report_summary['registry_coverage_percent']:.1f}%**",
        f"Expected classifications matched: **{report_summary['expectation_matches']}/{report_summary['total']}**",
        "",
        "## Status counts",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for status, count in report_summary["status_counts"].items():
        lines.append(f"| {status} | {count} |")
    lines += [
        "",
        "## Equation matrix",
        "",
        "| ID | Title | Status | Audit | Result |",
        "|---|---|---|---|---|",
    ]
    for item in results:
        title = item.title.replace("|", "\\|")
        reason = item.reason.replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {item.equation_id} | {title} | {item.status.value} | {item.audit_mode} | {reason} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strict-theory",
        action="store_true",
        help="return nonzero if any equation is classified FAIL",
    )
    args = parser.parse_args()

    results = run_full_audit()
    report_summary = summary(results)
    output = ROOT / "tables"
    output.mkdir(exist_ok=True)
    write_csv(results, output / "wct_full_coverage.csv")
    write_json(results, report_summary, output / "wct_full_coverage.json")
    write_markdown(results, report_summary, ROOT / "COVERAGE_MATRIX.md")

    print("WCT SymPy full-corpus audit")
    print("=" * 72)
    for status, count in report_summary["status_counts"].items():
        print(f"{status:<16} {count:>4}")
    print("-" * 72)
    print(f"registered: {report_summary['total']}")
    print(f"expected classifications matched: {report_summary['expectation_matches']}")
    print("reports: tables/wct_full_coverage.csv, tables/wct_full_coverage.json, COVERAGE_MATRIX.md")

    if report_summary["expectation_mismatches"]:
        return 2
    if args.strict_theory and any(result.status == AuditStatus.FAIL for result in results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
