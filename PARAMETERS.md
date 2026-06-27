# WCT Parameters -- Origins and Derivations

This document tracks the physical meaning and derivation status of all parameters used in Wave Confinement Theory calculations.

---

## Status Key

| Symbol | Meaning |
|--------|---------|
| [OK] | Derived from first principles or measured constants |
| [FIT] | Fitted to match observations |
| [?] | Origin unclear / needs documentation |
| [GEO] | Geometric or structural constant |

---

## 1. Fundamental Constants (External)

These are measured values from CODATA, not derived by WCT.

| Parameter | Value | Units | Source |
|-----------|-------|-------|--------|
| c | 2.99792458 x 10^8 | m/s | CODATA 2018 |
| hbar | 1.054571817 x 10^-34 | J*s | CODATA 2018 |
| G | 6.67430 x 10^-11 | m^3/kg/s^2 | CODATA 2018 |
| e | 1.602176634 x 10^-19 | C | CODATA 2018 |
| epsilon_0 | 8.8541878128 x 10^-12 | F/m | CODATA 2018 |

---

## 2. WCT Structural Parameters

### 2.1 Coherence Scale xi

| Parameter | Value | Status | Notes |
|-----------|-------|--------|-------|
| xi | 10^-5 m (10 um) | [?] | Used in suppression, fractal dimension |
| xi_0 | 10^-5 m | [?] | Initial coherence in recursive shells |

**Questions**:
- Is this the Compton wavelength of some particle?
- Electron Compton: lambda_C = h/(m_e c) ~= 2.4 x 10^-12 m (not 10 um)
- What physical scale does 10 um represent?

**Possible derivation**:
```
xi = 1/sqrt(W_psi)  where W_psi is the curvature scalar
If W_psi ~ 10^10 m^-2, then xi ~ 10^-5 m [OK]
```

---

### 2.2 Recursive Shell Parameters

| Parameter | Value | Status | Notes |
|-----------|-------|--------|-------|
| r | 0.5646 | [?][FIT] | Shell contraction ratio |
| beta | 3.95 | [?][FIT] | Curvature exponent |
| gamma | 0.05 | [?][FIT] | Entropy feedback coefficient |

**Used in**:
```python
E_n = r^(beta*n) x exp(-gamma*n)     # Suppression factor
xi_n = xi_0 x r^n                 # Shell coherence length
D_f = -log(E_n) / log(1/xi_n)   # Fractal dimension
```

**Key relationships**:
- As n -> inf: D_f -> beta + gamma/|ln(r)| ~= 4.04
- r = 0.5646 ~= 1/sqrt(pi) ~= 0.5642 (coincidence?)
- r ~= (1 - 1/e) ~= 0.632? No.
- r ~= 1 - alpha_fine ~= 0.9927? No.

**TODO**: Determine if r, beta, gamma are:
1. Derived from fundamental constants
2. Fitted to particle physics data
3. Chosen for mathematical convenience
4. Related to known ratios (pi, e, alpha, etc.)

---

### 2.3 Curvature Operator Parameters

| Parameter | Symbol | Value | Status | Notes |
|-----------|--------|-------|--------|-------|
| Regularization | epsilon | ~10^-10 | [GEO] | Prevents division by zero |
| Feedback | alpha | varies | [?] | In exp(-alpha|psi|^2) |
| Curvature weight | c_2 | 1 | [GEO] | In Lyapunov functional |
| Gradient weight | c_1 | 1 | [GEO] | In Lyapunov functional |

**Theta operator**:
$$\Theta[\psi] = -\frac{\nabla^2\psi}{\psi + \varepsilon e^{-\alpha|\psi|^2}}$$

---

### 2.4 Cosmology Parameters (CM equations)

| Parameter | Symbol | Status | Notes |
|-----------|--------|--------|-------|
| Potential coupling | C_Phi | [?] | Phi = -C_Phi Theta/k^2 |
| Sound speed coeff | beta_curv | [?] | In c_s^2 formula |
| Compression ratio | R(t) | [OK] | E_comp/E_rad |
| Diffusion | D_curv | [OK] | <|grad psi|^2>/<|psi|^2> |

---

## 3. Derived Quantities

These are calculated from the parameters above.

| Quantity | Formula | From Parameters |
|----------|---------|-----------------|
| Planck length | l_P = sqrt(hbarG/c^3) | c, G, hbar |
| Planck time | t_P = sqrt(hbarG/c^5) | c, G, hbar |
| Planck mass | m_P = sqrt(hbarc/G) | c, G, hbar |
| Fine-structure alpha | e^2/(4piepsilon_0hbarc) | e, epsilon_0, hbar, c |
| Cosmo constant Lambda | 1/xi^2 | xi |

---

## 4. Parameter Relationships to Investigate

### 4.1 Is r related to known constants?

```python
import numpy as np

r = 0.5646

# Test various relationships
print(f"r = {r}")
print(f"1/sqrt(pi) = {1/np.sqrt(np.pi):.4f}")           # 0.5642 <- CLOSE!
print(f"1/sqrt(e) = {1/np.sqrt(np.e):.4f}")            # 0.6065
print(f"alpha_fine = {1/137.036:.4f}")                 # 0.0073
print(f"1 - 1/sqrt(2) = {1 - 1/np.sqrt(2):.4f}")       # 0.2929
print(f"ln(2)/ln(pi) = {np.log(2)/np.log(np.pi):.4f}")  # 0.6055
print(f"2/pi - 1/pi^2 = {2/np.pi - 1/np.pi**2:.4f}") # 0.5355
```

**Result**: r ~= 1/sqrt(pi) to 0.07% -- significant?

### 4.2 Is beta related to dimensional constraints?

```python
beta = 3.95

# Spatial dimension bound is n <= 3
# Fractal dimension limit: D_f -> beta + gamma/|ln(r)| ~= 4.04
# This approaches 4 -- the dimension of spacetime?

print(f"beta = {beta}")
print(f"beta + gamma/|ln(r)| = {beta + 0.05/abs(np.log(0.5646)):.2f}")  # ~4.04
```

**Hypothesis**: beta ~= 4 - gamma/|ln(r)| to ensure D_f -> 4 (spacetime dimension)?

---

## 5. Open Questions

1. **Where does r = 0.5646 come from?**
   - Is it 1/sqrt(pi)?
   - Is it fitted to particle data?
   - Is it derived from curvature constraints?

2. **Why beta ~= 3.95?**
   - Is this tuned so D_f -> 4?
   - Does it come from Sobolev embedding (n <= 3)?

3. **What sets gamma = 0.05?**
   - Entropy production rate?
   - Fitted to CMB or particle spectrum?

4. **What physical system has xi = 10 um?**
   - This is macroscopic, not Planckian
   - Could be related to vacuum fluctuation scale?

---

## 6. Recommended Actions

1. [ ] Search papers/notes for original derivation of r, beta, gamma
2. [ ] Test if r = 1/sqrt(pi) exactly and document why
3. [ ] Verify if beta is chosen to give D_f -> 4
4. [ ] Determine if parameters were fitted to data (which data?)
5. [ ] Add derivation comments to all scripts using these values

---

## References

- `wct_validate_suppression.py` -- uses r, beta, gamma
- `wct_validate_fractal_dimension.py` -- uses r, beta, gamma, xi_0
- `wct_validate_time_to_energy.py` -- uses r, beta, gamma
- `EQUATIONS.md` -- E28-E34 (alpha-drop, entropy reduction)
