# WCT Validation: Force from Curvature Gradient (regularized, minimal)

import sympy as sp

# Symbols
x, y, z = sp.symbols('x y z', real=True)
eps = sp.symbols('eps', positive=True)

psi = sp.Function('psi')(x, y, z)

# Regularized curvature
laplacian = sp.diff(psi, x, 2) + sp.diff(psi, y, 2) + sp.diff(psi, z, 2)
W = -laplacian / (psi + eps)

# Force definition
F = [-sp.diff(W, v) for v in (x, y, z)]

print("Force from curvature gradient (regularized):")
for i, Fi in enumerate(F):
    print(f"F_{['x','y','z'][i]} =")
    sp.pprint(sp.simplify(Fi), use_unicode=False)
