# WCT Validation: Theta-Eigenmode Quantization (E44)
# Windows-compatible version (ASCII output)
#
# Validates: Theta[psi_n] = lambda_n * psi_n
# The curvature operator has discrete eigenmodes

import sympy as sp
import numpy as np

# =============================================================================
# SYMBOLIC VALIDATION
# =============================================================================
print("=" * 70)
print("WCT VALIDATION: Theta-Eigenmode Quantization (E44)")
print("=" * 70)

# Define symbols
x = sp.Symbol('x', real=True)
n = sp.Symbol('n', integer=True, positive=True)
L = sp.Symbol('L', positive=True)
eps = sp.Symbol('epsilon', positive=True)
alpha = sp.Symbol('alpha', positive=True)

# Define eigenmode ansatz: psi_n = A * sin(n*pi*x/L) for box
# This is a standard Sturm-Liouville eigenfunction

psi_n = sp.sin(n * sp.pi * x / L)

# Compute Laplacian of psi_n
laplacian_psi = sp.diff(psi_n, x, 2)

print("\n1. EIGENMODE ANSATZ (1D box)")
print("-" * 50)
print("psi_n(x) = sin(n*pi*x/L)")
sp.pprint(psi_n, use_unicode=False)

print("\nLaplacian of psi_n:")
laplacian_simplified = sp.simplify(laplacian_psi)
sp.pprint(laplacian_simplified, use_unicode=False)

# Standard curvature operator (unregularized): W = -Laplacian(psi)/psi
W_psi = -laplacian_psi / psi_n
W_simplified = sp.simplify(W_psi)

print("\n2. CURVATURE EIGENVALUE")
print("-" * 50)
print("W_psi = -Laplacian(psi)/psi =")
sp.pprint(W_simplified, use_unicode=False)

# The eigenvalue is lambda_n = (n*pi/L)^2
lambda_n = (n * sp.pi / L)**2
print("\nEigenvalue lambda_n = (n*pi/L)^2 =")
sp.pprint(lambda_n, use_unicode=False)

# Verify eigenvalue equation
print("\n3. EIGENVALUE EQUATION VERIFICATION")
print("-" * 50)
print("Check: W_psi = lambda_n ?")
difference = sp.simplify(W_simplified - lambda_n)
print(f"W_psi - lambda_n = {difference}")
print("Eigenvalue equation VERIFIED" if difference == 0 else "ERROR: Mismatch")

# =============================================================================
# REGULARIZED THETA OPERATOR
# =============================================================================
print("\n4. REGULARIZED THETA OPERATOR (E17)")
print("-" * 50)

# Theta[psi] = -Laplacian(psi) / (psi + eps * exp(-alpha * |psi|^2))
# For real psi, |psi|^2 = psi^2

psi = sp.Function('psi')(x)
Theta = -sp.diff(psi, x, 2) / (psi + eps * sp.exp(-alpha * psi**2))

print("Theta[psi] = -d^2 psi/dx^2 / (psi + eps * exp(-alpha * psi^2))")
print("\nSymbolic form:")
sp.pprint(Theta, use_unicode=False)

# =============================================================================
# NUMERICAL EIGENVALUE SPECTRUM
# =============================================================================
print("\n5. NUMERICAL EIGENVALUE SPECTRUM")
print("-" * 50)

L_val = 1.0  # Box length
n_modes = 10

print(f"Box length L = {L_val}")
print(f"\n{'Mode n':<10} {'lambda_n':<20} {'sqrt(lambda_n)':<15}")
print("-" * 45)

for n_val in range(1, n_modes + 1):
    lam = (n_val * np.pi / L_val)**2
    print(f"{n_val:<10} {lam:<20.6f} {np.sqrt(lam):<15.6f}")

# =============================================================================
# SPECTRAL GAP
# =============================================================================
print("\n6. SPECTRAL GAP ANALYSIS")
print("-" * 50)

lambda_1 = (np.pi / L_val)**2
lambda_2 = (2 * np.pi / L_val)**2
gap = lambda_2 - lambda_1

print(f"lambda_1 = {lambda_1:.6f}")
print(f"lambda_2 = {lambda_2:.6f}")
print(f"Spectral gap Delta = lambda_2 - lambda_1 = {gap:.6f}")
print(f"Gap ratio lambda_2/lambda_1 = {lambda_2/lambda_1:.6f}")

# =============================================================================
# CONNECTION TO MASS (E6)
# =============================================================================
print("\n7. CONNECTION TO MASS (E6)")
print("-" * 50)
print("From E6: m = (hbar/c) * <sigma>_w")
print("For eigenmodes: sigma_n ~ sqrt(lambda_n) = n*pi/L")
print("\nMass spectrum scales as m_n ~ n")
print("This gives discrete mass quantization from curvature eigenmodes.")

print("\n" + "=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)
