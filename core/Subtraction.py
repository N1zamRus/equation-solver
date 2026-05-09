from core.BigFloat import BigFloat, get_BASE, create_BigFloat
from core.BigFloat_utility import remove_top_zeros


def Sub(a: BigFloat, b: BigFloat):
    from core.Add import Add

    return Add(a, -b)


def sub_abs(a_blocks: list[int], b_blocks: list[int]) -> list[int]:
    BASE = get_BASE()
    max_len = max(len(a_blocks), len(b_blocks))

    result = []
    borrow = 0

    for i in range(max_len):
        a = a_blocks[i]
        b = b_blocks[i] if i < len(b_blocks) else 0

        total = a - b - borrow

        if total < 0:
            total += BASE
            borrow = 1
        else:
            borrow = 0

        result.append(total)

    return remove_top_zeros(result)
