"""Limit checks and integration test for the master script."""

import csv
import subprocess
import sys
from pathlib import Path

import sympy as sp

from wct_sympy.checks import check_koide, check_limits
from wct_sympy.equations import c, curvature_mass_expr, hbar, k_eff, me, mmu, mtau

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_k_eff_zero_implies_m_zero():
    expr = curvature_mass_expr()
    assert sp.limit(expr, k_eff, 0) == 0


def test_koide_symbols_are_positive():
    for sym in (me, mmu, mtau):
        assert sym.is_positive


def test_c_finite_and_nonzero_required():
    # Symbolic substitution at c=0 yields zoo (complex infinity).
    expr = curvature_mass_expr()
    bad = expr.subs(c, 0)
    assert bad == sp.zoo or bad.is_finite is False


def test_hbar_zero_collapses_mass():
    expr = curvature_mass_expr()
    assert expr.subs(hbar, 0) == 0


def test_check_limits_passes():
    r = check_limits()
    assert r.status == "PASS", r.failure_reason


def test_check_koide_no_pass_when_required_symbols_missing():
    """A check must not be marked PASS when its required inputs are absent."""
    r = check_koide(constants={"me": 0.511})
    assert r.status == "FAIL"


def test_check_all_writes_csv():
    """Integration: scripts/check_all.py creates tables/wct_sympy_checks.csv."""
    out_path = REPO_ROOT / "tables" / "wct_sympy_checks.csv"
    if out_path.exists():
        out_path.unlink()
    result = subprocess.run(
        [sys.executable, "scripts/check_all.py"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert out_path.exists(), f"CSV not created. stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    with out_path.open() as fh:
        rows = list(csv.DictReader(fh))
    assert rows, "CSV is empty"
    headers = set(rows[0].keys())
    for required in ("check_id", "name", "status", "value", "expected", "residual", "failure_reason"):
        assert required in headers
    ids = {row["check_id"] for row in rows}
    assert {"D1_10", "K1", "CURV1", "LIM1"}.issubset(ids)
