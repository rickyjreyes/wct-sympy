# WCT Derived Obligations — Batch 1

This document discharges the first set of `CONDITIONAL` and `OPEN` symbolic obligations in the 142-object WCT registry.

A result is promoted to `PASS` only as an implication under the assumptions stated below. The physical interpretation of the equations is not treated as experimentally established by these derivations.

## Status delta

| Status | Before | After | Delta |
|---|---:|---:|---:|
| `PASS` | 51 | 59 | +8 |
| `FAIL` | 0 | 0 | 0 |
| `CONDITIONAL` | 32 | 27 | -5 |
| `DEFINITION` | 23 | 26 | +3 |
| `OPEN` | 36 | 30 | -6 |
| **Total** | **142** | **142** | **0** |

The apparent `DEFINITION` delta is \(+3\), not \(+4\), because `E9` moves from `DEFINITION` to `PASS` while `CM12`, `CM13`, `CM16`, and `CM18` move from `OPEN` to `DEFINITION`.

---

## 1. E5 — Effective-wavenumber chain

### Definitions

Let:

- \(\Gamma\) be a closed loop;
- \(s\) be arclength;
- \(L_s=\oint_\Gamma ds>0\) be loop length;
- \(w(s)>0\) be the loop weight;
- \(\sigma(s)\) be the curvature spectral rate;
- \(arphi(s)\) be phase;
- \(n\in\mathbb Z\) be winding number.

The locking action is

$$
S[\varphi]
=
\oint_\Gamma w(s)\bigl(\partial_s\varphi-\sigma\bigr)^2ds
+
\Lambda\left(\oint_\Gamma\partial_s\varphi\,ds-2\pi n\right).
$$

### Variation

For \(arphi\mapstoarphi+\epsilon\eta\),

$$
\delta S
=
\oint_\Gamma
\left[2w(\partial_s\varphi-\sigma)+\Lambda\right]
\partial_s\eta\,ds.
$$

Integration by parts on a closed loop gives

$$
\partial_s\left[2w(\partial_s\varphi-\sigma)+\Lambda\right]=0.
$$

Therefore there is a constant \(\alpha\) such that

$$
w(\partial_s\varphi-\sigma)=\alpha,
$$

hence

$$
\partial_s\varphi
=
\sigma+\frac{\alpha}{w}.
$$

The winding condition gives

$$
2\pi n
=
\oint_\Gamma\sigma\,ds
+
\alpha\oint_\Gamma\frac{ds}{w(s)},
$$

so

$$
\alpha
=
\frac{2\pi n-\oint_\Gamma\sigma\,ds}
{\oint_\Gamma ds/w(s)}.
$$

### Exact-lock theorem

Exact locking means \(\alpha=0\). Therefore

$$
\oint_\Gamma\sigma\,ds=2\pi n.
$$

After absorbing orientation into \(|n|\),

$$
\frac{2\pi|n|}{L_s}
=
\frac{1}{L_s}\oint_\Gamma\sigma\,ds.
$$

If \(w(s)=w_0>0\) is constant, then

$$
\langle\sigma\rangle_w
=
\frac{\oint_\Gamma w_0\sigma\,ds}
{\oint_\Gamma w_0\,ds}
=
\frac{1}{L_s}\oint_\Gamma\sigma\,ds.
$$

Thus

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

### Worked example

For a circle of radius \(R=2\),

$$
\kappa=\frac12,
\qquad
\tau=0,
\qquad
\sigma=\frac12,
\qquad
L_s=4\pi.
$$

For \(n=1\),

$$
\oint_\Gamma\sigma\,ds
=
\frac12(4\pi)
=
2\pi,
$$

and therefore

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

### Definitions

Let

$$
\psi=\sqrt{u}\,e^{i\theta},
\qquad
u>0.
$$

Define the normalized phase current by

$$
\mathbf S
:=
\operatorname{Im}(\bar\psi\nabla\psi).
$$

### Derivation

Differentiate:

$$
\nabla\psi
=
e^{i\theta}
\left(
\nabla\sqrt{u}
+i\sqrt{u}\nabla\theta
\right).
$$

Multiply by \(ar\psi=\sqrt{u}e^{-i\theta}\):

$$
\bar\psi\nabla\psi
=
\frac12\nabla u
+i\,u\nabla\theta.
$$

Taking the imaginary part gives

$$
\boxed{
\mathbf S=u\nabla\theta
}.
$$

Thus `E9` is a derived identity once phase flux is defined as the normalized polar current.

### Worked example

Take

$$
u(x)=4,
\qquad
\theta(x)=3x.
$$

Then

$$
\psi(x)=2e^{3ix},
$$

and

$$
\operatorname{Im}(\bar\psi\,\partial_x\psi)
=
\operatorname{Im}\left(2e^{-3ix}\cdot6ie^{3ix}\right)
=12.
$$

Also

$$
u\,\partial_x\theta=4\cdot3=12.
$$

---

## 3. E13 and E14 — Band-pass functional and gradient flow

### Definitions

Let \(A\) be a complex amplitude. Define

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

Assume periodic boundary conditions or sufficient decay so that boundary terms vanish.

### Functional derivative

Treating \(A\) and \(ar A\) as independent variables,

$$
\frac{\delta\mathcal E}{\delta\bar A}
=
-rA+a\Delta A+b\Delta^2A+\beta|A|^2A.
$$

The negative \(L^2\)-gradient flow is

$$
\partial_tA
=-\frac{\delta\mathcal E}{\delta\bar A}.
$$

Therefore

$$
\boxed{
\partial_tA
=
rA-a\Delta A-b\Delta^2A-\beta|A|^2A
}.
$$

