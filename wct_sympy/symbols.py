"""Shared SymPy symbols and compact canonical expressions."""

from __future__ import annotations

import sympy as sp

s, x, t, k, n = sp.symbols("s x t k n", real=True)
a, b, r, beta, c0, mu = sp.symbols("a b r beta c0 mu", positive=True)
hbar, c, k_eff, mass = sp.symbols("hbar c k_eff mass", positive=True)
kappa, tau, sigma = sp.symbols("kappa tau sigma", real=True)
epsilon, alpha = sp.symbols("epsilon alpha", positive=True)
M, Delta = sp.symbols("M Delta", positive=True)
H, K = sp.symbols("H K", nonnegative=True)
R, Ls, V = sp.symbols("R L_s V", positive=True)
omega, lambda_j, Delta_star = sp.symbols(
    "omega lambda_j Delta_star", positive=True
)


def sigma_raw_expr() -> sp.Expr:
    return kappa**2 + tau**2


def sigma_expr() -> sp.Expr:
    return sp.sqrt(sigma_raw_expr())


def mass_expr() -> sp.Expr:
    return hbar * k_eff / c


def dispersion_expr() -> sp.Expr:
    return r + a * k**2 - b * k**4


def alpha_drop_expr(
    retention_ratios: list[sp.Expr],
    beta_term: sp.Expr = sp.Integer(0),
) -> sp.Expr:
    """Corrected alpha-drop exponent using retained fractions 0<rho<=1."""

    return 1 + sum(sp.log(rho, 2) for rho in retention_ratios) / n + beta_term
