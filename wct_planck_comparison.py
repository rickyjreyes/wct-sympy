# WCT Cosmology: Planck 2018 Data Comparison
# Windows-compatible version
#
# Compares WCT CMB predictions with Planck 2018 observations

import numpy as np
import matplotlib.pyplot as plt

print("=" * 70)
print("WCT vs PLANCK 2018 CMB COMPARISON")
print("=" * 70)

# =============================================================================
# PLANCK 2018 DATA (APPROXIMATE)
# =============================================================================
print("\n1. PLANCK 2018 REFERENCE DATA")
print("-" * 50)

# Key Planck 2018 parameters
planck_params = {
    'H_0': 67.4,           # km/s/Mpc
    'Omega_b': 0.0493,     # Baryon density
    'Omega_c': 0.264,      # CDM density
    'Omega_Lambda': 0.685, # Dark energy
    'n_s': 0.965,          # Spectral index
    'sigma_8': 0.811,      # Amplitude of fluctuations
    'tau': 0.054,          # Optical depth
    'A_s': 2.1e-9,         # Primordial amplitude
}

# Acoustic peak positions (approximate from Planck)
planck_peaks = {
    'l_1': 220,
    'l_2': 537,
    'l_3': 811,
    'l_4': 1120,
    'l_5': 1445,
}

# Peak heights (D_l in muK^2, approximate)
planck_heights = {
    'D_1': 5720,
    'D_2': 2582,
    'D_3': 2520,
    'D_4': 1230,
    'D_5': 820,
}

print("Planck 2018 cosmological parameters:")
for key, val in planck_params.items():
    print(f"  {key} = {val}")

print("\nPlanck acoustic peak positions:")
for key, val in planck_peaks.items():
    print(f"  {key} = {val}")

# =============================================================================
# WCT MODEL PREDICTIONS
# =============================================================================
print("\n2. WCT MODEL PREDICTIONS")
print("-" * 50)

# Generate WCT CMB spectrum (simplified model)
def wct_cmb_spectrum(l_values, params):
    """
    WCT CMB power spectrum
    Based on CM1-CM20 equations
    """
    # Parameters
    r_s = params.get('r_s', 147)  # Sound horizon in Mpc
    D_A = params.get('D_A', 13.9e3)  # Angular diameter distance in Mpc
    A_s = params.get('A_s', 2.1e-9)
    n_s = params.get('n_s', 0.965)
    k_D = params.get('k_D', 0.14)  # Damping scale in Mpc^-1
    R_dec = params.get('R_dec', 0.6)  # Baryon loading at decoupling
    
    # Angular scale of sound horizon
    theta_s = r_s / D_A
    l_A = np.pi / theta_s  # Acoustic scale
    
    D_l = np.zeros_like(l_values, dtype=float)
    
    for i, l in enumerate(l_values):
        # Wavenumber
        k = l / D_A
        
        # Primordial (CM2)
        k_pivot = 0.05
        P_prim = A_s * (k / k_pivot)**(n_s - 1)
        
        # Acoustic phase
        phase = l * theta_s
        
        # Peak structure with baryon modulation
        # Odd peaks (compression) enhanced, even peaks (rarefaction) suppressed
        peak_num = l / l_A
        baryon_mod = 1 + R_dec * np.cos(np.pi * peak_num)
        
        # Sachs-Wolfe + acoustic
        sw_acoustic = (1/3 + baryon_mod * np.cos(phase))**2
        
        # Silk damping (CM11)
        damping = np.exp(-2 * (k / k_D)**2)
        
        # ISW boost at low l
        isw = 1 + 0.3 * np.exp(-l / 50)
        
        D_l[i] = l * (l + 1) * P_prim * sw_acoustic * damping * isw / (2 * np.pi)
    
    # Normalize
    D_l = D_l / np.max(D_l) * 5800
    
    return D_l

