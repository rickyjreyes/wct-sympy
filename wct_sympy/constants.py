"""Physical constants used by WCT checks.

Values use CODATA 2018-style numbers as placeholders. Sources should be
verified against the latest CODATA release before publication.
"""

from __future__ import annotations

# --- Fundamental constants (SI) ---
# Source placeholder: CODATA 2018
HBAR = 1.054571817e-34       # J s         (M L^2 T^-1)
C = 2.99792458e8             # m/s         (L T^-1) - exact by definition
G = 6.67430e-11              # m^3 kg^-1 s^-2

# --- Charged lepton masses (MeV/c^2) ---
# Source placeholder: PDG 2022 central values
ME_MEV = 0.51099895000       # electron
MMU_MEV = 105.6583755        # muon
MTAU_MEV = 1776.86           # tau

# Convenience dictionary used by registry-driven checks.
CONSTANTS = {
    "hbar": HBAR,
    "c": C,
    "G": G,
    "me": ME_MEV,
    "mmu": MMU_MEV,
    "mtau": MTAU_MEV,
}
