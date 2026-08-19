from wct_sympy.audit import run_full_audit
from wct_sympy.models import AuditStatus


def by_id():
    return {result.equation_id: result for result in run_full_audit()}


def test_e15_modal_growth_is_exact_in_one_mode_reduction():
    item = by_id()["E15"]
    assert item.status == AuditStatus.PASS
    assert item.residual == 0.0
    assert item.value["quartic_coefficient"].is_positive


def test_cle5_flat_product_torus_laplacian_is_exact():
    item = by_id()["CLE5"]
    assert item.status == AuditStatus.PASS
    assert item.residual == 0.0
    assert item.value["eigenvalue"].is_nonnegative


def test_cle8_lowest_mode_is_unique_after_winding_and_chirality_are_fixed():
    item = by_id()["CLE8"]
    assert item.status == AuditStatus.PASS
    assert item.value["spectral_gap"].is_nonnegative
    assert item.value["zero_gap_modes"] == [0]


def test_top3_exact_gradient_flow_descends():
    item = by_id()["TOP3"]
    assert item.status == AuditStatus.PASS
    assert item.value["dE_dt"].is_nonpositive


def test_second_derivation_batch_increases_pass_count():
    results = list(run_full_audit())
    assert sum(item.status == AuditStatus.PASS for item in results) == 63
    assert len(results) == 142
