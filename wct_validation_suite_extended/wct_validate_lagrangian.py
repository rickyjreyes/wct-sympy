
import sympy as sp
from sympy import Function, symbols, Derivative, simplify

# Define variables and functions
x, t = sp.symbols('x t')
psi = sp.Function('psi')(x, t)
psi_star = sp.Function('psi_star')(x, t)
epsilon, lam, alpha = symbols('epsilon lambda alpha', positive=True)

# Regularized curvature W_psi
W = -sp.diff(psi, x, x) / (psi + epsilon * sp.exp(-lam * psi**2))

# Lagrangian density
L = sp.diff(psi, t)**2 - sp.diff(psi, x)**2 - alpha * W * psi**2

# Euler-Lagrange expression: d/dt(dL/d(∂_t psi)) - d/dx(dL/d(∂_x psi)) + dL/dpsi
dL_dpsi_t = sp.diff(L, sp.diff(psi, t))
d_dt_dL_dpsi_t = sp.diff(dL_dpsi_t, t)

dL_dpsi_x = sp.diff(L, sp.diff(psi, x))
d_dx_dL_dpsi_x = sp.diff(dL_dpsi_x, x)

dL_dpsi = sp.diff(L, psi)

# Euler-Lagrange equation
EL_eq = simplify(d_dt_dL_dpsi_t - d_dx_dL_dpsi_x - dL_dpsi)

print("Euler-Lagrange equation from WCT Lagrangian:")
sp.pprint(EL_eq, use_unicode=True)
