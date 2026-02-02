# WCT Numerical Solver: 1D Curvature-Feedback Evolution
# Windows-compatible version
#
# Solves the 1D WCT evolution equation (simplified UWCT):
# d psi/dt = -Theta[psi] + g|psi|^2 psi + diffusion terms
#
# where Theta[psi] = -d^2 psi/dx^2 / (psi + eps * exp(-alpha * |psi|^2))

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftfreq

print("=" * 70)
print("WCT 1D EVOLUTION SOLVER")
print("=" * 70)

# =============================================================================
# PARAMETERS
# =============================================================================
print("\n1. SIMULATION PARAMETERS")
print("-" * 50)

# Spatial domain
L = 10.0          # Domain length
N = 256           # Number of grid points
dx = L / N
x = np.linspace(0, L, N, endpoint=False)

# Time parameters
dt = 0.001        # Time step
T_max = 5.0       # Total simulation time
n_steps = int(T_max / dt)
save_every = 100  # Save frames every N steps

# WCT parameters
eps = 1e-6        # Regularization
alpha = 1.0       # Feedback strength
g = 1.0           # Nonlinear coefficient
D = 0.01          # Diffusion coefficient

print(f"Domain: [0, {L}] with N = {N} points")
print(f"dx = {dx:.4f}, dt = {dt:.4f}")
print(f"Total time: {T_max}, steps: {n_steps}")
print(f"WCT parameters: eps = {eps}, alpha = {alpha}, g = {g}")

# =============================================================================
# INITIAL CONDITION
# =============================================================================
print("\n2. INITIAL CONDITION")
print("-" * 50)

def initial_condition(x, mode='gaussian'):
    """Generate initial wavefunction"""
    if mode == 'gaussian':
        # Gaussian packet
        x0 = L / 2
        sigma = 0.5
        return np.exp(-(x - x0)**2 / (2 * sigma**2)) + 0.1
    elif mode == 'soliton':
        # Soliton-like
        x0 = L / 2
        return 1.0 / np.cosh(2 * (x - x0)) + 0.1
    elif mode == 'random':
        # Random perturbation
        return 0.5 + 0.1 * np.random.randn(len(x))
    else:
        return np.ones_like(x)

psi = initial_condition(x, mode='gaussian').astype(complex)
print(f"Initial mode: Gaussian")
print(f"Initial |psi|^2 integral = {np.sum(np.abs(psi)**2) * dx:.4f}")

# =============================================================================
# OPERATORS
# =============================================================================
print("\n3. OPERATORS")
print("-" * 50)

# Wavenumbers for spectral derivatives
k = fftfreq(N, dx) * 2 * np.pi
k2 = k**2

def laplacian(psi):
    """Spectral Laplacian"""
    psi_hat = fft(psi)
    return np.real(ifft(-k2 * psi_hat))

def theta_operator(psi, eps=eps, alpha=alpha):
    """WCT curvature operator: Theta[psi] = -Laplacian(psi) / (psi + eps*exp(-alpha*|psi|^2))"""
    lap = laplacian(psi)
    denominator = psi + eps * np.exp(-alpha * np.abs(psi)**2)
    # Avoid division by very small numbers
    denominator = np.where(np.abs(denominator) < 1e-10, 1e-10, denominator)
    return -lap / denominator

def rhs(psi):
    """Right-hand side of evolution equation"""
    theta = theta_operator(psi)
    nonlinear = g * np.abs(psi)**2 * psi
    diffusion = D * laplacian(psi)
    return -theta + nonlinear + diffusion

print("Operators defined:")
print("  - Spectral Laplacian (FFT-based)")
print("  - Theta operator (regularized)")
print("  - RHS = -Theta + g|psi|^2 psi + D*Laplacian")

# =============================================================================
# TIME EVOLUTION
# =============================================================================
print("\n4. TIME EVOLUTION")
print("-" * 50)

# Storage for snapshots
snapshots = [psi.copy()]
times = [0.0]

# Energy tracking
def compute_energy(psi):
    """WCT Lyapunov energy (E18)"""
    grad_psi = np.real(ifft(1j * k * fft(psi)))
    E_grad = np.sum(np.abs(grad_psi)**2) * dx
    theta = theta_operator(psi)
    E_theta = np.sum(np.abs(theta)**2) * dx
    return E_grad + E_theta

energies = [compute_energy(psi)]

print("Running evolution...")

# Simple Euler integration (for demonstration)
# For production, use RK4 or implicit methods
for step in range(n_steps):
    # RK2 (midpoint method)
    k1 = rhs(psi)
    k2 = rhs(psi + 0.5 * dt * k1)
    psi = psi + dt * k2
    
    # Save snapshots
    if (step + 1) % save_every == 0:
        snapshots.append(psi.copy())
        times.append((step + 1) * dt)
        energies.append(compute_energy(psi))
        
        if len(times) % 10 == 0:
            print(f"  t = {times[-1]:.2f}, E = {energies[-1]:.4f}")

print(f"Evolution complete. {len(snapshots)} snapshots saved.")

# =============================================================================
# VISUALIZATION
# =============================================================================
print("\n5. GENERATING PLOTS")
print("-" * 50)

# Plot final state
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# |psi|^2 evolution
ax = axes[0, 0]
n_show = min(10, len(snapshots))
for i in range(0, len(snapshots), max(1, len(snapshots)//n_show)):
    ax.plot(x, np.abs(snapshots[i])**2, alpha=0.7, label=f't={times[i]:.1f}')
ax.set_xlabel('x')
ax.set_ylabel('|psi|^2')
ax.set_title('Density Evolution')
ax.legend(loc='upper right', fontsize=8)
ax.grid(True)

# Energy vs time
ax = axes[0, 1]
ax.plot(times, energies, 'b-')
ax.set_xlabel('Time')
ax.set_ylabel('Energy')
ax.set_title('WCT Energy (E18)')
ax.grid(True)

# Curvature profile
ax = axes[1, 0]
theta_final = theta_operator(snapshots[-1])
ax.plot(x, np.real(theta_final))
ax.set_xlabel('x')
ax.set_ylabel('Theta[psi]')
ax.set_title('Final Curvature Profile')
ax.grid(True)

# Spacetime plot
ax = axes[1, 1]
density_matrix = np.array([np.abs(s)**2 for s in snapshots])
im = ax.imshow(density_matrix.T, aspect='auto', origin='lower',
               extent=[0, T_max, 0, L], cmap='viridis')
ax.set_xlabel('Time')
ax.set_ylabel('x')
ax.set_title('Spacetime Density |psi|^2')
plt.colorbar(im, ax=ax)

plt.tight_layout()
plt.savefig('wct_1d_evolution.png', dpi=150)
plt.close()

print("Saved: wct_1d_evolution.png")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SIMULATION COMPLETE")
print("=" * 70)
print(f"""
Results:
  Initial energy: {energies[0]:.6f}
  Final energy:   {energies[-1]:.6f}
  Energy change:  {(energies[-1] - energies[0])/energies[0]*100:.2f}%
  
  Initial norm:   {np.sum(np.abs(snapshots[0])**2)*dx:.6f}
  Final norm:     {np.sum(np.abs(snapshots[-1])**2)*dx:.6f}
  
Output: wct_1d_evolution.png
""")
