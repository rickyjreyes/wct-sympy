from wct_sympy.audit import run_full_audit
from wct_sympy.models import AuditStatus


def by_id():
    return {result.equation_id: result for result in run_full_audit()}


def test_e15_modal_growth_is_exact_in_one_mode_reduction():
    item = by_id()["E15"]
    assert item.status == AuditStatus.PASS
    assert item.residual == 0.0
    assert item.value["quartic_coefficient"].is_positive


def test_second_derivation_batch_increases_pass_count():
    results = list(run_full_audit())
    assert sum(item.status == AuditStatus.PASS for item in results) == 60
    assert len(results) == 142
