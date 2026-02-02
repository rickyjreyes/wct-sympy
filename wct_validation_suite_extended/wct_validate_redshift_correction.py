
import sympy as sp

# Define symbols
x = sp.Symbol('x')
psi = sp.Function('psi')(x)
alpha, c, k, m = sp.symbols('alpha c k m', positive=True)

# Define Wψ = -∇²ψ / ψ
W_psi = -sp.diff(psi, x, x) / psi

# Define effective frequency with curvature correction
omega_eff = sp.sqrt(c**2 * k**2 + m**2 + alpha * W_psi)

print("Redshift-Corrected Effective Frequency ω_eff:")
sp.pprint(sp.simplify(omega_eff), use_unicode=True)
