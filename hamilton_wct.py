# WCT: Hamiltonian Density Derivation
# Windows-compatible version (ASCII output)

from sympy import symbols, Function, diff, Abs, simplify, pprint, latex

# Define spacetime variables
x, y, t = symbols('x y t')
kappa, theta = symbols('kappa theta')
psi = Function('psi')(x, y, t)

# Time derivative
dpsi_dt = diff(psi, t)

# Define potential V(|psi|^2)
V = Function('V')(Abs(psi)**2)

# Define curvature scalar W_psi = -laplacian(psi) / psi
Wpsi = -(diff(psi, x, 2) + diff(psi, y, 2)) / psi

# Lagrangian L with time dependence
L = (1/2)*(dpsi_dt**2 + diff(psi, x)**2 + diff(psi, y)**2) \
    - V - kappa * Wpsi * Abs(psi)**2 - theta * Wpsi**2

# Canonical momentum pi = dL/d(d_t psi)
pi = diff(L, dpsi_dt)

# Hamiltonian density H = pi * d_t psi - L
H = simplify(pi * dpsi_dt - L)

# Output result
print("\nHamiltonian Density H:\n")
pprint(H, use_unicode=False)
print("\nLaTeX Format:\n")
print(latex(H))