Since

$$
\sigma(k)=r+ak^2-bk^4,
$$

and Fourier transformation sends

$$
\Delta\mapsto-k^2,
\qquad
\Delta^2\mapsto k^4,
$$

this is equivalent to

$$
\boxed{
\partial_tA
=
\sigma(-i\nabla)A-\beta|A|^2A
}.
$$

Thus `E13` follows from `E14` under the stated boundary assumptions.

### Worked one-mode example

For

$$
A(x,t)=q(t)e^{ikx},
$$

one has

$$
\Delta A=-k^2A,
\qquad
\Delta^2A=k^4A.
$$

Hence

$$
\dot q
=
(r+ak^2-bk^4)q-\beta|q|^2q.
$$

Taking

$$
r=1,
\quad
a=2,
\quad
b=1,
\quad
k=1,
\quad
\beta=1,
\quad
q=1,
$$

produces

$$
\dot q=(1+2-1)-1=1.
$$

---

## 4. E18 — Positivity and Lyapunov descent

### Definition

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

with

$$
c_1\ge0,
\qquad
c_2\ge0.
$$

Then

$$
\boxed{\mathcal E[\psi]\ge0}.
$$

### Gradient-flow theorem

Assume

$$
\partial_t\psi
=-\frac{\delta\mathcal E}{\delta\bar\psi}.
$$

The variational chain rule gives

$$
\frac{d\mathcal E}{dt}
=
2\operatorname{Re}
\left\langle
\frac{\delta\mathcal E}{\delta\bar\psi},
\partial_t\psi
\right\rangle.
$$

Substitute the flow:

$$
\frac{d\mathcal E}{dt}
=
-2
\left\|
\frac{\delta\mathcal E}{\delta\bar\psi}
\right\|_2^2
\le0.
$$

Up to the normalization convention for the complex gradient,

$$
\boxed{
\frac{d\mathcal E}{dt}
=-\left\|\frac{\delta\mathcal E}{\delta\bar\psi}\right\|_2^2
\le0
}.
$$

This proves Lyapunov descent for the exact negative gradient flow. It does not prove that the full WCT evolution equation is identical to that gradient flow.

---

## 5. E58 — Bounded band-selective Green kernel

### Definition

Let

$$
G(k)
=
\frac{1}{r+a(k^2-k_*^2)^2},
$$

with

$$
r>0,
\qquad
a>0.
$$

### Bound

Because

$$
a(k^2-k_*^2)^2\ge0,
$$

one has

$$
r+a(k^2-k_*^2)^2\ge r>0.
$$

Therefore

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

For \(r=2\), \(a=3\), and \(k_*=4\),

$$
G(4)=\frac12.
$$

At \(k=5\),

$$
G(5)
=
\frac{1}{2+3(25-16)^2}
=
\frac1{245}
<
\frac12.
$$

---

## 6. CM9 — First-order mode evolution

### Definitions

Start with the photon-like oscillator

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

and

$$
\dot v_\gamma
=-c_s^2k^2\delta_\gamma-k^2\Phi.
$$

Similarly, from

$$
\ddot\delta_b
+\mathcal R c_s^2k^2\delta_\gamma
=-k^2\Phi,
$$

with

$$
v_b:=\dot\delta_b,
$$

one obtains

$$
\dot\delta_b=v_b,
$$

$$
\dot v_b
=-\mathcal R c_s^2k^2\delta_\gamma-k^2\Phi.
$$

Therefore `CM9` is exactly the first-order representation of the `CM5` oscillator equations, provided both use the same coefficient convention.

### Worked example

Take

$$
c_s^2=\frac13,
\qquad
k=2,
\qquad
\delta_\gamma=3,
\qquad
\Phi=1.
$$

Then

$$
\dot v_\gamma
=-\frac13(4)(3)-4
=-8.
$$

Thus the second-order equation gives

$$
\ddot\delta_\gamma=-8,
$$

which is identical because \(v_\gamma=\dot\delta_\gamma\).

---

## 7. CM11 — Gaussian curvature damping

### Mode equation

Assume the curvature-diffusion contribution acts mode by mode as

$$
\dot\delta_k(t)
=-D_{\mathrm{curv}}(t)k^2\delta_k(t).
$$

Divide by \(\delta_k\):

$$
\frac{d}{dt}\ln\delta_k
=-k^2D_{\mathrm{curv}}(t).
$$

Integrating from \(0\) to \(t\),

$$
\ln\frac{\delta_k(t)}{\delta_k(0)}
=-k^2\int_0^tD_{\mathrm{curv}}(t')dt'.
$$

Hence

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

Then

$$
\boxed{
D(k,t)
=
\exp\left(-\frac{k^2}{k_D^2(t)}\right)
}.
$$

### Worked example

For constant diffusivity \(D_{\mathrm{curv}}=0.2\) over \(t=5\),

$$
k_D^{-2}=0.2\cdot5=1,
\qquad
k_D=1.
$$

At \(k=2\),

$$
D(2)=e^{-4}\approx0.0183156.
$$

---

## 8. Definition reclassifications

The following equations do not assert theorem-level consequences. They define observables or a model set and therefore belong in `DEFINITION`, not `OPEN`.

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

Whether that set is physically sufficient remains a separate model-closure question.

---

## Remaining boundary

This batch proves identities and implications internal to the encoded equations. It does not resolve:

- global existence or uniqueness of the full nonlinear PDE;
- coercivity of the complete WCT functional;
- unconditional entropy monotonicity;
- computational lower bounds;
- cosmological parameter closure;
- calibrated agreement with CMB or particle data;
- experimental validity of WCT.
