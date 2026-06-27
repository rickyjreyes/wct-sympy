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
| `FAIL` | Algebra, dimensions, logic, or an explicit counterexample contradicts the current statement. |
| `CONDITIONAL` | Missing sign, domain, regularity, counting, or model assumptions are required. |
| `DEFINITION` | A definition or ansatz, not a theorem. |
| `OPN` | Proof or empirical validation lies outside symbolic algebra. |

## Current classification after correction pass

| Status | Count |
|---|---:|
| PASS | 51 |
| FAIL | 0 |
| CONDITIONAL | 32 |
| DEFINITION | 23 |
| OPEN | 36 |
| **Total** | **142** |

These counts are not a theory score. They prevent definitions, conjectures, and phenomenological ansatze from being reported as symbolic proofs.

## Resolved contradictions

The correction pass replaces or weakens every previously encoded contradiction:

1. The node regularizer is now a modulus-squared reciprocal with strictly positive denominator.
2. Swift-Hohenberg fourth-order terms use an explicit negative sign for ultraviolet damping.
3. The weighted lock integral uses the derived `alpha*L_s` term.
4. `H^2` gives an `L^2` curvature bound; `L^infinity` curvature requires `H^s`, `s>n/2+2`.
5. Alpha-drop uses retained fractions in `(0,1]`; configuration-count claims remain conditional.
6. The entropy/support relation is `exp(H)<=K`.
7. Quality factor uses loss power, and the energy balance treats fusion as a source.
8. The gap-mass law is `m_eff^2=hbar^2 Delta_*/c^4`.
9. The selected wavelength is `2*pi*sqrt(2*b/a)`.
10. Coherence length is defined by a spectral second moment or gradient ratio.
11. The CLE variation includes its fourth-order term.
12. The CLE eigenvalue/radius chain uses `sigma_*^2` and `R=1/sigma_*`.
13. Periodic angular modes are an integer family; torus uniqueness is conditional.

A zero `FAIL` count means no contradiction remains in the **current encoded statements**. It does not imply that the conditional, open, or empirical claims are proven.

## Commands

```bash
python scripts/check_full_coverage.py
python scripts/check_lean_coverage.py
pytest -q
```

Strict theory mode now succeeds when no encoded `FAIL` remains:

```bash
python scripts/check_full_coverage.py --strict-theory
```

## Separation from `wct-lean`

`wct-sympy` does not depend on Lean at runtime. The repositories have separate jobs:

- `wct-sympy`: algebra, dimensions, limits, numerical residuals, and executable counterexamples;
- `wct-lean`: kernel-checked definitions, assumptions, lemmas, and theorems;
- `interoperability/lean_map.yaml`: metadata linking only claims with an existing Lean declaration.

A SymPy `PASS` is never labeled `PROVED`; {PROVED}` is reserved for declarations checked by Lean in `rickyjreyes/wct-lean`.

## Integration

The full path is additive. The original `wct_sympy/checks.py` and `scripts/check_all.py` remain available for the five-check harness, while `scripts/check_full_coverage.py` runs the corpus-wide audit.
