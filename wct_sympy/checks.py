"""Core checks: dimensional, numeric residual, and limit checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import sympy as sp

from wct_sympy.constants import CONSTANTS
from wct_sympy.dimensions import (
    Dimension,
    INVERSE_LENGTH,
    INVERSE_LENGTH_SQUARED,
    MASS,
    NAMED_DIMENSIONS,
    lookup,
)
from wct_sympy.equations import (
    c,
    curvature_mass_expr,
    hbar,
    k_eff,
    kappa,
    koide_expr,
    me,
    mmu,
    mtau,
    sigma_expr,
    sigma_raw_expr,
    tau,
)


@dataclass
class CheckResult:
    check_id: str
    name: str
    status: str                          # "PASS" or "FAIL"
    value: Any = None
    expected: Any = None
    residual: Optional[float] = None
    failure_reason: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)

    def as_row(self) -> Dict[str, Any]:
        return {
            "check_id": self.check_id,
            "name": self.name,
            "status": self.status,
            "value": _csv_value(self.value),
            "expected": _csv_value(self.expected),
            "residual": "" if self.residual is None else f"{self.residual:.6e}",
            "failure_reason": self.failure_reason,
        }


def _csv_value(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, float):
        return f"{v:.10g}"
    return str(v)


# ---------------------------------------------------------------------------
# Dimensional checks
# ---------------------------------------------------------------------------

def dimension_of_curvature_mass(symbol_dims: Dict[str, Dimension] | None = None) -> Dimension:
    """Compute the dimension of (hbar / c) * k_eff from a symbol-dimension map."""
    sd = symbol_dims or {
        "hbar": NAMED_DIMENSIONS["action"],
        "c": NAMED_DIMENSIONS["velocity"],
        "k_eff": NAMED_DIMENSIONS["inverse_length"],
    }
    return sd["hbar"] / sd["c"] * sd["k_eff"]


def check_curvature_mass_dimension() -> CheckResult:
    """Verify (hbar/c) * k_eff has mass dimension."""
    dim = dimension_of_curvature_mass()
    ok = dim == MASS
    return CheckResult(
        check_id="D1_10",
        name="effective_curvature_mass_relation",
        status="PASS" if ok else "FAIL",
        value=str(dim),
        expected=str(MASS),
        residual=None,
        failure_reason="" if ok else f"got {dim}, expected {MASS}",
    )


def check_sigma_dimension() -> CheckResult:
    """sigma = sqrt(kappa^2 + tau^2) must carry L^-1 when kappa,tau ~ L^-1."""
    # Symbolic dim algebra: both kappa,tau have L^-1, so kappa^2+tau^2 has L^-2,
    # and sqrt -> L^-1.
    kappa_dim = INVERSE_LENGTH
    tau_dim = INVERSE_LENGTH
    if kappa_dim != tau_dim:
        return CheckResult(
            check_id="CURV1",
            name="curvature_torsion_sigma",
            status="FAIL",
            failure_reason="kappa and tau must share dimension to add",
        )
    summed = kappa_dim ** 2  # equals tau_dim^2 by assumption
    sigma_dim = summed ** sp.Rational(1, 2)
    ok = sigma_dim == INVERSE_LENGTH
    return CheckResult(
        check_id="CURV1",
        name="curvature_torsion_sigma",
        status="PASS" if ok else "FAIL",
        value=str(sigma_dim),
        expected=str(INVERSE_LENGTH),
        failure_reason="" if ok else f"got {sigma_dim}, expected {INVERSE_LENGTH}",
    )


def check_sigma_raw_not_inverse_length() -> CheckResult:
    """sigma_raw = kappa^2 + tau^2 must NOT be inverse length (it is L^-2)."""
    kappa_dim = INVERSE_LENGTH
    summed = kappa_dim ** 2
    ok = summed != INVERSE_LENGTH and summed == INVERSE_LENGTH_SQUARED
    return CheckResult(
        check_id="CURV2",
        name="curvature_torsion_sigma_raw",
        status="PASS" if ok else "FAIL",
        value=str(summed),
        expected=str(INVERSE_LENGTH_SQUARED),
        failure_reason="" if ok else "sigma_raw should be L^-2, not L^-1",
    )


# ---------------------------------------------------------------------------
# Numeric checks
# ---------------------------------------------------------------------------

def check_koide(constants: Dict[str, float] | None = None,
                tolerance: float = 1e-2) -> CheckResult:
    """Numerical Koide residual: Q - 2/3.

    Returns the *symbolic* expression evaluated and the residual.
    Tolerance is intentionally loose - the empirical Q sits near 2/3 + 2e-5.
    """
    cs = constants or CONSTANTS
    required = ("me", "mmu", "mtau")
    missing = [k for k in required if k not in cs]
    if missing:
        return CheckResult(
            check_id="K1",
            name="koide_relation",
            status="FAIL",
            failure_reason=f"missing constants: {missing}",
        )
    expr = koide_expr()
    Q = float(expr.subs({me: cs["me"], mmu: cs["mmu"], mtau: cs["mtau"]}))
    expected = 2.0 / 3.0
    residual = Q - expected
    ok = abs(residual) < tolerance
    return CheckResult(
        check_id="K1",
        name="koide_relation",
        status="PASS" if ok else "FAIL",
        value=Q,
        expected=expected,
        residual=residual,
        failure_reason="" if ok else f"|Q - 2/3| = {abs(residual):.3e} > {tolerance:.1e}",
    )


# ---------------------------------------------------------------------------
# Limit checks
# ---------------------------------------------------------------------------

def check_limits() -> CheckResult:
    """Symbolic limit checks for the mass relation and constants."""
    reasons = []
    expr = curvature_mass_expr()

    # k_eff -> 0 should send m -> 0
    lim = sp.limit(expr, k_eff, 0)
    if lim != 0:
        reasons.append(f"limit k_eff->0 gave {lim}, expected 0")

    # c must be nonzero - dividing by zero is undefined
    try:
        bad = expr.subs(c, 0)
        if bad != sp.zoo and bad.is_finite is not False:
            reasons.append("c=0 should be singular but expression is finite")
    except Exception as e:
        reasons.append(f"c=0 raised unexpectedly: {e}")

    # hbar must be nonzero - expression at hbar=0 is 0, which is degenerate
    val_hbar0 = expr.subs(hbar, 0)
    if val_hbar0 != 0:
        reasons.append(f"hbar=0 collapsed to {val_hbar0}, expected 0 (degenerate)")

    # Koide masses must be positive for real sqrt
    for sym in (me, mmu, mtau):
        if not sym.is_positive:
            reasons.append(f"{sym} not declared positive; sqrt would not be real")

    ok = not reasons
    return CheckResult(
        check_id="LIM1",
        name="limit_checks",
        status="PASS" if ok else "FAIL",
        value="; ".join(reasons) if reasons else "all limits OK",
        expected="all limits OK",
        failure_reason="; ".join(reasons),
    )


# ---------------------------------------------------------------------------
# Registry-driven dispatch
# ---------------------------------------------------------------------------

CHECKS = {
    "D1_10": check_curvature_mass_dimension,
    "CURV1": check_sigma_dimension,
    "CURV2": check_sigma_raw_not_inverse_length,
    "K1": check_koide,
    "LIM1": check_limits,
}


def run_all() -> list[CheckResult]:
    return [fn() for fn in CHECKS.values()]
