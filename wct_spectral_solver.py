# WCT Numerical Solver: Spectral (Fourier-Space) Evolution
# Windows-compatible version
#
# Solves WCT equations entirely in Fourier space for efficiency.
# Tracks spectral entropy and mode dynamics.

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftfreq

print("=" * 70)
print("WCT SPECTRAL SOLVER (Fourier-Space)")
print("=" * 70)

# =============================================================================
# PARAMETERS
# =============================================================================
print("\n1. SIMULATION PARAMETERS")
print("-" * 50)

# Spatial domain
L = 2 * np.pi * 10  # Large domain for good k-resolution
N = 512
dx = L / N
x = np.linspace(0, L, N, endpoint=False)

# Wavenumbers
k = fftfreq(N, dx) * 2 * np.pi
k_abs = np.abs(k)

# Time parameters
dt = 0.001
T_max = 10.0
n_steps = int(T_max / dt)
save_every = 100

# WCT parameters
eps = 1e-6
alpha = 1.0
g = 0.5

# Band-pass parameters (Swift-Hohenberg)
k_star = 1.0      # Target wavenumber
sigma_k = 0.5     # Band width
mu = 0.1          # Growth rate

print(f"N = {N}, L = {L:.2f}")
print(f"k_max = {np.max(k):.2f}")
print(f"Target k* = {k_star}, band width sigma = {sigma_k}")

# =============================================================================
# SPECTRAL OPERATORS
# =============================================================================
print("\n2. SPECTRAL OPERATORS")
print("-" * 50)

# Band-pass filter (selects modes near k*)
def band_filter(k, k_star, sigma):
    """Gaussian band-pass centered at k*"""
    return np.exp(-(np.abs(k) - k_star)**2 / (2 * sigma**2))

# Growth rate function (E12)
def growth_rate(k, mu, k_star, sigma):
    """sigma(k) = mu * band_filter - damping at other k"""
    band = band_filter(k, k_star, sigma)
    return mu * band - 0.1 * (1 - band)  # Positive near k*, negative elsewhere

growth = growth_rate(k, mu, k_star, sigma_k)

print("Band-pass filter defined with Gaussian profile")
print(f"Growth rate: positive for |k - k*| < ~{2*sigma_k:.1f}")

# =============================================================================
# INITIAL CONDITION
# =============================================================================
print("\n3. INITIAL CONDITION")
print("-" * 50)

# Start with broadband noise
np.random.seed(42)
psi = 0.1 * np.random.randn(N) + 1j * 0.1 * np.random.randn(N)
psi_hat = fft(psi)

# Initial spectral power
power_initial = np.abs(psi_hat)**2

print("Initial: Complex Gaussian white noise")
print(f"Total initial power: {np.sum(power_initial):.4f}")

# =============================================================================
# SPECTRAL ENTROPY
# =============================================================================
def spectral_entropy(psi_hat):
    """Compute spectral entropy H_k (E30)"""
    power = np.abs(psi_hat)**2
    total = np.sum(power) + 1e-20
    P_k = power / total  # Normalized probability
    P_k = np.where(P_k > 1e-20, P_k, 1e-20)  # Avoid log(0)
    H = -np.sum(P_k * np.log(P_k))
    return H

def spectral_concentration(psi_hat, k, k_star, delta_k=0.5):
    """Fraction of power in target band (E62)"""
    power = np.abs(psi_hat)**2
    total = np.sum(power) + 1e-20
    mask = np.abs(np.abs(k) - k_star) < delta_k
    return np.sum(power[mask]) / total

# =============================================================================
# TIME EVOLUTION (SPECTRAL)
# =============================================================================
print("\n4. SPECTRAL EVOLUTION")
print("-" * 50)

# Storage
psi_hat_history = [psi_hat.copy()]
times = [0.0]
entropies = [spectral_entropy(psi_hat)]
concentrations = [spectral_concentration(psi_hat, k, k_star)]

print("Running spectral evolution...")

for step in range(n_steps):
    # Transform to real space for nonlinear term
    psi = ifft(psi_hat)
    
    # Nonlinear term: -g|psi|^2 psi
    nonlinear = -g * np.abs(psi)**2 * psi
    nonlinear_hat = fft(nonlinear)
    
    # Linear spectral evolution
    # d psi_hat/dt = growth(k) * psi_hat + nonlinear_hat
    
    # Semi-implicit Euler for linear part
    psi_hat = (psi_hat + dt * nonlinear_hat) / (1 - dt * growth)
    
    # Apply weak damping at very high k (stability)
    damping = np.exp(-0.001 * k**4 * dt)
    psi_hat = psi_hat * damping
    
    # Save
    if (step + 1) % save_every == 0:
        psi_hat_history.append(psi_hat.copy())
        times.append((step + 1) * dt)
        entropies.append(spectral_entropy(psi_hat))
        concentrations.append(spectral_concentration(psi_hat, k, k_star))
        
        if len(times) % 20 == 0:
            print(f"  t = {times[-1]:.2f}, H = {entropies[-1]:.2f}, eta = {concentrations[-1]:.3f}")

