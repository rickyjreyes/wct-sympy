from wct_sympy.audit import run_full_audit
from wct_sympy.models import AuditStatus


def by_id():
    return {result.equation_id: result for result in run_full_audit()}


def test_e22_raw_complex_gradient_correction_is_not_a_real_symmetric_metric():
    item = by_id()["E22"]
    assert item.status == AuditStatus.CONDITIONAL
    assert item.residual == 0.0
    assert item.value["hermitian_residual"] == 0
    assert item.value["sample_asymmetry"] != 0
    assert item.value["real_symmetry_residual"] == 0


def test_e68_printed_localized_bound_is_not_uniform_on_arbitrary_h1_in_3d():
    item = by_id()["E68"]
    assert item.status == AuditStatus.CONDITIONAL
    assert item.residual == 0.0
    assert item.value["rhs_limit_R_to_zero"] == 0
    assert str(item.value["lhs_over_rhs_limit_R_to_zero"]) == "oo"
