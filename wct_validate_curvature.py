
import sympy as sp
from sympy import symbols, Function, exp, simplify

x = sp.Symbol('x')
psi = Function('psi')(x)
epsilon, lam = symbols('epsilon lambda', positive=True)

# Define the entropy-regularized curvature scalar
W_reg = -sp.diff(psi, x, x) / (psi + epsilon * exp(-lam * psi**2))

# Simplify
W_simplified = simplify(W_reg)

print("Entropy-Regularized Curvature Scalar:")
sp.pprint(W_simplified)
