# wct-sympy: WCT Symbolic Audit Harness

This repository audits Wave Confinement Theory equations using SymPy. It checks dimensions, algebra, limits, numerical residuals, and cross-equation consistency. It does not prove WCT by itself.

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
python scripts/check_full_coverage.py
pytest -q
```

Generated reports:

```text
tables/wct_full_coverage.csv
tables/wct_full_coverage.json
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
scripts/            command-line entry points
tests/              regression tests
tables/             generated reports
```

For full coverage, add a stable ID to `equations/full_registry.yaml`, assign a checker in `wct_sympy/full_checks_*.py`, and add a test.
