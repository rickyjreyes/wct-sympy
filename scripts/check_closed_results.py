#!/usr/bin/env python3
"""Executable symbolic checks for narrow WCT closure results.

These checks verify algebraic implications only. They do not establish
existence or stability of a solution of the full nonlinear WCT PDE, nor do
they validate physical mass, gauge, gravity, cosmology, or empirical claims.
"""

from __future__ import annotations

import json
import sympy as sp


def run_checks() -> dict[str, bool]:
    hbar, c, k_geom, correction = sp.symbols(
        "hbar c k_geom correction", nonzero=True, real=True
    )
    winding = sp.symbols("n", integer=True)
    sigma_int = sp.symbols("Sigma", real=True)
    k = sp.symbols("k", nonzero=True, real=True)
    dmunu, dnumu, q = sp.symbols("dmunu dnumu q", nonzero=True, real=True)

    mass_identity = sp.simplify(
        (hbar / c) * (k_geom + correction)
        - ((hbar / c) * k_geom + (hbar / c) * correction)
    ) == 0

    exact_lock_forward = sp.simplify(
        (2 * sp.pi * winding - sigma_int).subs(
            sigma_int, 2 * sp.pi * winding
        )
    ) == 0

    pure_gauge = sp.simplify(
        ((dmunu - dnumu) / q).subs(dmunu, dnumu)
    ) == 0

    scale_ratio = sp.exp(2 * sp.pi / k)
    log_scale_identity = sp.simplify(sp.log(scale_ratio) - 2 * sp.pi / k) == 0

    mu, b, x, kstar = sp.symbols("mu b x kstar", real=True, positive=True)
    growth = mu - b * (x**2 - kstar**2) ** 2
    shell_stationary = sp.simplify(sp.diff(growth, x).subs(x, kstar)) == 0
    shell_curvature = sp.simplify(sp.diff(growth, x, 2).subs(x, kstar))
    shell_is_maximum = shell_curvature == -8 * b * kstar**2

    return {
        "conditional_mass_distributivity": bool(mass_identity),
        "exact_lock_zero_mismatch": bool(exact_lock_forward),
        "single_smooth_phase_is_pure_gauge": bool(pure_gauge),
        "dsi_log_frequency_identity": bool(log_scale_identity),
        "finite_k_shell_is_stationary": bool(shell_stationary),
        "finite_k_shell_has_negative_curvature": bool(shell_is_maximum),
    }


def main() -> int:
    results = run_checks()
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
