# Paper-level closure symbolic batch

This batch adds exact SymPy checks for the August 2026 WCT closure, compact-dynamics, and WCT-DSI revisions.

## Checks

`wct_sympy/paper_closure_checks.py` verifies:

1. DSI/WCT positive-log-coordinate round trip.
2. Convex-mixing contraction factor `1-L*delta` and perturbation margin `L*delta-epsilon`.
3. Exact quartic square completion behind the coercivity absorption estimate.
4. Three-dimensional fixed-mass dilation powers: mass `R^0`, gradient energy `R^-2`, biharmonic energy `R^-4`, quartic term `R^-3`.
5. Exact beta=0 amplitude-scaling quotient decrease
   `1/(t q+d)-1/(q+d)=-(t-1)q/((t q+d)(q+d))`.
6. Generalized Euler-Lagrange derivative of the real 1D quotient-curvature analogue `u''^2/(u^2+delta^2)`.

The accompanying pytest file makes every identity executable in the normal repository test suite.

## Boundary

These checks are paper-level verification objects. They do **not** automatically promote any of the 142 canonical registry entries. In particular, the 1D real quotient variation is a structural check, not the full complex-field variational theorem; the scaling checks do not prove concentration-compactness or existence of a minimizer; and the DSI bijection does not prove dynamical generation of DSI modes.
