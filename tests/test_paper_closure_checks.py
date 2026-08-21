from wct_sympy.paper_closure_checks import (
    check_beta0_amplitude_binding_identity,
    check_compact_contraction_factor,
    check_dsi_bijection,
    check_fixed_mass_spatial_scaling,
    check_quartic_coercivity_completion,
    check_real_1d_quotient_first_variation,
    run_paper_closure_checks,
)


def test_dsi_bijection_roundtrip():
    assert check_dsi_bijection()["passed"]


def test_compact_contraction_factor():
    assert check_compact_contraction_factor()["passed"]


def test_quartic_coercivity_completion():
    assert check_quartic_coercivity_completion()["passed"]


def test_fixed_mass_spatial_scaling():
    result = check_fixed_mass_spatial_scaling()
    assert result["passed"]
    assert str(result["mass"]) == "1"


def test_beta0_amplitude_binding_identity():
    assert check_beta0_amplitude_binding_identity()["passed"]


def test_real_1d_quotient_first_variation():
    assert check_real_1d_quotient_first_variation()["passed"]


def test_complete_paper_closure_batch():
    report = run_paper_closure_checks()
    assert report["passed"]
    assert len(report["checks"]) == 6
