# WCT Master Equation Architecture

This document defines the structural equations audited by `wct_sympy`.
The registry IDs are `M1` through `M8`, with the linear and nonlinear operator sectors separated as `M6A` and `M6B`.

## M1 — Curvature Locking Functional

For a closed loop `Gamma`, weight `w(s)`, phase `phi(s)`, curvature `kappa(s)`, and torsion `tau(s)`, define

```math
sigma(s)=\sqrt{kappa(s)^2+tau(s)^2}
```

```math
S_lock[phi]=\oint_Gamma w(s)(partial_s phi-sigma(s))^2 ds.
```

The associated mass identification is conditional on phase-curvature locking and

```math
m=(hbar/c)<sigma>_w.
```

## M2 — Nonsingular Curvature Operator and Lyapunov Candidate

Define the modulus-squared regularized reciprocal

```math
R_epsilon(psi)=conj(psi)/(|psi|^2+epsilon^2 exp(-2 alpha |psi|^2)),
```

and the curvature operator

```math
Theta_epsilon[psi]=-(Delta psi) R_epsilon(psi).
```

For `epsilon>0`, the denominator is strictly positive for every complex `psi`. For nonzero `psi`,

```math
R_epsilon(psi) -> 1/psi
```

as `epsilon -> 0`. The Lyapunov candidate is

```math
E_WCT[psi]=int(|grad psi|^2+|Theta_epsilon[psi]|^2) dx.
```

## M3 — Finite-Band Spectral Selector

```math
partial_t A = mu A-g|A|^2A-b(Delta+k_*^2)^2A,  b>0.
```

The Fourier growth rate contains

```math
-b(k^2-k_*^2)^2,
```

so off-shell ultraviolet modes are damped.

## M4 — Dimensional Stability Threshold

```math
H^2(Omega) -> L^infinity(Omega)  when  2>n/2.
```

For integer spatial dimension this gives `n<=3`.

## M5 — Curvature-Bounded Computation

```math
psi^(t+1)(x)=U(psi^t(x),{psi^t(y):y in N(x)}).
```

The model is constrained by a finite curvature resource functional. Complexity equivalences remain conditional on the computational model and encoding.

## M6A — Unified Linear Operator

```math
L_WCT=c1(Delta+sigma^2)-c2(Delta+k_*^2)^2+i c3 m+c4 R^(-(2+n/p)),  c2>0.
```

## M6B — Nonlinear Curvature Operator

```math
N_curv[psi]=-(Delta psi) conj(psi)/(|psi|^2+epsilon^2 exp(-2 alpha |psi|^2)).
```

The operator is registered as a proposed nonlinear curvature operator; uniqueness remains an open theorem obligation.

## M7 — Full Curvature-Wavefield Equation

```math
partial_t psi=N_curv[psi]+g|psi|^2psi+c1(Delta+sigma^2)psi-c2(Delta+k_*^2)^2psi+i c3 m psi+c4 R^(-(2+n/p))psi+eta psi circle xi(t),  c2>0.
```

The explicit negative fourth-order sign supplies finite-band damping.

## M8 — Curvature-Acoustic Cosmology System

The phenomenological system couples curvature, an effective potential, acoustic perturbations, damping, and log-periodic modulation:

```math
Phi(k,t)=-C_Phi Theta(k,t)/k^2,
```

```math
delta_g(E)=A_g cos(k_l log(E/E_0)+phi).
```

This sector is classified as open pending derivation, parameter closure, and data-level tests.

## Audit policy

Each master equation is classified as one of `PASS`, `FAIL`, `CONDITIONAL`, `DEFINITION`, or `OPEN`. A SymPy `PASS` means the encoded algebraic, dimensional, or counterexample check passed; it is not a Lean proof or empirical validation.
