# WCT Derived Obligations — Batch 1

This document discharges the first set of `CONDITIONAL` and `OPEN` symbolic obligations in the 142-object WCT registry.

A result is promoted to `PASS` only as an implication under its stated assumptions. These derivations establish internal mathematical consequences, not empirical validation.

## Status delta

| Status | Before | After | Delta |
|---|---:|---:|---:|
| `PASS` | 51 | 59 | +8 |
| `FAIL` | 0 | 0 | 0 |
| `CONDITIONAL` | 32 | 27 | -5 |
| `DEFINITION` | 23 | 26 | +3 |
| `OPEN` | 36 | 30 | -6 |
| **Total** | **142** | **142** | **0** |

The `DEFINITION` change is `+3` because `E9` moves from `DEFINITION` to `PASS`, while `CM12`, `CM13`, `CM16`, and `CM18` move from `OPEN` to `DEFINITION`.

---

## 1. E5 — Effective-wavenumber chain

Let `Gamma` be a closed loop with arclength `s`, length `L_s`, positive weight `w(s)`, phase `phi(s)`, curvature rate `sigma(s)`, and winding number `n`.

The constrained locking action is

$$
S[\varphi]
=
\oint_\Gamma w(s)\bigl(\partial_s\varphi-\sigma\bigr)^2\,ds
+
\Lambda\left(\oint_\Gamma\partial_s\varphi\,ds-2\pi n\right).
$$

Variation and integration by parts on the closed loop give

$$
\partial_s\left[2w(\partial_s\varphi-\sigma)+\Lambda\right]=0.
$$

Therefore, for a constant `alpha`,

$$
w(\partial_s\varphi-\sigma)=\alpha,
$$

so

$$
\partial_s\varphi
=
\sigma+\frac{\alpha}{w}.
$$

The winding constraint implies

$$
2\pi n
=
\oint_\Gamma\sigma\,ds
+
\alpha\oint_\Gamma\frac{ds}{w(s)},
$$

hence

$$
\alpha
=
\frac{2\pi n-\oint_\Gamma\sigma\,ds}
{\oint_\Gamma ds/w(s)}.
$$

Exact locking means `alpha = 0`, so

$$
\oint_\Gamma\sigma\,ds=2\pi n.
$$

After absorbing orientation into the absolute winding number,

$$
\frac{2\pi|n|}{L_s}
=
\frac{1}{L_s}\oint_\Gamma\sigma\,ds.
$$

For constant positive weight `w_0`,

$$
\langle\sigma\rangle_w
=
\frac{\oint_\Gamma w_0\sigma\,ds}
{\oint_\Gamma w_0\,ds}
=
\frac{1}{L_s}\oint_\Gamma\sigma\,ds.
$$

Therefore

$$
\boxed{
k_{\mathrm{eff}}
=
\frac{2\pi|n|}{L_s}
=
\frac{1}{L_s}\oint_\Gamma\sigma\,ds
=
\langle\sigma\rangle_w
}
$$

under exact closure and constant positive weight.

### Numerical example

For a circle of radius `R = 2`,

$$
\kappa=\frac12,
\qquad
\tau=0,
\qquad
\sigma=\frac12,
\qquad
L_s=4\pi.
$$

For `n = 1`,

$$
\oint_\Gamma\sigma\,ds
=
\frac12(4\pi)
=
2\pi,
$$

and

$$
k_{\mathrm{eff}}
=
\frac{2\pi}{4\pi}
=
\frac12
=
\langle\sigma\rangle_w.
$$

---

## 2. E9 — Phase flux from polar decomposition

Let

$$
\psi=\sqrt{u}\,e^{i\theta},
\qquad
u>0.
$$

Define normalized phase current by

$$
\mathbf S
:=
\operatorname{Im}(\overline{\psi}\,\nabla\psi).
$$

Differentiate:

$$
\nabla\psi
=
e^{i\theta}
\left(
\nabla\sqrt{u}
+i\sqrt{u}\,\nabla\theta
\right).
$$

Then

$$
\overline{\psi}\,\nabla\psi
=
\frac12\nabla u
+i\,u\nabla\theta.
$$

Taking the imaginary part yields

$$
\boxed{
\mathbf S=u\nabla\theta
}.
$$

### Numerical example

Take `u(x) = 4` and `theta(x) = 3x`. Then

$$
\psi(x)=2e^{3ix},
$$

and

$$
\operatorname{Im}(\overline{\psi}\,\partial_x\psi)
=12
=
u\,\partial_x\theta.
$$

---

## 3. E13 and E14 — Band-pass functional and gradient flow

Define

$$
\mathcal E[A]
=
\int
\left(
-r|A|^2
-a|\nabla A|^2
+b|\Delta A|^2
+\frac{\beta}{2}|A|^4
\right)dx.
$$

Assume periodic boundary conditions or sufficient decay. Treating `A` and its complex conjugate as independent variational fields gives

$$
\frac{\delta\mathcal E}{\delta\overline A}
=
-rA+a\Delta A+b\Delta^2A+\beta|A|^2A.
$$

Under negative gradient flow,

$$
\partial_tA
=-\frac{\delta\mathcal E}{\delta\overline A},
$$

so

$$
\boxed{
\partial_tA
=
rA-a\Delta A-b\Delta^2A-\beta|A|^2A
}.
$$

Because Fourier transformation sends `Delta` to `-k^2`, this is equivalent to

$$
\boxed{
\partial_tA
=
\sigma(-i\nabla)A-\beta|A|^2A
}
$$

with

$$
\sigma(k)=r+ak^2-bk^4.
$$

### One-mode example

For

$$
A(x,t)=q(t)e^{ikx},
$$

