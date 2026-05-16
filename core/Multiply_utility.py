from math import pi, cos, sin


ROOTS_CACHE = {}


def next_power_two(need: int) -> int:
    n = 1
    while n < need:
        n *= 2
    return n


def get_cache_roots(n: int) -> tuple[list[complex], list[complex]]:
    if n not in ROOTS_CACHE:
        w_forward = []
        w_reverse = []
        for k in range(n // 2):
            angle = 2 * pi * k / n
            w = complex(cos(angle), sin(angle))
            w_forward.append(w)
            w_reverse.append(w.conjugate())
        ROOTS_CACHE[n] = (w_forward, w_reverse)
    return ROOTS_CACHE[n]


def blocks_to_complex(a_blocks: list[int], b_blocks: list[int], n: int) -> list[complex]:
    result = [0] * n
    for i in range(n):
        result[i] = complex(a_blocks[i], b_blocks[i])
    return result


def reverse_bits(a: list[int]) -> None:
    """
    0 = 00 -> 00 = 0
    1 = 01 -> 10 = 2
    2 = 10 -> 01 = 1
    3 = 11 -> 11 = 3
    """
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit

        if i < j:
            temp = a[i]
            a[i] = a[j]
            a[j] = temp


def unpack_fft(c_fft: list[complex], n: int) -> tuple[list[complex], list[complex]]:
    """
    A = (z + conj(z)) / 2
    B = (z - conj(z)) / 2i
    """
    a_fft = [0] * n
    b_fft = [0] * n

    c0 = c_fft[0].conjugate()
    a_fft[0] = (c_fft[0] + c0) / 2
    b_fft[0] = (c_fft[0] - c0) / (2j)

    for k in range(1, n):
        ck = c_fft[n - k].conjugate()
        a_fft[k] = (c_fft[k] + ck) / 2
        b_fft[k] = (c_fft[k] - ck) / (2j)

    return a_fft, b_fft


def normalize_fft(c_blocks: list[complex], n: int) -> list[complex]:
    inv_n = 1 / n
    for i in range(len(c_blocks)):
        c_blocks[i] *= inv_n
    return c_blocks


def round_coeffs(c_blocks: list[complex], n: int) -> list[int]:
    coeffs = [0] * n
    for i in range(n):
        coeffs[i] = round(c_blocks[i].real)
    return coeffs