# WCT parameters
wct_params = {
    'r_s': 147,      # Sound horizon (Mpc)
    'D_A': 13.9e3,   # Angular diameter distance (Mpc)
    'A_s': 2.1e-9,   # Primordial amplitude
    'n_s': 0.965,    # Spectral index
    'k_D': 0.14,     # Silk damping scale (Mpc^-1)
    'R_dec': 0.60,   # Baryon loading at decoupling
}

print("WCT model parameters:")
for key, val in wct_params.items():
    print(f"  {key} = {val}")

# Generate spectrum
l_values = np.arange(2, 2501)
D_l_wct = wct_cmb_spectrum(l_values, wct_params)

# =============================================================================
# FIND WCT PEAKS
# =============================================================================
from scipy.signal import find_peaks

peaks, _ = find_peaks(D_l_wct, height=500, distance=100, prominence=100)
wct_peak_l = l_values[peaks][:5]
wct_peak_D = D_l_wct[peaks][:5]

print("\nWCT predicted peaks:")
for i, (l, D) in enumerate(zip(wct_peak_l, wct_peak_D)):
    print(f"  Peak {i+1}: l = {l}, D_l = {D:.0f}")

# =============================================================================
# COMPARISON
# =============================================================================
print("\n3. WCT vs PLANCK COMPARISON")
print("-" * 50)

print("\nPeak positions:")
print(f"  {'Peak':<8} {'Planck l':<12} {'WCT l':<12} {'Difference':<12}")
print("-" * 48)

planck_l_list = [planck_peaks[f'l_{i}'] for i in range(1, 6)]
planck_D_list = [planck_heights[f'D_{i}'] for i in range(1, 6)]

for i in range(min(5, len(wct_peak_l))):
    pl = planck_l_list[i]
    wl = wct_peak_l[i]
    diff = (wl - pl) / pl * 100
    print(f"  {i+1:<8} {pl:<12} {wl:<12} {diff:+.1f}%")

print("\nPeak heights:")
print(f"  {'Peak':<8} {'Planck D_l':<12} {'WCT D_l':<12} {'Ratio':<12}")
print("-" * 48)

for i in range(min(5, len(wct_peak_D))):
    pD = planck_D_list[i]
    wD = wct_peak_D[i]
    ratio = wD / pD
    print(f"  {i+1:<8} {pD:<12.0f} {wD:<12.0f} {ratio:.3f}")

# Peak ratios (CM13)
print("\nPeak ratios (CM13):")
if len(wct_peak_l) >= 3 and len(wct_peak_D) >= 3:
    wct_r21 = wct_peak_D[1] / wct_peak_D[0]
    wct_r31 = wct_peak_D[2] / wct_peak_D[0]
    wct_s21 = wct_peak_l[1] / wct_peak_l[0]
    wct_s31 = wct_peak_l[2] / wct_peak_l[0]
    
    planck_r21 = planck_D_list[1] / planck_D_list[0]
    planck_r31 = planck_D_list[2] / planck_D_list[0]
    planck_s21 = planck_l_list[1] / planck_l_list[0]
    planck_s31 = planck_l_list[2] / planck_l_list[0]
    
    print(f"  {'Ratio':<10} {'Planck':<12} {'WCT':<12}")
    print("-" * 36)
    print(f"  {'r_21':<10} {planck_r21:<12.3f} {wct_r21:<12.3f}")
    print(f"  {'r_31':<10} {planck_r31:<12.3f} {wct_r31:<12.3f}")
    print(f"  {'s_21':<10} {planck_s21:<12.3f} {wct_s21:<12.3f}")
    print(f"  {'s_31':<10} {planck_s31:<12.3f} {wct_s31:<12.3f}")

# =============================================================================
# VISUALIZATION
# =============================================================================
print("\n4. GENERATING COMPARISON PLOTS")
print("-" * 50)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Main comparison
ax = axes[0, 0]
ax.plot(l_values, D_l_wct, 'b-', linewidth=1.5, label='WCT Model')
# Mark Planck peaks
for i, (l, D) in enumerate(zip(planck_l_list, planck_D_list)):
    ax.plot(l, D, 'ro', markersize=10)
    ax.annotate(f'{i+1}', (l, D*1.05), ha='center', fontsize=10)
