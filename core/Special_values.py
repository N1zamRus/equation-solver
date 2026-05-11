from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.BigFloat import BigFloat, get_sign, is_zero
from solver.models import Coefs
from solver.models import get_a, get_b, get_c


ZERO = BigFloat(1, [0], 0)


class Special(ABC):
    @abstractmethod
    def __add__(self, other: "Nan" | BigFloat | "Infinity"):
        pass

    @abstractmethod
    def __radd__(self, other: "Nan" | BigFloat | "Infinity"):
        pass

    @abstractmethod
    def __sub__(self, other: "Nan" | BigFloat | "Infinity"):
        pass

    @abstractmethod
    def __rsub__(self, other: "Nan" | BigFloat | "Infinity"):
        pass

    @abstractmethod
    def __mul__(self, other: "Nan" | BigFloat | "Infinity"):
        pass

    @abstractmethod
    def __rmul__(self, other: "Nan" | BigFloat | "Infinity"):
        pass

    @abstractmethod
    def __truediv__(self, other: "Nan" | BigFloat | "Infinity"):
        pass

    @abstractmethod
    def __rtruediv__(self, other: "Nan" | BigFloat | "Infinity"):
        pass

    @abstractmethod
    def __neg__(self):
        pass

    @abstractmethod
    def __abs__(self):
        pass


class Nan(Special):
    def __add__(self, other: "Nan" | BigFloat | "Infinity"):
        return Nan()

    def __radd__(self, other: "Nan" | BigFloat | "Infinity"):
        return Nan()

    def __sub__(self, other: "Nan" | BigFloat | "Infinity"):
        return Nan()

    def __rsub__(self, other: "Nan" | BigFloat | "Infinity"):
        return Nan()

    def __mul__(self, other: "Nan" | BigFloat | "Infinity"):
        return Nan()

    def __rmul__(self, other: "Nan" | BigFloat | "Infinity"):
        return Nan()

    def __truediv__(self, other: "Nan" | BigFloat | "Infinity"):
        return Nan()

    def __rtruediv__(self, other: "Nan" | BigFloat | "Infinity"):
        return Nan()

    def __neg__(self):
        return Nan()

    def __abs__(self):
        return Nan()

    def __eq__(self, other: "Nan" | BigFloat | "Infinity"):
        return False

    def __ne__(self, other: "Nan" | BigFloat | "Infinity"):
        return True

    def __lt__(self, other: "Nan" | BigFloat | "Infinity"):
        return False

    def __le__(self, other: "Nan" | BigFloat | "Infinity"):
        return False

    def __gt__(self, other: "Nan" | BigFloat | "Infinity"):
        return False

    def __ge__(self, other: "Nan" | BigFloat | "Infinity"):
        return False

    def __repr__(self):
        return "nan"


@dataclass
class Infinity(Special):
    sign: int

    def __add__(self, other: "Nan" | BigFloat | "Infinity"):
        if is_nan(other):
            return Nan()

        if is_infinity(other):
            if self.sign != other.sign:
                return Nan()
            return Infinity(self.sign)

        if is_finite(other):
            return Infinity(self.sign)

    def __radd__(self, other: "Nan" | BigFloat | "Infinity"):
        return self.__add__(other)

    def __sub__(self, other: "Nan" | BigFloat | "Infinity"):
        if is_nan(other):
            return Nan()

        if is_infinity(other):
            if self.sign == other.sign:
                return Nan()
            return Infinity(self.sign)

        if is_finite(other):
            return Infinity(self.sign)

    def __rsub__(self, other: "Nan" | BigFloat | "Infinity"):
        if is_nan(other):
            return Nan()

        if is_infinity(other):
            return other.__sub__(self)

        if is_finite(other):
            return Infinity(-self.sign)

    def __mul__(self, other: "Nan" | BigFloat | "Infinity"):
        if is_nan(other):
            return Nan()

        if is_infinity(other):
            return Infinity(self.sign * other.sign)

        if is_finite(other):
            if is_zero_value(other):
                return Nan()
            return Infinity(self.sign * value_sign(other))

    def __rmul__(self, other: "Nan" | BigFloat | "Infinity"):
        return self.__mul__(other)

    def __truediv__(self, other: "Nan" | BigFloat | "Infinity"):
        if is_nan(other):
            return Nan()

        if is_infinity(other):
            return Nan()

        if is_finite(other):
            if is_zero_value(other):
                return Infinity(self.sign)
            return Infinity(self.sign * value_sign(other))

    def __rtruediv__(self, other: "Nan" | BigFloat | "Infinity"):
        if is_nan(other):
            return Nan()

        if is_infinity(other):
            return Nan()

        if is_finite(other):
            return ZERO

    def __neg__(self):
        return Infinity(-self.sign)

    def __abs__(self):
        return Infinity(1)

    def __eq__(self, other: "Nan" | BigFloat | "Infinity"):
        if is_nan(other):
            return False

        if is_infinity(other):
            return self.sign == other.sign

        return False

    def __ne__(self, other: "Nan" | BigFloat | "Infinity"):
        return not self.__eq__(other)

    def __lt__(self, other: "Nan" | BigFloat | "Infinity"):
        if is_nan(other):
            return False

        if is_infinity(other):
            return self.sign < other.sign

        if is_finite(other):
            return self.sign < 0

    def __le__(self, other: "Nan" | BigFloat | "Infinity"):
        if is_nan(other):
            return False

        if is_infinity(other):
            return self.sign <= other.sign

        if is_finite(other):
            return self.sign < 0

    def __gt__(self, other: "Nan" | BigFloat | "Infinity"):
        if is_nan(other):
            return False

        if is_infinity(other):
            return self.sign > other.sign

        if is_finite(other):
            return self.sign > 0

    def __ge__(self, other: "Nan" | BigFloat | "Infinity"):
        if is_nan(other):
            return False

        if is_infinity(other):
            return self.sign >= other.sign

        if is_finite(other):
            return self.sign > 0

    def __repr__(self):
        return "inf" if self.sign > 0 else "-inf"


def is_nan(value: "Nan" | BigFloat | "Infinity"):
    return isinstance(value, Nan)


def is_infinity(value: "Nan" | BigFloat | "Infinity"):
    return isinstance(value, Infinity)


def is_special_value(value: "Nan" | BigFloat | "Infinity"):
    return is_nan(value) or is_infinity(value)


def is_finite(value: "Nan" | BigFloat | "Infinity"):
    return isinstance(value, BigFloat)


def is_zero_value(value: "Nan" | BigFloat | "Infinity"):
    if isinstance(value, BigFloat):
        return is_zero(value)
    return False


def value_sign(value: Nan | BigFloat | "Infinity"):
    if isinstance(value, Infinity):
        return value.sign

    if isinstance(value, BigFloat):
        if is_zero(value):
            return 1
        return get_sign(value)

def has_special_coefs(coefs) -> bool:
    return (
        is_special_value(get_a(coefs))
        or is_special_value(get_b(coefs))
        or is_special_value(get_c(coefs))
    )