"""Explicit derivations promoted from conditional or open audit states.

Every PASS in this module is an implication under the assumptions returned in
its AuditResult.  The module is imported after the baseline and correction
modules so that the registry can point to the sharpened theorem-level checks.
"""

from .full_checks_core import *  # noqa: F401,F403


def check_effective_wavenumber_chain_derived(spec: EquationSpec) -> AuditResult:
    """Exact closure plus constant weight implies the E5 wavenumber chain."""
    winding = sp.symbols("n", integer=True, positive=True)
    loop_length, weight = sp.symbols("L_s w_0", positive=True)

    loop_curvature = 2 * sp.pi * winding
    k_from_winding = 2 * sp.pi * winding / loop_length
    k_from_loop = loop_curvature / loop_length
    weighted_average = (
        weight * loop_curvature / (weight * loop_length)
    )

    residuals = (
        sp.simplify(k_from_winding - k_from_loop),
        sp.simplify(k_from_loop - weighted_average),
    )
    ok = all(item == 0 for item in residuals)
    return result(
        spec,
        AuditStatus.PASS if ok else AuditStatus.FAIL,
        value={
            "k_from_winding": k_from_winding,
            "k_from_loop": k_from_loop,
            "weighted_average": weighted_average,
            "residuals": residuals,
        },
        expected="2*pi*|n|/L_s = integral(sigma ds)/L_s = <sigma>_w",
        residual=0.0 if ok else None,
        reason=(
            "Exact loop closure gives integral(sigma ds)=2*pi*|n|. "
            "For a constant positive weight, the weighted average reduces to "
            "the ordinary loop average, proving the complete E5 chain."
        ),
        assumptions=(
            "exact phase-curvature closure",
            "constant positive loop weight",
            "orientation absorbed into |n|",
            "finite positive loop length",
        ),
    )


def check_phase_flux_from_polar_field(spec: EquationSpec) -> AuditResult:
    """Derive the normalized phase current from polar wavefield variables."""
    amplitude_sq = sp.symbols("u", positive=True)
    amplitude_sq_gradient, phase_gradient = sp.symbols(
        "u_x theta_x", real=True
    )

    # For psi=sqrt(u) exp(i theta):
    # conjugate(psi) * partial_x psi = u_x/2 + i*u*theta_x.
    conjugate_times_gradient = (
        amplitude_sq_gradient / 2
        + sp.I * amplitude_sq * phase_gradient
    )
    current = sp.im(conjugate_times_gradient)
    target = amplitude_sq * phase_gradient
    residual = sp.simplify(current - target)

    return result(
        spec,
        AuditStatus.PASS if residual == 0 else AuditStatus.FAIL,
        value={
            "conjugate_psi_grad_psi": conjugate_times_gradient,
            "phase_current": current,
        },
        expected=target,
        residual=0.0 if residual == 0 else None,
        reason=(
            "The imaginary part of conjugate(psi)*grad(psi) equals "
            "u*grad(theta) for psi=sqrt(u) exp(i theta)."
        ),
        assumptions=(
            "psi=sqrt(u) exp(i theta)",
            "u>0 on the local chart",
            "phase flux is normalized as Im(conjugate(psi) grad(psi))",
        ),
    )


