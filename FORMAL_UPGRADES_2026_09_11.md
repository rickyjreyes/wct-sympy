# September 2026 Symbolic Formal Upgrades

`wct_sympy/formal_upgrades.py` adds five exact paper-level certificates. They are intentionally separate from the 142-object canonical status registry unless and until a canonical equation claim is mapped to the same mathematical statement and scope.

## Certificates

1. **Toroidal selector**
   - verifies `1/4 - eta^2(1-eta^2) = (eta^2-1/2)^2`;
   - verifies equality occurs at `eta = +/-1/sqrt(2)` and records the positive physical branch.

2. **Finite-band Hessian maximum**
   - verifies `R k^2-q k^4 = R^2/(4q)-q(k^2-R/(2q))^2`;
   - verifies `q=d^-2` gives `k_star^2=R d^2/2` and `lambda_max=R^2 d^2/4`.

3. **Helix curvature scale**
   - verifies `kappa^2+tau^2 = 1/(R^2+p^2)`;
   - verifies `p=n eta R` gives `1/[R^2(1+n^2 eta^2)]`.

4. **Core integrability threshold**
   - solves `2p-2>-1` exactly as `p>1/2`.

5. **Constrained curvature locking**
   - differentiates `w(phi'-sigma)^2 + lambda phi'`;
   - solves stationarity as `phi'=sigma-lambda/(2w)`;
   - verifies exact locking is recovered when the multiplier vanishes.

## Scope

These are algebraic or symbolic certificates. They do not establish PDE existence, nonlinear orbital stability, a particle spectrum, topological charge quantization, or empirical validity. The corresponding Lean theorems live in `rickyjreyes/wct-lean` on the companion formal-upgrade branch/PR.

Run directly with:

```bash
pytest -q tests/test_formal_upgrades.py
```

or run the full repository suite with:

```bash
pytest -q
```