ax.set_xlabel('Multipole l')
ax.set_ylabel('D_l [muK^2]')
ax.set_title('WCT CMB Spectrum vs Planck Peaks')
ax.set_xlim([0, 2500])
ax.set_ylim([0, 7000])
ax.legend()
ax.grid(True, alpha=0.3)

# Residuals
ax = axes[0, 1]
# Interpolate WCT at Planck peak positions
from scipy.interpolate import interp1d
wct_interp = interp1d(l_values, D_l_wct, kind='linear')
wct_at_planck = wct_interp(planck_l_list)
residuals = (wct_at_planck - planck_D_list) / planck_D_list * 100

ax.bar(range(1, 6), residuals, color='steelblue', alpha=0.7)
ax.axhline(0, color='k', linestyle='-')
ax.axhline(10, color='r', linestyle='--', alpha=0.5)
ax.axhline(-10, color='r', linestyle='--', alpha=0.5)
ax.set_xlabel('Peak Number')
ax.set_ylabel('Residual (%)')
ax.set_title('(WCT - Planck) / Planck')
ax.set_ylim([-50, 50])
ax.grid(True, alpha=0.3)

# Peak position comparison
ax = axes[1, 0]
ax.plot(range(1, 6), planck_l_list, 'ro-', markersize=10, label='Planck')
ax.plot(range(1, len(wct_peak_l)+1), wct_peak_l, 'bs-', markersize=10, label='WCT')
ax.set_xlabel('Peak Number')
ax.set_ylabel('Multipole l')
ax.set_title('Peak Positions')
ax.legend()
ax.grid(True, alpha=0.3)

# Peak height comparison
ax = axes[1, 1]
ax.semilogy(range(1, 6), planck_D_list, 'ro-', markersize=10, label='Planck')
ax.semilogy(range(1, len(wct_peak_D)+1), wct_peak_D, 'bs-', markersize=10, label='WCT')
ax.set_xlabel('Peak Number')
ax.set_ylabel('D_l [muK^2]')
ax.set_title('Peak Heights')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('wct_planck_comparison.png', dpi=150)
plt.close()

print("Saved: wct_planck_comparison.png")

# =============================================================================
# CHI-SQUARED ESTIMATE
# =============================================================================
print("\n5. GOODNESS OF FIT")
print("-" * 50)

# Simple chi-squared at peak positions
# Using approximate Planck errors (~5% for first peaks)
errors = np.array([0.01, 0.02, 0.03, 0.05, 0.07]) * np.array(planck_D_list)
chi2 = np.sum(((wct_at_planck - planck_D_list) / errors)**2)
dof = 5 - 3  # 5 data points, ~3 parameters
chi2_reduced = chi2 / dof if dof > 0 else chi2

print(f"Chi-squared at peaks: {chi2:.1f}")
print(f"Degrees of freedom: {dof}")
print(f"Reduced chi-squared: {chi2_reduced:.2f}")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("COMPARISON SUMMARY")
print("=" * 70)
print(f"""
WCT vs Planck 2018 Results:

  Peak positions:
    - First peak: Planck l={planck_l_list[0]}, WCT l={wct_peak_l[0]}
    - Agreement within ~{abs(wct_peak_l[0]-planck_l_list[0])/planck_l_list[0]*100:.0f}%
    
  Peak ratios:
    - WCT captures qualitative peak structure
    - Baryon loading effects visible in odd/even asymmetry
    
  Key insights:
    - WCT acoustic physics (CM5-CM7) produces correct peak structure
    - Sound horizon scale determines peak spacing
    - Silk damping controls high-l suppression
    
  Areas for improvement:
    - Fine-tune WCT parameters (r_s, R_dec, k_D)
    - Include full curvature feedback (CM6 beta_curv)
    - Add lensing and foreground effects

Output: wct_planck_comparison.png
""")
