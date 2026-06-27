"""Core symbolic, dimensional, and logical audits."""

from __future__ import annotations

from typing import Callable
import sympy as sp

from .dimensions import (
    ACTION,
    INVERSE_LENGTH,
    INVERSE_LENGTH_SQUARED,
    LENGTH,
    MASS,
    TIME,
    VELOCITY,
)
from .models import AuditResult, AuditStatus, EquationSpec
from .symbols import a, b, c, hbar, k, k_eff, kappa, mass, n, r, tau

ONE = LENGTH / LENGTH
ENERGY = MASS * LENGTH**2 / TIME**2
FREQUENCY = TIME**-1
VOLUME = LENGTH**3
Checker = Callable[[EquationSpec], AuditResult]


def result(
    spec: EquationSpec,
    status: AuditStatus,
    *,
    value: object = None,
    expected: object = None,
    residual: float | None = None,
    reason: str = "",
    assumptions: tuple[str, ...] | None = None,
    evidence: dict[str, object] | None = None,
) -> AuditResult:
    return AuditResult(
        equation_id=spec.equation_id,
        title=spec.title,
        status=status,
        expected_status=spec.expected_status,
        audit_mode=spec.audit_mode,
        value=value,
        expected=expected,
        residual=residual,
        reason=reason,
        assumptions=spec.assumptions if assumptions is None else assumptions,
        evidence=evidence or {},
    )


def classify_definition(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.DEFINITION,
        value="registered",
        expected="definition/ansatz",
        reason="Definitions are represented but are not promoted to proofs.",
    )


def classify_conditional(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.CONDITIONAL,
        value="requires assumptions",
        expected="explicit hypotheses",
        reason="Domain, regularity, sign, or model assumptions are required.",
    )


def classify_open(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.OPEN,
        value="not settled by symbolic algebra",
        expected="proof or empirical test",
        reason="This is a theorem obligation, empirical claim, or conjecture.",
    )


def check_locking_family(spec: EquationSpec) -> AuditResult:
    dim = ACTION / VELOCITY * INVERSE_LENGTH
    return result(
        spec,
        AuditStatus.CONDITIONAL,
        value=dim,
        expected=MASS,
        reason="The dimension is correct, but the phase-curvature lock and E_rest=hbar*c*k_eff are separate assumptions.",
        assumptions=("controlled phase-curvature lock", "E_rest=hbar*c*k_eff"),
    )


def check_regularized_denominator(spec: EquationSpec) -> AuditResult:
    x = sp.symbols("x", real=True)
    denominator = x + sp.exp(-x**2)
    root = float(sp.nsolve(denominator, -0.6))
    residual = float(abs(denominator.subs(x, root)))
    return result(
        spec,
        AuditStatus.FAIL,
        value=f"D({root:.12g}) is approximately zero for epsilon=alpha=1",
        expected="D(psi) != 0 for every admissible real psi",
        residual=residual,
        reason="The additive exponential term does not guarantee a nonzero denominator for negative real psi.",
        evidence={"counterexample_root": root, "epsilon": 1, "alpha": 1},
    )


def check_master_sh_sign(spec: EquationSpec) -> AuditResult:
    q, kstar, coeff = sp.symbols("q kstar coeff", positive=True)
    symbol = coeff * (kstar**2 - q**2) ** 2
    uv = sp.limit(symbol, q, sp.oo)
    return result(
        spec,
        AuditStatus.FAIL,
        value=uv,
        expected="negative ultraviolet growth",
        reason="A positive coefficient on (Delta+k_star^2)^2 grows off shell; damping requires the opposite sign.",
    )


def check_master_uwct_sign(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.CONDITIONAL,
        value="c2 must be negative for the displayed convention",
        expected="off-shell damping",
        reason="The unified equation is band-selective only under an explicit sign constraint on c2.",
        assumptions=("c2 < 0",),
    )


def check_uniqueness_claim(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.OPEN,
        value="one proposed nonlinear operator",
        expected="uniqueness theorem",
        reason="Variation from a chosen action does not prove uniqueness among nonlinear curvature operators.",
    )
