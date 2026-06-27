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

### Phase-flux and finite-band selection

`E9`-`E16` cover phase flux, winding, shell closure, and

```math
sigma(k)=r+a k^2-b k^4,
k_*=sqrt(a/(2b)).
```

### Curvature feedback

`E17`-`E23` cover

```math
Theta[psi]=-Delta psi/(psi+epsilon exp(-alpha|psi|^2))
```

and its Lyapunov and cavity sectors.

### Dimensional stability

`E24`-`E27` and `E65`-`E70` cover the threshold

```math
H^2(Omega)->L^infinity(Omega), 2>n/2,
```

which gives integer `n<=3`.

### Entropy and recursive state evolution

`E28`-`E36` and `E72`-`E81` cover alpha-drop, entropy, support, recursive decay, and information-cost claims. The audit checks the standard bound `exp(H)<=K` for support size `K`.

### Computation and resources

`E37`-`E43` and `E71`-`E80` cover bandlimits, channel capacity, physical resources, and model-relative complexity statements.

### Cavity and effective mass

`E44`-`E56` cover quality factor, power balance, gap dimensions, commutators, and effective potentials.

### Spectral projection

`E57`-`E64` cover shell symbols, Green kernels, projections, thresholds, and the wavelength implied by `k_*=sqrt(a/(2b))`.

### Curvature-locked electron

`CLE1`-`CLE10` cover locking, toroidal separation, periodic modes, eigenmodes, and radius/eigenvalue conventions.

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
