#!/usr/bin/env python3
"""Run only the limit checks (LIM1)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from wct_sympy.checks import check_limits  # noqa: E402


def main() -> int:
    r = check_limits()
    print(f"{r.check_id} {r.name}: {r.status}")
    print(f"  detail: {r.value}")
    if r.status != "PASS":
        print(f"  reason: {r.failure_reason}")
    return 0 if r.status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
