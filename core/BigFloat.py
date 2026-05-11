from __future__ import annotations
from core.BigFloat_utility import (
    BASE,
    BASE_DIGITS,
    get_mantiss,
    bigfloat_string,
    slice_blocks,
    make_carry,
    div_blocks_10,
    drop_zero_blocks,
    del_zeros,
    compare_abs,
    shift_exp,
    parse_sign,
    parse_exponent,
    parse_fraction,
    remove_top_zeros,
    cut_blocks,
    calc_new_exp,
    no_rounding_needed,
)
from core.Special_values import Nan, Infinity


class BigFloat:
    BASE_DIGITS = BASE_DIGITS
    BASE = BASE

    def __init__(self, sign: int, blocks: list[int], exp10: int):
        self.sign = sign
        self.blocks = blocks
        self.exp10 = exp10

    def __repr__(self) -> str:
        return bigfloat_string(self)

    def __abs__(self) -> BigFloat:
        return BigFloat(sign=1, blocks=self.blocks, exp10=self.exp10)

    def __neg__(self) -> BigFloat:
        return BigFloat(sign=-1 * self.sign, blocks=self.blocks, exp10=self.exp10)

    def __eq__(self, other: BigFloat) -> bool:
        return compare(self, other) == 0

    def __ne__(self, other: BigFloat) -> bool:
        return compare(self, other) != 0

    def __lt__(self, other: BigFloat) -> bool:
        return compare(self, other) < 0

    def __le__(self, other: BigFloat) -> bool:
        return compare(self, other) <= 0

    def __gt__(self, other: BigFloat) -> bool:
        return compare(self, other) > 0

    def __ge__(self, other: BigFloat) -> bool:
        return compare(self, other) >= 0


def get_blocks(cls: BigFloat) -> list[int]:
    return cls.blocks


def get_sign(cls: BigFloat) -> int:
    return cls.sign


def get_exp10(cls: BigFloat) -> int:
    return cls.exp10


def get_BASE(cls=BigFloat) -> int:
    return cls.BASE


def get_BASE_DIGITS(cls=BigFloat) -> int:
    return cls.BASE_DIGITS


def is_zero(number: BigFloat) -> bool:
    blocks = get_blocks(number)
    for val in blocks:
        if val != 0:
            return False
    return True


def create_BigFloat(num: str) -> BigFloat:
    num = num.replace(",", ".").replace("_", "")

    sign, num = parse_sign(num)

    if num == "nan":
        return Nan()

    if num in ("inf", "Infinity", "infinity"):
        return Infinity(sign)
    
    num, exp_from_e = parse_exponent(num)
    num, exp_from_dot = parse_fraction(num)

    exp10 = exp_from_e + exp_from_dot
    num = num.lstrip("0") or "0"

    blocks = slice_blocks(num, get_BASE_DIGITS())
    return normalize(BigFloat(sign, blocks, exp10))


def normalize(num: BigFloat) -> BigFloat:
    sign = num.sign
    exp10 = num.exp10
    blocks = num.blocks.copy()

    blocks = remove_top_zeros(blocks)

    if not blocks:
        return BigFloat(1, [0], 0)

    if exp10 < 0:
        blocks, exp10 = drop_zero_blocks(blocks, exp10, get_BASE_DIGITS())

        while exp10 < 0 and blocks[0] % 10 == 0:
            div_blocks_10(blocks, get_BASE())
            exp10 += 1

    blocks = remove_top_zeros(blocks)

    if not blocks:
        return BigFloat(1, [0], 0)

    return BigFloat(sign, blocks, exp10)


def align(a: BigFloat, b: BigFloat) -> tuple[BigFloat, BigFloat]:
    min_exp = min(a.exp10, b.exp10)

    if a.exp10 > min_exp:
        a = shift_exp(a, a.exp10 - min_exp)

    if b.exp10 > min_exp:
        b = shift_exp(b, b.exp10 - min_exp)

    return a, b


def compare(self: BigFloat, other: BigFloat) -> int:
    a = normalize(self)
    b = normalize(other)

    if is_zero(a) and is_zero(b):
        return 0

    if a.sign != b.sign:
        return 1 if a.sign > b.sign else -1

    a, b = align(a, b)
    cmp_abs = compare_abs(a, b)

    if a.sign == 1:
        return cmp_abs
    else:
        return -cmp_abs


def BigFloat_round(num: BigFloat, precision: int) -> BigFloat:
    blocks = get_blocks(num)
    exp = get_exp10(num)
    old_len = len(blocks)

    if no_rounding_needed(blocks, precision):
        return num

    new_blocks = cut_blocks(blocks, precision)
    new_exp = calc_new_exp(exp, old_len, len(new_blocks), get_BASE_DIGITS())

    return BigFloat(get_sign(num), new_blocks, new_exp)