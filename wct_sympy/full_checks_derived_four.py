"""Fourth explicit derivation batch."""

import sympy as sp

from .full_checks_core import result
from .models import AuditResult, AuditStatus, EquationSpec


def check_mean_amplitude_closure_error_bound_v2(spec: EquationSpec) -> AuditResult:
    """Quantify CORR2 under a uniform relative denominator-intermittency bound."""
    k = sp.symbols("k", nonnegative=True)
    qeff = sp.symbols("Q_eff", positive=True)
    eta = sp.symbols("eta", positive=True)

    closure = k**4 / qeff
    lower = k**4 / (qeff * (1 + eta))
    upper = k**4 / (qeff * (1 - eta))
    lower_ratio = sp.simplify(lower / closure)
    upper_ratio = sp.simplify(upper / closure)
    relative_error_cap = sp.simplify(upper_ratio - 1)

    identities = (
        sp.simplify(lower_ratio - 1 / (1 + eta)) == 0
        and sp.simplify(upper_ratio - 1 / (1 - eta)) == 0
        and sp.simplify(relative_error_cap - eta / (1 - eta)) == 0
        and sp.limit(relative_error_cap, eta, 0, dir="+") == 0
    )
    return result(
        spec,
        AuditStatus.PASS if identities else AuditStatus.FAIL,
        value={
            "mean_closure": closure,
            "lower_bound": lower,
            "upper_bound": upper,
            "lower_ratio": lower_ratio,
            "upper_ratio": upper_ratio,
            "relative_error_cap": relative_error_cap,
            "small_intermittency_limit": sp.limit(relative_error_cap, eta, 0, dir="+"),
        },
        expected="quantified weak-intermittency reciprocal-denominator enclosure",
        residual=0.0 if identities else None,
        reason=(
            "If the positive local denominator Q obeys "
            "(1-eta)Q_eff <= Q <= (1+eta)Q_eff with 0<=eta<1, reciprocal "
            "monotonicity gives k^4/[Q_eff(1+eta)] <= k^4/Q <= "
            "k^4/[Q_eff(1-eta)]. The worst relative deviation from k^4/Q_eff "
            "is eta/(1-eta), tending to zero with intermittency."
        ),
        assumptions=(
            "Q_eff=D_eff^2=<|psi|^2>+epsilon^2>0",
            "C_Theta(k,x)=k^4/Q(x) in the local closure sector",
            "0<=eta<1",
            "(1-eta)Q_eff<=Q(x)<=(1+eta)Q_eff",
        ),
    )
