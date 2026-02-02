# WCT Validation: Mass Accumulation Integrand
# Windows-compatible version (ASCII output)

import sympy as sp

# Define variables
x = sp.symbols('x')
psi = sp.Function('psi')(x)

# Define curvature scalar W_psi = -laplacian(psi) / psi
W_psi = -sp.diff(psi, x, x) / psi

# Define integrand: W_psi * |psi|^2 (mass density)
mass_density = W_psi * psi**2

# Simplify expression
mass_density_simplified = sp.simplify(mass_density)

print("Mass accumulation integrand W_psi * |psi|^2:")
sp.pprint(mass_density_simplified, use_unicode=False)
