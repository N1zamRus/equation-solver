from core.BigFloat import (
    BigFloat,
    get_blocks,
    get_exp10,
    make_carry,
    normalize,
    get_sign,
    create_BigFloat,
    bigfloat_string,
    BigFloat_round,
)
from core.Multiply_utility import (
    next_power_two,
    get_cache_roots,
    blocks_to_complex,
    unpack_fft,
    normalize_fft,
    round_coeffs,
    fft_butterfly,
    reverse_bits,
)
from decimal import getcontext, MAX_EMAX, MIN_EMIN

getcontext().prec = 21000
getcontext().Emax = MAX_EMAX
getcontext().Emin = MIN_EMIN

N = 0


def FFT(a: list[complex], w_root: list[complex]) -> list[complex]:
    length = 2
    n = len(a)

    if n == 1:
        return a

    while length <= n:
        step = n // length
        for start in range(0, n, length):
            for j in range(0, length // 2):
                w = w_root[j * step]
                fft_butterfly(a, start + j, start + j + length // 2, w)
        length *= 2

    return a


def Mul(a: BigFloat, b: BigFloat, precision=2026) -> BigFloat:
    global N

    result_sign = get_sign(a) * get_sign(b)
    result_exp10 = get_exp10(a) + get_exp10(b)

    a_blocks = get_blocks(a).copy()
    b_blocks = get_blocks(b).copy()

    result_len = len(a_blocks) + len(b_blocks) - 1
    N = next_power_two(result_len)

    w_default, w_revers = get_cache_roots(N)

    a_blocks += [0] * (N - len(a_blocks))
    b_blocks += [0] * (N - len(b_blocks))

    c = blocks_to_complex(a_blocks, b_blocks, N)

    reverse_bits(c)
    c_fft = FFT(c, w_default)

    a_fft, b_fft = unpack_fft(c_fft, N)

    c_blocks = [a_fft[i] * b_fft[i] for i in range(N)]

    reverse_bits(c_blocks)
    c_blocks = FFT(c_blocks, w_revers)

    c_blocks = normalize_fft(c_blocks, N)
    coeffs = round_coeffs(c_blocks, N)

    res_BF = normalize(BigFloat(result_sign, make_carry(coeffs), result_exp10))

    if precision != 0:
        res_BF = BigFloat_round(res_BF, precision)

    return res_BF


def short_Mul(num: BigFloat, multiplier: int, exp_multiplier: int = 0) -> BigFloat:
    res_sign = get_sign(num) * (1 if multiplier > 0 else -1)
    res_exp = get_exp10(num) + exp_multiplier
    num_blocks = get_blocks(num).copy()

    num_blocks = multiply_blocks(num_blocks, multiplier)
    num_blocks = make_carry(num_blocks)

    return BigFloat(res_sign, num_blocks, res_exp)


def multiply_blocks(blocks: list[int], multiplier: int) -> list[int]:
    for i in range(len(blocks)):
        blocks[i] *= abs(multiplier)
    return blocks

KARATSUBA_LIMIT = 15


def add_blocks(a: list[int], b: list[int]) -> list[int]:
    length = max(len(a), len(b))
    result = [0] * length
    for i in range(len(a)):
        result[i] += a[i]
    for i in range(len(b)):
        result[i] += b[i]
    return result


def sub_blocks(a: list[int], b: list[int]) -> list[int]:
    length = max(len(a), len(b))
    result = [0] * length
    for i in range(len(a)):
        result[i] += a[i]
    for i in range(len(b)):
        result[i] -= b[i]
    return result


def shift_blocks(blocks: list[int], n: int) -> list[int]:
    return [0] * n + blocks


def naive_mul_blocks(a: list[int], b: list[int]) -> list[int]:
    if not a or not b:
        return [0]
    c = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            c[i + j] += a[i] * b[j]
    return c


def calc_z(a_blocks: list[int], b_blocks: list[int]) -> list[int]:
    if len(a_blocks) <= KARATSUBA_LIMIT or len(b_blocks) <= KARATSUBA_LIMIT:
        return naive_mul_blocks(a_blocks, b_blocks)

    mid = max(len(a_blocks), len(b_blocks)) // 2

    a_low, a_high = a_blocks[:mid], a_blocks[mid:]
    b_low, b_high = b_blocks[:mid], b_blocks[mid:]

    z0 = calc_z(a_low, b_low)
    z2 = calc_z(a_high, b_high)
    z1 = sub_blocks(
        calc_z(add_blocks(a_low, a_high), add_blocks(b_low, b_high)),
        add_blocks(z0, z2),
    )

    result = add_blocks(z0, shift_blocks(z1, mid))
    result = add_blocks(result, shift_blocks(z2, mid * 2))
    return result


def middle_mul(a: BigFloat, b: BigFloat) -> BigFloat:
    a_blocks = get_blocks(a).copy()
    b_blocks = get_blocks(b).copy()

    result_blocks = calc_z(a_blocks, b_blocks)
    result_blocks = make_carry(result_blocks)

    return normalize(BigFloat(get_sign(a) * get_sign(b), result_blocks, get_exp10(a) + get_exp10(b)))


FFT_THRESHOLD = 150


def smart_mul(a: BigFloat, b: BigFloat, precision: int = 2026) -> BigFloat:
    max_blocks = max(len(get_blocks(a)), len(get_blocks(b)))
    if max_blocks < FFT_THRESHOLD:
        result = middle_mul(a, b)
        if precision != 0:
            result = BigFloat_round(result, precision)
        return result
    return Mul(a, b, precision)