#!/usr/bin/env python3
"""Master checker: runs every WCT check and writes tables/wct_sympy_checks.csv."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from wct_sympy.checks import run_all  # noqa: E402

CSV_FIELDS = ["check_id", "name", "status", "value", "expected", "residual", "failure_reason"]


def main() -> int:
    results = run_all()

    out_dir = REPO_ROOT / "tables"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "wct_sympy_checks.csv"

    with out_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for r in results:
            writer.writerow(r.as_row())

    print("WCT symbolic audit harness")
    print("=" * 50)
    n_pass = 0
    for r in results:
        marker = "PASS" if r.status == "PASS" else "FAIL"
        line = f"{r.check_id:<8} {r.name:<40} {marker}"
        if r.residual is not None:
            line += f"  residual={r.residual:.3e}"
        print(line)
        if r.failure_reason:
            print(f"           reason: {r.failure_reason}")
        n_pass += int(r.status == "PASS")
    print("=" * 50)
    print(f"{n_pass}/{len(results)} checks PASSED")
    print(f"CSV written to: {out_path.relative_to(REPO_ROOT)}")

    return 0 if n_pass == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
