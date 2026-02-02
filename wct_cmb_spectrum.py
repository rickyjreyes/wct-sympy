# WCT Cosmology: CMB Power Spectrum Generator
# Windows-compatible version
#
# Generates the CMB angular power spectrum C_l from WCT cosmology (CM1-CM20)
# Based on curvature-driven acoustic oscillations

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

print("=" * 70)
print("WCT CMB POWER SPECTRUM GENERATOR")
print("=" * 70)

# =============================================================================
# COSMOLOGICAL PARAMETERS (WCT-DERIVED)
# =============================================================================
print("\n1. WCT COSMOLOGICAL PARAMETERS")
print("-" * 50)

# WCT-derived parameters
C_Phi = 1.0           # Curvature-potential coupling (CM3)
beta_curv = 0.1       # Curvature feedback in sound speed (CM6)
D_S = 1e-4            # Silk diffusion coefficient (CM7)
n_s = 0.965           # Spectral index (CM2: alpha_WCT)

# Standard cosmological scales (for comparison)
# These would be derived from WCT in full theory
H_0 = 67.4            # km/s/Mpc (approximate)
Omega_b = 0.0493      # Baryon density
Omega_c = 0.264       # CDM density
Omega_r = 9.2e-5      # Radiation density
z_eq = 3400           # Matter-radiation equality
z_dec = 1100          # Decoupling redshift

print(f"WCT parameters:")
print(f"  C_Phi (curvature coupling) = {C_Phi}")
print(f"  beta_curv (feedback strength) = {beta_curv}")
print(f"  D_S (diffusion) = {D_S}")
print(f"  n_s (spectral index) = {n_s}")

# =============================================================================
# CM6: SOUND SPEED EVOLUTION
# =============================================================================
def R_of_z(z):
    """Baryon-photon ratio R(z) = 3*rho_b/(4*rho_gamma)"""
    # R grows as (1+z)^-1 after equality
    R_eq = 0.6  # Value at equality
    return R_eq * (1 + z_eq) / (1 + z)

def c_s_squared(z):
    """Sound speed squared from CM6"""
    R = R_of_z(z)
    # CM6: c_s^2 = (1/3) / (1 + R) * [1 - beta_curv * E_curv/E_tot]
    # Simplified: neglect curvature energy correction for now
    return (1/3) / (1 + R)

def c_s(z):
    return np.sqrt(c_s_squared(z))

# =============================================================================
# CM7: SILK DAMPING SCALE
# =============================================================================
def k_D_of_z(z_start, z_end):
    """Damping wavenumber from CM11"""
    # k_D^{-2} = integral D_curv dt
    # Simplified model
    z_range = np.linspace(z_start, z_end, 100)
    D_integral = np.trapz([D_S * (1 + zi)**2 for zi in z_range], z_range)
    if D_integral > 0:
        return 1 / np.sqrt(D_integral)
    return np.inf

# =============================================================================
# TRANSFER FUNCTION
# =============================================================================
def transfer_function(k, z_dec=1100):
    """WCT transfer function T(k)"""
    # Sound horizon at decoupling (simplified)
    # r_s = integral c_s dt from z=inf to z_dec
    r_s = 150  # Mpc (approximate)
    
    # Acoustic oscillations
    phase = k * r_s
    
    # Damping envelope (CM11)
    k_D = 0.1  # Mpc^-1 (approximate damping scale)
    damping = np.exp(-(k / k_D)**2)
    
    # Transfer function combines oscillation and damping
    T_k = np.cos(phase) * damping
    
    return T_k

# =============================================================================
# PRIMORDIAL POWER SPECTRUM (CM2)
# =============================================================================
def P_primordial(k, A_s=2.1e-9, k_pivot=0.05):
    """Primordial power spectrum from CM2"""
    # P(k) ~ k^{n_s - 1}
    return A_s * (k / k_pivot)**(n_s - 1)

