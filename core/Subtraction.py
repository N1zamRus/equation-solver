from core.BigFloat import BigFloat, get_BASE, create_BigFloat


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

    while result and result[-1] == 0:
        result.pop()

    return result


if __name__ == "__main__":
    a = create_BigFloat("5")
    b = create_BigFloat("2")

    print(Sub(a, b))
