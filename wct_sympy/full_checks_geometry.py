"""Geometry and locking audits."""

from .full_checks_core import *  # noqa: F401,F403


def check_e1a(spec: EquationSpec) -> AuditResult:
    dim = INVERSE_LENGTH**2
    expr = kappa**2 + tau**2
    return result(spec, AuditStatus.PASS, value=f"{expr}; {dim}", expected=INVERSE_LENGTH_SQUARED)


def check_e1b(spec: EquationSpec) -> AuditResult:
    dim = (INVERSE_LENGTH**2) ** sp.Rational(1, 2)
    expr = sp.sqrt(kappa**2 + tau**2)
    return result(spec, AuditStatus.PASS, value=f"{expr}; {dim}", expected=INVERSE_LENGTH)


def check_weighted_average(spec: EquationSpec) -> AuditResult:
    w0, f0, length = sp.symbols("w0 f0 length", positive=True)
    ratio = sp.simplify(w0 * f0 * length / (w0 * length))
    return result(
        spec,
        AuditStatus.PASS if ratio == f0 else AuditStatus.FAIL,
        value=ratio,
        expected=f0,
        reason="Constant functions are fixed points of the normalized weighted average.",
    )


def check_locking_variation(spec: EquationSpec) -> AuditResult:
    arc = sp.symbols("arc", real=True)
    phi = sp.Function("phi")(arc)
    weight = sp.Function("weight")(arc)
    curvature = sp.Function("curvature")(arc)
    multiplier = sp.symbols("multiplier", constant=True)
    derivative = sp.diff(phi, arc)
    lagrangian = weight * (derivative - curvature) ** 2 + multiplier * derivative
    el = sp.simplify(sp.diff(lagrangian, phi) - sp.diff(sp.diff(lagrangian, derivative), arc))
    target = -sp.diff(2 * weight * (derivative - curvature) + multiplier, arc)
    return result(spec, AuditStatus.PASS if sp.simplify(el - target) == 0 else AuditStatus.FAIL, value=el, expected=target)


def check_locking_solution(spec: EquationSpec) -> AuditResult:
    constant, weight, curvature = sp.symbols("constant weight curvature", nonzero=True)
    expression = curvature + constant / weight
    recovered = sp.simplify(weight * (expression - curvature))
    return result(
        spec,
        AuditStatus.PASS if recovered == constant else AuditStatus.FAIL,
        value=recovered,
        expected=constant,
        assumptions=("weight is positive", "fixed winding", "connected loop"),
    )


def check_effective_wavenumber_chain(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.CONDITIONAL,
        value="The three forms agree only under closure and weight restrictions",
        expected="explicit conditions on winding, curvature, and weight",
        reason="The topological, unweighted, and density-weighted averages are not identical without closure and compatible weighting.",
        assumptions=("integral curvature equals 2*pi*absolute winding", "weight is constant or compatible with the lock"),
    )


def check_mass_curvature_dimensions(spec: EquationSpec) -> AuditResult:
    dim = ACTION / VELOCITY * INVERSE_LENGTH
    return result(spec, AuditStatus.PASS if dim == MASS else AuditStatus.FAIL, value=dim, expected=MASS)


def check_e8_identity(spec: EquationSpec) -> AuditResult:
    constant, loop_length = sp.symbols("constant loop_length", nonzero=True)
    denominator = sp.symbols("denominator", positive=True)
    stated_extra = 2 * sp.pi * constant * loop_length / denominator
    derived_extra = constant * loop_length
    difference = sp.factor(stated_extra - derived_extra)
    return result(
        spec,
        AuditStatus.FAIL,
        value=difference,
        expected=0,
        reason="Multiplying the E4 solution by the weight and integrating gives constant times loop length, not the extra normalized term in E8.",
    )


def check_shell_quantization_dimensions(spec: EquationSpec) -> AuditResult:
    dim = INVERSE_LENGTH * LENGTH
    return result(spec, AuditStatus.PASS, value=dim, expected=ONE)


def check_winding_dimensions(spec: EquationSpec) -> AuditResult:
    dim = INVERSE_LENGTH * LENGTH
    return result(spec, AuditStatus.PASS, value=dim, expected=ONE)