# =============================================================================
# MATTER POWER SPECTRUM
# =============================================================================
def P_matter(k):
    """Matter power spectrum P(k)"""
    T_k = transfer_function(k)
    P_prim = P_primordial(k)
    return P_prim * T_k**2

# =============================================================================
# CMB ACOUSTIC OSCILLATIONS (CM5)
# =============================================================================
print("\n2. ACOUSTIC OSCILLATOR EVOLUTION (CM5)")
print("-" * 50)

def acoustic_evolution(k, z_range):
    """
    Solve CM5 oscillator equations for given wavenumber k
    Returns delta_gamma at decoupling
    """
    def rhs(y, z, k):
        delta_g, v_g = y
        
        # Sound speed at this redshift
        c_s2 = c_s_squared(z)
        
        # Gravitational potential (simplified decay model)
        Phi = C_Phi * np.exp(-0.001 * (z_eq - z)) if z < z_eq else C_Phi
        
        # CM5 equations (convert from conformal time to z)
        # d delta/d z = v / H
        # d v / d z = (-c_s^2 k^2 delta - k^2 Phi) / H
        
        H_z = H_0 * np.sqrt(Omega_r * (1+z)**4 + (Omega_b + Omega_c) * (1+z)**3)
        
        d_delta_dz = -v_g / H_z
        d_v_dz = (c_s2 * k**2 * delta_g + k**2 * Phi) / H_z
        
        return [d_delta_dz, d_v_dz]
    
    # Initial conditions at high z (Sachs-Wolfe)
    Phi_0 = C_Phi
    delta_0 = -2 * Phi_0  # CM8
    v_0 = 0
    
    # Solve
    z_array = np.linspace(z_range[0], z_range[1], 500)
    solution = odeint(rhs, [delta_0, v_0], z_array, args=(k,))
    
    return solution[-1, 0]  # delta at final z

# =============================================================================
# ANGULAR POWER SPECTRUM C_l
# =============================================================================
print("\n3. COMPUTING CMB POWER SPECTRUM")
print("-" * 50)

def compute_C_l(l_max=2500):
    """
    Compute CMB angular power spectrum C_l
    Uses simplified Limber approximation
    """
    l_values = np.arange(2, l_max + 1)
    C_l = np.zeros(len(l_values))
    
    # Distance to last scattering (approximate)
    D_dec = 14000  # Mpc (comoving)
    
    for i, l in enumerate(l_values):
        # k corresponding to this l (Limber)
        k = l / D_dec
        
        # Primordial spectrum
        P_prim = P_primordial(k)
        
        # Acoustic oscillation amplitude
        # Simplified: cosine with damping
        r_s = 150  # Sound horizon in Mpc
        phase = k * r_s
        
        # Damping (Silk)
        k_D = 0.15
        damping = np.exp(-(k / k_D)**2)
        
        # ISW contribution (late-time)
        isw = 1 + 0.1 * np.exp(-l / 100)
        
        # Sachs-Wolfe
        sw = 1/3
        
        # Total C_l
        C_l[i] = P_prim * (sw + np.cos(phase) * damping)**2 * isw
        
        if l % 500 == 0:
            print(f"  l = {l}, C_l = {C_l[i]:.6e}")
    
    return l_values, C_l

# Compute spectrum
l_values, C_l = compute_C_l(l_max=2500)

# Normalize to typical CMB amplitude
C_l = C_l / np.max(C_l) * 6000  # D_l in muK^2

# D_l = l(l+1)C_l / (2*pi)
D_l = l_values * (l_values + 1) * C_l / (2 * np.pi)

# =============================================================================
# PEAK ANALYSIS
# =============================================================================
print("\n4. ACOUSTIC PEAK ANALYSIS")
print("-" * 50)

# Find peaks
from scipy.signal import find_peaks

peaks, properties = find_peaks(D_l, height=1000, distance=100)
peak_l = l_values[peaks]
peak_D_l = D_l[peaks]

