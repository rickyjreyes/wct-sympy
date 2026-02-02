# wct_validate_metric.py
# Proof-grade effective metric validation
# Windows-compatible, ASCII output only

import sympy as sp
import numpy as np
import sys

# ----------------------------
# Symbolic setup
# ----------------------------

t, x, y, z = sp.symbols('t x y z')
coords = [t, x, y, z]

psi = sp.Function('psi')(*coords)
kappa = sp.Symbol('kappa', positive=True)

# Minkowski background metric (-+++)
eta = sp.diag(-1, 1, 1, 1)

# Effective metric construction
g_eff = sp.MutableDenseNDimArray(eta)

for mu in range(4):
    for nu in range(4):
        g_eff[mu, nu] += (
            kappa
            * sp.diff(psi, coords[mu])
            * sp.diff(psi, coords[nu])
            / (psi**2)
        )

print("=== Symbolic Effective Metric g_eff ===")
for mu in range(4):
    for nu in range(4):
        print(f"g_eff[{mu},{nu}] =")
        sp.pprint(sp.simplify(g_eff[mu, nu]), use_unicode=False)
        print()

# ----------------------------
# Numerical validation (FIXED)
# ----------------------------

print("=== Numeric Effective Metric Validation ===")

# Smooth, strictly nonzero test field
psi_test = (
    1.0
    + 0.1 * sp.cos(2 * sp.pi * x)
    * sp.cos(2 * sp.pi * y)
    * sp.cos(2 * sp.pi * z)
    * sp.cos(2 * sp.pi * t)
)

# Explicit derivatives of test field
subs_map = {
    psi: psi_test,
    sp.diff(psi, t): sp.diff(psi_test, t),
    sp.diff(psi, x): sp.diff(psi_test, x),
    sp.diff(psi, y): sp.diff(psi_test, y),
    sp.diff(psi, z): sp.diff(psi_test, z),
}

param_vals = {kappa: 0.1}

# Substitute everything BEFORE lambdify
g_num = sp.Matrix(4, 4, lambda i, j:
    g_eff[i, j].subs(subs_map).subs(param_vals)
)

g_num = sp.simplify(g_num)

# Lambdify only after derivatives are gone
g_func = sp.lambdify((t, x, y, z), g_num, "numpy")

# Sample spacetime point (generic)
pt = (0.13, 0.21, 0.34, 0.55)

g_val = np.array(g_func(*pt), dtype=float)

# ----------------------------
# Checks
# ----------------------------

# 1. Symmetry check
sym_err = np.max(np.abs(g_val - g_val.T))
print(f"Max symmetry violation |g - g^T| = {sym_err:.3e}")

assert sym_err < 1e-12, (
    f"[FAIL] Metric is not symmetric (max diff = {sym_err})"
)

# 2. Finite entries check
if not np.isfinite(g_val).all():
    raise AssertionError("[FAIL] Metric contains NaN or Inf")

# 3. Signature check
eigvals = np.linalg.eigvalsh(g_val)

num_neg = np.sum(eigvals < 0)
num_pos = np.sum(eigvals > 0)
num_zero = np.sum(np.isclose(eigvals, 0, atol=1e-10))

print("Metric eigenvalues:", eigvals)
print(f"Signature: {num_neg} negative, {num_pos} positive, {num_zero} zero")

assert num_zero == 0, (
    "[FAIL] Metric is degenerate (zero eigenvalue)"
)

assert num_neg == 1 and num_pos == 3, (
    f"[FAIL] Metric signature violation: "
    f"{num_neg} negative, {num_pos} positive"
)

print("[PASS] Effective metric is symmetric, finite, and Lorentzian.")
sys.exit(0)
