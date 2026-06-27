from wct_sympy.audit import run_full_audit, summary
from wct_sympy.models import AuditStatus


def by_id():
    return {result.equation_id: result for result in run_full_audit()}


def test_all_audits_match_declared_expected_classification():
    results = run_full_audit()
    assert all(result.expectation_matches for result in results)
    assert summary(results)["expectation_mismatches"] == 0


def test_corrected_regularizer_is_strictly_positive():
    item = by_id()["E17"]
    assert item.status == AuditStatus.PASS
    assert item.evidence["is_positive"] is True


def test_corrected_alpha_drop_is_feasible_and_count_claims_are_conditional():
    results = by_id()
    assert results["E28"].status == AuditStatus.PASS
    assert results["E28"].value["alpha_minus_one"].is_negative
    for equation_id in ("E32", "E41", "E72"):
        assert results[equation_id].status == AuditStatus.CONDITIONAL


def test_entropy_support_direction_is_corrected():
    item = by_id()["E33"]
    assert item.status == AuditStatus.PASS
    assert item.value["exp_entropy"] <= item.value["support_size"]


def test_embedding_threshold_is_exact():
    item = by_id()["E24"]
    assert item.status == AuditStatus.PASS
    assert item.value == [1, 2, 3]


def test_cle_periodic_family_is_quantized_not_unique():
    item = by_id()["CLE7"]
    assert item.status == AuditStatus.PASS
    assert item.value["ode_residual"] == 0
    assert item.value["periodic_residual"] == 0


def test_resolved_registry_has_no_known_failures():
    report = summary(run_full_audit())
    assert report["status_counts"].get("FAIL", 0) == 0
    assert report["status_counts"] == {
        "CONDITIONAL": 27,
        "DEFINITION": 26,
        "OPEN": 30,
        "PASS": 59,
    }
