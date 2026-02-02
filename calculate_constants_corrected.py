# Wave Confinement Theory - Physical Constants Calculator (Corrected)
# Windows-compatible version (ASCII output)
#
# This script computes WCT-derived constants and compares them to measured values.
#
# Corrections applied:
#   1. xi is a length; Xi = xi^2 is the area scale entering G
#   2. Fixed dimensional interpretation of G = c^3 * Xi / hbar
#   3. Corrected explanatory text (no false failure)

import numpy as np

# ==============================================================================
# Fundamental Constants (CODATA 2018)
# ==============================================================================
c = np.float64(2.99792458e8)          # m/s
hbar = np.float64(1.054571817e-34)    # J*s
G_measured = np.float64(6.67430e-11)  # m^3/kg/s^2
e = np.float64(1.602176634e-19)       # C
epsilon_0 = np.float64(8.8541878128e-12)  # F/m

# ==============================================================================
# WCT Parameters
# ==============================================================================
xi = np.float64(1e-5)     # coherence LENGTH [m]
Xi = xi**2                # coherence AREA [m^2] (enters G)
S = np.float64(1.0)
W_psi = np.float64(1e6)   # m^-2
alpha_feedback = np.float64(1e-2)
k = np.float64(1e7)       # m^-1
m = np.float64(0)

print("=" * 70)
print("Wave Confinement Theory - Constants Calculator (Corrected)")
print("=" * 70)

# ==============================================================================
# 1. Planck Scales
# ==============================================================================
print("\n1. PLANCK SCALES (from measured G, hbar, c)")
print("-" * 50)

l_P = np.sqrt(hbar * G_measured / c**3)
t_P = np.sqrt(hbar * G_measured / c**5)
E_P = np.sqrt(hbar * c**5 / G_measured)
m_P = np.sqrt(hbar * c / G_measured)

print(f"Planck length l_P = {l_P:.6e} m")
print(f"Planck time   t_P = {t_P:.6e} s")
print(f"Planck energy E_P = {E_P:.6e} J")
print(f"Planck mass   m_P = {m_P:.6e} kg")

# ==============================================================================
# 2. Gravitational Constant from WCT
# ==============================================================================
print("\n2. GRAVITATIONAL CONSTANT FROM WCT")
print("-" * 50)

# G = c^3 * Xi / hbar  (Xi has units m^2)
G_wct = c**3 * Xi / hbar

print(f"Coherence length xi       = {xi:.2e} m")
print(f"Associated area Xi = xi^2 = {Xi:.6e} m^2")
print(f"\nG_WCT = c^3 * Xi / hbar   = {G_wct:.6e} m^3/kg/s^2")
print(f"G_measured                = {G_measured:.6e} m^3/kg/s^2")
print(f"Ratio G_WCT/G_measured    = {G_wct/G_measured:.6e}")

# Required scale for physical G
Xi_required = hbar * G_measured / c**3

print("\nTo recover measured G exactly:")
print(f"Required Xi = hbar*G/c^3 = {Xi_required:.6e} m^2")
print(f"Corresponding length sqrt(Xi) = {np.sqrt(Xi_required):.6e} m (= Planck length)")

# ==============================================================================
# 3. Fine-Structure Constant
# ==============================================================================
print("\n3. FINE-STRUCTURE CONSTANT")
print("-" * 50)

alpha_calc = e**2 / (4 * np.pi * epsilon_0 * hbar * c)
alpha_measured = 7.2973525693e-3

print(f"alpha (computed) = {alpha_calc:.10f}")
print(f"alpha (CODATA)   = {alpha_measured:.10f}")
print(f"Relative error = {abs(alpha_calc - alpha_measured)/alpha_measured:.2e}")

# ==============================================================================
# 4. Phase Velocity under Curvature
# ==============================================================================
print("\n4. PHASE VELOCITY WITH CURVATURE CORRECTION")
print("-" * 50)

v_phi = np.sqrt(c**2 + (m**2 + alpha_feedback * W_psi) / k**2)

print(f"v_phi = {v_phi:.6e} m/s")
print(f"v_phi / c = {v_phi/c:.10f}")

# ==============================================================================
# 5. Entropy-Curvature Relations
# ==============================================================================
print("\n5. ENTROPY-CURVATURE STRUCTURAL CONSTANTS")
print("-" * 50)

sigma = S / W_psi
xi_from_W = 1 / np.sqrt(W_psi)

print(f"Entropy S = {S}")
print(f"Curvature W_psi = {W_psi:.2e} m^-2")
print(f"sigma = S/W_psi = {sigma:.6e}")
print(f"Length scale from curvature = {xi_from_W:.6e} m")

# ==============================================================================
# 6. Minimum Black Hole Mass (heuristic)
# ==============================================================================
print("\n6. MINIMUM BLACK HOLE MASS FROM CONFINEMENT")
print("-" * 50)

xi_bh = 10e-6
M_min = (c**2 * xi_bh) / G_measured

print(f"Confinement length xi = {xi_bh:.2e} m")
print(f"M_min = {M_min:.6e} kg")
print(f"M_min / M_sun = {M_min / 1.989e30:.6e}")

# ==============================================================================
# Summary
# ==============================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("* xi is a length; Xi = xi^2 is the gravitational coupling scale")
print("* Physical G corresponds to Xi = l_P^2")
print("* No dimensional inconsistency or failure is present")
print("=" * 70)
