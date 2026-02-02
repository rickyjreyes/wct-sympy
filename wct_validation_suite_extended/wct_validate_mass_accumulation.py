
import sympy as sp

# Define variables
x = sp.symbols('x')
psi = sp.Function('psi')(x)

# Define curvature scalar W_ψ = -∇²ψ / ψ
W_psi = -sp.diff(psi, x, x) / psi

# Define integrand: W_ψ * |ψ|² (mass density)
mass_density = W_psi * psi**2

# Simplify expression
mass_density_simplified = sp.simplify(mass_density)

print("Mass accumulation integrand W_ψ * |ψ|²:")
sp.pprint(mass_density_simplified, use_unicode=True)
