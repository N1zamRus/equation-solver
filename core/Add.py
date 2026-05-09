from core.BigFloat import (
    BigFloat,
    get_sign,
    get_exp10,
    get_blocks,
    get_BASE,
    align,
    normalize,
)

from core.Subtraction import sub_abs


def add_same_sign(a: BigFloat, b: BigFloat) -> BigFloat:
    res_blocks = add_abs(get_blocks(a), get_blocks(b))
    return normalize(BigFloat(get_sign(a), res_blocks, get_exp10(a)))


def add_diff_sign(a: BigFloat, b: BigFloat) -> BigFloat:
    if abs(a) > abs(b):
        res_blocks = sub_abs(get_blocks(a), get_blocks(b))
        return normalize(BigFloat(get_sign(a), res_blocks, get_exp10(a)))

    if abs(a) < abs(b):
        res_blocks = sub_abs(get_blocks(b), get_blocks(a))
        return normalize(BigFloat(get_sign(b), res_blocks, get_exp10(a)))

    return BigFloat(1, [0], 0)


def Add(a: BigFloat, b: BigFloat) -> BigFloat:
    a, b = align(a, b)

    if get_sign(a) == get_sign(b):
        return add_same_sign(a, b)

    return add_diff_sign(a, b)


def add_abs(a_blocks: list[int], b_blocks: list[int]):
    max_len = max(len(a_blocks), len(b_blocks))
    BASE = get_BASE()

    result = []
    carry = 0

    for i in range(max_len):
        a = a_blocks[i] if i < len(a_blocks) else 0
        b = b_blocks[i] if i < len(b_blocks) else 0

        total = a + b + carry

        result.append(total % BASE)
        carry = total // BASE

    if carry:
        result.append(carry)

    return result