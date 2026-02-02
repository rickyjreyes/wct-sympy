
import sympy as sp

# Define symbols and function
x, y, z = sp.symbols('x y z')
psi = sp.Function('psi')(x, y, z)

# Define curvature Wψ
laplacian_psi = sp.diff(psi, x, x) + sp.diff(psi, y, y) + sp.diff(psi, z, z)
W_psi = -laplacian_psi / psi

# Compute gradient of Wψ: Fi = -∇i(Wψ)
Fx = -sp.diff(W_psi, x)
Fy = -sp.diff(W_psi, y)
Fz = -sp.diff(W_psi, z)

# Output force components
print("Force from curvature gradient components:")
print("F_x = ")
sp.pprint(sp.simplify(Fx), use_unicode=True)
print("
F_y = ")
sp.pprint(sp.simplify(Fy), use_unicode=True)
print("
F_z = ")
sp.pprint(sp.simplify(Fz), use_unicode=True)
