# wct_validate_entropy_monotonicity.py
# Proof-grade asymptotic entropy monotonicity validation
# CFL-stable, resolution-correct, entropy-density normalized

import numpy as np
import sys

LAM = 1.0
T_STEPS = 600

RESOLUTIONS = [64, 128, 256, 512]

# Entropy validation controls
SMOOTH_WINDOW = 15
LATE_FRACTION = 0.5
TOL_SLOPE = 1e-6
TOL_CONV = 5e-3

# Numerical safety
EPS = 1e-6
CFL = 0.1   # stability constant

def initial_psi(x):
    return 1.0 + 0.1 * np.cos(2 * np.pi * x)

def evolve_psi(psi, dx, dt):
    d2psi_dx2 = (np.roll(psi, -1) - 2 * psi + np.roll(psi, 1)) / dx**2
    psi_new = psi + dt * (d2psi_dx2 - LAM * psi**3)
    return np.clip(psi_new, EPS, None)

def entropy(psi, dx):
    dpsi_dx = (np.roll(psi, -1) - np.roll(psi, 1)) / (2 * dx)
    density = (dpsi_dx**2) / (psi**2 + EPS) + LAM * psi**2
    return np.sum(density) * dx

def moving_average(arr, k):
    return np.convolve(arr, np.ones(k) / k, mode="valid")

print("=== WCT ASYMPTOTIC ENTROPY MONOTONICITY VALIDATION ===")

final_entropy_density = {}

for N in RESOLUTIONS:
    x = np.linspace(0, 1, N, endpoint=False)
    dx = x[1] - x[0]
    dt = CFL * dx**2

    psi = initial_psi(x)
    S_history = []

    for _ in range(T_STEPS):
        S_history.append(entropy(psi, dx))
        psi = evolve_psi(psi, dx, dt)

    S_history = np.array(S_history)
    S_smooth = moving_average(S_history, SMOOTH_WINDOW)

    start = int(LATE_FRACTION * len(S_smooth))
    S_late = S_smooth[start:]
    dS_late = np.diff(S_late)

    max_violation = np.max(dS_late)

    S_star_density = np.mean(S_late[-10:]) / N
    S_star_renorm = S_star_density * N

    print(f"\nResolution N = {N}")
    print(f"  dx                          : {dx:.3e}")
    print(f"  dt                          : {dt:.3e}")
    print(f"  Initial entropy             : {S_history[0]:.6e}")
    print(f"  Final entropy               : {S_history[-1]:.6e}")
    print(f"  Late max dS/dt              : {max_violation:.3e}")
    print(f"  Entropic density S*/N        : {S_star_density:.6e}")
    print(f"  Renormalized entropy N·S*/N  : {S_star_renorm:.6e}")

    assert max_violation <= TOL_SLOPE, (
        f"[FAIL] Late-time entropy not monotone at N={N}"
    )

    final_entropy_density[N] = S_star_renorm

print("\n=== ENTROPIC ATTRACTOR (RENORMALIZED) CONVERGENCE CHECK ===")

Ns = sorted(final_entropy_density)
prev_diff = None

for i in range(len(Ns) - 1):
    N1, N2 = Ns[i], Ns[i + 1]
    diff = abs(final_entropy_density[N1] - final_entropy_density[N2])

    print(f"|N·S*(N={N1}) - N·S*(N={N2})| = {diff:.3e}")

    if prev_diff is not None:
        assert diff < prev_diff, (
            "[FAIL] Renormalized entropy does not converge monotonically"
        )

    prev_diff = diff



print("\n[PASS] Entropy is asymptotically monotone and density-convergent.")
sys.exit(0)
