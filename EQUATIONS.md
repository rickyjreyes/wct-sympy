# WCT Canonical Equation Families

This index corresponds to the 142 objects in `equations/full_registry.yaml`. Executable semantics are in `wct_sympy/full_checks_*.py`.

## Audit statuses

`PASS` means the encoded implication follows. `FAIL` means algebra, dimensions, logic, or a counterexample contradicts it. `CONDITIONAL` requires added assumptions. `DEFINITION` is not a theorem. `OPEN` requires analysis or experiment beyond SymPy.

## Families

### Rest energy and loop locking

`E1A`, `E1B`, `E2`-`E8` cover

```math
sigma_dens=kappa^2+tau^2,
sigma=sqrt(kappa^2+tau^2),
m=(hbar/c)<sigma>_w.
```

The corrected weighted lock identity is

```math
oint_Gamma w partial_s(phi) ds
=
oint_Gamma w sigma ds + alpha L_s.
```

### Phase-flux and finite-band selection

`E9`-`E16` cover phase flux, winding, shell closure, and

```math
sigma(k)=r+a k^2-b k^4,
k_*=sqrt(a/(2b)).
```

### Curvature feedback

`E17`-`E23` use the nonsingular regularized reciprocal

```math
R_epsilon(psi)=conj(psi)/(|psi|^2+epsilon^2 exp(-2 alpha |psi|^2)),
```

and

```math
Theta_epsilon[psi]=-(Delta psi)R_epsilon(psi).
```

The denominator is strictly positive for `epsilon>0`.

### Dimensional stability

`E24`-`E27` and `E65`-`E70` distinguish two regularity statements:

```math
psi in H^2, |D_epsilon(psi)|>=delta
  => ||Theta_epsilon[psi]||_L2 <= delta^(-1)||Delta psi||_L2,
```

and

```math
psi in H^s, s>n/2+2
  => Theta_epsilon[psi] in L^infinity.
```

The exact embedding threshold `H^2 -> L^infinity` gives integer `n<=3`; nonlinear subcriticality is a separate hypothesis.

### Entropy and recursive state evolution

`E28` uses retained fractions `rho_t in (0,1]`:

```math
alpha(n)=1+(1/n) sum_t log_2(rho_t)+beta(n),
```

with the explicit condition

```math
beta(n)<-(1/n)sum_t log_2(rho_t)
```

when `alpha(n)<1` is required.

`E31` is conditional on a model-specific entropy-production proof. `E32`, `E41`, and `E72` remain conditional because the corrected exponent does not by itself prove the configuration-count bound.

For support size `K`,

```math
H<=log K,
exp(H)<=K.
```

### Computation and resources

`E37`-`E43` and `E71`-`E80` cover bandlimits, channel capacity, physical resources, and model-relative complexity statements.

### Cavity and effective mass

`E44`-`E56` include the corrected relations

```math
Q_eff=omega U/P_loss,
```

```math
dW/dt=P_in+P_fusion-P_loss-P_out,
```

and, for

```math
omega_j^2=c^2 lambda_j+Delta_*,
```

```math
m_eff^2=hbar^2 Delta_*/c^4.
```

### Spectral projection

`E57`-`E64` cover shell symbols, Green kernels, projections, thresholds, and

```math
lambda_*=2 pi/k_*=2 pi sqrt(2b/a).
```

### Curvature-locked electron

`CLE1`-`CLE10` use the consistent inverse-length convention

```math
-Delta psi=sigma_*^2 psi,
R=1/sigma_*.
```

For the real one-dimensional reduction with

```math
q=-psi_xx/psi-sigma_*^2,
```

the corrected generalized Euler-Lagrange equation is

```math
q psi_xx/psi^2-psi_xx-d_x^2(q/psi)=0.
```

Periodic angular modes form the family

```math
f(theta)=A cos(m theta)+B sin(m theta),  m in Z_{\ge 0}.
```

A torus eigenmode is not unique without an added lowest-mode, winding, chirality, normalization, and phase-selection principle; `CLE8` is therefore conditional.

### Coherence length

The corrected spectral/physical-space coherence length is

```math
xi_coh=(sum_k p_k |k|^2)^(-1/2)
```

or equivalently

```math
xi_coh=sqrt(int |psi|^2 dx / int |grad psi|^2 dx).
```

### Logarithmic transforms

`G1`, `EX`, `EY`, `EZ`, and `FA` cover log-periodic modulation, the logarithmic Laplacian identity, and Cole-Hopf reduction.

### Curvature-acoustic cosmology

`CM1`-`CM20` cover curvature density, acoustic perturbations, damping, peak metrics, horizons, and closure laws. These remain open pending full derivation and calibrated data tests.

### Topology and corrections

`TOP1`-`TOP9` and `CORR1`-`CORR6` ensure topology definitions and correction notes are included in coverage accounting.

## Complete coverage

- Master systems: `M1`-`M5`, `M6A`, `M6B`, `M7`, `M8`
- Canonical equations: `E1A`, `E1B`, `E2`-`E82`
- Electron family: `CLE1`-`CLE10`
- Cosmology: `CM1`-`CM20`
- Log sector: `G1`, `EX`, `EY`, `EZ`, `FA`
- Topology/corrections: `TOP1`-`TOP9`, `CORR1`-`CORR6`

Total: **142 registered equation objects**.
