from wct_sympy.audit import run_full_audit
from wct_sympy.models import AuditStatus


def result(equation_id):
    return next(item for item in run_full_audit() if item.equation_id == equation_id)


def test_dispersion_peak_derivation():
    item = result("E12")
    assert item.status == AuditStatus.PASS
    assert item.value["second_derivative"].is_negative


def test_log_laplacian_identity():
    assert result("EX").status == AuditStatus.PASS


def test_cole_hopf_identity():
    assert result("EZ").status == AuditStatus.PASS


def test_e12_e64_factor_mismatch():
    item = result("E64")
    assert item.status == AuditStatus.FAIL
    assert str(item.value["ratio"]) == "sqrt(2)"
