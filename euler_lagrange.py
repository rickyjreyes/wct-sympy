# WCT: Euler-Lagrange Field Equation Derivation
# Windows-compatible version (ASCII output)

from sympy import symbols, Function, diff, Abs, simplify, pprint, latex

# Define variables and field
x, y = symbols('x y')
kappa, theta = symbols('kappa theta')  # coupling constants
psi = Function('psi')(x, y)
V = Function('V')(Abs(psi)**2)  # general potential term

# Define curvature scalar W_psi
Wpsi = -(diff(psi, x, 2) + diff(psi, y, 2)) / psi

# Define the full Lagrangian L
L = (1/2)*(diff(psi, x)**2 + diff(psi, y)**2) - V - kappa * Wpsi * Abs(psi)**2 - theta * Wpsi**2

# Compute Euler-Lagrange equation: dL/dpsi - d_mu(dL/d(d_mu psi))
dL_dpsi = diff(L, psi)
dL_dpsix = diff(L, diff(psi, x))
dL_dpsiy = diff(L, diff(psi, y))
d_dx_dL_dpsix = diff(dL_dpsix, x)
d_dy_dL_dpsiy = diff(dL_dpsiy, y)

# Final Euler-Lagrange field equation
euler_lagrange_eq = simplify(dL_dpsi - d_dx_dL_dpsix - d_dy_dL_dpsiy)

# Output result
print("\nEuler-Lagrange Field Equation for Wave Confinement Theory:\n")
pprint(euler_lagrange_eq, use_unicode=False)
print("\nLaTeX Format:\n")
print(latex(euler_lagrange_eq))
