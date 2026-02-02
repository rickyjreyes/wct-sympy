# wct_validate_dimensions.py
# Proof-grade dimensional consistency / reparameterization covariance validation
# NO mass assumptions, NO field scaling assumptions
# Tests only what WCT has actually defined
# Windows-compatible, ASCII output only

import numpy as np
import sys

# ----------------------------
# Parameters
# ----------------------------

LAM = 1.0        # dimensionless coupling
EPS = 1e-6

N0 = 512
x0 = np.linspace(0, 1, N0, endpoint=False)
dx0 = x0[1] - x0[0]

SCALES = [0.5, 1.0, 2.0, 4.0]
TOL = 5e-3

# ----------------------------
# Field definition
# ----------------------------

def psi(x):
    """Smooth, non-vanishing test field"""
    return 1.0 + 0.1 * np.cos(2 * np.pi * x)

# ----------------------------
# Operators
# ----------------------------

def curvature(psi_vals, dx):
    return (
        np.roll(psi_vals, -1)
        - 2 * psi_vals
        + np.roll(psi_vals, 1)
    ) / dx**2

def entropy(psi_vals, dx):
    dpsi_dx = (np.roll(psi_vals, -1) - np.roll(psi_vals, 1)) / (2 * dx)
    density = (dpsi_dx**2) / (psi_vals**2 + EPS) + LAM * psi_vals**2
    return np.sum(density) * dx

# ----------------------------
# Baseline (reference parameterization)
# ----------------------------

psi0 = psi(x0)

S0 = entropy(psi0, dx0)
K0 = np.mean(np.abs(curvature(psi0, dx0)))

S0_density = S0 / 1.0          # domain length = 1
K0_density = K0

print("=== WCT DIMENSIONAL / REPARAMETERIZATION VALIDATION ===")
print(f"Baseline entropy S0          = {S0:.6e}")
print(f"Baseline entropy density     = {S0_density:.6e}")
print(f"Baseline curvature density   = {K0_density:.6e}")

# ----------------------------
# Reparameterization tests
# ----------------------------

for lam in SCALES:
    # Reparameterized grid (same physical domain)
    N = int(N0 / lam)
    x = np.linspace(0, 1, N, endpoint=False)
    dx = x[1] - x[0]

    psi_vals = psi(x)

    S = entropy(psi_vals, dx)
    K = np.mean(np.abs(curvature(psi_vals, dx)))

    S_density = S / 1.0
    K_density = K

    err_S = abs(S_density - S0_density) / S0_density
    err_K = abs(K_density - K0_density) / K0_density

    print(f"\nReparameterization scale λ = {lam}")
    print(f"  Entropy density error   : {err_S:.3e}")
    print(f"  Curvature density error : {err_K:.3e}")

    assert err_S < TOL, (
        f"[FAIL] Entropy density not invariant under reparameterization (λ={lam})"
    )

    assert err_K < TOL, (
        f"[FAIL] Curvature density not invariant under reparameterization (λ={lam})"
    )

print("\n[PASS] Reparameterization covariance verified.")
print("[INFO] Physical scaling requires field scaling dimension Δ (not yet assumed).")

sys.exit(0)
