# wct-sympy

**Executable symbolic audit infrastructure for Wave Confinement Theory**

[![WCT symbolic audit](https://github.com/rickyjreyes/wct-sympy/actions/workflows/sympy.yml/badge.svg)](https://github.com/rickyjreyes/wct-sympy/actions/workflows/sympy.yml)
[![Full SymPy audit](https://github.com/rickyjreyes/wct-sympy/actions/workflows/full-audit.yml/badge.svg)](https://github.com/rickyjreyes/wct-sympy/actions/workflows/full-audit.yml)

`wct-sympy` converts the WCT equation corpus into executable checks for:

- symbolic identities and variational derivatives;
- physical dimensions;
- spectral extrema and sign conventions;
- limiting behavior and denominator safety;
- numerical residuals and explicit counterexamples;
- consistency between equations describing the same quantity.

It is an **audit and regression system**, not a proof that Wave Confinement Theory is physically correct.

## Current audit state

The registry contains **142 stable equation objects**:

- 9 master systems: `M1`-`M8`, with `M6A` and `M6B` separated;
- 83 canonical equations: `E1A`, `E1B`, `E2`-`E82`;
- 10 curvature-locked electron equations: `CLE1`-`CLE10`;
- 20 curvature-acoustic cosmology equations: `CM1`-`CM20`;
- 5 logarithmic or auxiliary equations: `G1`, `EX`, `EY`, `EZ`, `FA`;
- 15 topology and correction objects: `TOP1`-`TOP9`, `CORR1`-`CORR6`.

| Status | Count | Meaning |
|---|---:|---|
| `PASS` | **51** | The encoded algebraic, dimensional, numerical, or logical check succeeds under its declared assumptions. |
| `FAIL` | **0** | No currently encoded statement is contradicted by its assigned checker. |
| `CONDITIONAL` | **32** | Explicit sign, domain, regularity, counting, model, or boundary assumptions are still required. |
| `DEFINITION` | **23** | The object is a definition or ansatz rather than a theorem. |
| `OPEN` | **36** | The claim requires analysis, formal proof, calibrated simulation, or experiment beyond SymPy. |
| **Total** | **142** | Complete registry coverage. |

A zero `FAIL` count means

$$
\text{no known contradiction remains in the current encoded statements.}
$$

It does **not** mean that

$$
32\ \text{conditional claims}+36\ \text{open claims}
$$

have been proved or experimentally validated.

## Correction pass

The repository originally encoded 24 contradictions. Each was handled by one of two legitimate operations:

$$
\text{incorrect equation}\longrightarrow\text{corrected equation}
$$

or

$$
\text{unproved unconditional claim}\longrightarrow\text{conditional claim}.
$$

### 1. Nonsingular curvature regularization

$$
R_\varepsilon(\psi)
=
\frac{\bar\psi}
{|\psi|^2+\varepsilon^2e^{-2\alpha|\psi|^2}},
\qquad
\Theta_\varepsilon[\psi]
=
-(\Delta\psi)R_\varepsilon(\psi).
$$

For $\varepsilon>0$, the denominator is strictly positive.

### 2. Finite-band damping sign

$$
\partial_tA
=
\mu A-g|A|^2A-b(\Delta+k_*^2)^2A,
\qquad b>0.
$$

The Fourier contribution is $-b(k^2-k_*^2)^2$, so ultraviolet modes are damped.

### 3. Weighted locking identity

From $\partial_s\varphi=\sigma+\alpha/w$,

$$
\oint_\Gamma w\,\partial_s\varphi\,ds
=
\oint_\Gamma w\sigma\,ds+\alpha L_s.
$$

### 4. Curvature regularity split

$$
\psi\in H^2,\quad |D_\varepsilon(\psi)|\ge\delta>0
\Longrightarrow
\|\Theta_\varepsilon[\psi]\|_{L^2}
\le
\delta^{-1}\|\Delta\psi\|_{L^2}.
$$

Bounded curvature requires stronger regularity:

$$
\psi\in H^s,\qquad s>\frac n2+2
\Longrightarrow
\Theta_\varepsilon[\psi]\in L^\infty.
$$

### 5. Entropy and support direction

For support size $K$,

$$
H\le\log K,
\qquad
e^H\le K.
$$

### 6. Quality factor and power balance

$$
Q=\omega\frac{U}{P_{\mathrm{loss}}},
$$

$$
\frac{dW}{dt}
=
P_{\mathrm{in}}+P_{\mathrm{fusion}}-P_{\mathrm{loss}}-P_{\mathrm{out}}.
$$

### 7. Effective mass from a spectral gap

If

$$
\omega_j^2=c^2\lambda_j+\Delta_*,
$$

then

$$
m_{\mathrm{eff}}^2
=
\frac{\hbar^2\Delta_*}{c^4}.
$$

### 8. Selected wavelength

From

$$
k_* = \sqrt{\frac{a}{2b}},
$$

the corresponding wavelength is

$$
\lambda_*
=
\frac{2\pi}{k_*}
=
2\pi\sqrt{\frac{2b}{a}}.
$$

### 9. Curvature-locked electron sector

The radius/eigenvalue convention is

$$
-\Delta\psi=\sigma_*^2\psi,
\qquad
R=\frac1{\sigma_*}.
$$

Periodic angular modes form the integer family

$$
f(\theta)=A\cos(m\theta)+B\sin(m\theta),
\qquad m\in\mathbb Z_{\ge0},
$$

rather than a unique constant solution.

### 10. Coherence length

$$
\xi_{\mathrm{coh}}
=
\left(\sum_k p_k|k|^2\right)^{-1/2}
=
\left(
\frac{\int|\psi|^2dx}
{\int|\nabla\psi|^2dx}
\right)^{1/2}.
$$

## Repository boundaries

| Repository or document | Responsibility |
|---|---|
| `rickyjreyes/wct-sympy` | Algebra, dimensions, limits, numerical residuals, consistency checks, and executable counterexamples. |
| `rickyjreyes/wct-lean` | Kernel-checked definitions, assumptions, lemmas, and theorems. |
| `MASTER_EQUATIONS.md` | Canonical master architecture. |
| `EQUATIONS.md` | Canonical equation families and corrected forms. |
| `equations/full_registry.yaml` | Stable equation IDs, checker assignments, and expected statuses. |
| `interoperability/lean_map.yaml` | Explicit SymPy-to-Lean relationship metadata. |

A SymPy `PASS` is never reported as a Lean proof. `PROVED` is reserved for declarations successfully checked by the Lean kernel.

## Reproduce the audit

```bash
git clone https://github.com/rickyjreyes/wct-sympy.git
cd wct-sympy
python -m pip install -r requirements.txt
pytest -q
python scripts/check_all.py
python scripts/check_full_coverage.py
python scripts/check_full_coverage.py --strict-theory
python scripts/check_lean_coverage.py
```

The CI matrix runs the full audit on Python 3.10, 3.11, and 3.12.

## Generated outputs

```text
tables/wct_sympy_checks.csv
tables/wct_full_coverage.csv
tables/wct_full_coverage.json
tables/lean_coverage.json
COVERAGE_MATRIX.md
FULL_COVERAGE_STATUS.txt
```

These outputs make the registry machine-readable for notebooks, documentation systems, graph databases, and formalization workflows.

## Project layout

```text
wct_sympy/          symbolic audit implementation
equations/          machine-readable registries
interoperability/   SymPy-to-Lean declaration map
scripts/            command-line entry points
tests/              regression tests
tables/             generated reports
```

## Audit policy

Every equation object must have:

1. a stable ID;
2. a canonical source location;
3. an assigned checker;
4. an expected scientific status;
5. regression coverage when executable semantics exist.

A claim is not labeled `PASS` merely because it is syntactically represented. It must satisfy an actual symbolic, dimensional, numerical, or logical check. Claims requiring PDE existence theory, global convergence, uniqueness, phenomenological calibration, or experiment remain `CONDITIONAL` or `OPEN` until those obligations are discharged.

## Primary documentation

- [`MASTER_EQUATIONS.md`](MASTER_EQUATIONS.md)
- [`EQUATIONS.md`](EQUATIONS.md)
- [`FULL_COVERAGE.md`](FULL_COVERAGE.md)
- [`COVERAGE_MATRIX.md`](COVERAGE_MATRIX.md)
- [`WCT_GAP_ANALYSIS.md`](WCT_GAP_ANALYSIS.md)

## Scientific interpretation

The repository currently establishes

$$
\boxed{
\text{internal symbolic consistency of the corrected encoded equation set}
}
$$

It does not yet establish

$$
\boxed{
\text{global PDE well-posedness, uniqueness, physical completeness, or empirical validity of WCT}
}
$$

Those remaining obligations belong to formal analysis, Lean formalization, calibrated simulation, and experiment.