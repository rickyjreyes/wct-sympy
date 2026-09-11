from wct_sympy.formal_upgrades import (
    check_core_integrability_threshold,
    check_curvature_lock_stationarity,
    check_helix_curvature_scale,
    check_hessian_finite_band_maximum,
    check_torus_shape_selector,
    run_formal_upgrades,
)


def test_torus_shape_selector():
    assert check_torus_shape_selector()["passed"]


def test_hessian_finite_band_maximum():
    assert check_hessian_finite_band_maximum()["passed"]


def test_helix_curvature_scale():
    assert check_helix_curvature_scale()["passed"]


def test_core_integrability_threshold():
    assert check_core_integrability_threshold()["passed"]


def test_curvature_lock_stationarity():
    assert check_curvature_lock_stationarity()["passed"]


def test_formal_upgrade_batch():
    report = run_formal_upgrades()
    assert report["passed"], report
