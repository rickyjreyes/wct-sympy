"""Tests for the Koide numeric check."""

import math

from wct_sympy.checks import check_koide
from wct_sympy.equations import koide_expr, me, mmu, mtau


def test_koide_expr_evaluates_numerically():
    Q = float(koide_expr().subs({me: 0.511, mmu: 105.66, mtau: 1776.86}))
    assert math.isfinite(Q)
    assert 0.5 < Q < 0.9  # well within range of 2/3


def test_koide_check_passes_with_pdg_values():
    r = check_koide()
    assert r.status == "PASS", r.failure_reason
    assert abs(r.residual) < 1e-2


def test_koide_check_fails_on_missing_constants():
    r = check_koide(constants={"me": 0.511, "mmu": 105.66})  # mtau missing
    assert r.status == "FAIL"
    assert "missing" in r.failure_reason
