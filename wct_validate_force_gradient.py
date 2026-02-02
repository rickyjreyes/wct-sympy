# WCT Validation: Force from Curvature Gradient (regularized)

import sympy as sp

# Symbols
x, y, z = sp.symbols('x y z', real=True)
eps = sp.symbols('eps', positive=True)

psi = sp.Function('psi')(x, y, z)

# Regularized curvature
laplacian = sp.diff(psi, x, 2) + sp.diff(psi, y, 2) + sp.diff(psi, z, 2)
W_psi = -laplacian / (psi + eps)

# Force = -grad W
Fx = -sp.diff(W_psi, x)
Fy = -sp.diff(W_psi, y)
Fz = -sp.diff(W_psi, z)

print("Regularized force components:")
sp.pprint(sp.simplify(Fx), use_unicode=False)
sp.pprint(sp.simplify(Fy), use_unicode=False)
sp.pprint(sp.simplify(Fz), use_unicode=False)
