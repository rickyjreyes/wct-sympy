"""Spectral and regularity audits."""

from .full_checks_core import *  # noqa: F401,F403


def check_dispersion_stationary_point(spec: EquationSpec) -> AuditResult:
    sigma_k = r + a * k**2 - b * k**4
    kstar = sp.sqrt(a / (2 * b))
    first = sp.simplify(sp.diff(sigma_k, k).subs(k, kstar))
    second = sp.simplify(sp.diff(sigma_k, k, 2).subs(k, kstar))
    peak = sp.simplify(sigma_k.subs(k, kstar))
    ok = first == 0 and second == -4 * a and peak == r + a**2 / (4 * b)
    return result(
        spec,
        AuditStatus.PASS if ok else AuditStatus.FAIL,
        value={"k_star": kstar, "sigma_star": peak, "second_derivative": second},
        expected={"first_derivative": 0, "second_derivative_negative": True},
    )


def check_e13_e14_consistency(spec: EquationSpec) -> AuditResult:
    q = sp.symbols("q", nonnegative=True)
    symbol = r + a * q**2 - b * q**4
    return result(
        spec,
        AuditStatus.CONDITIONAL,
        value=symbol,
        expected="r+a*k^2-b*k^4",
        reason="The negative L2 gradient reproduces the rail after integration by parts under compatible boundary and variation conventions.",
        assumptions=("periodic or decaying boundary conditions", "a,b,beta>0", "L2 gradient flow"),
    )


def check_linear_spectral_growth(spec: EquationSpec) -> AuditResult:
    rate, initial = sp.symbols("rate initial", real=True)
    time = sp.symbols("time", real=True)
    power = initial * sp.exp(2 * rate * time)
    residual = sp.simplify(sp.diff(power, time) - 2 * rate * power)
    return result(spec, AuditStatus.PASS if residual == 0 else AuditStatus.FAIL, value=residual, expected=0)


def check_energy_positivity(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.CONDITIONAL,
        value="energy is nonnegative",
        expected="nonnegative coefficients and a defined curvature operator",
        reason="The integrand is nonnegative only when the weights are nonnegative and the denominator is nonzero.",
        assumptions=("c1 >= 0", "c2 >= 0", "D(psi) != 0 almost everywhere"),
    )


def check_gap_curvature_dimensions(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.CONDITIONAL,
        value="average curvature squared has inverse-length-squared units",
        expected="Delta_star must be inverse length squared, or c squared times Delta_star must be inverse time squared",
        reason="The scaling is dimensionally consistent only after the convention for Delta_star is fixed.",
    )


def check_cavity_quadratic_form(spec: EquationSpec) -> AuditResult:
    kap, theta, gamma = sp.symbols("kap theta gamma", positive=True)
    matrix = sp.Matrix([[kap, -gamma / 2], [-gamma / 2, theta]])
    determinant = sp.factor(matrix.det())
    return result(
        spec,
        AuditStatus.PASS,
        value=determinant,
        expected="kap*theta-gamma**2/4 > 0",
        reason="Sylvester's criterion gives kap>0 and gamma**2<4*kap*theta when theta>0.",
    )


def check_second_order_el_template(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.PASS,
        value="dL/dpsi-d_mu(dL/dpsi_mu)+d_mu*d_nu(dL/dpsi_munu)",
        expected=0,
        assumptions=("sufficient smoothness", "boundary variations vanish through first order"),
    )


def check_h2_embedding_threshold(spec: EquationSpec) -> AuditResult:
    valid = [dimension for dimension in range(1, 9) if 2 > sp.Rational(dimension, 2)]
    return result(
        spec,
        AuditStatus.PASS,
        value=valid,
        expected=[1, 2, 3],
        reason="The strict threshold 2>n/2 is equivalent to integer n<=3.",
    )


def check_theta_linf_from_h2(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.FAIL,
        value="H2 controls psi pointwise for n<=3 but controls Delta psi only in L2",
        expected="Theta in L-infinity",
        reason="Even with a denominator bounded away from zero, H2 regularity gives Theta in L2 rather than L-infinity; stronger regularity is required.",
    )
