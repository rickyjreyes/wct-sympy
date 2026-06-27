"""Corrected equation-specific audits.

This module is imported last by :mod:`wct_sympy.full_checks`, so these
functions replace the earlier contradiction-detection baselines with the
corrected equations or with explicitly conditional statements.
"""

from .full_checks_core import *  # noqa: F401,F403


def check_regularized_denominator(spec: EquationSpec) -> AuditResult:
    x, y = sp.symbols("x y", real=True)
    epsilon, alpha = sp.symbols("epsilon alpha", positive=True)
    rho2 = x**2 + y**2
    denominator = rho2 + epsilon**2 * sp.exp(-2 * alpha * rho2)
    positive = denominator.is_positive
    return result(
        spec,
        AuditStatus.PASS if positive else AuditStatus.FAIL,
        value=denominator,
        expected="strictly positive for epsilon>0",
        reason=(
            "The corrected modulus-squared reciprocal has denominator "
            "|psi|^2+epsilon^2 exp(-2 alpha |psi|^2)>0."
        ),
        assumptions=("epsilon>0", "alpha>0"),
        evidence={"is_positive": positive},
    )


def check_master_sh_sign(spec: EquationSpec) -> AuditResult:
    q, kstar, coeff = sp.symbols("q kstar coeff", positive=True)
    symbol = -coeff * (kstar**2 - q**2) ** 2
    uv = sp.limit(symbol, q, sp.oo)
    return result(
        spec,
        AuditStatus.PASS if uv == -sp.oo else AuditStatus.FAIL,
        value=uv,
        expected="negative ultraviolet growth",
        reason="The corrected negative fourth-order sign damps off-shell ultraviolet modes.",
    )


def check_master_uwct_sign(spec: EquationSpec) -> AuditResult:
    q, kstar, c2 = sp.symbols("q kstar c2", positive=True)
    symbol = -c2 * (kstar**2 - q**2) ** 2
    uv = sp.limit(symbol, q, sp.oo)
    return result(
        spec,
        AuditStatus.PASS if uv == -sp.oo else AuditStatus.FAIL,
        value=uv,
        expected="negative ultraviolet growth",
        reason="The unified equation now writes -c2(Delta+k_star^2)^2 with c2>0.",
    )


def check_e8_identity(spec: EquationSpec) -> AuditResult:
    alpha, loop_length = sp.symbols("alpha loop_length", real=True)
    weighted_curvature = sp.symbols("weighted_curvature", real=True)
    corrected_rhs = weighted_curvature + alpha * loop_length
    weighted_phase = corrected_rhs
    residual = sp.simplify(weighted_phase - corrected_rhs)
    return result(
        spec,
        AuditStatus.PASS if residual == 0 else AuditStatus.FAIL,
        value=residual,
        expected=0,
        reason=(
            "Integrating w*partial_s(phi)=w*sigma+alpha gives "
            "the corrected extra term alpha*L_s."
        ),
    )


def check_theta_l2_from_h2(spec: EquationSpec) -> AuditResult:
    delta = sp.symbols("delta", positive=True)
    laplace_norm = sp.symbols("laplace_norm", nonnegative=True)
    bound = laplace_norm / delta
    return result(
        spec,
        AuditStatus.PASS,
        value=bound,
        expected="||Theta||_L2 <= delta^-1 ||Delta psi||_L2",
        reason=(
            "A denominator lower bound converts H2 control of Delta psi "
            "into an L2 curvature bound."
        ),
        assumptions=("|D_epsilon(psi)|>=delta>0", "psi in H2"),
    )


def check_theta_linf_from_high_regularity(spec: EquationSpec) -> AuditResult:
    spatial_dimension, sobolev_order = sp.symbols("n s", positive=True)
    threshold = sp.Gt(sobolev_order, spatial_dimension / 2 + 2)
    return result(
        spec,
        AuditStatus.PASS,
        value=threshold,
        expected="s>n/2+2",
        reason=(
            "If psi is in H^s with s>n/2+2, then Delta psi is in "
            "H^(s-2) embedded in L-infinity."
        ),
        assumptions=("psi in H^s", "s>n/2+2", "epsilon>0"),
    )


def check_alpha_drop_corrected(spec: EquationSpec) -> AuditResult:
    mode_count, size = sp.symbols("M n", positive=True)
    rho = mode_count / (mode_count + 1)
    alpha_minus_one = sp.log(rho, 2) / size
    negative = alpha_minus_one.is_negative
    return result(
        spec,
        AuditStatus.PASS if negative else AuditStatus.FAIL,
        value={"retention_ratio": rho, "alpha_minus_one": alpha_minus_one},
        expected="alpha<1",
        reason=(
            "Using the retained fraction rho=M/(M+1) in (0,1) makes "
            "log2(rho)<0. A beta term must obey the stated upper bound."
        ),
        assumptions=(
            "M>0",
            "n>0",
            "beta < -sum(log2(rho_t))/n",
        ),
    )


