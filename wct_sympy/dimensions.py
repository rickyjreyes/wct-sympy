"""Dimension algebra over (M, L, T) exponents.

Represent physical dimensions as exponent triples M^a L^b T^c.
Supports multiplication, division, integer/rational powers, and equality.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Union

Number = Union[int, float, Fraction]


def _to_fraction(x: Number) -> Fraction:
    if isinstance(x, Fraction):
        return x
    if isinstance(x, int):
        return Fraction(x)
    # float -> rational, but limit denominator to avoid noise
    return Fraction(x).limit_denominator(10**6)


@dataclass(frozen=True)
class Dimension:
    """Physical dimension as exponent triple M^a L^b T^c."""

    M: Fraction = Fraction(0)
    L: Fraction = Fraction(0)
    T: Fraction = Fraction(0)

    def __init__(self, M: Number = 0, L: Number = 0, T: Number = 0):
        object.__setattr__(self, "M", _to_fraction(M))
        object.__setattr__(self, "L", _to_fraction(L))
        object.__setattr__(self, "T", _to_fraction(T))

    def __mul__(self, other: "Dimension") -> "Dimension":
        if not isinstance(other, Dimension):
            return NotImplemented
        return Dimension(self.M + other.M, self.L + other.L, self.T + other.T)

    def __truediv__(self, other: "Dimension") -> "Dimension":
        if not isinstance(other, Dimension):
            return NotImplemented
        return Dimension(self.M - other.M, self.L - other.L, self.T - other.T)

    def __pow__(self, exponent: Number) -> "Dimension":
        e = _to_fraction(exponent)
        return Dimension(self.M * e, self.L * e, self.T * e)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Dimension):
            return NotImplemented
        return self.M == other.M and self.L == other.L and self.T == other.T

    def __hash__(self) -> int:
        return hash((self.M, self.L, self.T))

    def is_dimensionless(self) -> bool:
        return self.M == 0 and self.L == 0 and self.T == 0

    def __repr__(self) -> str:
        parts = []
        for sym, exp in (("M", self.M), ("L", self.L), ("T", self.T)):
            if exp == 0:
                continue
            if exp == 1:
                parts.append(sym)
            else:
                parts.append(f"{sym}^{exp}")
        return " ".join(parts) if parts else "1"


# --- Base dimensions ---
DIMENSIONLESS = Dimension(0, 0, 0)
MASS = Dimension(1, 0, 0)
LENGTH = Dimension(0, 1, 0)
TIME = Dimension(0, 0, 1)

# --- Derived dimensions used in WCT equations ---
VELOCITY = LENGTH / TIME                 # c: L T^-1
ACTION = MASS * (LENGTH ** 2) / TIME     # hbar: M L^2 T^-1
INVERSE_LENGTH = LENGTH ** -1            # k: L^-1
INVERSE_LENGTH_SQUARED = LENGTH ** -2    # L^-2

# Name -> Dimension lookup used by the registry
NAMED_DIMENSIONS = {
    "dimensionless": DIMENSIONLESS,
    "mass": MASS,
    "length": LENGTH,
    "time": TIME,
    "velocity": VELOCITY,
    "action": ACTION,
    "inverse_length": INVERSE_LENGTH,
    "inverse_length_squared": INVERSE_LENGTH_SQUARED,
}


def lookup(name: str) -> Dimension:
    if name not in NAMED_DIMENSIONS:
        raise KeyError(f"Unknown dimension name: {name!r}")
    return NAMED_DIMENSIONS[name]
