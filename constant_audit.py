import sympy as sp

# Define base symbols
c, hbar, G, Lambda, xi = sp.symbols('c hbar G Lambda xi', real=True, positive=True)
m, alpha, W_psi, k, phi = sp.symbols('m alpha W_psi k phi', real=True)
e, epsilon_0 = sp.symbols('e epsilon_0', real=True, positive=True)
S = sp.Symbol('S', real=True, positive=True)

# 1. Gravitational Constant G
G_expr = c**3 / (hbar * sp.sqrt(Lambda))

# 2. Speed of Light from Planck Scales
l_P = sp.sqrt(hbar * G / c**3)
t_P = sp.sqrt(hbar * G / c**5)
c_expr = l_P / t_P

# 3. Planck’s Constant from E_P * t_P
E_P = sp.sqrt(hbar * c**5 / G)
hbar_expr = E_P * t_P

# 4. Fine-Structure Constant
alpha_expr = e**2 / (4 * sp.pi * epsilon_0 * hbar * c)

# 5. Cosmological Constant from coherence scale
Lambda_expr = 1 / xi**2

# 6. Planck Scales
l_P_val = sp.sqrt(hbar * G / c**3)
t_P_val = sp.sqrt(hbar * G / c**5)
E_P_val = sp.sqrt(hbar * c**5 / G)

# 7. Phase Velocity under curvature and mass
v_phi_expr = sp.sqrt(c**2 + (m**2 + alpha * W_psi) / k**2)

# 8. Structural Constants
sigma_expr = S / W_psi
xi_expr = 1 / sp.sqrt(W_psi)

# Output all expressions
results = {
    "G from c, hbar, Lambda": G_expr,
    "c from Planck scales": c_expr,
    "hbar from Planck Energy * Time": hbar_expr,
    "Fine-structure alpha": alpha_expr,
    "Lambda from coherence scale": Lambda_expr,
    "Planck Length": l_P_val,
    "Planck Time": t_P_val,
    "Planck Energy": E_P_val,
    "Phase velocity v_phi": v_phi_expr,
    "Entropy-Curvature Ratio sigma": sigma_expr,
    "Vacuum coherence length xi": xi_expr
}

for name, expr in results.items():
    print(f"{name}:\n{sp.pretty(expr)}\n")
