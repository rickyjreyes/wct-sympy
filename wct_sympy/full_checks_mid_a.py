"""Information, capacity, and balance audits."""

from .full_checks_core import *  # noqa: F401,F403


def check_alpha_drop_conflict(spec: EquationSpec) -> AuditResult:
    M0 = sp.symbols("M0", positive=True)
    q = (M0 + 1) / M0
    log_positive = sp.log(q, 2).is_positive
    return result(
        spec,
        AuditStatus.FAIL,
        value={"q": q, "log2_q_positive": log_positive, "alpha_lower_bound": ">1 if beta>=0"},
        expected="alpha<1",
        reason="Since q_t=(M_t+1)/M_t>1, each logarithmic term is positive; the displayed alpha formula exceeds one whenever beta is nonnegative.",
    )


def check_state_decay_iteration(spec: EquationSpec) -> AuditResult:
    d1, d2, initial = sp.symbols("d1 d2 initial", positive=True)
    state1 = sp.exp(-d1) * initial
    state2 = sp.exp(-d2) * state1
    expected = sp.exp(-(d1 + d2)) * initial
    residual = sp.simplify(state2 - expected)
    return result(spec, AuditStatus.PASS if residual == 0 else AuditStatus.FAIL, value=residual, expected=0)


def check_entropy_bounds(spec: EquationSpec) -> AuditResult:
    probabilities = [sp.Rational(1, 2), sp.Rational(1, 2)]
    entropy = sp.simplify(-sum(p * sp.log(p) for p in probabilities))
    return result(spec, AuditStatus.PASS, value=entropy, expected=sp.log(2))


def check_self_referential_entropy_drop(spec: EquationSpec) -> AuditResult:
    drop, coeff, kstar = sp.symbols("drop coeff kstar", positive=True)
    reduced = sp.simplify((coeff * kstar**2 * drop) / drop)
    return result(
        spec,
        AuditStatus.FAIL,
        value=f"for positive drop the statement reduces to 1 approximately greater than {reduced}",
        expected="an independently defined right-hand side",
        reason="The same drop appears on both sides, so the equation does not determine its magnitude.",
    )


def check_support_entropy_direction(spec: EquationSpec) -> AuditResult:
    p1 = sp.Rational(9, 10)
    p2 = sp.Rational(1, 10)
    entropy = -p1 * sp.log(p1) - p2 * sp.log(p2)
    effective = float(sp.exp(entropy).evalf())
    return result(
        spec,
        AuditStatus.FAIL,
        value={"support_size": 2, "exp_entropy": effective},
        expected="exp(H) <= support size",
        reason="For a distribution supported on K modes, H<=log(K), so the stated inequality is reversed except at uniform equality.",
    )


def check_bandlimit_dimensions(spec: EquationSpec) -> AuditResult:
    dim = ENERGY / (ACTION * VELOCITY)
    return result(spec, AuditStatus.PASS if dim == INVERSE_LENGTH else AuditStatus.FAIL, value=dim, expected=INVERSE_LENGTH)


def check_channel_capacity_dimensions(spec: EquationSpec) -> AuditResult:
    dim = VOLUME * INVERSE_LENGTH**3
    return result(spec, AuditStatus.PASS if dim == ONE else AuditStatus.FAIL, value=dim, expected=ONE)


def check_q_factor_dimensions(spec: EquationSpec) -> AuditResult:
    dim = FREQUENCY * ENERGY / ENERGY
    return result(
        spec,
        AuditStatus.FAIL,
        value=dim,
        expected=ONE,
        reason="A dimensionless Q uses angular frequency times stored energy divided by loss power; the displayed denominator is an energy integral rather than power loss.",
    )


def check_power_balance_form(spec: EquationSpec) -> AuditResult:
    return result(
        spec,
        AuditStatus.FAIL,
        value="P_in = P_loss + P_fusion",
        expected="dW/dt = P_in + P_fusion - P_loss, subject to defined output channels",
        reason="Fusion power is a source in the confined-energy balance unless explicitly redefined as extracted output.",
    )
