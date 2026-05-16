from core.BigFloat import BigFloat, get_sign, is_zero
from core.BigFloat_math import Add, Sub, Mul, short_Mul, Div, Sqrt
from core.Special_values import Nan, Infinity, is_nan, is_infinity


ZERO = BigFloat(1, [0], 0)


NumberValue = Nan | BigFloat | Infinity


def is_zero_value(value: NumberValue):
    if isinstance(value, BigFloat):
        return is_zero(value)
    return False


def value_sign(value: BigFloat | Infinity):
    if isinstance(value, Infinity):
        return value.sign

    if isinstance(value, BigFloat):
        if is_zero(value):
            return 1
        return get_sign(value)


def special_is_zero(value: NumberValue):
    if is_nan(value):
        return False

    if is_infinity(value):
        return False

    return is_zero(value)


def special_neg(value: NumberValue):
    if is_nan(value):
        return Nan()

    if is_infinity(value):
        return Infinity(-value.sign)

    return -value


def special_add(left: NumberValue, right: NumberValue):
    if is_nan(left) or is_nan(right):
        return Nan()

    if is_infinity(left) and is_infinity(right):
        if left.sign != right.sign:
            return Nan()
        return Infinity(left.sign)

    if is_infinity(left):
        return Infinity(left.sign)

    if is_infinity(right):
        return Infinity(right.sign)

    return Add(left, right)


def special_sub(left: NumberValue, right: NumberValue):
    if is_nan(left) or is_nan(right):
        return Nan()

    if is_infinity(left) and is_infinity(right):
        if left.sign == right.sign:
            return Nan()
        return Infinity(left.sign)

    if is_infinity(left):
        return Infinity(left.sign)

    if is_infinity(right):
        return Infinity(-right.sign)

    return Sub(left, right)


def special_mul(left: NumberValue, right: NumberValue, precision: int):
    if is_nan(left) or is_nan(right):
        return Nan()

    if is_infinity(left) and is_infinity(right):
        return Infinity(left.sign * right.sign)

    if is_infinity(left):
        if is_zero_value(right):
            return Nan()
        return Infinity(left.sign * value_sign(right))

    if is_infinity(right):
        if is_zero_value(left):
            return Nan()
        return Infinity(value_sign(left) * right.sign)

    return Mul(left, right, precision)


def special_short_mul(value: NumberValue, multiplier: int, exp_multiplier: int = 0):
    if is_nan(value):
        return Nan()

    if is_infinity(value):
        if multiplier == 0:
            return Nan()

        multiplier_sign = 1 if multiplier > 0 else -1
        return Infinity(value.sign * multiplier_sign)

    return short_Mul(value, multiplier, exp_multiplier)


def special_div(left: NumberValue, right: NumberValue, precision: int):
    if is_nan(left) or is_nan(right):
        return Nan()

    if is_infinity(left) and is_infinity(right):
        return Nan()

    if is_infinity(left):
        if is_zero_value(right):
            return Infinity(left.sign)

        return Infinity(left.sign * value_sign(right))

    if is_infinity(right):
        return ZERO

    if is_zero(right):
        if is_zero(left):
            return Nan()

        return Infinity(value_sign(left))

    return Div(left, right, precision)


def special_sqrt(value: NumberValue, precision: int):
    if is_nan(value):
        return Nan()

    if is_infinity(value):
        if value.sign > 0:
            return Infinity(1)
        return Nan()

    if get_sign(value) < 0 and not is_zero(value):
        return Nan()

    return Sqrt(value, precision)


def special_lt(left: NumberValue, right: NumberValue):
    """self < other"""
    if is_nan(left) or is_nan(right):
        return False

    if is_infinity(left) and is_infinity(right):
        return left.sign < right.sign

    if is_infinity(left):
        return left.sign < 0

    if is_infinity(right):
        return right.sign > 0

    return left < right


def special_ge(left: NumberValue, right: NumberValue):
    """self >= other"""
    if is_nan(left) or is_nan(right):
        return False

    if is_infinity(left) and is_infinity(right):
        return left.sign >= right.sign

    if is_infinity(left):
        return left.sign > 0

    if is_infinity(right):
        return right.sign < 0

    return left >= right