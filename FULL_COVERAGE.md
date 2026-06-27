# SymPy Full Coverage for the WCT Corpus

The audit contains 142 stable equation objects. A `PASS` means the encoded implication follows under its stated assumptions; it is not a Lean proof or empirical validation.

## Current classification

| Status | Count |
|---|---:|
| PASS | 59 |
| FAIL | 0 |
| CONDITIONAL | 27 |
| DEFINITION | 26 |
| OPEN | 30 |
| **Total** | **142** |

## Derivation batch 1

Eight objects are promoted to `PASS`:

- `E5`: exact loop closure and constant positive weight imply the effective-wavenumber chain.
- `E9`: for `psi=sqrt(u) exp(i theta)`, the normalized phase current is `u grad(theta)`.
- `E13`, `E14`: the band-pass functional generates the amplitude equation under negative gradient flow.
- `E18`: nonnegative coefficients give `E>=0`; exact negative gradient flow gives `dE/dt<=0`.
- `E58`: for positive `r` and `a`, the Green kernel obeys `0<G(k)<=1/r`.
- `CM9`: the first-order velocity system is equivalent to the second-order oscillator equations.
- `CM11`: curvature diffusion integrates to the Gaussian mode-damping envelope.

Four objects are reclassified as definitions rather than open theorem obligations:

- `CM12`: dimensionless power spectrum;
- `CM13`: peak ratios;
- `CM16`: horizon scale;
- `CM18`: closure set.

The original registry remains the historical baseline. `equations/derived_overrides.yaml` contains only the new derivation results.

## Audit policy

| Status | Meaning |
|---|---|
| `PASS` | The encoded implication follows under declared assumptions. |
| `FAIL` | Algebra, dimensions, logic, or a counterexample contradicts the statement. |
| `CONDITIONAL` | Additional mathematical or model hypotheses are still required. |
| `DEFINITION` | A definition or ansatz, not a theorem. |
| `OPEN` | Proof or empirical validation remains unresolved. |

A zero `FAIL` count does not prove the open or conditional physics.

## Commands

```bash
python scripts/check_full_coverage.py
python scripts/check_lean_coverage.py
pytest -q
```

`wct-sympy` supplies symbolic audits. Kernel-checked theorem status remains the role of `wct-lean`.
