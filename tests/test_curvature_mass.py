"""Tests for D1_10 and the curvature sigma distinctions."""

from wct_sympy.checks import (
    check_curvature_mass_dimension,
    check_sigma_dimension,
    check_sigma_raw_not_inverse_length,
)
from wct_sympy.dimensions import INVERSE_LENGTH, INVERSE_LENGTH_SQUARED, MASS


def test_curvature_mass_passes():
    r = check_curvature_mass_dimension()
    assert r.status == "PASS"
    assert r.value == str(MASS)


def test_sigma_dimension_passes():
    r = check_sigma_dimension()
    assert r.status == "PASS"
    assert r.value == str(INVERSE_LENGTH)


def test_sigma_raw_distinct_from_sigma():
    r = check_sigma_raw_not_inverse_length()
    assert r.status == "PASS"
    assert r.value == str(INVERSE_LENGTH_SQUARED)
