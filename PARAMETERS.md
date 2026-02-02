# WCT Parameters — Origins and Derivations

This document tracks the physical meaning and derivation status of all parameters used in Wave Confinement Theory calculations.

---

## Status Key

| Symbol | Meaning |
|--------|---------|
| ✓ | Derived from first principles or measured constants |
| ⚡ | Fitted to match observations |
| ❓ | Origin unclear / needs documentation |
| 📐 | Geometric or structural constant |

---

## 1. Fundamental Constants (External)

These are measured values from CODATA, not derived by WCT.

| Parameter | Value | Units | Source |
|-----------|-------|-------|--------|
| c | 2.99792458 × 10⁸ | m/s | CODATA 2018 |
| ℏ | 1.054571817 × 10⁻³⁴ | J·s | CODATA 2018 |
| G | 6.67430 × 10⁻¹¹ | m³/kg/s² | CODATA 2018 |
| e | 1.602176634 × 10⁻¹⁹ | C | CODATA 2018 |
| ε₀ | 8.8541878128 × 10⁻¹² | F/m | CODATA 2018 |

---

## 2. WCT Structural Parameters

### 2.1 Coherence Scale ξ

| Parameter | Value | Status | Notes |
|-----------|-------|--------|-------|
| ξ | 10⁻⁵ m (10 μm) | ❓ | Used in suppression, fractal dimension |
| ξ₀ | 10⁻⁵ m | ❓ | Initial coherence in recursive shells |

**Questions**:
- Is this the Compton wavelength of some particle?
- Electron Compton: λ_C = h/(m_e c) ≈ 2.4 × 10⁻¹² m (not 10 μm)
- What physical scale does 10 μm represent?

**Possible derivation**:
```
ξ = 1/√W_ψ  where W_ψ is the curvature scalar
If W_ψ ~ 10¹⁰ m⁻², then ξ ~ 10⁻⁵ m ✓
```

---

### 2.2 Recursive Shell Parameters

| Parameter | Value | Status | Notes |
|-----------|-------|--------|-------|
| r | 0.5646 | ❓⚡ | Shell contraction ratio |
| β | 3.95 | ❓⚡ | Curvature exponent |
| γ | 0.05 | ❓⚡ | Entropy feedback coefficient |

**Used in**:
```python
E_n = r^(β·n) × exp(-γ·n)     # Suppression factor
ξ_n = ξ₀ × r^n                 # Shell coherence length
D_f = -log(E_n) / log(1/ξ_n)   # Fractal dimension
```

**Key relationships**:
- As n → ∞: D_f → β + γ/|ln(r)| ≈ 4.04
- r = 0.5646 ≈ 1/√π ≈ 0.5642 (coincidence?)
- r ≈ (1 - 1/e) ≈ 0.632? No.
- r ≈ 1 - α_fine ≈ 0.9927? No.

**TODO**: Determine if r, β, γ are:
1. Derived from fundamental constants
2. Fitted to particle physics data
3. Chosen for mathematical convenience
4. Related to known ratios (π, e, α, etc.)

---

### 2.3 Curvature Operator Parameters

| Parameter | Symbol | Value | Status | Notes |
|-----------|--------|-------|--------|-------|
| Regularization | ε | ~10⁻¹⁰ | 📐 | Prevents division by zero |
| Feedback | α | varies | ❓ | In exp(-α|ψ|²) |
| Curvature weight | c₂ | 1 | 📐 | In Lyapunov functional |
| Gradient weight | c₁ | 1 | 📐 | In Lyapunov functional |

**Θ operator**:
$$\Theta[\psi] = -\frac{\nabla^2\psi}{\psi + \varepsilon e^{-\alpha|\psi|^2}}$$

---

### 2.4 Cosmology Parameters (CM equations)

| Parameter | Symbol | Status | Notes |
|-----------|--------|--------|-------|
| Potential coupling | C_Φ | ❓ | Φ = -C_Φ Θ/k² |
| Sound speed coeff | β_curv | ❓ | In c_s² formula |
| Compression ratio | R(t) | ✓ | E_comp/E_rad |
| Diffusion | D_curv | ✓ | ⟨|∇ψ|²⟩/⟨|ψ|²⟩ |

---

## 3. Derived Quantities

These are calculated from the parameters above.

| Quantity | Formula | From Parameters |
|----------|---------|-----------------|
| Planck length | l_P = √(ℏG/c³) | c, G, ℏ |
| Planck time | t_P = √(ℏG/c⁵) | c, G, ℏ |
| Planck mass | m_P = √(ℏc/G) | c, G, ℏ |
| Fine-structure α | e²/(4πε₀ℏc) | e, ε₀, ℏ, c |
| Cosmo constant Λ | 1/ξ² | ξ |

---

## 4. Parameter Relationships to Investigate

### 4.1 Is r related to known constants?

```python
import numpy as np

r = 0.5646

# Test various relationships
print(f"r = {r}")
print(f"1/√π = {1/np.sqrt(np.pi):.4f}")           # 0.5642 ← CLOSE!
print(f"1/√e = {1/np.sqrt(np.e):.4f}")            # 0.6065
print(f"α_fine = {1/137.036:.4f}")                 # 0.0073
print(f"1 - 1/√2 = {1 - 1/np.sqrt(2):.4f}")       # 0.2929
print(f"ln(2)/ln(π) = {np.log(2)/np.log(np.pi):.4f}")  # 0.6055
print(f"2/π - 1/π² = {2/np.pi - 1/np.pi**2:.4f}") # 0.5355
```

**Result**: r ≈ 1/√π to 0.07% — significant?

### 4.2 Is β related to dimensional constraints?

```python
beta = 3.95

# Spatial dimension bound is n ≤ 3
# Fractal dimension limit: D_f → β + γ/|ln(r)| ≈ 4.04
# This approaches 4 — the dimension of spacetime?

print(f"β = {beta}")
print(f"β + γ/|ln(r)| = {beta + 0.05/abs(np.log(0.5646)):.2f}")  # ~4.04
```

**Hypothesis**: β ≈ 4 - γ/|ln(r)| to ensure D_f → 4 (spacetime dimension)?

---

## 5. Open Questions

1. **Where does r = 0.5646 come from?**
   - Is it 1/√π?
   - Is it fitted to particle data?
   - Is it derived from curvature constraints?

2. **Why β ≈ 3.95?**
   - Is this tuned so D_f → 4?
   - Does it come from Sobolev embedding (n ≤ 3)?

3. **What sets γ = 0.05?**
   - Entropy production rate?
   - Fitted to CMB or particle spectrum?

4. **What physical system has ξ = 10 μm?**
   - This is macroscopic, not Planckian
   - Could be related to vacuum fluctuation scale?

---

## 6. Recommended Actions

1. ☐ Search papers/notes for original derivation of r, β, γ
2. ☐ Test if r = 1/√π exactly and document why
3. ☐ Verify if β is chosen to give D_f → 4
4. ☐ Determine if parameters were fitted to data (which data?)
5. ☐ Add derivation comments to all scripts using these values

---

## References

- `wct_validate_suppression.py` — uses r, β, γ
- `wct_validate_fractal_dimension.py` — uses r, β, γ, ξ₀
- `wct_validate_time_to_energy.py` — uses r, β, γ
- `EQUATIONS.md` — E28-E34 (α-drop, entropy reduction)
