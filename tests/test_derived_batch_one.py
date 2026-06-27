from wct_sympy.audit import run_full_audit
from wct_sympy.models import AuditStatus


def by_id():
    return {result.equation_id: result for result in run_full_audit()}


def test_effective_wavenumber_chain_is_exact_under_declared_hypotheses():
    item = by_id()["E5"]
    assert item.status == AuditStatus.PASS
    assert item.residual == 0.0
    assert item.value["residuals"] == (0, 0)


def test_phase_flux_is_the_polar_wavefield_current():
    item = by_id()["E9"]
    assert item.status == AuditStatus.PASS
    assert item.residual == 0.0


def test_bandpass_functional_generates_amplitude_flow():
    results = by_id()
    for equation_id in ("E13", "E14"):
        item = results[equation_id]
        assert item.status == AuditStatus.PASS
        assert item.residual == 0.0
        assert item.value["variation_residual"] == 0
        assert item.value["flow_residual"] == 0


def test_exact_negative_gradient_flow_is_lyapunov_descent():
    item = by_id()["E18"]
    assert item.status == AuditStatus.PASS
    assert item.value["energy"].is_nonnegative
    assert item.value["dE_dt"].is_nonpositive


def test_green_kernel_is_bounded_when_r_and_a_are_positive():
    item = by_id()["E58"]
    assert item.status == AuditStatus.PASS
    assert item.value["denominator_minus_r"].is_nonnegative


def test_cm9_is_exact_first_order_rewrite():
    item = by_id()["CM9"]
    assert item.status == AuditStatus.PASS
    assert item.residual == 0.0
    assert item.value["gamma_residual"] == 0
    assert item.value["baryon_residual"] == 0


def test_cm11_is_exact_gaussian_mode_damping():
    item = by_id()["CM11"]
    assert item.status == AuditStatus.PASS
    assert item.residual == 0.0
    assert item.value["ode_residual"] == 0


def test_cosmology_observables_are_definitions_not_open_theorems():
    results = by_id()
    for equation_id in ("CM12", "CM13", "CM16", "CM18"):
        assert results[equation_id].status == AuditStatus.DEFINITION
