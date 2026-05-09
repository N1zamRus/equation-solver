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
