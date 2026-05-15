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


def fft_butterfly(a: list[complex], i: int, j: int, w: complex) -> None:
    u = a[i]
    v = a[j] * w

    a[i] = u + v
    a[j] = u - v


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
    a_fft = []
    b_fft = []

    for k in range(n):
        a_fft.append((c_fft[k] + c_fft[(n - k) % n].conjugate()) / 2)
        b_fft.append((c_fft[k] - c_fft[(n - k) % n].conjugate()) / (2j))

    return a_fft, b_fft


def normalize_fft(c_blocks: list[complex], n: int) -> list[complex]:
    for i in range(len(c_blocks)):
        c_blocks[i] = c_blocks[i] / n
    return c_blocks


def round_coeffs(c_blocks: list[complex], n: int) -> list[int]:
    coeffs = []
    for i in range(n):
        coeffs.append(round(c_blocks[i].real))
    return coeffs

