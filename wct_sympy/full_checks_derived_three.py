"""Third explicit derivation batch for canonical WCT audit entries.

The checks in this module close displayed implications under explicit uniform-
margin, denominator, or discrete-counting hypotheses, and record cross-equation
constraints where the full physical claim remains conditional.
"""

from .full_checks_core import *  # noqa: F401,F403


def check_subexponential_exploration_margin_derived(spec: EquationSpec) -> AuditResult:
    """Derive E32 from a uniform tail margin in the corrected alpha-drop law."""
    avg_log = sp.symbols("A", real=True)
    margin = sp.symbols("delta", positive=True)
    slack = sp.symbols("s", nonnegative=True)
    beta = -avg_log - margin - slack
    alpha = sp.simplify(1 + avg_log + beta)
    tail_upper = 1 - margin
    gap_to_upper = sp.simplify(tail_upper - alpha)
    ok = (
        sp.simplify(alpha - (1 - margin - slack)) == 0
        and gap_to_upper.is_nonnegative is True
        and sp.simplify(1 - tail_upper) == margin
        and margin.is_positive is True
    )
    return result(
        spec,
        AuditStatus.PASS if ok else AuditStatus.FAIL,
        value={"alpha_tail": alpha, "uniform_tail_upper": tail_upper, "gap_to_upper": gap_to_upper},
        expected="uniform delta>0 margin implies alpha(n)<=1-delta eventually, hence limsup alpha<1",
        residual=0.0 if ok else None,
        reason=(
            "Let A(n)=(1/n) sum_t log2 rho_t(n). If beta(n)<=-A(n)-delta uniformly "
            "on a tail for delta>0, then alpha(n)<=1-delta<1 on that tail, hence "
            "limsup alpha(n)<1."
        ),
        assumptions=(
            "alpha(n)=1+A(n)+beta(n) with A(n)=(1/n) sum_t log2 rho_t(n)",
            "there exist delta>0 and N such that beta(n)<=-A(n)-delta for all n>=N",
            "the retained-fraction logarithmic average A(n) is finite on that tail",
        ),
    )


def check_phase_coherence_lower_gradient_bound_derived(spec: EquationSpec) -> AuditResult:
    """Derive E50 finiteness from an L2 field and a positive phase-gradient floor."""
    density = sp.symbols("u", nonnegative=True)
    delta = sp.symbols("delta", positive=True)
    excess = sp.symbols("q", nonnegative=True)
    grad_mag = delta + excess
    integrand = sp.simplify(density / grad_mag)
    upper_integrand = sp.simplify(density / delta)
    gap = sp.factor(upper_integrand - integrand)
    ok = integrand.is_nonnegative is True and gap.is_nonnegative is True
    return result(
        spec,
        AuditStatus.PASS if ok else AuditStatus.FAIL,
        value={
            "gradient_magnitude": grad_mag,
            "coherence_integrand": integrand,
            "pointwise_upper_bound": upper_integrand,
            "upper_minus_integrand": gap,
        },
        expected="0<=C[psi]<=delta^(-1)||psi||_2^2<infinity when |grad theta|>=delta>0",
        residual=0.0 if ok else None,
        reason=(
            "Writing |grad theta|=delta+q with delta>0 and q>=0 gives "
            "0<=|psi|^2/|grad theta|<=|psi|^2/delta. For psi in L2, integration "
            "makes the phase-coherence functional finite."
        ),
        assumptions=(
            "psi is square-integrable on the integration region",
            "|grad theta|>=delta>0 almost everywhere on that region",
            "the phase-gradient magnitude is measurable",
        ),
    )


def check_alpha_drop_counting_bound_derived(spec: EquationSpec) -> AuditResult:
    """Derive E41/E72 from explicit count-retention fractions and a correction factor."""
    n = sp.symbols("n", positive=True, integer=True)
    beta = sp.symbols("beta", real=True)
    retention_slacks = sp.symbols("r0:3", nonnegative=True)
    retained = tuple(1 / (1 + s) for s in retention_slacks)
    retention_product = sp.prod(retained)
    log_retention_sum = sp.Add(*(sp.log(rho, 2) for rho in retained))
    alpha = 1 + log_retention_sum / n + beta
    iterative_upper = sp.exp(sp.log(2) * n * (1 + beta)) * retention_product
    alpha_upper = sp.exp(sp.log(2) * alpha * n)
    exponent_residual = sp.simplify(alpha_upper / iterative_upper - 1)
    count_slacks = sp.symbols("q0:5", nonnegative=True)
    realized_count = iterative_upper / sp.prod(1 + q for q in count_slacks)
    count_gap = sp.factor(iterative_upper - realized_count)
    ok = exponent_residual == 0 and count_gap.is_nonnegative is True
    return result(
        spec,
        AuditStatus.PASS if ok else AuditStatus.FAIL,
        value={
            "retained_fractions": retained,
            "retention_product": retention_product,
            "alpha": alpha,
            "iterated_count_upper": iterative_upper,
            "alpha_count_upper": alpha_upper,
            "upper_minus_realized": count_gap,
        },
        expected="count<=2^n prod_t rho_t 2^(beta n)=2^(alpha(n)n)",
        residual=0.0 if ok else None,
        reason=(
            "Actual discrete count-retention bounds iterate multiplicatively. With initial "
            "count at most 2^n and correction factor at most 2^(beta n), E28's alpha "
            "definition makes the resulting upper bound exactly 2^(alpha(n)n)."
        ),
        assumptions=(
            "the physical pruning state has a finite discrete encoding with initial count M_0<=2^n",
            "each declared rho_t(n) is an actual count-retention bound M_(t+1)<=rho_t M_t",
            "0<rho_t(n)<=1 for every pruning step",
            "the multiplicative correction/exploration factor is at most 2^(beta(n)n)",
            "alpha(n) uses the same rho_t(n) and beta(n) as E28",
        ),
    )


