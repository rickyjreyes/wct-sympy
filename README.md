# wct-sympy: WCT Symbolic Audit Harness

`wct-sympy` audits Wave Confinement Theory equations with SymPy. It checks symbolic algebra, physical dimensions, limits, numerical residuals, executable counterexamples, and cross-equation consistency. It does not prove WCT by itself.

## Repository roles

| Repository | Responsibility |
|---|---|
| `rickyjreyes/wct-sympy` | Executable symbolic and dimensional audits |
| `rickyjreyes/wct-lean` | Kernel-checked definitions, lemmas, and theorems |
| WCT equation documents | Canonical equation IDs and scientific statements |

A SymPy `PASS` is not a Lean proof. `PROVED` is reserved for declarations checked by Lean.

## Full-corpus audit

The registry contains 142 objects: `M1`-`M8` (with `M6A`/`M6B`), `E1A`, `E1B`, `E2`-`E82`, `CLE1`-`CLE10`, `CM1`-`CM20`, `G1`, `EX`, `EY`, `EZ`, `FA`, `TOP1`-`TOP9`, and `CORR1`-`CORR6`.

| Status | Count |
|---|---:|
| PASS | 51 |
| FAIL | 0 |
| CONDITIONAL | 32 |
| DEFINITION | 23 |
| OPEN | 36 |
| Total | 142 |

Zero `FAIL` means no known contradiction remains in the current encoded statements. It does not prove the 32 conditional or 36 open claims.

## Run

```bash
pip install -r requirements.txt
pytest -q
python scripts/check_all.py
python scripts/check_full_coverage.py
python scripts/check_full_coverage.py --strict-theory
python scripts/check_lean_coverage.py
```

Generated reports are written to `tables/` and `COVERAGE_MATRIX.md`.

## Layout

```text
wct_sympy/          audit implementation
equations/          machine-readable registries
interoperability/   SymPy-to-Lean declaration map
scripts/            command-line entry points
tests/              regression tests
tables/             generated reports
```

See `FULL_COVERAGE.md`, `EQUATIONS.md`, and `MASTER_EQUATIONS.md` for the corrected equation architecture and audit policy.