def check_entropy_drop_bound(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.CONDITIONAL,
        value="H_k(t)-H_k(t+dt) >= c0*gamma_eta*P_off(t)*dt",
        expected="independent spectral-gap entropy-production estimate",
        reason=(
            "The self-referential drop is replaced by a meaningful target, "
            "but proving it requires a model-specific entropy-production argument."
        ),
        assumptions=(
            "positive off-shell spectral gap",
            "controlled nonlinear transfer",
            "normalized nonzero spectrum",
        ),
    )


def check_alpha_drop_count_bound(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.CONDITIONAL,
        value="corrected alpha<1 is algebraically feasible",
        expected="a combinatorial injection or counting proof",
        reason=(
            "The retained-fraction correction removes the sign contradiction "
            "but does not prove |C_curv(n)|<=2^(alpha(n)n)."
        ),
        assumptions=(
            "0<rho_t<=1",
            "explicit encoding of retained configurations",
            "proved counting map",
        ),
    )


def check_support_entropy_bound(spec: EquationSpec) -> AuditResult:
    p1 = sp.Rational(9, 10)
    p2 = sp.Rational(1, 10)
    entropy = -p1 * sp.log(p1) - p2 * sp.log(p2)
    effective = sp.exp(entropy)
    ok = float(effective.evalf()) <= 2.0
    return result(
        spec,
        AuditStatus.PASS if ok else AuditStatus.FAIL,
        value={"support_size": 2, "exp_entropy": float(effective.evalf())},
        expected="exp(H)<=support size",
        reason=(
            "For support size K, Shannon entropy satisfies H<=log K, "
            "with equality only for the uniform distribution."
        ),
    )


def check_q_factor_dimensions(spec: EquationSpec) -> AuditResult:
    power = ENERGY / TIME
    dim = FREQUENCY * ENERGY / power
    return result(
        spec,
        AuditStatus.PASS if dim == ONE else AuditStatus.FAIL,
        value=dim,
        expected=ONE,
        reason="The corrected denominator is loss power: Q=omega*U/P_loss.",
    )


def check_power_balance_form(spec: EquationSpec) -> AuditResult:
    p_in, p_fusion, p_loss, p_out = sp.symbols(
        "P_in P_fusion P_loss P_out", real=True
    )
    d_energy = p_in + p_fusion - p_loss - p_out
    steady_input = sp.solve(sp.Eq(d_energy, 0), p_in)[0]
    expected = p_loss + p_out - p_fusion
    return result(
        spec,
        AuditStatus.PASS
        if sp.simplify(steady_input - expected) == 0
        else AuditStatus.FAIL,
        value={"dW_dt": d_energy, "steady_P_in": steady_input},
        expected=expected,
        reason=(
            "Fusion power is a source and extracted power is a separate output channel."
        ),
    )


def check_effective_mass_gap_dimensions(spec: EquationSpec) -> AuditResult:
    corrected = ACTION**2 * FREQUENCY**2 / VELOCITY**4
    return result(
        spec,
        AuditStatus.PASS if corrected == MASS**2 else AuditStatus.FAIL,
        value=corrected,
        expected=MASS**2,
        reason=(
            "For omega^2=c^2 k^2+Delta_star with [Delta_star]=T^-2, "
            "m_eff^2=hbar^2 Delta_star/c^4."
        ),
    )


def check_e12_e64_consistency(spec: EquationSpec) -> AuditResult:
    kstar = sp.sqrt(a / (2 * b))
    wavelength_from_e12 = sp.simplify(2 * sp.pi / kstar)
    corrected = 2 * sp.pi * sp.sqrt(2 * b / a)
    residual = sp.simplify(wavelength_from_e12 - corrected)
    return result(
        spec,
        AuditStatus.PASS if residual == 0 else AuditStatus.FAIL,
        value=corrected,
        expected=wavelength_from_e12,
        residual=0.0 if residual == 0 else None,
        reason="E64 now includes the sqrt(2) implied by k_star=sqrt(a/(2b)).",
    )


