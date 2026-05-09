from core.BigFloat import (
    BigFloat,
    get_BASE,
    get_blocks,
    get_exp10,
    get_sign,
    normalize,
    get_BASE_DIGITS,
)
from core.BigFloat_utility import slice_blocks
from core.Multiply import Mul
from core.Subtraction import Sub
from core.Division_utility import (
    calc_top,
    calc_scale,
    calc_x0_mantissa,
    calc_work_precision,
    has_enough_blocks,
    newton_step,
)


def make_x0(b: BigFloat) -> BigFloat:
    b = abs(normalize(b))
    b_blocks = get_blocks(b)

    take = min(4, len(b_blocks))
    dropped = len(b_blocks) - take

    top = calc_top(b_blocks, dropped, get_BASE())
    scale = calc_scale(dropped, get_exp10(b), get_BASE_DIGITS())

    int_x0, div_digits = calc_x0_mantissa(top, take, get_BASE_DIGITS())
    res_exp = -div_digits - scale

    return normalize(BigFloat(1, slice_blocks(str(int_x0), get_BASE_DIGITS()), res_exp))


def Inv(b: BigFloat, iteration=15, precision=2005, extra_blocks=5) -> BigFloat:
    result_sign = get_sign(b)
    b_abs = abs(normalize(b))

    x = make_x0(b_abs)

    current_blocks = 2
    max_work_precision = precision + extra_blocks

    for _ in range(iteration):
        if has_enough_blocks(x, precision):
            break

        current_blocks *= 2
        work_precision = calc_work_precision(current_blocks, extra_blocks, max_work_precision)

        x = newton_step(b_abs, x, current_blocks, work_precision)

    if result_sign < 0:
        x = -x

    return normalize(x)


def Div(a: BigFloat, b: BigFloat, precision=2026) -> BigFloat:
    inv_b = Inv(b, iteration=12, precision=precision)
    return Mul(a, inv_b, precision)