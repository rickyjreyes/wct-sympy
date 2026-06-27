# SymPy Full Coverage for the WCT Corpus

This layer expands `wct-sympy` from a five-check harness into a full-corpus audit. It does not mark every displayed equation as proved.

## Coverage

The registry contains **142 stable equation IDs**:

- 9 master systems: `M1`-`M8`, with `M6A` and `M6B` separated;
- 83 canonical equations: `E1A`, `E1B`, `E2`-`E82`;
- 10 curvature-locking equations: `CLE1`-`CLE10`;
- 20 cosmology equations: `CM1`-`CM20`;
- `G1`, `EX`, `EY`, `EZ`, and `FA`;
- topology and correction-note IDs `TOP1`-`TOP9` and `CORR1`-`CORR6`.

Every ID has a checker and an expected scientific status.

| Status | Meaning |
|---|---|
| `PASS` | The encoded implication follows under its declared assumptions. |
| `FAIL` | Algebra, dimensions, logic, or an explicit counterexample contradicts the statement. |
| `CONDITIONAL` | Missing sign, domain, regularity, or model assumptions are required. |
| `DEFINITION` | A definition or ansatz, not a theorem. |
| `OPEN` | Proof or empirical validation lies outside symbolic algebra. |

## Baseline classification

| Status | Count |
|---|---:|
| PASS | 32 |
| FAIL | 24 |
| CONDITIONAL | 27 |
| DEFINITION | 23 |
| OPEN | 36 |
| **Total** | **142** |

These counts are not a theory score. They prevent definitions, conjectures, and phenomenological ansatze from being reported as symbolic proofs.

## Encoded regression findings

1. `psi + epsilon*exp(-alpha*psi**2)` is not globally nonzero for real negative `psi`; the code computes a root for `epsilon=alpha=1`.
2. The alpha-drop form is incompatible with `alpha<1` when each logarithmic term is positive and the remaining correction is nonnegative.
3. For support size `K`, `H<=log(K)` and therefore `exp(H)<=K`; the reverse inequality is not general.
4. `E12` gives `lambda_star=2*pi*sqrt(2*b/a)`, exposing the factor-of-`sqrt(2)` discrepancy in `E64`.
5. The CLE chain mixes inverse-length and inverse-length-squared conventions for `sigma_star`.

## Commands

```bash
python scripts/check_full_coverage.py
pytest -q
```

Strict theory mode returns nonzero while any encoded scientific contradiction remains:

```bash
python scripts/check_full_coverage.py --strict-theory
```

Normal mode exits successfully when the implementation reproduces the declared baseline, including expected scientific failures.

## Integration

The new path is additive. The original `wct_sympy/checks.py` and `scripts/check_all.py` remain available for the five-check harness, while `scripts/check_full_coverage.py` runs the corpus-wide audit.