def check_gap_mass_consistency_constraint(spec: EquationSpec) -> AuditResult:
    """E19 remains conditional, but E6+E49 fix its coefficient if the sectors coincide."""
    hbar, c, sigma, coeff = sp.symbols("hbar c sigma C_gap", positive=True)
    delta_k = coeff * sigma**2
    delta_omega = c**2 * delta_k
    mass_sq_from_gap = sp.simplify(hbar**2 * delta_omega / c**4)
    mass_sq_from_e6 = sp.simplify((hbar * sigma / c) ** 2)
    ratio = sp.simplify(mass_sq_from_gap / mass_sq_from_e6)
    coefficient_solution = sp.solve(sp.Eq(mass_sq_from_gap, mass_sq_from_e6), coeff)
    ok = ratio == coeff and coefficient_solution == [1]
    return result(
        spec,
        AuditStatus.CONDITIONAL if ok else AuditStatus.FAIL,
        value={
            "delta_k": delta_k,
            "delta_omega": delta_omega,
            "mass_squared_from_gap": mass_sq_from_gap,
            "mass_squared_from_E6": mass_sq_from_e6,
            "mass_squared_ratio": ratio,
            "consistency_coefficient": coefficient_solution,
        },
        expected="E6/E49 consistency forces C_gap=1 if Delta_k=C_gap<sigma>^2 is the same mass-gap sector",
        residual=0.0 if ok else None,
        reason=(
            "Writing Delta_k*=C_gap<sigma>^2 and Delta_omega*=c^2 Delta_k*, E49 gives "
            "m_eff^2=C_gap(hbar<sigma>/c)^2. Exact identification with E6 therefore "
            "forces C_gap=1. The spectral statement Delta_k* proportional to <sigma>^2 "
            "still needs an independent operator/spectral derivation, so E19 remains conditional."
        ),
        assumptions=(
            "E19 and E49 refer to the same positive spectral-gap sector",
            "the E6 curvature scale and the E19 averaged curvature scale are identified",
            "hbar, c, and the relevant curvature scale are nonzero",
        ),
    )


def check_topology_curvature_energy_mass_constraint(spec: EquationSpec) -> AuditResult:
    """TOP7 diagnostic in the torsion-free constant-curvature planar reduction."""
    hbar, c, kappa = sp.symbols("hbar c kappa", positive=True)
    epsilon_kappa = kappa**2
    mass = hbar * kappa / c
    squared_ratio = sp.simplify(mass**2 / epsilon_kappa)
    linear_ratio = sp.simplify(mass / epsilon_kappa)
    linear_ratio_derivative = sp.simplify(sp.diff(linear_ratio, kappa))
    ok = squared_ratio == hbar**2 / c**2 and linear_ratio_derivative != 0
    return result(
        spec,
        AuditStatus.CONDITIONAL if ok else AuditStatus.FAIL,
        value={
            "epsilon_kappa": epsilon_kappa,
            "planar_mass": mass,
            "mass_squared_over_energy": squared_ratio,
            "mass_over_energy": linear_ratio,
            "d_mass_over_energy_d_kappa": linear_ratio_derivative,
        },
        expected="constant-curvature E6 reduction gives m^2 proportional to epsilon_kappa, not a universal m proportional to epsilon_kappa",
        residual=0.0 if ok else None,
        reason=(
            "For torsion-free constant curvature, E6 gives m=(hbar/c)kappa while the "
            "TOP7 curvature energy density is epsilon_kappa=kappa^2. Hence "
            "m^2=(hbar/c)^2 epsilon_kappa. The ratio m/epsilon_kappa varies as 1/kappa, "
            "so the proposed universal linear mass-energy proxy is not derived by E6 in "
            "this sector. TOP7 therefore remains conditional and requires a different "
            "fixed-class argument if its linear proportionality is to survive."
        ),
        assumptions=(
            "torsion vanishes",
            "curvature is positive and constant along the normalized loop",
            "TOP7's curvature-energy proxy is epsilon_kappa=(1/L) integral kappa^2 ds",
            "E6 supplies the mass identification in the same sector",
        ),
    )
