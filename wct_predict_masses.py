# -*- coding: utf-8 -*-
"""
WCT Particle Mass Predictions
Windows-compatible version

Based on the curvature-locking equations (CLE1-CLE10, E6-E7)

Key equations:
  E6: m = (hbar/c) <sigma>_w  where sigma = sqrt(kappa^2 + tau^2)
  CLE9: R = 1/sigma*  (Compton radius from curvature)
"""

import numpy as np

# Fundamental constants (CODATA 2018)
c = 2.99792458e8        # m/s
hbar = 1.054571817e-34  # J*s
eV_to_J = 1.602176634e-19  # J/eV
MeV_to_J = eV_to_J * 1e6
GeV_to_J = eV_to_J * 1e9

# Measured particle masses
m_e = 0.51099895       # MeV/c^2
m_mu = 105.6583755     # MeV/c^2
m_tau = 1776.86        # MeV/c^2

m_u = 2.16             # MeV/c^2 (up quark, approximate)
m_d = 4.67             # MeV/c^2 (down quark, approximate)
m_s = 93.4             # MeV/c^2 (strange quark)
m_c = 1270             # MeV/c^2 (charm)
m_b = 4180             # MeV/c^2 (bottom)
m_t = 172760           # MeV/c^2 (top)

print("=" * 70)
print("WCT PARTICLE MASS ANALYSIS")
print("=" * 70)

# =============================================================================
# 1. ELECTRON AS FUNDAMENTAL CURVATURE SCALE
# =============================================================================
print("\n1. ELECTRON CURVATURE SCALE (Reference)")
print("-" * 50)

# Electron Compton wavelength
lambda_C_e = hbar / (m_e * MeV_to_J / c**2) / c  # in meters
R_e = lambda_C_e / (2 * np.pi)  # Compton radius

# Curvature from electron mass
sigma_e = m_e * MeV_to_J / (hbar * c)  # in m^-1

print(f"   Electron mass: {m_e:.6f} MeV/c^2")
print(f"   Compton wavelength lambda_C = {lambda_C_e:.6e} m")
print(f"   Compton radius R = lambda_C/(2*pi) = {R_e:.6e} m = {R_e*1e15:.2f} fm")
print(f"   Curvature sigma_e = m_e*c / hbar = {sigma_e:.6e} m^-1")
print(f"   Check: R * sigma = {R_e * sigma_e:.6f} (should be ~1)")

# =============================================================================
# 2. KOIDE FORMULA CHECK
# =============================================================================
print("\n2. KOIDE FORMULA (Charged Leptons)")
print("-" * 50)

# Koide formula: (m_e + m_mu + m_tau) / (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2 = 2/3
sqrt_masses = np.sqrt(m_e) + np.sqrt(m_mu) + np.sqrt(m_tau)
sum_masses = m_e + m_mu + m_tau
koide_ratio = sum_masses / (sqrt_masses**2)
koide_theoretical = 2/3

print(f"   sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau) = {sqrt_masses:.6f} sqrt(MeV)")
print(f"   m_e + m_mu + m_tau = {sum_masses:.4f} MeV")
print(f"   Koide ratio Q = Sum(m) / (Sum(sqrt(m)))^2 = {koide_ratio:.10f}")
print(f"   Theoretical Q = 2/3 = {koide_theoretical:.10f}")
print(f"   Deviation: {(koide_ratio - koide_theoretical)*100:.6f}%")

# =============================================================================
# 3. CURVATURE HARMONIC HYPOTHESIS
# =============================================================================
print("\n3. CURVATURE HARMONIC ANALYSIS")
print("-" * 50)

# Hypothesis: Masses arise from curvature eigenvalues
# If m_n = m_e * f(n) where f(n) is a harmonic function

# Mass ratios relative to electron
r_mu = m_mu / m_e
r_tau = m_tau / m_e

print(f"   m_mu / m_e = {r_mu:.6f}")
print(f"   m_tau / m_e = {r_tau:.6f}")
print(f"   m_tau / m_mu = {m_tau/m_mu:.6f}")

