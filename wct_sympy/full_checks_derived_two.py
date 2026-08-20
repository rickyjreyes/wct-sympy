"""Second explicit derivation batch for canonical WCT audit entries.

PASS results here are narrow implications under their returned assumptions; they
must not be read as proofs of stronger nonlinear PDE or empirical claims.
"""

from .full_checks_core import *  # noqa: F401,F403


def check_modal_growth_bound_derived(spec: EquationSpec) -> AuditResult:
    """Derive E15 exactly in the isolated real one-mode cubic reduction."""
    amplitude, growth = sp.symbols("A sigma", real=True)
    saturation = sp.symbols("beta", positive=True)

    # One-mode reduction of E13: A_dot = sigma*A - beta*A^3.
    amplitude_rate = growth * amplitude - saturation * amplitude**3
    power = amplitude**2
    power_rate = sp.simplify(sp.diff(power, amplitude) * amplitude_rate)
    quartic_coefficient = 2 * saturation
    target = 2 * growth * amplitude**2 - quartic_coefficient * amplitude**4
    residual = sp.simplify(power_rate - target)
    ok = residual == 0 and quartic_coefficient.is_positive is True

    return result(
        spec,
        AuditStatus.PASS if ok else AuditStatus.FAIL,
        value={
            "one_mode_flow": amplitude_rate,
            "power_rate": power_rate,
            "quartic_coefficient": quartic_coefficient,
        },
        expected="d|A_k|^2/dt = 2*sigma(k)|A_k|^2 - c|A_k|^4 with c=2*beta>0",
        residual=0.0 if ok else None,
        reason=(
            "For the isolated real one-mode cubic reduction of E13, differentiating "
            "A^2 gives the E15 modal power law exactly, with c=2*beta>0. "
            "The registered inequality therefore holds as equality in this reduction."
        ),
        assumptions=(
            "isolated real Fourier-mode reduction",
            "A_dot=sigma(k) A-beta A^3",
            "beta>0",
            "mode-coupling and phase-transfer terms are neglected",
        ),
    )


def check_flat_product_torus_laplacian_derived(spec: EquationSpec) -> AuditResult:
    """Derive CLE5 exactly on the flat product torus metric."""
    theta, phi = sp.symbols("theta phi", real=True)
    m, n = sp.symbols("m n", integer=True)
    major_radius, minor_radius = sp.symbols("R r", positive=True)

    mode = sp.exp(sp.I * (m * theta + n * phi))
    product_laplacian = (
        sp.diff(mode, theta, 2) / major_radius**2
        + sp.diff(mode, phi, 2) / minor_radius**2
    )
    eigenvalue = m**2 / major_radius**2 + n**2 / minor_radius**2
    target = -eigenvalue * mode
    residual = sp.simplify(product_laplacian - target)
    ok = residual == 0 and eigenvalue.is_nonnegative is True

    return result(
        spec,
        AuditStatus.PASS if ok else AuditStatus.FAIL,
        value={
            "mode": mode,
            "product_laplacian": product_laplacian,
            "eigenvalue": eigenvalue,
        },
        expected="Delta psi_mn = -(m^2/R^2+n^2/r^2) psi_mn",
        residual=0.0 if ok else None,
        reason=(
            "For the exact flat product metric ds^2=R^2 dtheta^2+r^2 dphi^2, "
            "the separated Fourier mode exp(i(m theta+n phi)) is an eigenmode "
            "of the product Laplacian with eigenvalue m^2/R^2+n^2/r^2."
        ),
        assumptions=(
            "flat product torus metric",
            "R>0 and r>0",
            "m,n are integers",
            "thin-torus geometric correction terms are neglected when this is used as an approximation",
        ),
    )


def check_torus_lowest_mode_selection_derived(spec: EquationSpec) -> AuditResult:
    """Close CLE8 once winding/chirality and the lowest-mode rule are explicit."""
    m = sp.symbols("m", integer=True)
    major_radius, minor_radius = sp.symbols("R r", positive=True)

    # Fixed chirality and winding n=+1.  The remaining integer label is m.
    eigenvalue_m = m**2 / major_radius**2 + 1 / minor_radius**2
    selected_eigenvalue = 1 / minor_radius**2
    spectral_gap = sp.simplify(eigenvalue_m - selected_eigenvalue)
    zero_gap_modes = sp.solve(sp.Eq(spectral_gap, 0), m)
    ok = (
        spectral_gap.is_nonnegative is True
        and zero_gap_modes == [0]
    )

    return result(
        spec,
        AuditStatus.PASS if ok else AuditStatus.FAIL,
        value={
            "lambda_m1": eigenvalue_m,
            "lambda_01": selected_eigenvalue,
            "spectral_gap": spectral_gap,
            "zero_gap_modes": zero_gap_modes,
        },
        expected="for fixed n=+1, lambda_(m,1)>=lambda_(0,1), equality iff m=0",
        reason=(
            "On the flat product torus, fixing winding and chirality to n=+1 "
            "leaves lambda_(m,1)=m^2/R^2+1/r^2. Its excess above the m=0 "
            "mode is m^2/R^2>=0, and for integer m equality occurs only at m=0. "
            "Normalization and global phase then select the canonical mode up to phase."
        ),
        assumptions=(
            "flat product torus spectrum from CLE5",
            "R>0 and r>0",
            "fixed winding and chirality n=+1",
            "select the lowest admissible eigenvalue",
            "fixed normalization and quotient by global phase",
        ),
    )


def check_topology_gradient_flow_descent_derived(spec: EquationSpec) -> AuditResult:
    """Derive TOP3 energy descent for an exact negative gradient flow."""
    gradient_components = sp.symbols("g0:4", real=True)
    gradient_norm_sq = sp.Add(*(component**2 for component in gradient_components))
    energy_rate = -gradient_norm_sq
    ok = gradient_norm_sq.is_nonnegative is True and energy_rate.is_nonpositive is True

    return result(
        spec,
        AuditStatus.PASS if ok else AuditStatus.FAIL,
        value={
            "gradient_norm_squared": gradient_norm_sq,
            "dE_dt": energy_rate,
        },
        expected="dE_loop/dt=-||delta E_loop/delta gamma||^2<=0",
        reason=(
            "The chain rule for an exact negative gradient flow gives the inner "
            "product of the gradient with its negative, hence minus the squared "
            "gradient norm. The finite-component symbolic calculation verifies "
            "the sign identity; the Hilbert-space statement uses the same identity."
        ),
        assumptions=(
            "E_loop is differentiable on the chosen configuration space",
            "gamma_t=-delta E_loop/delta gamma is the exact gradient flow",
            "the self-avoidance contribution is differentiable on the admissible class",
            "sufficient regularity/boundary conditions justify the chain rule",
        ),
    )
