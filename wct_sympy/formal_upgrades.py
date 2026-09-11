"""Exact symbolic certificates for high-value WCT derivations.

These checks are intentionally narrower than the associated physical claims.
They certify algebraic identities and threshold reductions that can be tested
without assuming PDE existence, spectral completeness, or empirical validity.
"""

from __future__ import annotations

import sympy as sp


def check_torus_shape_selector() -> dict[str, object]:
    """Certify the algebra behind the toroidal Willmore selector.

    For x = eta**2,

        1/4 - x(1-x) = (x-1/2)**2 >= 0.

    Hence eta**2(1-eta**2) is globally bounded by 1/4, with equality only
    at eta**2=1/2.  On 0<eta<1 this is the exact algebraic selector behind
    the minimum of pi**2/(eta*sqrt(1-eta**2)).
    """
    eta = sp.symbols("eta", real=True)
    shape_sq = eta**2 * (1 - eta**2)
    square_certificate = (eta**2 - sp.Rational(1, 2)) ** 2
    residual = sp.factor(sp.Rational(1, 4) - shape_sq - square_certificate)
    equality_roots = sp.solve(
        sp.Eq(shape_sq, sp.Rational(1, 4)), eta,
        domain=sp.S.Reals,
    )
    expected_roots = [-sp.sqrt(2) / 2, sp.sqrt(2) / 2]
    roots_ok = set(equality_roots) == set(expected_roots)
    return {
        "passed": residual == 0 and roots_ok,
        "shape_sq": shape_sq,
        "square_certificate": square_certificate,
        "residual": residual,
        "equality_roots": equality_roots,
        "physical_branch_eta": sp.sqrt(2) / 2,
    }


def check_hessian_finite_band_maximum() -> dict[str, object]:
    """Complete the square for the finite-band Hessian growth law.

    The generic form R*k**2 - q*k**4 with q>0 has the exact decomposition

        R**2/(4*q) - q*(k**2 - R/(2*q))**2.

    Therefore the maximum is R**2/(4*q), attained when k**2=R/(2*q).
    Setting q=d**(-2) recovers k_star**2=R*d**2/2 and
    lambda_max=R**2*d**2/4.
    """
    R, q, k, d = sp.symbols("R q k d", positive=True)
    growth = R * k**2 - q * k**4
    completed = R**2 / (4 * q) - q * (k**2 - R / (2 * q)) ** 2
    residual = sp.factor(growth - completed)
    kstar_sq = sp.simplify((R / (2 * q)).subs(q, d**-2))
    lambda_max = sp.simplify((R**2 / (4 * q)).subs(q, d**-2))
    return {
        "passed": (
            residual == 0
            and sp.simplify(kstar_sq - R * d**2 / 2) == 0
            and sp.simplify(lambda_max - R**2 * d**2 / 4) == 0
        ),
        "growth": growth,
        "completed_square": completed,
        "residual": residual,
        "kstar_sq": kstar_sq,
        "lambda_max": lambda_max,
    }


def check_helix_curvature_scale() -> dict[str, object]:
    """Verify the exact squared curvature-torsion scale for a helix."""
    R, pitch = sp.symbols("R p", real=True)
    denominator = R**2 + pitch**2
    kappa = R / denominator
    tau = pitch / denominator
    sigma_sq = sp.factor(kappa**2 + tau**2)
    residual = sp.cancel(sigma_sq - 1 / denominator)

    n, r, eta = sp.symbols("n r eta", real=True)
    winding_substitution = sp.simplify(
        (1 / (R**2 + pitch**2)).subs(pitch, n * r).subs(r, eta * R)
    )
    expected_aspect = 1 / (R**2 * (1 + n**2 * eta**2))
    aspect_residual = sp.cancel(winding_substitution - expected_aspect)
    return {
        "passed": residual == 0 and aspect_residual == 0,
        "kappa": kappa,
        "tau": tau,
        "sigma_sq": sigma_sq,
        "aspect_sigma_sq": winding_substitution,
        "residual": residual,
        "aspect_residual": aspect_residual,
        "assumptions": "R^2+p^2 != 0; for sigma use the positive square root",
    }


def check_core_integrability_threshold() -> dict[str, object]:
    """Verify the p>1/2 threshold for the radial core integral."""
    p = sp.symbols("p", real=True)
    exponent = 2 * p - 2
    threshold_residual = sp.simplify((exponent + 1) / 2 - (p - sp.Rational(1, 2)))
    solution = sp.solve_univariate_inequality(exponent > -1, p, relational=False)
    expected = sp.Interval.open(sp.Rational(1, 2), sp.oo)
    return {
        "passed": threshold_residual == 0 and solution == expected,
        "radial_exponent": exponent,
        "convergence_condition": exponent > -1,
        "solution": solution,
        "threshold_residual": threshold_residual,
    }


def check_curvature_lock_stationarity() -> dict[str, object]:
    """Verify the exact constrained pointwise locking relation.

    For density w*(phi_prime-sigma)^2 + lambda*phi_prime, stationarity in
    phi_prime gives

        phi_prime = sigma - lambda/(2*w).

    Exact phi_prime=sigma therefore requires zero multiplier (or the global
    compatibility condition that makes the multiplier vanish).
    """
    w = sp.symbols("w", nonzero=True, real=True)
    phase_prime, sigma, multiplier = sp.symbols(
        "phi_prime sigma lambda", real=True
    )
    density = w * (phase_prime - sigma) ** 2 + multiplier * phase_prime
    stationarity = sp.diff(density, phase_prime)
    solution = sp.solve(sp.Eq(stationarity, 0), phase_prime)
    expected = sigma - multiplier / (2 * w)
    residual = sp.simplify(solution[0] - expected) if len(solution) == 1 else sp.nan
    exact_lock_residual = sp.simplify(expected.subs(multiplier, 0) - sigma)
    return {
        "passed": residual == 0 and exact_lock_residual == 0,
        "stationarity": stationarity,
        "solution": solution,
        "expected": expected,
        "residual": residual,
        "exact_lock_residual": exact_lock_residual,
    }


def run_formal_upgrades() -> dict[str, object]:
    """Run the complete September 2026 formal-upgrade batch."""
    checks = {
        "torus_shape_selector": check_torus_shape_selector(),
        "hessian_finite_band_maximum": check_hessian_finite_band_maximum(),
        "helix_curvature_scale": check_helix_curvature_scale(),
        "core_integrability_threshold": check_core_integrability_threshold(),
        "curvature_lock_stationarity": check_curvature_lock_stationarity(),
    }
    return {
        "passed": all(bool(item["passed"]) for item in checks.values()),
        "checks": checks,
    }
