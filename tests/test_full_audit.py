from wct_sympy.audit import run_full_audit, summary
from wct_sympy.models import AuditStatus


def by_id():
    return {result.equation_id: result for result in run_full_audit()}


def test_all_audits_match_declared_expected_classification():
    results = run_full_audit()
    assert all(result.expectation_matches for result in results)
    assert summary(results)["expectation_mismatches"] == 0


def test_regularizer_counterexample_is_executable():
    item = by_id()["E17"]
    assert item.status == AuditStatus.FAIL
    assert abs(float(item.evidence["counterexample_root"])) > 0
    assert item.residual is not None and item.residual < 1e-10


def test_alpha_drop_internal_conflict_is_detected():
    results = by_id()
    for equation_id in ("E28", "E32", "E41", "E72"):
        assert results[equation_id].status == AuditStatus.FAIL
        assert "exceeds one" in results[equation_id].reason


def test_entropy_support_direction_is_detected():
    item = by_id()["E33"]
    assert item.status == AuditStatus.FAIL
    assert item.value["exp_entropy"] < item.value["support_size"]


def test_embedding_threshold_is_exact():
    item = by_id()["E24"]
    assert item.status == AuditStatus.PASS
    assert item.value == [1, 2, 3]


def test_cle_periodic_counterexample_is_detected():
    item = by_id()["CLE7"]
    assert item.status == AuditStatus.FAIL
    assert item.value["ode_residual"] == 0
    assert item.value["periodic_residual"] == 0
