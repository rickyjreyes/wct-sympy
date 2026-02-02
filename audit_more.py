# WCT Audit: Additional Derivations
# Windows-compatible version (ASCII output)

from sympy import symbols, Function, diff, Abs, exp, integrate, log, pi, simplify, latex

# === Variables ===
x, y, r, theta = symbols('x y r theta')
eps, alpha, kappa, theta_sym = symbols('epsilon alpha kappa theta')
psi = Function('psi')(x, y)
psi_1d = Function('psi')(x)
phi = Function('phi')(x, y)

# === 1. Curvature Scalar W_psi ===
Wpsi = -(diff(psi, x, 2) + diff(psi, y, 2)) / psi

# === 2. Regularized W_psi (epsilon) ===
Wpsi_eps = -(diff(psi, x, 2) + diff(psi, y, 2)) / (psi + eps * exp(-alpha * Abs(psi)**2))

# === 3. Entropy S ===
p = Abs(psi_1d)**2 / integrate(Abs(psi_1d)**2, (x, -1, 1))
S = -integrate(p * log(p), (x, -1, 1))

# === 4. Sigma = <S> / <|W_psi|> ===
sigma = S / integrate(Abs(Wpsi), (x, -1, 1), (y, -1, 1))  # Note: symbolic only

# === 5. Gamma = <(grad phi)^2> / <phi^2> ===
grad_phi_sq = diff(phi, x)**2 + diff(phi, y)**2
phi_sq = phi**2
gamma = integrate(grad_phi_sq, (x, -1, 1), (y, -1, 1)) / integrate(phi_sq, (x, -1, 1), (y, -1, 1))

# === 6. Emergent Constants ===
c, hbar, Lambda = symbols('c hbar Lambda')
e, epsilon_0 = symbols('e epsilon_0')

G_expr = c**3 / (hbar * Lambda**0.5)
alpha_expr = e**2 / (4 * pi * epsilon_0 * hbar * c)

# === Output in LaTeX ===
expressions = {
    "W_psi": Wpsi,
    "W_psi (epsilon)": Wpsi_eps,
    "Entropy S": S,
    "Sigma": sigma,
    "Gamma": gamma,
    "G": G_expr,
    "alpha": alpha_expr
}

for name, expr in expressions.items():
    print(f"{name}:")
    print(latex(expr))
    print()