print(f"Evolution complete. {len(times)} snapshots.")

# =============================================================================
# ANALYSIS
# =============================================================================
print("\n5. SPECTRAL ANALYSIS")
print("-" * 50)

# Final power spectrum
power_final = np.abs(psi_hat_history[-1])**2

# Find dominant mode
k_positive = k[k > 0]
power_positive = power_final[k > 0]
k_dominant = k_positive[np.argmax(power_positive)]

print(f"Initial entropy: H = {entropies[0]:.4f}")
print(f"Final entropy: H = {entropies[-1]:.4f}")
print(f"Entropy reduction: {(entropies[0] - entropies[-1])/entropies[0]*100:.1f}%")
print(f"\nInitial concentration: eta = {concentrations[0]:.4f}")
print(f"Final concentration: eta = {concentrations[-1]:.4f}")
print(f"\nDominant wavenumber: k = {k_dominant:.3f} (target: {k_star})")

# =============================================================================
# VISUALIZATION
# =============================================================================
print("\n6. GENERATING PLOTS")
print("-" * 50)

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Initial power spectrum
ax = axes[0, 0]
ax.semilogy(k[k > 0], power_initial[k > 0], 'b-', alpha=0.5, label='Initial')
ax.semilogy(k[k > 0], power_final[k > 0], 'r-', linewidth=2, label='Final')
ax.axvline(k_star, color='g', linestyle='--', label=f'k* = {k_star}')
ax.set_xlabel('k')
ax.set_ylabel('Power')
ax.set_title('Power Spectrum Evolution')
ax.legend()
ax.grid(True)
ax.set_xlim([0, 3*k_star])

# Entropy vs time
ax = axes[0, 1]
ax.plot(times, entropies, 'b-', linewidth=2)
ax.set_xlabel('Time')
ax.set_ylabel('Spectral Entropy H')
ax.set_title('Entropy Decay (E30)')
ax.grid(True)

# Concentration vs time
ax = axes[0, 2]
ax.plot(times, concentrations, 'r-', linewidth=2)
ax.set_xlabel('Time')
ax.set_ylabel('Concentration eta')
ax.set_title('Mode Concentration (E62)')
ax.grid(True)

# Real-space evolution
ax = axes[1, 0]
for i in [0, len(times)//4, len(times)//2, -1]:
    psi_real = np.real(ifft(psi_hat_history[i]))
    ax.plot(x, psi_real, alpha=0.7, label=f't={times[i]:.1f}')
ax.set_xlabel('x')
ax.set_ylabel('Re(psi)')
ax.set_title('Real-Space Evolution')
ax.legend()
ax.grid(True)

# Spectrogram (time-frequency)
ax = axes[1, 1]
spectrogram = np.array([np.abs(h)**2 for h in psi_hat_history])
# Only show positive k
k_mask = (k > 0) & (k < 3*k_star)
im = ax.imshow(np.log10(spectrogram[:, k_mask].T + 1e-10), 
               aspect='auto', origin='lower',
               extent=[0, T_max, 0, k[k_mask][-1]], cmap='hot')
ax.set_xlabel('Time')
ax.set_ylabel('k')
ax.set_title('Spectrogram (log power)')
plt.colorbar(im, ax=ax)

# Growth rate function
ax = axes[1, 2]
ax.plot(k[k > 0], growth[k > 0], 'b-', linewidth=2)
ax.axhline(0, color='k', linestyle='-', alpha=0.3)
ax.axvline(k_star, color='r', linestyle='--', label=f'k* = {k_star}')
ax.set_xlabel('k')
ax.set_ylabel('Growth rate')
ax.set_title('Spectral Growth Function (E12)')
ax.legend()
ax.grid(True)
ax.set_xlim([0, 3*k_star])

plt.tight_layout()
plt.savefig('wct_spectral_evolution.png', dpi=150)
plt.close()

print("Saved: wct_spectral_evolution.png")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SIMULATION COMPLETE")
print("=" * 70)
print(f"""
Key Results:
  
  1. SPECTRAL ENTROPY (E30):
     Initial H = {entropies[0]:.4f}
     Final H = {entropies[-1]:.4f}
     Entropy decreased by {(entropies[0] - entropies[-1])/entropies[0]*100:.1f}%
     
  2. MODE CONCENTRATION (E62):
     Initial eta = {concentrations[0]:.4f}
     Final eta = {concentrations[-1]:.4f}
     Power concentrated in target band
     
  3. DOMINANT WAVENUMBER:
     k_dominant = {k_dominant:.3f}
     k_target = {k_star}
     Ratio = {k_dominant/k_star:.3f}
     
Physical Interpretation:
  - Broadband noise self-organizes into band-limited state
  - Entropy decreases as power concentrates (E31-E34)
  - Selected wavelength lambda = 2*pi/k = {2*np.pi/k_dominant:.2f}
  - Consistent with WCT spectral selection (E12-E16)

Output: wct_spectral_evolution.png
""")
