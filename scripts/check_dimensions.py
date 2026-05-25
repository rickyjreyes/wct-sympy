#!/usr/bin/env python3
"""Run only dimensional checks."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from wct_sympy.checks import (  # noqa: E402
    check_curvature_mass_dimension,
    check_sigma_dimension,
    check_sigma_raw_not_inverse_length,
)


def main() -> int:
    results = [
        check_curvature_mass_dimension(),
        check_sigma_dimension(),
        check_sigma_raw_not_inverse_length(),
    ]
    fail = 0
    for r in results:
        print(f"{r.check_id} {r.name}: {r.status}  ({r.value} == {r.expected})")
        if r.status != "PASS":
            print(f"  reason: {r.failure_reason}")
            fail += 1
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
