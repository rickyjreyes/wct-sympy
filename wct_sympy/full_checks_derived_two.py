"""Second explicit derivation batch for canonical WCT audit entries.

PASS results here are narrow implications under their returned assumptions; they
must not be read as proofs of stronger nonlinear PDE or empirical claims.
"""

from .full_checks_core import *  # noqa: F401,F403


def check_modal_growth_bound_derived(spec: EquationSpec) -> AuditResult:
    """Derive E15 exactly in the isolated real one-mode cubic reduction."""
    amplitude, growth = sp.symbols("A sigma", real=True)
    saturation = sp.symbols("beta", positive=True)

    # One-mode reduction of E13: A_dot = sigma*A - beta*A^3.
    amplitude_rate = growth * amplitude - saturation * amplitude**3
    power = amplitude**2
    power_rate = sp.simplify(sp.diff(power, amplitude) * amplitude_rate)
    quartic_coefficient = 2 * saturation
    target = 2 * growth * amplitude**2 - quartic_coefficient * amplitude**4
    residual = sp.simplify(power_rate - target)
    ok = residual == 0 and quartic_coefficient.is_positive is True

    return result(
        spec,
        AuditStatus.PASS if ok else AuditStatus.FAIL,
        value={
            "one_mode_flow": amplitude_rate,
            "power_rate": power_rate,
            "quartic_coefficient": quartic_coefficient,
        },
        expected="d|A_k|^2/dt = 2*sigma(k)|A_k|^2 - c|A_k|^4 with c=2*beta>0",
        residual=0.0 if ok else None,
        reason=(
            "For the isolated real one-mode cubic reduction of E13, differentiating "
            "A^2 gives the E15 modal power law exactly, with c=2*beta>0. "
            "The registered inequality therefore holds as equality in this reduction."
        ),
        assumptions=(
            "isolated real Fourier-mode reduction",
            "A_dot=sigma(k) A-beta A^3",
            "beta>0",
            "mode-coupling and phase-transfer terms are neglected",
        ),
    )