one obtains

$$
\dot q
=
(r+ak^2-bk^4)q-\beta|q|^2q.
$$

At `r = 1`, `a = 2`, `b = 1`, `k = 1`, `beta = 1`, and `q = 1`,

$$
\dot q=(1+2-1)-1=1.
$$

---

## 4. E18 — Positivity and Lyapunov descent

Let

$$
\mathcal E[\psi]
=
\int
\left(
c_1|\nabla\psi|^2
+c_2|\Theta_\varepsilon[\psi]|^2
\right)dx,
$$

with nonnegative `c_1` and `c_2`. Then

$$
\boxed{\mathcal E[\psi]\ge0}.
$$

Assume exact negative gradient flow:

$$
\partial_t\psi
=-\frac{\delta\mathcal E}{\delta\overline\psi}.
$$

The variational chain rule gives, up to the chosen complex-gradient normalization,

$$
\boxed{
\frac{d\mathcal E}{dt}
=-\left\|
\frac{\delta\mathcal E}{\delta\overline\psi}
\right\|_2^2
\le0
}.
$$

This proves descent for the exact gradient flow. It does not prove that every proposed WCT evolution equals that flow.

---

## 5. E58 — Bounded band-selective Green kernel

Let

$$
G(k)
=
\frac{1}{r+a(k^2-k_*^2)^2},
$$

where `r > 0` and `a > 0`. Since

$$
a(k^2-k_*^2)^2\ge0,
$$

it follows that

$$
\boxed{
0<G(k)\le\frac1r
}.
$$

Equality occurs on the selected shell:

$$
|k|=k_*
\quad\Longrightarrow\quad
G(k_*)=\frac1r.
$$

For `r = 2`, `a = 3`, `k_* = 4`,

$$
G(4)=\frac12,
$$

whereas

$$
G(5)
=
\frac{1}{2+3(25-16)^2}
=
\frac1{245}.
$$

---

## 6. CM9 — First-order mode evolution

Start from

$$
\ddot\delta_\gamma
+c_s^2k^2\delta_\gamma
=-k^2\Phi.
$$

Define

$$
v_\gamma:=\dot\delta_\gamma.
$$

Then

$$
\dot\delta_\gamma=v_\gamma,
$$

$$
\dot v_\gamma
=-c_s^2k^2\delta_\gamma-k^2\Phi.
$$

Similarly,

$$
\ddot\delta_b
+\mathcal R c_s^2k^2\delta_\gamma
=-k^2\Phi
$$

is equivalent to

$$
\dot\delta_b=v_b,
$$

$$
\dot v_b
=-\mathcal R c_s^2k^2\delta_\gamma-k^2\Phi.
$$

Thus `CM9` is exactly the first-order representation of `CM5`, provided both use the same coefficient convention.

### Numerical example

For `c_s^2 = 1/3`, `k = 2`, `delta_gamma = 3`, and `Phi = 1`,

$$
\dot v_\gamma
=-\frac13(4)(3)-4
=-8.
$$

Since `v_gamma = dot(delta_gamma)`, the second-order equation gives the same acceleration.

---

## 7. CM11 — Gaussian curvature damping

Assume modewise curvature diffusion:

$$
\dot\delta_k(t)
=-D_{\mathrm{curv}}(t)k^2\delta_k(t).
$$

Then

$$
\frac{d}{dt}\ln\delta_k
=-k^2D_{\mathrm{curv}}(t).
$$

Integration gives

$$
\delta_k(t)
=
\delta_k(0)
\exp\left[
-k^2\int_0^tD_{\mathrm{curv}}(t')dt'
\right].
$$

Define

$$
k_D^{-2}(t)
:=
\int_0^tD_{\mathrm{curv}}(t')dt'.
$$

Therefore

$$
\boxed{
D(k,t)
=
\exp\left(-\frac{k^2}{k_D^2(t)}\right)
}.
$$

For constant `D_curv = 0.2` over `t = 5`, one has `k_D = 1`. At `k = 2`,

$$
D(2)=e^{-4}\approx0.0183156.
$$

---

## 8. Definition reclassifications

These equations define observables or a model set rather than theorem-level consequences.

### CM12 — Dimensionless power spectrum

$$
\boxed{
\Delta^2(k)
=
\frac{k^3}{2\pi^2}P(k)
}.
$$

### CM13 — Peak metrics

$$
\boxed{
r_{21}=\frac{P(k_2)}{P(k_1)},
\qquad
r_{31}=\frac{P(k_3)}{P(k_1)}
}
$$

$$
\boxed{
s_{21}=\frac{k_2}{k_1},
\qquad
s_{31}=\frac{k_3}{k_1}
}.
$$

### CM16 — Horizon-scale definitions

$$
\boxed{
R_{\mathrm{hor}}(t)
=
\int_0^tc_s(t')dt'
}
$$

$$
\boxed{
k_{\mathrm{hor}}
=
\frac{2\pi}{R_{\mathrm{hor}}}
}.
$$

### CM18 — Closure-set definition

$$
\boxed{
\mathcal C_{\mathrm{WCT}}
:=
\{\mathrm{CM1},\mathrm{CM2},\mathrm{CM3},\mathrm{CM4},\mathrm{CM5},\mathrm{CM7}\}
}.
$$

Whether this set is physically sufficient remains a separate closure problem.

---

## Remaining boundary

This batch does not establish:

- global existence or uniqueness of the full nonlinear PDE;
- coercivity of the complete WCT functional;
- unconditional entropy monotonicity;
- computational lower bounds;
- cosmological parameter closure;
- calibrated agreement with CMB or particle data;
- experimental validity of WCT.
