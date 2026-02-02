# WCT: Regularized Hamiltonian Density
# Windows-compatible version (ASCII output)

from sympy import symbols, Function, diff, Abs, simplify, pprint, latex

# === Declare variables ===
x, y, t = symbols('x y t')
kappa, theta, epsilon = symbols('kappa theta epsilon')  # epsilon added for regularization
psi = Function('psi')(x, y, t)

# === Time derivative ===
dpsi_dt = diff(psi, t)

# === Potential energy V(|psi|^2) ===
V = Function('V')(Abs(psi)**2)

# === Curvature scalar W_psi = -laplacian(psi) / psi ===
Wpsi = -(diff(psi, x, 2) + diff(psi, y, 2)) / psi

# === Lagrangian L ===
L = (1/2)*(dpsi_dt**2 + diff(psi, x)**2 + diff(psi, y)**2) \
    - V - kappa * Wpsi * Abs(psi)**2 - theta * Wpsi**2

# === Canonical momentum pi = dL/d(d_t psi) ===
pi = diff(L, dpsi_dt)

# === Regularized Hamiltonian H = (pi * d_t psi - L) / (psi^2 + epsilon) ===
regularized_denominator = psi**2 + epsilon
H_reg = simplify((pi * dpsi_dt - L) / regularized_denominator)

# === Output the symbolic result ===
print("\nRegularized Hamiltonian Density H:\n")
pprint(H_reg, use_unicode=False)
print("\nLaTeX Format:\n")
print(latex(H_reg))
