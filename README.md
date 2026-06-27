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
| `PASS` | **59** | The encoded implication follows under its declared assumptions. |
| `FAIL` | **0** | No current encoded statement is contradicted by its assigned checker. |
| `CONDITIONAL` | **27** | Additional mathematical or model assumptions remain required. |
| `DEFINITION` | **26** | The object is a definition or ansatz rather than a theorem. |
| `OPEN` | **30** | Analysis, formal proof, calibrated simulation, or experiment remains unresolved. |
| **Total** | **142** | Complete registry coverage. |

A zero `FAIL` count means no known contradiction remains in the current encoded statements. It does **not** prove the 27 conditional or 30 open obligations.

## Derivation batch 1

The first explicit derivation pass promotes eight equation objects to `PASS`:

1. `E5`: exact loop closure plus constant positive weight proves the effective-wavenumber chain.
2. `E9`: polar decomposition gives the normalized phase current.
3. `E13` and `E14`: the band-pass functional generates the amplitude equation under negative gradient flow.
4. `E18`: nonnegative coefficients give a nonnegative functional, and exact negative gradient flow gives monotone descent.
5. `E58`: positive spectral offset bounds the Green kernel.
6. `CM9`: the first-order velocity system is equivalent to the second-order oscillator system.
7. `CM11`: curvature diffusion integrates to the Gaussian damping envelope.

Four cosmology entries are reclassified from `OPEN` to `DEFINITION`:

- `CM12`: dimensionless power-spectrum definition;
- `CM13`: peak-ratio definitions;
- `CM16`: horizon-scale definitions;
- `CM18`: closure-set definition.

The historical baseline remains in `equations/full_registry.yaml`. Additive theorem and classification changes are isolated in `equations/derived_overrides.yaml`.

See [`DERIVATIONS_BATCH_1.md`](DERIVATIONS_BATCH_1.md) for the assumptions, derivations, and numerical examples.

## Representative derived identities

### Phase current

For

$$
\psi=\sqrt{u}\,e^{i\theta},
$$

one obtains

$$
\operatorname{Im}(\overline\psi\,\nabla\psi)=u\nabla\theta.
$$

### Band-pass gradient flow

From

$$
\mathcal E[A]
=
\int\left(-r|A|^2-a|\nabla A|^2+b|\Delta A|^2+\frac{\beta}{2}|A|^4\right)dx,
$$

negative gradient flow gives

$$
\partial_tA=rA-a\Delta A-b\Delta^2A-\beta|A|^2A.
$$

### Lyapunov descent

For exact negative gradient flow,

$$
\partial_t\psi=-\frac{\delta\mathcal E}{\delta\overline\psi},
$$

one has

$$
\frac{d\mathcal E}{dt}
=-\left\|\frac{\delta\mathcal E}{\delta\overline\psi}\right\|_2^2
\le0.
$$

### Green-kernel bound

For `r>0` and `a>0`,

$$
G(k)=\frac{1}{r+a(k^2-k_*^2)^2}
$$

satisfies

$$
0<G(k)\le\frac1r.
$$

## Repository boundaries

| Component | Responsibility |
|---|---|
| `wct-sympy` | Algebra, dimensions, limits, residuals, consistency checks, and executable counterexamples. |
| `wct-lean` | Kernel-checked definitions, assumptions, lemmas, and theorems. |
| `MASTER_EQUATIONS.md` | Canonical master architecture. |
| `EQUATIONS.md` | Canonical equation families and corrected forms. |
| `equations/full_registry.yaml` | Historical baseline registry. |
| `equations/derived_overrides.yaml` | Additive derivation and reclassification results. |
| `interoperability/lean_map.yaml` | SymPy-to-Lean relationship metadata. |

A SymPy `PASS` is never reported as a Lean proof. `PROVED` is reserved for declarations accepted by the Lean kernel.

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

## Primary documentation

- [`MASTER_EQUATIONS.md`](MASTER_EQUATIONS.md)
- [`EQUATIONS.md`](EQUATIONS.md)
- [`DERIVATIONS_BATCH_1.md`](DERIVATIONS_BATCH_1.md)
- [`FULL_COVERAGE.md`](FULL_COVERAGE.md)
- [`COVERAGE_MATRIX.md`](COVERAGE_MATRIX.md)
- [`WCT_GAP_ANALYSIS.md`](WCT_GAP_ANALYSIS.md)

## Scientific boundary

The repository establishes internal symbolic consequences of the corrected encoded equation set. It does not establish global PDE well-posedness, uniqueness, physical completeness, or empirical validity of WCT.
