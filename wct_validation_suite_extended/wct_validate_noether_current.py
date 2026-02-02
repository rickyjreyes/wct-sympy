
import sympy as sp

# Define variables
t = sp.Symbol('t')
psi = sp.Function('psi')(t)
psi_star = sp.conjugate(psi)

# Noether current from phase symmetry
j_0 = sp.I * (psi_star * sp.diff(psi, t) - psi * sp.diff(psi_star, t))
j_0_simplified = sp.simplify(j_0)

print("Noether Current j^0:")
sp.pprint(j_0_simplified, use_unicode=True)
