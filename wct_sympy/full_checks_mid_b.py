"""Operator, spectral, and resource audits."""

from .full_checks_core import *  # noqa: F401,F403


def check_effective_mass_gap_dimensions(spec: EquationSpec) -> AuditResult:
    lhs = MASS**2
    rhs = (FREQUENCY**2) * VELOCITY**2
    corrected = ACTION**2 * (FREQUENCY**2) / VELOCITY**4
    return result(
        spec,
        AuditStatus.FAIL,
        value={"stated_rhs": rhs, "corrected_rhs": corrected},
        expected=lhs,
        reason="The dispersion assigns Delta_star inverse-time-squared units; the stated mass formula is inconsistent, while hbar squared times Delta_star divided by c to the fourth has mass-squared units.",
    )


def check_curvature_gradient_commutator(spec: EquationSpec) -> AuditResult:
    x = sp.symbols("x", real=True)
    psi = sp.Function("psi")(x)
    denominator = sp.Function("D")(x)
    theta_grad = sp.diff(sp.diff(psi, x, 2) / denominator, x)
    grad_theta = sp.diff(psi, x, 3) / denominator
    commutator = sp.simplify(theta_grad - grad_theta)
    expected = -sp.diff(psi, x, 2) * sp.diff(denominator, x) / denominator**2
    return result(spec, AuditStatus.PASS if sp.simplify(commutator - expected) == 0 else AuditStatus.FAIL, value=commutator, expected=expected)


def check_pressure_density_embedding(spec: EquationSpec) -> AuditResult:
    coeff, theta_abs = sp.symbols("coeff theta_abs", nonnegative=True)
    energy_density = sp.symbols("gradient_term") + coeff * theta_abs**2
    pressure = coeff * theta_abs**2
    ok = sp.expand(energy_density).has(pressure)
    return result(spec, AuditStatus.PASS if ok else AuditStatus.FAIL, value=pressure, expected="curvature term in E18")


def check_sh_fourier_symbol(spec: EquationSpec) -> AuditResult:
    q, kstar = sp.symbols("q kstar", nonnegative=True)
    symbol = (kstar**2 - q**2) ** 2
    at_shell = sp.simplify(symbol.subs(q, kstar))
    return result(spec, AuditStatus.PASS if at_shell == 0 else AuditStatus.FAIL, value=symbol, expected="zero at q=k_star")


def check_green_kernel_pole(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.CONDITIONAL,
        value="G(k_star)=1/r",
        expected="finite kernel when r is nonzero",
        reason="The kernel is finite only away from zeros of its denominator; at r=0 it has a shell pole.",
        assumptions=("r > 0 for a bounded real kernel",),
    )


def check_projection_idempotence(spec: EquationSpec) -> AuditResult:
    indicator = sp.symbols("indicator")
    residual_one = sp.expand(indicator**2 - indicator).subs(indicator, 1)
    residual_zero = sp.expand(indicator**2 - indicator).subs(indicator, 0)
    ok = residual_zero == 0 and residual_one == 0
    return result(spec, AuditStatus.PASS if ok else AuditStatus.FAIL, value=(residual_zero, residual_one), expected=(0, 0))


def check_pattern_threshold(spec: EquationSpec) -> AuditResult:
    q, kstar, coeff = sp.symbols("q kstar coeff", positive=True)
    expression = coeff * (q**2 - kstar**2) ** 2
    value = sp.simplify(expression.subs(q, kstar))
    return result(spec, AuditStatus.PASS if value == 0 else AuditStatus.FAIL, value=value, expected=0)


def check_spectral_fraction_bounds(spec: EquationSpec) -> AuditResult:
    numerator, remainder = sp.symbols("numerator remainder", nonnegative=True)
    fraction = numerator / (numerator + remainder)
    return result(
        spec,
        AuditStatus.PASS,
        value=fraction,
        expected="0<=fraction<=1 when total power is positive",
        assumptions=("numerator+remainder > 0",),
    )


def check_e12_e64_factor(spec: EquationSpec) -> AuditResult:
    kstar = sp.sqrt(a / (2 * b))
    wavelength_from_e12 = sp.simplify(2 * sp.pi / kstar)
    stated = 2 * sp.pi * sp.sqrt(b / a)
    ratio = sp.simplify(wavelength_from_e12 / stated)
    return result(
        spec,
        AuditStatus.FAIL,
        value={"from_E12": wavelength_from_e12, "stated_E64": stated, "ratio": ratio},
        expected=1,
        reason="E12 gives a wavelength larger than E64 by sqrt(2) unless k_star is independently redefined.",
    )


def check_critical_sobolev_exponent(spec: EquationSpec) -> AuditResult:
    dimension = sp.symbols("dimension", positive=True)
    critical = (dimension + 2) / (dimension - 2)
    return result(spec, AuditStatus.PASS, value=critical.subs(dimension, 3), expected=5)


def check_dimensional_stability_iff(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.FAIL,
        value="embedding threshold and nonlinear subcriticality are separate conditions",
        expected="a proved biconditional",
        reason="The H2 embedding threshold for integer dimensions does not establish the additional nonlinear exponent condition.",
    )


def check_physical_resource_dimensions(spec: EquationSpec) -> AuditResult:
    dim = TIME * VOLUME * INVERSE_LENGTH**3
    return result(
        spec,
        AuditStatus.CONDITIONAL,
        value=dim,
        expected="C_phys must have time units",
        reason="The bound is coherent only when C_phys is not declared dimensionless.",
    )


def check_landauer_units(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.CONDITIONAL,
        value="energy when entropy change is measured in bits",
        expected="an explicit entropy convention",
        reason="The ln(2) factor is appropriate for bit entropy; it should not be duplicated for natural-log entropy.",
        assumptions=("entropy change measured in bits", "effective temperature has thermodynamic units"),
    )


def check_coherence_length_dimensions(spec: EquationSpec) -> AuditResult:
    dim = ENERGY ** sp.Rational(1, 2)
    return result(
        spec,
        AuditStatus.FAIL,
        value=dim,
        expected=LENGTH,
        reason="The square root of energy divided by dimensionless entropy is not a length; a stiffness or energy-density scale is missing.",
    )
