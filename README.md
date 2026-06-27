# wct-sympy: WCT Symbolic Audit Harness

This repository audits Wave Confinement Theory equations using SymPy. It checks dimensions, algebra, limits, numerical residuals, executable counterexamples, and cross-equation consistency. It does not prove WCT by itself.

## Repository roles

| Repository | Responsibility |
|---|---|
| `rickyjreyes/wct-sympy` | Symbolic algebra, dimensions, limits, numerical residuals, and counterexamples |
| `rickyjreyes/wct-lean` | Kernel-checked definitions, assumptions, lemmas, and theorems |
| WCT equation documents | Canonical equation IDs and scientific statements |

`wct-sympy` has **no Lean runtime dependency**. The machine-readable bridge at `interoperability/lean_map.yaml` maps a small set of matching claims to declaration names in `wct-lean`.

Status words are intentionally distinct:

- `PASS`: the registered SymPy or numerical check passed;
- `FAIL`: algebra, dimensions, logic, or a counterexample contradicts the statement;
- `CONDITIONAL`: additional assumptions are required;
- `DEFINITION`: represented, but not a theorem;
- `OPEN`: not settled by symbolic algebra;
- `PROVED`: reserved for a declaration kernel-checked in `wct-lean`.

A SymPy `PASS` is never reported as a Lean proof.

## Full-corpus audit

The full registry contains 142 equation objects:

- `M1`-`M8`, with `M6A` and `M6B` separated;
- `E1A`, `E1B`, `E2`-`E82`;
- `CLE1`-`CLE10`;
- `CM1`-`CM20`;
- `G1`, `EX`, `EY`, `EZ`, `FA`;
- `TOP1`-`TOP9` and `CORR1`-`CORR6`.

Run:

```bash
pip install -r requirements.txt
pytest -q
python scripts/check_all.py
python scripts/check_full_coverage.py
python scripts/check_lean_coverage.py
```

Generated reports:

```text
tables/wct_sympy_checks.csv
tables/wct_full_coverage.csv
tables/wct_full_coverage.json
tables/lean_coverage.json
COVERAGE_MATRIX.md
```

Strict theory mode returns nonzero while an encoded contradiction remains:

```bash
python scripts/check_full_coverage.py --strict-theory
```

Normal mode succeeds when all registered equations reproduce their declared classifications. A scientific `FAIL` means the audit detected a contradiction; it is not a software failure.

| Status | Count |
|---|---:|
| PASS | 32 |
| FAIL | 24 |
| CONDITIONAL | 27 |
| DEFINITION | 23 |
| OPEN | 36 |
| Total | 142 |

See `FULL_COVERAGE.md`, `EQUATIONS.md`, and `MASTER_EQUATIONS.md`.

## Lean bridge

Validate the local mapping metadata without installing Lean:

```bash
python scripts/check_lean_coverage.py
```

This checks that:

1. every mapped ID exists in the legacy or full SymPy registry;
2. every mapping names at least one Lean declaration;
3. formal support, dimensional support, domain safety, and TODO relationships are not conflated;
4. a stated Lean TODO is never counted as a proof.

The actual formal build remains in the separate repository:

```bash
cd ../wct-lean
lake build
```

The bridge does not claim that all 142 equations are formalized. It records only declarations that currently exist and labels their exact relationship to the SymPy claim.

## Original compatibility harness

The original five checks remain available:

```bash
python scripts/check_all.py
python scripts/check_dimensions.py
python scripts/check_koide.py
python scripts/check_curvature_mass.py
python scripts/check_limits.py
```

They cover:

| ID | Purpose |
|---|---|
| D1_10 | curvature-mass dimensions |
| CURV1 | `sqrt(kappa^2+tau^2)` has `L^-1` |
| CURV2 | `kappa^2+tau^2` has `L^-2` |
| K1 | charged-lepton Koide residual |
| LIM1 | boundary and positivity assumptions |

## Layout

```text
wct_sympy/          audit implementation
equations/          machine-readable registries
interoperability/   SymPy-to-Lean declaration map
scripts/            command-line entry points
tests/              regression tests
tables/             generated reports
```

For full coverage, add a stable ID to `equations/full_registry.yaml`, assign a checker in `wct_sympy/full_checks_*.py`, and add a test. Add a Lean mapping only when a corresponding declaration actually exists in `wct-lean`.
