from __future__ import annotations
from math import floor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.BigFloat import BigFloat


def make_scale(scale: int, top: int) -> tuple[int, int]:
    if scale % 2 != 0:
        scale -= 1
        top *= 10
    return scale, top


def calc_x0_mantissa(top: int, take_digits: int) -> tuple[int, int]:
    sqrt_digits = (len(str(top)) + 1) // 2
    k = take_digits + sqrt_digits - 1

    res_mantiss = floor(10**k / top**0.5)
    return res_mantiss, k


def calc_next_sqrt(a: BigFloat, x_old: BigFloat, work_precision: int) -> BigFloat:
    from core.BigFloat import BigFloat, BigFloat_round, normalize
    from core.Multiply import Mul, short_Mul
    from core.Subtraction import Sub

    THREE = BigFloat(1, [3], 0)

    a_work = BigFloat_round(a, work_precision)

    qx = Mul(x_old, x_old, work_precision)
    ax2 = Mul(a_work, qx, work_precision)

    staple = Sub(THREE, ax2)
    x_staple = Mul(x_old, staple, work_precision)

    x_new = short_Mul(x_staple, 5, -1)
    return BigFloat_round(normalize(x_new), work_precision)