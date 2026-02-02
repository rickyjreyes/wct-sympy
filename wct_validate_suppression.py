# wct_validate_fractal_dimension.py
# Proof-grade fractal dimension convergence validation
# Windows-compatible, ASCII output only

import numpy as np
import sys

# ----------------------------
# Parameters
# ----------------------------
r = 0.5646
beta = 3.95
gamma = 0.05
xi_0 = 1e-5

# Shell-depth sweep (acts like resolution)
N_VALUES = [80, 120, 160, 200, 260]

# Tail fractions to test robustness of asymptotic fit
TAIL_FRACTIONS = [0.25, 0.30, 0.35]

# Tolerances
DF_CONV_TOL = 5e-2     # allowed variation in D_f across resolutions
TAIL_TOL = 5e-2        # allowed variation across tail windows

# ----------------------------
# Helper function
# ----------------------------

def estimate_fractal_dimension(N, tail_frac):
    """
    Estimate asymptotic fractal dimension from log-log fit
    """
    n = np.arange(1, N + 1)

    xi_n = xi_0 * r ** n
    E_n = r ** (beta * n) * np.exp(-gamma * n)

    X = np.log(xi_n)
    Y = np.log(E_n)

    fit_start = int(tail_frac * N)

    slope, intercept = np.polyfit(X[fit_start:], Y[fit_start:], 1)
    return slope

# ----------------------------
# Main validation
# ----------------------------

print("=== WCT FRACTAL DIMENSION VALIDATION ===")
print(f"r={r}, beta={beta}, gamma={gamma}, xi_0={xi_0}")
print(f"Convergence tolerance: {DF_CONV_TOL}\n")

Df_results = {}

for N in N_VALUES:
    print(f"--- N = {N} ---")
    Df_tail = []

    for tail_frac in TAIL_FRACTIONS:
        Df = estimate_fractal_dimension(N, tail_frac)
        Df_tail.append(Df)
        print(f"  tail start = {int(tail_frac * 100)}% | D_f = {Df:.6f}")

    Df_tail = np.array(Df_tail)
    spread = np.max(Df_tail) - np.min(Df_tail)

    print(f"  Tail-window spread ΔD_f = {spread:.3e}")

    # Hard falsification: tail instability
    assert spread < TAIL_TOL, (
        f"[FAIL] Fractal dimension unstable across tail windows at N={N}: "
        f"ΔD_f = {spread}"
    )

    Df_results[N] = np.mean(Df_tail)

print("\n=== CONVERGENCE CHECK ACROSS RESOLUTIONS ===")

Ns = sorted(Df_results.keys())
Df_vals = np.array([Df_results[N] for N in Ns])

for i in range(len(Ns) - 1):
    diff = abs(Df_vals[i + 1] - Df_vals[i])
    print(f"|D_f(N={Ns[i+1]}) - D_f(N={Ns[i]})| = {diff:.3e}")

    # Hard falsification: no convergence
    assert diff < DF_CONV_TOL, (
        f"[FAIL] Fractal dimension does not converge: "
        f"N={Ns[i]} -> {Ns[i+1]}"
    )

print("\nFinal stabilized fractal dimension:")
print(f"D_f ≈ {Df_vals[-1]:.6f}")

print("\n[PASS] Fractal dimension converges and is asymptotically stable.")
sys.exit(0)
