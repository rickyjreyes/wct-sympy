# WCT Validation: Entropy Monotonicity
# Windows-compatible version (ASCII output)

import sympy as sp

# Define spacetime variables and psi field
t, x = sp.symbols('t x')
psi = sp.Function('psi')(x, t)

# Define entropy functional S = integral [(grad psi)^2 / |psi|^2 + lambda |psi|^2] dx
lam = sp.Symbol('lambda', positive=True)

# Spatial derivative of psi
dpsi_dx = sp.diff(psi, x)
entropy_density = (dpsi_dx**2) / (psi**2) + lam * psi**2

# Time derivative of entropy density (dS/dt local)
d_entropy_dt = sp.diff(entropy_density, t)

# Simplify
d_entropy_dt_simplified = sp.simplify(d_entropy_dt)

print("Local time derivative of entropy density dS/dt:")
sp.pprint(d_entropy_dt_simplified, use_unicode=False)