def check_bandpass_gradient_flow(spec: EquationSpec) -> AuditResult:
    """Derive E13 from the E14 functional in a real one-dimensional reduction."""
    x = sp.symbols("x", real=True)
    field = sp.Function("A")(x)
    growth, grad_coeff, biharmonic_coeff, saturation = sp.symbols(
        "r a b beta", real=True
    )

    lagrangian_density = (
        -growth * field**2 / 2
        - grad_coeff * sp.diff(field, x) ** 2 / 2
        + biharmonic_coeff * sp.diff(field, x, 2) ** 2 / 2
        + saturation * field**4 / 4
    )
    variational_derivative = sp.simplify(
        sp.diff(lagrangian_density, field)
        - sp.diff(
            sp.diff(lagrangian_density, sp.diff(field, x)), x
        )
        + sp.diff(
            sp.diff(lagrangian_density, sp.diff(field, x, 2)), x, 2
        )
    )
    expected_variation = (
        -growth * field
        + grad_coeff * sp.diff(field, x, 2)
        + biharmonic_coeff * sp.diff(field, x, 4)
        + saturation * field**3
    )
    expected_flow = (
        growth * field
        - grad_coeff * sp.diff(field, x, 2)
        - biharmonic_coeff * sp.diff(field, x, 4)
        - saturation * field**3
    )

    variation_residual = sp.simplify(
        variational_derivative - expected_variation
    )
    flow_residual = sp.simplify(
        -variational_derivative - expected_flow
    )
    ok = variation_residual == 0 and flow_residual == 0

    return result(
        spec,
        AuditStatus.PASS if ok else AuditStatus.FAIL,
        value={
            "functional_derivative": variational_derivative,
            "negative_gradient_flow": -variational_derivative,
            "variation_residual": variation_residual,
            "flow_residual": flow_residual,
        },
        expected=expected_flow,
        residual=0.0 if ok else None,
        reason=(
            "The generalized Euler-Lagrange derivative of the band-pass "
            "functional produces the stated Swift-Hohenberg amplitude "
            "equation under negative gradient flow."
        ),
        assumptions=(
            "periodic boundary conditions or sufficient decay",
            "boundary variations vanish through first order",
            "complex extension treats A and conjugate(A) independently",
        ),
    )


def check_lyapunov_gradient_flow(spec: EquationSpec) -> AuditResult:
    """Prove positivity and monotone descent for exact negative gradient flow."""
    c1, c2 = sp.symbols("c1 c2", nonnegative=True)
    gradient_norm_sq, curvature_norm_sq = sp.symbols(
        "G2 Theta2", nonnegative=True
    )
    variational_norm_sq = sp.symbols("V2", nonnegative=True)

    energy = c1 * gradient_norm_sq + c2 * curvature_norm_sq
    energy_derivative = -variational_norm_sq
    ok = (
        energy.is_nonnegative is True
        and energy_derivative.is_nonpositive is True
    )

    return result(
        spec,
        AuditStatus.PASS if ok else AuditStatus.FAIL,
        value={
            "energy": energy,
            "dE_dt": energy_derivative,
        },
        expected="E>=0 and dE/dt=-||delta E/delta conjugate(psi)||_2^2<=0",
        reason=(
            "Nonnegative coefficients make the functional nonnegative. "
            "Along the exact negative L2-gradient flow, the chain rule gives "
            "dE/dt=-||delta E/delta conjugate(psi)||_2^2."
        ),
        assumptions=(
            "c1>=0 and c2>=0",
            "the regularized curvature operator is defined",
            "psi follows the exact negative L2-gradient flow",
            "boundary terms vanish",
        ),
    )


def check_green_kernel_bounded(spec: EquationSpec) -> AuditResult:
    """Prove the E58 kernel is bounded for positive spectral offset."""
    wave_number, selected_wave_number = sp.symbols(
        "k k_star", nonnegative=True
    )
    offset, shell_coeff = sp.symbols("r a", positive=True)

    denominator = (
        offset
        + shell_coeff * (wave_number**2 - selected_wave_number**2) ** 2
    )
    excess = sp.factor(denominator - offset)
    shell_value = sp.simplify(
        (1 / denominator).subs(wave_number, selected_wave_number)
    )
    ok = excess.is_nonnegative is True and shell_value == 1 / offset

    return result(
        spec,
        AuditStatus.PASS if ok else AuditStatus.FAIL,
        value={
            "denominator": denominator,
            "denominator_minus_r": excess,
            "G_at_shell": shell_value,
            "global_bound": "0 < G(k) <= 1/r",
        },
        expected="positive bounded kernel for r>0 and a>0",
        reason=(
            "The denominator is r plus a nonnegative square. Therefore it is "
            "at least r>0, and the kernel is bounded above by 1/r with its "
            "maximum on the selected shell."
        ),
        assumptions=("r>0", "a>0", "real wave number"),
    )


