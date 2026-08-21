"""Paper-level symbolic checks for the August 2026 WCT closure revisions.

These checks verify exact algebraic identities used in the revised closure,
compact-dynamics, and WCT-DSI papers. They intentionally do not change the
142-object canonical registry on their own: a paper-level identity is promoted
to a canonical equation status only when the registry claim and scope match.
"""

from __future__ import annotations

import sympy as sp


def check_dsi_bijection() -> dict[str, object]:
    """Verify the positive-log-coordinate DSI/WCT round trip."""
    m, delta_log, n = sp.symbols("m Delta_log n", positive=True)
    ell = m * delta_log / n
    scale_ratio = sp.exp(ell)
    recovered_n = sp.simplify(m * delta_log / sp.log(scale_ratio))
    residual = sp.simplify(recovered_n - n)
    return {
        "passed": residual == 0,
        "ell": ell,
        "scale_ratio": scale_ratio,
        "recovered_n": recovered_n,
        "residual": residual,
    }


def check_compact_contraction_factor() -> dict[str, object]:
    """Verify convex mixing gives the paper's strict contraction factor."""
    mix, delta, epsilon = sp.symbols("L delta epsilon", real=True)
    base_factor = sp.expand((1 - mix) + mix * (1 - delta))
    perturbed_factor = sp.expand(base_factor + epsilon)
    base_residual = sp.simplify(base_factor - (1 - mix * delta))
    margin_residual = sp.simplify(
        (1 - perturbed_factor) - (mix * delta - epsilon)
    )
    return {
        "passed": base_residual == 0 and margin_residual == 0,
        "base_factor": base_factor,
        "perturbed_factor": perturbed_factor,
        "base_residual": base_residual,
        "margin_residual": margin_residual,
    }


def check_quartic_coercivity_completion() -> dict[str, object]:
    """Verify the square completion behind quadratic-to-quartic absorption."""
    eta, r = sp.symbols("eta r", positive=True)
    lhs = eta * r**4 - r**2 + sp.Rational(1, 4) / eta
    rhs = (2 * eta * r**2 - 1) ** 2 / (4 * eta)
    residual = sp.simplify(lhs - rhs)
    return {
        "passed": residual == 0,
        "lhs": lhs,
        "square_completion": rhs,
        "residual": residual,
    }


def check_fixed_mass_spatial_scaling() -> dict[str, object]:
    """Verify the R-exponents for the 3D mass-preserving dilation.

    For psi_R(x)=R^(-3/2) psi(x/R), this checks the volume/amplitude powers
    entering mass, gradient energy, biharmonic energy, and the quartic term.
    """
    radius = sp.symbols("R", positive=True)
    mass_factor = sp.simplify(radius**-3 * radius**3)
    gradient_factor = sp.simplify(radius**-5 * radius**3)
    laplacian_factor = sp.simplify(radius**-7 * radius**3)
    quartic_factor = sp.simplify(radius**-6 * radius**3)
    passed = (
        mass_factor == 1
        and gradient_factor == radius**-2
        and laplacian_factor == radius**-4
        and quartic_factor == radius**-3
    )
    return {
        "passed": passed,
        "mass": mass_factor,
        "gradient_sq": gradient_factor,
        "laplacian_sq": laplacian_factor,
        "quartic": quartic_factor,
    }


def check_beta0_amplitude_binding_identity() -> dict[str, object]:
    """Verify the exact quotient decrease under u -> sqrt(t) u.

    If q=|u|^2 and d=delta^2, then the quotient contribution to specific
    energy changes through

        1/(t q+d) - 1/(q+d)
          = -(t-1) q / ((t q+d)(q+d)).

    For t>1 and q>0 the right-hand side is strictly negative. This is the
    algebraic core used by the beta=0 energy-per-mass monotonicity argument.
    """
    t, q, d = sp.symbols("t q d", positive=True)
    lhs = 1 / (t * q + d) - 1 / (q + d)
    rhs = -(t - 1) * q / ((t * q + d) * (q + d))
    residual = sp.simplify(lhs - rhs)
    return {
        "passed": residual == 0,
        "difference": sp.factor(lhs),
        "negative_form": rhs,
        "residual": residual,
    }


def check_real_1d_quotient_first_variation() -> dict[str, object]:
    """Verify the generalized Euler-Lagrange derivative of the quotient term.

    This is a real one-dimensional analogue of
        integral |Delta u|^2/(u^2+delta^2) dx.
    It checks the exact second-derivative Euler-Lagrange structure, not the
    complete complex-field variational theorem.
    """
    x = sp.symbols("x", real=True)
    delta_sq = sp.symbols("delta_sq", positive=True)
    u = sp.Function("u")(x)
    u2 = sp.diff(u, x, 2)
    density = u2**2 / (u**2 + delta_sq)

    derived = sp.simplify(
        sp.diff(density, u)
        + sp.diff(sp.diff(density, u2), x, 2)
    )
    expected = (
        -2 * u * u2**2 / (u**2 + delta_sq) ** 2
        + sp.diff(2 * u2 / (u**2 + delta_sq), x, 2)
    )
    residual = sp.simplify(derived - expected)
    return {
        "passed": residual == 0,
        "derived": derived,
        "expected": expected,
        "residual": residual,
    }


def run_paper_closure_checks() -> dict[str, object]:
    """Run the complete paper-level closure batch."""
    checks = {
        "dsi_bijection": check_dsi_bijection(),
        "compact_contraction": check_compact_contraction_factor(),
        "quartic_coercivity": check_quartic_coercivity_completion(),
        "fixed_mass_scaling": check_fixed_mass_spatial_scaling(),
        "beta0_binding": check_beta0_amplitude_binding_identity(),
        "quotient_first_variation_1d": check_real_1d_quotient_first_variation(),
    }
    return {
        "passed": all(bool(item["passed"]) for item in checks.values()),
        "checks": checks,
    }
