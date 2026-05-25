"""Symbolic WCT equations expressed with sympy.

This module hosts the canonical sympy expressions used by the dimension
and numerical checks.
"""

from __future__ import annotations

import sympy as sp

# --- Symbols (positive where physically meaningful) ---
m = sp.Symbol("m", positive=True)
hbar = sp.Symbol("hbar", positive=True)
c = sp.Symbol("c", positive=True)
k_eff = sp.Symbol("k_eff", positive=True)
kappa = sp.Symbol("kappa", real=True)
tau = sp.Symbol("tau", real=True)

me = sp.Symbol("me", positive=True)
mmu = sp.Symbol("mmu", positive=True)
mtau = sp.Symbol("mtau", positive=True)


# --- Equations ---

def curvature_mass_expr():
    """m = hbar/c * k_eff -> right-hand side."""
    return hbar / c * k_eff


def koide_expr():
    """Koide ratio Q = (me+mmu+mtau)/(sqrt(me)+sqrt(mmu)+sqrt(mtau))^2."""
    return (me + mmu + mtau) / (sp.sqrt(me) + sp.sqrt(mmu) + sp.sqrt(mtau)) ** 2


def sigma_expr():
    """sigma = sqrt(kappa^2 + tau^2). Expected dimension: L^-1.

    Assumes kappa and tau both carry inverse-length dimension.
    """
    return sp.sqrt(kappa ** 2 + tau ** 2)


def sigma_raw_expr():
    """sigma_raw = kappa^2 + tau^2. Expected dimension: L^-2."""
    return kappa ** 2 + tau ** 2
