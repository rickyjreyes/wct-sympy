"""Third explicit derivation batch for canonical WCT audit entries.

The checks in this module close only the displayed implications under explicit
uniform-margin or denominator hypotheses.  They do not add empirical or PDE
claims beyond those assumptions.
"""

from .full_checks_core import *  # noqa: F401,F403


def check_subexponential_exploration_margin_derived(spec: EquationSpec) -> AuditResult:
    """Derive E32 from a uniform tail margin in the corrected alpha-drop law."""
    avg_log = sp.symbols("A", real=True)
    margin = sp.symbols("delta", positive=True)
    slack = sp.symbols("s", nonnegative=True)

    # Write the hypothesis beta <= -A-delta as beta=-A-delta-s, s>=0.
    beta = -avg_log - margin - slack
    alpha = sp.simplify(1 + avg_log + beta)
    tail_upper = 1 - margin
    gap_to_upper = sp.simplify(tail_upper - alpha)
    ok = (
        sp.simplify(alpha - (1 - margin - slack)) == 0
        and gap_to_upper.is_nonnegative is True
        and sp.simplify(1 - tail_upper) == margin
        and margin.is_positive is True
    )

    return result(
        spec,
        AuditStatus.PASS if ok else AuditStatus.FAIL,
        value={
            "alpha_tail": alpha,
            "uniform_tail_upper": tail_upper,
            "gap_to_upper": gap_to_upper,
        },
        expected="uniform delta>0 margin implies alpha(n)<=1-delta eventually, hence limsup alpha<1",
        residual=0.0 if ok else None,
        reason=(
            "Let A(n)=(1/n) sum_t log2 rho_t(n).  If there are delta>0 and N "
            "such that beta(n)<=-A(n)-delta for every n>=N, write the inequality "
            "as beta(n)=-A(n)-delta-s(n) with s(n)>=0.  Then the corrected E28 "
            "formula gives alpha(n)=1-delta-s(n)<=1-delta<1 on the whole tail. "
            "Therefore limsup alpha(n)<=1-delta<1, which is exactly E32."
        ),
        assumptions=(
            "alpha(n)=1+A(n)+beta(n) with A(n)=(1/n) sum_t log2 rho_t(n)",
            "there exist delta>0 and N such that beta(n)<=-A(n)-delta for all n>=N",
            "the retained-fraction logarithmic average A(n) is finite on that tail",
        ),
    )


def check_phase_coherence_lower_gradient_bound_derived(spec: EquationSpec) -> AuditResult:
    """Derive E50 finiteness from an L2 field and a positive phase-gradient floor."""
    density = sp.symbols("u", nonnegative=True)
    delta = sp.symbols("delta", positive=True)
    excess = sp.symbols("q", nonnegative=True)

    # Parameterize |grad theta| >= delta by |grad theta|=delta+q, q>=0.
    grad_mag = delta + excess
    integrand = sp.simplify(density / grad_mag)
    upper_integrand = sp.simplify(density / delta)
    gap = sp.factor(upper_integrand - integrand)
    ok = (
        integrand.is_nonnegative is True
        and gap.is_nonnegative is True
        and sp.simplify(upper_integrand - integrand - gap) == 0
    )

    return result(
        spec,
        AuditStatus.PASS if ok else AuditStatus.FAIL,
        value={
            "gradient_magnitude": grad_mag,
            "coherence_integrand": integrand,
            "pointwise_upper_bound": upper_integrand,
            "upper_minus_integrand": gap,
        },
        expected="0<=C[psi]<=delta^(-1)||psi||_2^2<infinity when |grad theta|>=delta>0",
        residual=0.0 if ok else None,
        reason=(
            "Writing |grad theta|=delta+q with delta>0 and q>=0 gives the exact "
            "pointwise inequality 0<=|psi|^2/|grad theta|<=|psi|^2/delta. "
            "If psi is in L2, integration yields 0<=C[psi]<=||psi||_2^2/delta<infinity. "
            "Thus the original singularity is removed by the canonical positive "
            "phase-gradient lower bound."
        ),
        assumptions=(
            "psi is square-integrable on the integration region",
            "|grad theta|>=delta>0 almost everywhere on that region",
            "the phase-gradient magnitude is measurable",
        ),
    )
