from core.BigFloat import (
    BigFloat,
    get_BASE,
    get_exp10,
    get_BASE_DIGITS,
    normalize,
    BigFloat_round,
    get_blocks,
)
from core.BigFloat_utility import slice_blocks
from core.Multiply import Mul
from core.Division_utility import calc_work_precision, calc_top, calc_scale
from core.Sqrt_utility import calc_next_sqrt, make_scale, calc_x0_mantissa

BASE_DIGITS = get_BASE_DIGITS()
BASE = get_BASE()


def make_x0(a: BigFloat, extra_blocks: int = 10) -> BigFloat:
    a = abs(normalize(a))
    a_blocks = get_blocks(a)

    take = min(4, len(a_blocks))
    take_digits = take * BASE_DIGITS + extra_blocks
    dropped = len(a_blocks) - take

    top = calc_top(a_blocks, dropped, BASE)
    scale = calc_scale(dropped, get_exp10(a), BASE_DIGITS)

    scale, top = make_scale(scale, top)

    res_mantiss, k = calc_x0_mantissa(top, take_digits)
    res_exp = -k - scale // 2

    res_bgf = BigFloat(1, slice_blocks(str(res_mantiss), BASE_DIGITS), res_exp)
    return normalize(res_bgf)


def Sqrt(a: BigFloat, precision: int = 2050, extra_blocks: int = 20, iteration: int = 12) -> BigFloat:
    x_old = make_x0(a, 10)
    current_blocks = 2
    max_work_precision = precision + extra_blocks

    for _ in range(iteration):
        current_blocks *= 2
        work_precision = calc_work_precision(current_blocks, extra_blocks, max_work_precision)

        x_old = calc_next_sqrt(a, x_old, work_precision)

        if enough_blocks(current_blocks, precision):
            break

    result = Mul(a, x_old, precision + extra_blocks)
    result = BigFloat_round(result, precision)
    return normalize(result)

def enough_blocks(current_blocks: int, precision: int) -> bool:
    return current_blocks >= precision