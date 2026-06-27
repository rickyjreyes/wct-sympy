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

## M2 — Curvature Operator and Lyapunov Candidate

```math
Theta[psi]=-Delta psi/(psi+epsilon exp(-alpha|psi|^2)).
```

```math
E_WCT[psi]=int(|grad psi|^2+|Theta[psi]|^2) dx.
```

The audit explicitly tests whether the displayed denominator is globally nonzero; it is not without an admissible-set restriction.

## M3 — Finite-Band Spectral Selector

```math
partial_t A = mu A-g|A|^2A+b(Delta+k_*^2)^2A.
```

For `b>0`, off-shell suppression requires a negative sign in front of the fourth-order term, or an explicitly negative coefficient.

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
L_WCT=c1(Delta+sigma^2)+c2(Delta+k_*^2)^2+i c3 m+c4 R^(-(2+n/p)).
```

## M6B — Nonlinear Curvature Operator

```math
N_curv[psi]=-Delta psi/(psi+epsilon exp(-alpha|psi|^2)).
```

The operator is registered as a proposed nonlinear curvature operator; uniqueness is an open theorem obligation.

## M7 — Full Curvature-Wavefield Equation

```math
partial_t psi=N_curv[psi]+g|psi|^2psi+c1(Delta+sigma^2)psi+c2(Delta+k_*^2)^2psi+i c3 m psi+c4 R^(-(2+n/p))psi+eta psi circle xi(t).
```

Finite-band damping requires the sign condition on `c2` stated under M3.

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

Each master equation is classified as one of `PASS`, `FAIL`, `CONDITIONAL`, `DEFINITION`, or `OPEN`. A `FAIL` means a stated implication is contradicted by algebra, dimensions, or a counterexample; it does not mean the software failed.
