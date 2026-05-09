from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.BigFloat import BigFloat


def calc_top(b_blocks: list[int], dropped: int, base: int) -> int:
    top = 0
    for i in range(len(b_blocks) - 1, dropped - 1, -1):
        top = top * base + b_blocks[i]
    return top


def calc_scale(dropped: int, exp10: int, base_digits: int) -> int:
    return dropped * base_digits + exp10


def calc_x0_mantissa(top: int, take: int, base_digits: int) -> tuple[int, int]:
    take_digits = take * base_digits + 20
    div_digits = take_digits - 1

    int_x0 = 10 ** div_digits // top
    return int_x0, div_digits


def calc_work_precision(current_blocks: int, extra_blocks: int, max_work_precision: int) -> int:
    return min(current_blocks + extra_blocks, max_work_precision)


def has_enough_blocks(x: BigFloat, precision: int) -> bool:
    from core.BigFloat import get_blocks
    return len(get_blocks(x)) >= precision


def newton_step(b_abs: BigFloat, x: BigFloat, current_blocks: int, work_precision: int) -> BigFloat:
    from core.BigFloat import BigFloat, BigFloat_round
    from core.Multiply import Mul
    from core.Subtraction import Sub

    TWO = BigFloat(1, [2], 0)
    bx = Mul(BigFloat_round(b_abs, current_blocks + 10), x, work_precision)
    right = Sub(TWO, bx)
    return Mul(x, right, work_precision)