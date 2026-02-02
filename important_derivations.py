# WCT: Important Derivations
# Windows-compatible version (ASCII output)

from sympy import symbols, Function, diff, Abs, exp, simplify, integrate, log, pi, pprint

# Declare variables
x, y, r, theta = symbols('x y r theta')
eps, alpha, kappa, theta_sym = symbols('epsilon alpha kappa theta')
psi_xy = Function('psi')(x, y)
psi_1d = Function('psi')(x)
psi_polar = Function('psi')(r, theta)

# 1. Curvature Scalar W_psi
Wpsi = -(diff(psi_xy, x, 2) + diff(psi_xy, y, 2)) / psi_xy

# 2. Regularized W_psi (epsilon)
Wpsi_eps = -(diff(psi_xy, x, 2) + diff(psi_xy, y, 2)) / (psi_xy + eps * exp(-alpha * Abs(psi_xy)**2))

# 3. Entropy S (symbolic, continuous)
p = Abs(psi_1d)**2 / integrate(Abs(psi_1d)**2, (x, -1, 1))
S = -integrate(p * log(p), (x, -1, 1))

# 4. Beta Ratio (topological resonance)
partial_theta_sq = diff(psi_polar, theta)**2
partial_r_sq = diff(psi_polar, r)**2
avg_theta = integrate(partial_theta_sq, (theta, 0, 2*pi), (r, 0, 1)) / (2*pi)
avg_r = integrate(partial_r_sq, (theta, 0, 2*pi), (r, 0, 1)) / (2*pi)
beta_ratio = simplify(avg_theta / avg_r)

# 5. Lagrangian L
V = Function('V')(Abs(psi_xy)**2)
Lagrangian = (1/2)*(diff(psi_xy, x)**2 + diff(psi_xy, y)**2) - V - kappa * Wpsi * Abs(psi_xy)**2 - theta_sym * Wpsi**2

# Print expressions
print("Curvature Scalar W_psi:")
pprint(Wpsi, use_unicode=False)
print("\nRegularized W_psi (epsilon):")
pprint(Wpsi_eps, use_unicode=False)
print("\nEntropy S:")
pprint(S, use_unicode=False)
print("\nBeta Ratio beta:")
pprint(beta_ratio, use_unicode=False)
print("\nLagrangian L:")
pprint(Lagrangian, use_unicode=False)
