from BigFloat import (
    BigFloat,
    get_sign,
    get_exp10,
    get_blocks,
    get_BASE,
    align,
    normalize,
)

from Subtraction import sub_abs


def Add(a: BigFloat, b: BigFloat):
    a, b = align(a, b)

    a_blocks = get_blocks(a)
    b_blocks = get_blocks(b)

    if get_sign(a) == get_sign(b):
        res_blocks = add_abs(a_blocks, b_blocks)
        res_sign = get_sign(a)
        res_exp = get_exp10(a)

        return normalize(BigFloat(res_sign, res_blocks, res_exp))

    if abs(a) > abs(b):
        res_blocks = sub_abs(a_blocks, b_blocks)
        res_sign = get_sign(a)
        res_exp = get_exp10(a)

        return normalize(BigFloat(res_sign, res_blocks, res_exp))

    elif abs(a) < abs(b):
        res_blocks = sub_abs(b_blocks, a_blocks)
        res_sign = get_sign(b)
        res_exp = get_exp10(a)

        return normalize(BigFloat(res_sign, res_blocks, res_exp))

    else:
        return BigFloat(1, [0], 0)


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