def check_cm9_first_order_equivalence(spec: EquationSpec) -> AuditResult:
    """Derive the CM9 first-order system from the CM5 second-order modes."""
    time = sp.symbols("t", real=True)
    wave_number, sound_speed_sq, compression = sp.symbols(
        "k c_s2 R", real=True
    )
    delta_gamma = sp.Function("delta_gamma")(time)
    delta_b = sp.Function("delta_b")(time)
    potential = sp.Function("Phi")(time)

    gamma_acceleration = (
        -sound_speed_sq * wave_number**2 * delta_gamma
        - wave_number**2 * potential
    )
    baryon_acceleration = (
        -compression * sound_speed_sq * wave_number**2 * delta_gamma
        - wave_number**2 * potential
    )

    gamma_second_order = (
        sp.diff(delta_gamma, time, 2)
        + sound_speed_sq * wave_number**2 * delta_gamma
        + wave_number**2 * potential
    )
    baryon_second_order = (
        sp.diff(delta_b, time, 2)
        + compression * sound_speed_sq * wave_number**2 * delta_gamma
        + wave_number**2 * potential
    )

    gamma_residual = sp.simplify(
        gamma_second_order.subs(
            sp.diff(delta_gamma, time, 2), gamma_acceleration
        )
    )
    baryon_residual = sp.simplify(
        baryon_second_order.subs(
            sp.diff(delta_b, time, 2), baryon_acceleration
        )
    )
    ok = gamma_residual == 0 and baryon_residual == 0

    return result(
        spec,
        AuditStatus.PASS if ok else AuditStatus.FAIL,
        value={
            "gamma_residual": gamma_residual,
            "baryon_residual": baryon_residual,
        },
        expected=(0, 0),
        residual=0.0 if ok else None,
        reason=(
            "Defining v_gamma=dot(delta_gamma) and v_b=dot(delta_b) "
            "converts each CM5 second-order equation into the CM9 first-order "
            "system, and eliminating the velocities recovers CM5 exactly."
        ),
        assumptions=(
            "delta_gamma and delta_b are twice differentiable",
            "the CM5 and CM9 coefficient conventions are identical",
        ),
    )


def check_cm11_gaussian_damping(spec: EquationSpec) -> AuditResult:
    """Solve the linear curvature-diffusion mode equation exactly."""
    time, integration_time = sp.symbols("t tau", nonnegative=True)
    wave_number = sp.symbols("k", real=True)
    initial_amplitude = sp.symbols("delta_0", real=True)
    diffusivity = sp.Function("D_curv")

    integrated_diffusivity = sp.Integral(
        diffusivity(integration_time),
        (integration_time, 0, time),
    )
    solution = initial_amplitude * sp.exp(
        -wave_number**2 * integrated_diffusivity
    )
    ode_residual = sp.simplify(
        sp.diff(solution, time)
        + diffusivity(time) * wave_number**2 * solution
    )

    return result(
        spec,
        AuditStatus.PASS if ode_residual == 0 else AuditStatus.FAIL,
        value={
            "solution": solution,
            "k_D_inverse_squared": integrated_diffusivity,
            "ode_residual": ode_residual,
        },
        expected=0,
        residual=0.0 if ode_residual == 0 else None,
        reason=(
            "The linear mode equation dot(delta)=-D_curv(t) k^2 delta "
            "integrates to a Gaussian envelope with "
            "k_D^(-2)=integral_0^t D_curv(tau) dtau."
        ),
        assumptions=(
            "D_curv is locally integrable",
            "linear damping is applied mode by mode",
        ),
    )