# Check for integer relationships
print(f"\n   Looking for patterns:")
print(f"   sqrt(m_mu/m_e) = {np.sqrt(r_mu):.4f} (approx {round(np.sqrt(r_mu))})")
print(f"   cbrt(m_tau/m_e) = {r_tau**(1/3):.4f}")
print(f"   (m_mu/m_e)^(1/4) = {r_mu**0.25:.4f}")

# =============================================================================
# 4. WCT MASS FORMULA EXPLORATION
# =============================================================================
print("\n4. WCT MASS FROM CURVATURE (Exploration)")
print("-" * 50)

# From E6-E7: m = (hbar/c) <sqrt(kappa^2 + tau^2)>
# For toroidal geometry: kappa ~ 1/R, tau ~ winding

def mass_from_curvature(sigma_avg):
    """Calculate mass from average curvature sigma = <sqrt(kappa^2 + tau^2)>"""
    m_J = (hbar / c) * sigma_avg  # mass in kg
    m_MeV = m_J * c**2 / MeV_to_J  # convert to MeV/c^2
    return m_MeV

# Working backwards: what curvature gives observed muon mass?
sigma_mu_needed = m_mu * MeV_to_J / (hbar * c)
sigma_tau_needed = m_tau * MeV_to_J / (hbar * c)

print(f"   sigma_e (electron) = {sigma_e:.6e} m^-1")
print(f"   sigma_mu (needed for muon) = {sigma_mu_needed:.6e} m^-1")
print(f"   sigma_tau (needed for tau) = {sigma_tau_needed:.6e} m^-1")
print(f"\n   Curvature ratios:")
print(f"   sigma_mu / sigma_e = {sigma_mu_needed/sigma_e:.4f}")
print(f"   sigma_tau / sigma_e = {sigma_tau_needed/sigma_e:.4f}")

# =============================================================================
# 5. PREDICTIVE TEST: EXTEND TO QUARKS
# =============================================================================
print("\n5. QUARK MASS CURVATURE ANALYSIS")
print("-" * 50)

quarks = [
    ("up", m_u),
    ("down", m_d),
    ("strange", m_s),
    ("charm", m_c),
    ("bottom", m_b),
    ("top", m_t),
]

print(f"   {'Quark':<10} {'Mass (MeV)':<12} {'sigma (m^-1)':<15} {'sigma/sigma_e':<10}")
print(f"   {'-'*10} {'-'*12} {'-'*15} {'-'*10}")

for name, mass in quarks:
    sigma = mass * MeV_to_J / (hbar * c)
    ratio = sigma / sigma_e
    print(f"   {name:<10} {mass:<12.2f} {sigma:<15.4e} {ratio:<10.2f}")

# =============================================================================
# 6. SUMMARY TABLE
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: CURVATURE-MASS CORRESPONDENCE")
print("=" * 70)

particles = [
    ("electron", m_e),
    ("muon", m_mu),
    ("tau", m_tau),
    ("up", m_u),
    ("down", m_d),
    ("strange", m_s),
    ("charm", m_c),
    ("bottom", m_b),
    ("top", m_t),
]

print(f"\n{'Particle':<10} {'Mass (MeV)':<12} {'R = hbar/mc (m)':<15} {'sigma = mc/hbar (m^-1)':<15}")
print("-" * 60)

for name, mass in particles:
    R = hbar / (mass * MeV_to_J / c**2) / c
    sigma = mass * MeV_to_J / (hbar * c)
    print(f"{name:<10} {mass:<12.4f} {R:<15.4e} {sigma:<15.4e}")

print("\n" + "=" * 70)
print("OPEN QUESTIONS FOR WCT:")
print("=" * 70)
print("""
1. What determines the discrete spectrum of allowed curvatures sigma_n?
2. Can Koide's 2/3 ratio be derived from curvature-locking topology?
3. Why are quark masses so different from leptons?
4. What sets the electron mass scale (sigma_e) as fundamental?
5. Can WCT predict m_tau from m_e and m_mu?
""")
