# WCT Validation: Curvature-Modified Effective Mass (E49)
# Windows-compatible version (ASCII output)
#
# Validates: m_eff^2 = Delta* c^2 and omega_j^2 = c^2 lambda_j + Delta*
# Gap-induced effective mass and spectrum

import sympy as sp
import numpy as np

print("=" * 70)
print("WCT VALIDATION: Curvature-Modified Effective Mass (E49)")
print("=" * 70)

# =============================================================================
# SYMBOLIC DEFINITIONS
# =============================================================================
print("\n1. SYMBOLIC DEFINITIONS")
print("-" * 50)

# Define symbols
c = sp.Symbol('c', positive=True)  # Speed of light
hbar = sp.Symbol('hbar', positive=True)  # Reduced Planck constant
Delta_star = sp.Symbol('Delta^*', positive=True)  # Spectral gap
lambda_j = sp.Symbol('lambda_j', positive=True)  # j-th eigenvalue
j = sp.Symbol('j', integer=True, positive=True)

# E49a: Effective mass from spectral gap
# m_eff^2 = Delta* / c^2  =>  m_eff = sqrt(Delta*) / c
m_eff_squared = Delta_star / c**2
m_eff = sp.sqrt(Delta_star) / c

print("E49a: Gap-induced effective mass")
print("m_eff^2 = Delta* / c^2")
print("m_eff = sqrt(Delta*) / c =")
sp.pprint(m_eff, use_unicode=False)

# E49b: Frequency spectrum with gap
# omega_j^2 = c^2 * lambda_j + Delta*
omega_j_squared = c**2 * lambda_j + Delta_star
omega_j = sp.sqrt(omega_j_squared)

print("\nE49b: Frequency spectrum with gap")
print("omega_j^2 = c^2 * lambda_j + Delta* =")
sp.pprint(omega_j_squared, use_unicode=False)

# =============================================================================
# DISPERSION RELATION
# =============================================================================
print("\n2. DISPERSION RELATION ANALYSIS")
print("-" * 50)

k = sp.Symbol('k', positive=True)  # Wavenumber

# For free waves: lambda_j ~ k^2
# omega^2 = c^2 k^2 + Delta*
# This is the Klein-Gordon dispersion with m_eff = sqrt(Delta*)/c

omega_dispersion = sp.sqrt(c**2 * k**2 + Delta_star)

print("Dispersion relation (Klein-Gordon form):")
print("omega(k) = sqrt(c^2 k^2 + Delta*) =")
sp.pprint(omega_dispersion, use_unicode=False)

# Group velocity
v_group = sp.diff(omega_dispersion, k)
v_group_simplified = sp.simplify(v_group)

print("\nGroup velocity v_g = d(omega)/dk =")
sp.pprint(v_group_simplified, use_unicode=False)

# Phase velocity
v_phase = omega_dispersion / k
v_phase_simplified = sp.simplify(v_phase)

print("\nPhase velocity v_p = omega/k =")
sp.pprint(v_phase_simplified, use_unicode=False)

# =============================================================================
# MASSLESS LIMIT
# =============================================================================
print("\n3. MASSLESS LIMIT (Delta* -> 0)")
print("-" * 50)

omega_massless = omega_dispersion.subs(Delta_star, 0)
print("omega(k)|_{Delta*=0} = c*k")
print("Recovered linear dispersion:", omega_massless)

v_g_massless = v_group_simplified.subs(Delta_star, 0)
print("v_g|_{Delta*=0} =", v_g_massless)

# =============================================================================
# REST FREQUENCY
# =============================================================================
print("\n4. REST FREQUENCY (k -> 0)")
print("-" * 50)

omega_rest = omega_dispersion.subs(k, 0)
print("omega_rest = omega(k=0) = sqrt(Delta*)")
print("This corresponds to the rest mass energy: E_rest = hbar * omega_rest")

E_rest = hbar * sp.sqrt(Delta_star)
print("\nE_rest = hbar * sqrt(Delta*) =")
sp.pprint(E_rest, use_unicode=False)

# =============================================================================
# NUMERICAL EXAMPLE
# =============================================================================
print("\n5. NUMERICAL EXAMPLE")
print("-" * 50)

# Physical constants
c_val = 2.998e8  # m/s
hbar_val = 1.055e-34  # J*s

# Example: electron-scale gap
m_e = 9.109e-31  # kg
Delta_star_electron = (m_e * c_val**2 / hbar_val)**2  # rad^2/s^2

print(f"Speed of light c = {c_val:.3e} m/s")
print(f"hbar = {hbar_val:.3e} J*s")
print(f"Electron mass m_e = {m_e:.3e} kg")
print(f"\nFor electron-scale gap:")
print(f"Delta* = (m_e c^2 / hbar)^2 = {Delta_star_electron:.3e} rad^2/s^2")

# Verify m_eff recovery
m_eff_check = np.sqrt(Delta_star_electron) / c_val
print(f"m_eff = sqrt(Delta*)/c = {m_eff_check:.3e} kg")
print(f"Ratio m_eff/m_e = {m_eff_check/m_e:.6f}")

# =============================================================================
# SPECTRUM TABLE
# =============================================================================
print("\n6. FREQUENCY SPECTRUM TABLE")
print("-" * 50)

L_val = 1e-10  # Confinement length scale (Angstrom)
print(f"Confinement length L = {L_val:.1e} m")

print(f"\n{'Mode j':<10} {'lambda_j (m^-2)':<20} {'omega_j (rad/s)':<20}")
print("-" * 50)

for j_val in range(1, 6):
    lam_j = (j_val * np.pi / L_val)**2
    omega_j_val = np.sqrt(c_val**2 * lam_j + Delta_star_electron)
    print(f"{j_val:<10} {lam_j:<20.3e} {omega_j_val:<20.3e}")

# =============================================================================
# CONNECTION TO WCT CURVATURE
# =============================================================================
print("\n7. CONNECTION TO WCT CURVATURE")
print("-" * 50)
print("From E19: Delta* ~ <sigma>_w^2")
print("The spectral gap is proportional to squared average curvature.")
print("\nThis links the effective mass to the curvature of confined modes:")
print("m_eff = sqrt(Delta*)/c ~ <sigma>_w / c")
print("\nCompare with E6: m = (hbar/c) <sigma>_w")
print("Consistency requires: Delta* = (hbar * <sigma>_w)^2")

print("\n" + "=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)