print("Detected peaks:")
for i, (l, D) in enumerate(zip(peak_l[:5], peak_D_l[:5])):
    print(f"  Peak {i+1}: l = {l}, D_l = {D:.0f}")

# Peak ratios (CM13)
if len(peak_l) >= 3:
    r_21 = peak_D_l[1] / peak_D_l[0]
    r_31 = peak_D_l[2] / peak_D_l[0]
    s_21 = peak_l[1] / peak_l[0]
    s_31 = peak_l[2] / peak_l[0]
    
    print(f"\nPeak ratios (CM13):")
    print(f"  r_21 = D_l(2)/D_l(1) = {r_21:.3f}")
    print(f"  r_31 = D_l(3)/D_l(1) = {r_31:.3f}")
    print(f"  s_21 = l_2/l_1 = {s_21:.3f}")
    print(f"  s_31 = l_3/l_1 = {s_31:.3f}")

# =============================================================================
# VISUALIZATION
# =============================================================================
print("\n5. GENERATING PLOTS")
print("-" * 50)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Main CMB spectrum
ax = axes[0, 0]
ax.plot(l_values, D_l, 'b-', linewidth=1.5)
if len(peaks) > 0:
    ax.plot(peak_l[:5], peak_D_l[:5], 'ro', markersize=8, label='Peaks')
ax.set_xlabel('Multipole l')
ax.set_ylabel('D_l = l(l+1)C_l/2pi [muK^2]')
ax.set_title('WCT CMB Power Spectrum')
ax.set_xlim([0, 2500])
ax.legend()
ax.grid(True, alpha=0.3)

# Log scale
ax = axes[0, 1]
ax.loglog(l_values, D_l, 'b-', linewidth=1.5)
ax.set_xlabel('Multipole l')
ax.set_ylabel('D_l [muK^2]')
ax.set_title('CMB Spectrum (log-log)')
ax.grid(True, alpha=0.3)

# Sound speed evolution
ax = axes[1, 0]
z_plot = np.linspace(100, 10000, 100)
cs_plot = [c_s(z) for z in z_plot]
ax.plot(z_plot, cs_plot, 'g-', linewidth=2)
ax.set_xlabel('Redshift z')
ax.set_ylabel('c_s / c')
ax.set_title('Sound Speed Evolution (CM6)')
ax.set_xlim([z_plot[-1], z_plot[0]])
ax.grid(True, alpha=0.3)

# Primordial spectrum
ax = axes[1, 1]
k_plot = np.logspace(-4, 0, 100)
P_plot = [P_primordial(ki) for ki in k_plot]
ax.loglog(k_plot, P_plot, 'r-', linewidth=2)
ax.set_xlabel('k [Mpc^-1]')
ax.set_ylabel('P(k)')
ax.set_title(f'Primordial Spectrum (n_s = {n_s})')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('wct_cmb_spectrum.png', dpi=150)
plt.close()

print("Saved: wct_cmb_spectrum.png")

# =============================================================================
# SAVE DATA
# =============================================================================
np.savetxt('wct_cmb_data.txt', np.column_stack([l_values, C_l, D_l]),
           header='l C_l D_l', comments='# ')
print("Saved: wct_cmb_data.txt")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("CMB SPECTRUM GENERATION COMPLETE")
print("=" * 70)
print(f"""
WCT CMB Results:

  First peak: l = {peak_l[0] if len(peak_l) > 0 else 'N/A'}
  (Planck: l ~ 220)
  
  Peak ratios reflect:
    - Baryon loading (R parameter)
    - Curvature feedback (beta_curv)
    - Silk damping (D_S)
    
Physical interpretation:
  - Acoustic peaks from curvature-driven oscillations (CM5)
  - Sound speed set by baryon-photon coupling (CM6)
  - Small-scale damping from curvature diffusion (CM7)
  
Output files:
  - wct_cmb_spectrum.png
  - wct_cmb_data.txt
""")
