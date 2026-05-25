# wct-sympy: WCT Symbolic Audit Harness

This repo is a symbolic audit harness for Wave Confinement Theory (WCT)
equations. It checks dimensional consistency, algebraic identities,
numerical residuals, and limit behavior. **It does not prove WCT by itself.**

Every important WCT equation in the registry can be checked by code:

```
WCT paper equations
  -> symbol registry  (equations/registry.yaml)
  -> dimensional checks  (wct_sympy/dimensions.py)
  -> symbolic simplifications  (wct_sympy/equations.py)
  -> numerical residual checks  (wct_sympy/checks.py)
  -> machine-readable PASS/FAIL output  (tables/wct_sympy_checks.csv)
```

## Layout

```
wct_sympy/        core library (Dimension algebra, equations, checks, registry loader)
equations/        machine-readable registry of WCT equations
scripts/          CLI entry points (check_all, check_dimensions, ...)
tests/            pytest suite
tables/           generated CSV output of check results
PAPER_MAP.md      mapping from check IDs to papers / claims
```

## Quick start

```bash
pip install -r requirements.txt
python scripts/check_all.py
pytest -q
```

`check_all.py` writes a machine-readable summary to
`tables/wct_sympy_checks.csv` with columns:

```
check_id, name, status, value, expected, residual, failure_reason
```

## Individual checks

```bash
python scripts/check_dimensions.py     # D1_10, CURV1, CURV2
python scripts/check_koide.py          # K1
python scripts/check_curvature_mass.py # D1_10 only
python scripts/check_limits.py         # LIM1
```

## Current checks

| ID     | Name                                 | What it verifies                                  |
|--------|--------------------------------------|---------------------------------------------------|
| D1_10  | effective_curvature_mass_relation    | `(hbar/c) * k_eff` carries mass dimension         |
| CURV1  | curvature_torsion_sigma              | `sqrt(kappa^2 + tau^2)` carries `L^-1`            |
| CURV2  | curvature_torsion_sigma_raw          | `kappa^2 + tau^2` carries `L^-2` (not `L^-1`)     |
| K1     | koide_relation                       | Koide ratio numerically close to `2/3`            |
| LIM1   | limit_checks                         | `k_eff -> 0 => m -> 0`; `c`, `hbar` finite/nonzero|

## Adding a new equation

1. Add an entry to `equations/registry.yaml`.
2. Add a check function in `wct_sympy/checks.py` returning a `CheckResult`.
3. Register it in `CHECKS` so `run_all()` picks it up.
4. Add a unit test under `tests/`.
5. Add a mapping line in `PAPER_MAP.md`.
