"""Tests for the Dimension algebra and the headline dimensional checks."""

from wct_sympy.dimensions import (
    ACTION,
    DIMENSIONLESS,
    Dimension,
    INVERSE_LENGTH,
    INVERSE_LENGTH_SQUARED,
    LENGTH,
    MASS,
    TIME,
    VELOCITY,
)


def test_base_dimensions():
    assert MASS == Dimension(1, 0, 0)
    assert LENGTH == Dimension(0, 1, 0)
    assert TIME == Dimension(0, 0, 1)


def test_multiplication_division():
    assert MASS * LENGTH == Dimension(1, 1, 0)
    assert (MASS * LENGTH) / LENGTH == MASS
    assert LENGTH / LENGTH == DIMENSIONLESS


def test_power():
    assert LENGTH ** 2 == Dimension(0, 2, 0)
    assert LENGTH ** -1 == INVERSE_LENGTH
    assert (LENGTH ** 2) ** 0.5 == LENGTH


def test_derived_dimensions():
    assert VELOCITY == Dimension(0, 1, -1)
    assert ACTION == Dimension(1, 2, -1)


def test_hbar_over_c_times_k_eff_is_mass():
    """The headline dimensional identity m = (hbar/c) * k_eff."""
    dim = ACTION / VELOCITY * INVERSE_LENGTH
    assert dim == MASS


def test_sigma_dimension_is_inverse_length():
    """sigma = sqrt(kappa^2 + tau^2) with kappa,tau ~ L^-1 -> L^-1."""
    summed = INVERSE_LENGTH ** 2  # kappa^2+tau^2 share dim, so it's L^-2
    sigma_dim = summed ** 0.5
    assert sigma_dim == INVERSE_LENGTH


def test_sigma_raw_is_NOT_inverse_length():
    """sigma_raw = kappa^2 + tau^2 has L^-2, not L^-1."""
    summed = INVERSE_LENGTH ** 2
    assert summed != INVERSE_LENGTH
    assert summed == INVERSE_LENGTH_SQUARED


def test_dimensionless_is_neutral():
    assert MASS * DIMENSIONLESS == MASS
    assert DIMENSIONLESS.is_dimensionless()