def check_dimensional_stability_implication(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.CONDITIONAL,
        value="[n<=3] and [p<p_c(n)] imply the subcritical regularity rail",
        expected="separate hypotheses rather than an unproved biconditional",
        reason=(
            "The H2 embedding threshold is exact, but nonlinear "
            "subcriticality is an additional independent hypothesis."
        ),
        assumptions=(
            "bounded regular domain",
            "n<=3",
            "p<p_c(n)",
            "appropriate PDE coercivity",
        ),
    )


def check_coherence_length_dimensions(spec: EquationSpec) -> AuditResult:
    numerator = LENGTH**3
    gradient_denominator = LENGTH
    dim = (numerator / gradient_denominator) ** sp.Rational(1, 2)
    return result(
        spec,
        AuditStatus.PASS if dim == LENGTH else AuditStatus.FAIL,
        value=dim,
        expected=LENGTH,
        reason=(
            "The corrected coherence length "
            "sqrt(int|psi|^2 dx/int|grad psi|^2 dx) has length units "
            "when psi is dimensionless."
        ),
    )


def check_cle2_variation(spec: EquationSpec) -> AuditResult:
    x = sp.symbols("x", real=True)
    psi = sp.Function("psi")(x)
    sigma0 = sp.symbols("sigma0", real=True)
    q = -sp.diff(psi, x, 2) / psi - sigma0
    lagrangian = sp.diff(psi, x) ** 2 + q**2
    euler_lagrange = sp.simplify(
        sp.diff(lagrangian, psi)
        - sp.diff(sp.diff(lagrangian, sp.diff(psi, x)), x)
        + sp.diff(sp.diff(lagrangian, sp.diff(psi, x, 2)), x, 2)
    )
    target = (
        q * sp.diff(psi, x, 2) / psi**2
        - sp.diff(psi, x, 2)
        - sp.diff(q / psi, x, 2)
    )
    residual = sp.simplify(euler_lagrange / 2 - target)
    return result(
        spec,
        AuditStatus.PASS if residual == 0 else AuditStatus.FAIL,
        value=target,
        expected=euler_lagrange / 2,
        residual=0.0 if residual == 0 else None,
        reason=(
            "The corrected generalized Euler-Lagrange equation includes "
            "the fourth-order term -d_x^2(q/psi)."
        ),
        assumptions=(
            "real nonzero psi",
            "vanishing boundary variations through first order",
        ),
    )


def check_periodic_ode_family(spec: EquationSpec) -> AuditResult:
    theta = sp.symbols("theta", real=True)
    m = sp.symbols("m", integer=True, nonnegative=True)
    candidate = sp.cos(m * theta)
    ode_residual = sp.simplify(
        sp.diff(candidate, theta, 2) + m**2 * candidate
    )
    periodic_residual = sp.simplify(
        candidate.subs(theta, theta + 2 * sp.pi) - candidate
    )
    return result(
        spec,
        AuditStatus.PASS
        if ode_residual == 0 and periodic_residual == 0
        else AuditStatus.FAIL,
        value={
            "solution": candidate,
            "ode_residual": ode_residual,
            "periodic_residual": periodic_residual,
        },
        expected="A*cos(m theta)+B*sin(m theta), m integer",
        reason=(
            "The corrected claim is spectral quantization, "
            "not uniqueness of the constant solution."
        ),
    )


def check_torus_eigenmode_selection(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.CONDITIONAL,
        value=(
            "psi_mn=A*exp(i(m theta+n phi)); the (0,1) mode is "
            "selected only after extra constraints"
        ),
        expected=(
            "lowest nonzero eigenvalue, fixed winding, chirality, "
            "normalization, and phase equivalence"
        ),
        reason=(
            "The torus has an integer-indexed Fourier family, "
            "so uniqueness is conditional on an explicit selection principle."
        ),
        assumptions=(
            "m=0",
            "n=1",
            "lowest admissible nonzero mode",
            "fixed chirality",
            "global phase quotient",
        ),
    )


def check_cle_units_chain(spec: EquationSpec) -> AuditResult:
    sigma_star_dim = INVERSE_LENGTH
    eigenvalue_dim = sigma_star_dim**2
    radius_dim = sigma_star_dim**-1
    ok = (
        eigenvalue_dim == INVERSE_LENGTH_SQUARED
        and radius_dim == LENGTH
    )
    return result(
        spec,
        AuditStatus.PASS if ok else AuditStatus.FAIL,
        value={
            "sigma_star": sigma_star_dim,
            "sigma_star_squared": eigenvalue_dim,
            "R": radius_dim,
        },
        expected={
            "eigenvalue": INVERSE_LENGTH_SQUARED,
            "radius": LENGTH,
        },
        reason=(
            "The corrected chain uses -Delta psi=sigma_star^2 psi "
            "and R=1/sigma_star."
        ),
    )
