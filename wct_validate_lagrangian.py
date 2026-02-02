# WCT Validation: Euler–Lagrange from curvature-regularized Lagrangian

import sympy as sp

x, t = sp.symbols('x t')
eps, alpha = sp.symbols('eps alpha', positive=True)

psi = sp.Function('psi')(x, t)

# Regularized curvature
W = -sp.diff(psi, x, 2) / (psi + eps)

# Proper Lagrangian density
L = (
    sp.diff(psi, t)**2
    - sp.diff(psi, x)**2
    - alpha * W**2
)

# Euler–Lagrange
EL = (
    sp.diff(sp.diff(L, sp.diff(psi, t)), t)
    - sp.diff(sp.diff(L, sp.diff(psi, x)), x)
    - sp.diff(L, psi)
)

print("Euler–Lagrange equation:")
sp.pprint(sp.simplify(EL), use_unicode=False)
