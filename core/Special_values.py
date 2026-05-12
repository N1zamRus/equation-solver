from __future__ import annotations
from dataclasses import dataclass

class Nan:
    def __neg__(self):
        return Nan()

    def __abs__(self):
        return Nan()

    def __eq__(self, other):
        return False

    def __ne__(self, other):
        return True

    def __repr__(self):
        return "nan"


@dataclass
class Infinity:
    sign: int

    def __neg__(self):
        return Infinity(-self.sign)

    def __abs__(self):
        return Infinity(1)

    def __repr__(self):
        return "inf" if self.sign > 0 else "-inf"


def is_nan(value):
    return isinstance(value, Nan)


def is_infinity(value):
    return isinstance(value, Infinity)


def is_special_value(value):
    return is_nan(value) or is_infinity(value)
