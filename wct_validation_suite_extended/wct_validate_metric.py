
import sympy as sp
from sympy import Function, symbols, simplify

# Define spacetime coordinates
t, x, y, z = sp.symbols('t x y z')
coords = [t, x, y, z]

# Define field psi(t, x, y, z)
psi = Function('psi')(*coords)
kappa = sp.Symbol('kappa', positive=True)

# Initialize flat Minkowski metric (signature: -+++)
eta = sp.diag(-1, 1, 1, 1)

# Construct effective metric: g_eff = eta + kappa * ∂_μ ψ ∂_ν ψ / |ψ|^2
g_eff = sp.MutableDenseNDimArray(eta)

for mu in range(4):
    for nu in range(4):
        g_eff[mu, nu] += kappa * sp.diff(psi, coords[mu]) * sp.diff(psi, coords[nu]) / (psi**2)

# Print symbolic effective metric
print("Emergent Effective Metric g_eff[μν]:")
for mu in range(4):
    for nu in range(4):
        print(f"g_eff[{mu},{nu}] = ")
        sp.pprint(simplify(g_eff[mu, nu]), use_unicode=True)
        print()
