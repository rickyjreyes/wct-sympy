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


def test_e32_uniform_margin_implies_subexponential_tail():
    item = by_id()["E32"]
    assert item.status == AuditStatus.PASS
    assert item.residual == 0.0
    assert item.value["gap_to_upper"].is_nonnegative


def test_e50_positive_phase_gradient_floor_bounds_coherence():
    item = by_id()["E50"]
    assert item.status == AuditStatus.PASS
    assert item.residual == 0.0
    assert item.value["coherence_integrand"].is_nonnegative
    assert item.value["upper_minus_integrand"].is_nonnegative


def test_e41_and_e72_follow_from_discrete_retention_count_bounds():
    results = by_id()
    for equation_id in ("E41", "E72"):
        item = results[equation_id]
        assert item.status == AuditStatus.PASS
        assert item.residual == 0.0
        assert item.value["upper_minus_realized"].is_nonnegative


def test_e19_gap_coefficient_is_fixed_if_mass_sectors_are_identified():
    item = by_id()["E19"]
    assert item.status == AuditStatus.CONDITIONAL
    assert item.residual == 0.0
    assert item.value["mass_squared_ratio"].name == "C_gap"
    assert item.value["consistency_coefficient"] == [1]


def test_top7_planar_reduction_is_mass_squared_not_linear_mass_energy():
    item = by_id()["TOP7"]
    assert item.status == AuditStatus.CONDITIONAL
    assert item.residual == 0.0
    assert item.value["d_mass_over_energy_d_kappa"] != 0


def test_corr2_mean_amplitude_closure_has_quantified_error_band():
    item = by_id()["CORR2"]
    assert item.status == AuditStatus.PASS
    assert item.residual == 0.0
    assert str(item.value["lower_ratio"]) == "1/(eta + 1)"
    assert str(item.value["upper_ratio"]) == "-1/(eta - 1)"
    assert str(item.value["relative_error_cap"]) == "-eta/(eta - 1)"
    assert item.value["small_intermitttency_limit"] == 0


def test_fourth_derivation_batch_increases_pass_count():
    results = list(run_full_audit())
    assert sum(item.status == AuditStatus.PASS for item in results) == 68
    assert len(results) == 142