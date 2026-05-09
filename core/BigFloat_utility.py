from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from BigFloat import BigFloat

BASE_DIGITS = 5
BASE = 10 ** BASE_DIGITS


def get_mantiss(cls: BigFloat) -> str:
    if not cls.blocks:
        return "0"

    parts = [str(cls.blocks[-1])]

    for i in range(len(cls.blocks) - 2, -1, -1):
        parts.append(str(cls.blocks[i]).zfill(cls.BASE_DIGITS))

    return "".join(parts)


def bigfloat_string(num: BigFloat) -> str:
    output_line = get_mantiss(num)
    num_sign = "-" if num.sign == -1 and output_line != "0" else ""
    num_exp = num.exp10

    if num_exp == 0:
        return num_sign + output_line
    if num_exp > 0:
        return num_sign + output_line + "0" * num_exp

    dot_pos = len(output_line) + num_exp
    if dot_pos > 0:
        return num_sign + output_line[:dot_pos] + "." + output_line[dot_pos:]
    else:
        return num_sign + "0." + "0" * (-dot_pos) + output_line


def slice_blocks(mantissa: str, base_digits: int = BASE_DIGITS) -> list[int]:
    blocks = []

    for i in range(len(mantissa), 0, -base_digits):
        start = max(0, i - base_digits)
        block = mantissa[start:i]
        blocks.append(int(block))

    return blocks


def make_carry(coeffs: list[int], base: int = BASE) -> list[int]:
    carry = 0
    blocks = []

    for x in coeffs:
        x = int(x) + carry

        blocks.append(x % base)
        carry = x // base

    while carry > 0:
        blocks.append(carry % base)
        carry //= base

    while len(blocks) > 1 and blocks[-1] == 0:
        blocks.pop()

    return blocks


def div_blocks_10(blocks: list[int], base: int) -> None:
    carry = 0

    for i in range(len(blocks) - 1, -1, -1):
        top = carry * base + blocks[i]
        blocks[i] = top // 10
        carry = top % 10

    while len(blocks) > 1 and blocks[-1] == 0:
        blocks.pop()


def drop_zero_blocks(blocks: list[int], exp10: int, base_digits: int) -> tuple[list[int], int]:
    drop = 0

    while True:
        if exp10 + base_digits > 0:
            break
        if len(blocks) - drop <= 1:
            break
        if blocks[drop] != 0:
            break

        drop += 1
        exp10 += base_digits

    if drop != 0:
        blocks = blocks[drop:]

    return blocks, exp10


def del_zeros(blocks: list[int]) -> list[int]:
    blocks = blocks.copy()

    while len(blocks) > 1 and blocks[-1] == 0:
        blocks.pop()

    return blocks


def compare_abs(a: BigFloat, b: BigFloat) -> int:
    a_blocks = del_zeros(a.blocks)
    b_blocks = del_zeros(b.blocks)

    if len(a_blocks) > len(b_blocks):
        return 1
    if len(a_blocks) < len(b_blocks):
        return -1

    for i in range(len(a_blocks) - 1, -1, -1):
        if a_blocks[i] > b_blocks[i]:
            return 1
        if a_blocks[i] < b_blocks[i]:
            return -1

    return 0


def shift_exp(num: BigFloat, exp_diff: int) -> BigFloat:
    from core.BigFloat import BigFloat

    if exp_diff <= 0:
        return BigFloat(num.sign, num.blocks.copy(), num.exp10)

    base = num.BASE
    base_digits = num.BASE_DIGITS

    block_shift = exp_diff // base_digits
    digit_shift = exp_diff % base_digits

    blocks = num.blocks.copy()

    if block_shift > 0:
        blocks = [0] * block_shift + blocks

    if digit_shift > 0:
        mul = 10 ** digit_shift
        carry = 0
        for i in range(len(blocks)):
            val = blocks[i] * mul + carry
            blocks[i] = val % base
            carry = val // base
        while carry > 0:
            blocks.append(carry % base)
            carry //= base

    return BigFloat(num.sign, blocks, num.exp10 - exp_diff)


def parse_sign(num: str) -> tuple[int, str]:
    if num[0] == "-":
        return -1, num[1:]
    if num[0] == "+":
        return 1, num[1:]
    return 1, num


def parse_exponent(num: str) -> tuple[str, int]:
    if "e" in num or "E" in num:
        parts = num.split("e") if "e" in num else num.split("E")
        return parts[0], int(parts[1])
    return num, 0


def parse_fraction(num: str) -> tuple[str, int]:
    if "." in num:
        dot_pos = num.find(".")
        digits_after_dot = len(num) - dot_pos - 1
        num = num.replace(".", "")
        return num, -digits_after_dot
    return num, 0


def remove_top_zeros(blocks: list[int]) -> list[int]:
    while blocks and blocks[-1] == 0:
        blocks.pop()
    return blocks


def cut_blocks(blocks: list[int], precision: int) -> list[int]:
    return blocks[-precision:]


def calc_new_exp(exp: int, old_len: int, new_len: int, base_digits: int) -> int:
    return exp + (old_len - new_len) * base_digits


def no_rounding_needed(blocks: list[int], precision: int) -> bool:
    return len(blocks) < precision