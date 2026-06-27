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

- 9 master systems: `M1`–`M8`, with `M6A` and `M6B` separated;
- 83 canonical equations: `E1A`, `E1B`, `E2`–`E82`;
- 10 curvature-locked electron equations: `CLE1`–`CLE10`;
- 20 curvature-acoustic cosmology equations: `CM1`–`CM20`;
- 5 logarithmic or auxiliary equations: `G1`, `EX`, `EY`, `EZ`, `FA`;
- 15 topology and correction objects: `TOP1`–`TOP9`, `CORR1`–`CORR6`.

| Status | Count | Meaning |
|---|---:|---|
| `PASS` | **51** | The encoded algebraic, dimensional, numerical, or logical check succeeds under its declared assumptions. |
| `FAIL` | **0** | No currently encoded statement is contradicted by its assigned checker. |
| `CONDITIONAL` | **32** | Explicit sign, domain, regularity, counting, model, or boundary assumptions are still required. |
| `DEFINITION` | **23** | The object is a definition or ansatz rather than a theorem. |
| `OPEN` | **36** | The claim requires analysis, formal proof, calibrated simulation, or experiment beyond SymPy. |
| **Total** | **142** | Complete registry coverage. |

A zero `FAIL` count means:

```text
No known contradiction remains in the current encoded statements.
```

It does **not** mean that the remaining claims have been proved or experimentally validated:

```text
32 conditional claims + 36 open claims = 68 unresolved obligations
```

## Correction pass

The repository originally encoded 24 contradictions. Each was handled by one of two legitimate operations:

```text
incorrect equation → corrected equation
```

or

```text
unproved unconditional claim → conditional claim
```

### 1. Nonsingular curvature regularization

```text
Rε(ψ) = ψ̄ / (|ψ|² + ε² exp(−2α|ψ|²))
Θε[ψ] = −(Δψ)Rε(ψ)
```

For `ε > 0`, the denominator is strictly positive.

### 2. Finite-band damping sign

```text
∂ₜA = μA − g|A|²A − b(Δ + k⋆²)²A,    b > 0
```

The Fourier contribution is

```text
−b(k² − k⋆²)²
```

so ultraviolet modes are damped.

### 3. Weighted locking identity

From

```text
∂ₛφ = σ + α/w
```

it follows that

```text
∮Γ w ∂ₛφ ds = ∮Γ wσ ds + αLₛ
```

### 4. Curvature regularity split

```text
ψ ∈ H²,  |Dε(ψ)| ≥ δ > 0
    ⇒ ‖Θε[ψ]‖L² ≤ δ⁻¹‖Δψ‖L²
```

Bounded curvature requires stronger regularity:

```text
ψ ∈ Hˢ,  s > n/2 + 2
    ⇒ Θε[ψ] ∈ L∞
```

### 5. Entropy and support direction

For support size `K`:

```text
H ≤ log K
exp(H) ≤ K
```

Equality holds only for a uniform distribution on its support.

### 6. Quality factor and power balance

```text
Q = ωU / P(loss)
```

```text
dW/dt = P(in) + P(fusion) − P(loss) − P(out)
```

### 7. Effective mass from a spectral gap

If

```text
ωⱼ² = c²λⱼ + Δ⋆
```

then

```text
m_eff² = ℏ²Δ⋆ / c⁴
```

### 8. Selected wavelength

From

```text
k⋆ = √(a / 2b)
```

it follows that

```text
λ⋆ = 2π/k⋆ = 2π√(2b/a)
```

### 9. Curvature-locked electron sector

The consistent eigenvalue and radius convention is

```text
−Δψ = σ⋆²ψ
R = 1/σ⋆
```

Periodic angular modes form the integer family

```text
f(θ) = A cos(mθ) + B sin(mθ),    m ∈ ℤ≥0
```

rather than a unique constant solution.

### 10. Coherence length

```text
ξ(coh) = (Σₖ pₖ|k|²)⁻¹ᐟ²
       = √(∫|ψ|² dx / ∫|∇ψ|² dx)
```

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

A claim is not labeled `PASS` merely because it is syntactically represented. It must satisfy an actual symbolic, dimensional, numerical, or logical check.

Claims requiring PDE existence theory, global convergence, uniqueness, phenomenological calibration, or experiment remain `CONDITIONAL` or `OPEN` until those obligations are discharged.

## Primary documentation

- [`MASTER_EQUATIONS.md`](MASTER_EQUATIONS.md)
- [`EQUATIONS.md`](EQUATIONS.md)
- [`FULL_COVERAGE.md`](FULL_COVERAGE.md)
- [`COVERAGE_MATRIX.md`](COVERAGE_MATRIX.md)
- [`WCT_GAP_ANALYSIS.md`](WCT_GAP_ANALYSIS.md)

## Scientific interpretation

The repository currently establishes:

```text
internal symbolic consistency of the corrected encoded equation set
```

It does not yet establish:

```text
global PDE well-posedness, uniqueness, physical completeness,
or empirical validity of Wave Confinement Theory
```

Those remaining obligations belong to formal analysis, Lean formalization, calibrated simulation, and experiment.
