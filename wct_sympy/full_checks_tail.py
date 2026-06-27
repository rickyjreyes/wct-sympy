"""Extended CLE and logarithmic-transform audits."""

from .full_checks_core import *  # noqa: F401,F403


def check_cle2_variation(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.FAIL,
        value="displayed local term only",
        expected="the full fourth-order Euler-Lagrange operator",
        reason="Since W_psi depends on second derivatives and on psi in the denominator, variation generates derivative and denominator terms omitted by CLE2.",
    )


def check_separation_substitution(spec: EquationSpec) -> AuditResult:
    major, minor, sigma0 = sp.symbols("major minor sigma0", positive=True)
    radial_ratio, angular_ratio = sp.symbols("radial_ratio angular_ratio")
    starting = -(radial_ratio / major**2 + angular_ratio / minor**2) - sigma0
    reduced = sp.expand(starting * major**2)
    expected = -radial_ratio - major**2 * angular_ratio / minor**2 - sigma0 * major**2
    return result(spec, AuditStatus.PASS if sp.simplify(reduced - expected) == 0 else AuditStatus.FAIL, value=reduced, expected=expected)


def check_periodic_ode_claim(spec: EquationSpec) -> AuditResult:
    theta = sp.symbols("theta", real=True)
    candidate = sp.cos(theta)
    ode_residual = sp.simplify(sp.diff(candidate, theta, 2) + candidate)
    periodic_residual = sp.simplify(candidate.subs(theta, theta + 2 * sp.pi) - candidate)
    return result(
        spec,
        AuditStatus.FAIL,
        value={"solution": candidate, "ode_residual": ode_residual, "periodic_residual": periodic_residual},
        expected="only a constant solution",
        reason="cos(theta) is a smooth nonconstant periodic solution when the coefficient equals one.",
    )


def check_torus_eigenmode_uniqueness(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.FAIL,
        value="exp(i*(m*theta+n*phi)) gives an integer-indexed family",
        expected="a unique mode",
        reason="The flat torus has infinitely many Fourier eigenmodes; uniqueness requires an additional lowest-mode, winding, symmetry, or energy condition.",
    )


def check_cle_units_chain(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.FAIL,
        value="W_psi has inverse-length-squared units while R=1/sigma_star assigns sigma_star inverse-length units",
        expected="one consistent convention for sigma_star",
        reason="CLE3/CLE4 and CLE9/CLE10 use sigma_star with incompatible dimensions. If sigma_star is inverse length, the eigenvalue equation requires sigma_star squared.",
    )


def check_log_modulation(spec: EquationSpec) -> AuditResult:
    energy, reference, amplitude, frequency, phase = sp.symbols("energy reference amplitude frequency phase", positive=True, real=True)
    expression = amplitude * sp.cos(frequency * sp.log(energy / reference) + phase)
    return result(
        spec,
        AuditStatus.PASS,
        value=expression,
        expected="a dimensionless logarithm and bounded modulation",
        assumptions=("energy>0", "reference>0", "energy/reference is dimensionless"),
    )


def check_log_laplacian_identity(spec: EquationSpec) -> AuditResult:
    x = sp.symbols("x", real=True)
    u = sp.Function("u")(x)
    psi = sp.exp(u)
    residual = sp.simplify(sp.diff(psi, x, 2) / psi - (sp.diff(u, x, 2) + sp.diff(u, x) ** 2))
    return result(spec, AuditStatus.PASS if residual == 0 else AuditStatus.FAIL, value=residual, expected=0)


def check_log_flow_reduction(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.PASS,
        value="u_t = Delta u + |grad u|^2",
        expected="the substitution psi=exp(u) into the diffusion equation",
        assumptions=("psi is positive or a consistent complex logarithm branch is fixed",),
    )


def check_cole_hopf(spec: EquationSpec) -> AuditResult:
    x, time = sp.symbols("x time", real=True)
    u = sp.Function("u")(x, time)
    psi = sp.exp(u)
    expression = sp.simplify(sp.diff(psi, time) - sp.diff(psi, x, 2))
    factored = sp.factor(expression / psi)
    expected = sp.diff(u, time) - sp.diff(u, x, 2) - sp.diff(u, x) ** 2
    return result(spec, AuditStatus.PASS if sp.simplify(factored - expected) == 0 else AuditStatus.FAIL, value=factored, expected=expected)
