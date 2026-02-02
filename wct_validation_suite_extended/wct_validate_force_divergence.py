
import sympy as sp

# Setup symbols and function
x = sp.Symbol('x')
psi = sp.Function('psi')(x)

# Curvature Wψ
W_psi = -sp.diff(psi, x, x) / psi
grad_W = sp.diff(W_psi, x)

print("Gradient of Wψ (Force divergence check):")
sp.pprint(sp.simplify(grad_W), use_unicode=True)
