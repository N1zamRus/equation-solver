from decimal import Decimal, getcontext, MAX_EMAX, MIN_EMIN
from core.Multiply import Mul
from core.BigFloat import create_BigFloat, bigfloat_string
from time import perf_counter
from tests.test_utility import to_decimal, make_signed_random_pairs
from random import Random

import pytest

MUL_TIMES = []

RANDOM_PAIRS_COUNT = 100
RANDOM_NUMBER_LENGTH = 10000
RANDOM_SEED = 534119

getcontext().prec = RANDOM_NUMBER_LENGTH * 2 + 10
getcontext().Emax = MAX_EMAX
getcontext().Emin = MIN_EMIN

@pytest.mark.parametrize("left, right", [
    ("0", "1"),
    ("1", "1"),
    ("-1", "1"),
    ("-1", "-1"),
    ("2", "3"),
    ("1,5", "2"),
    ("1000", "1000"),
    ("0", "0"),
    ("-7", "8"),
    ("0,1", "0,1"),
])
def test_multiply_edge_cases(left, right):
    left_bigfloat = create_BigFloat(left)
    right_bigfloat = create_BigFloat(right)

    actual = Mul(left_bigfloat, right_bigfloat)

    expected = to_decimal(left) * to_decimal(right)
    actual_str = f"{Decimal(bigfloat_string(actual)):.10010f}"
    expected_str = f"{expected:.10010f}"

    assert actual_str[:10000] == expected_str[:10000]


@pytest.mark.parametrize("left, right", [
    ("99999", "99999"),       # произведение переполняет один блок: 9999800001
    ("100000", "100000"),     # BASE * BASE = BASE^2 = 10000000000
    ("99999", "100001"),      # 99999 * 100001 = 9999999999 (граница блока)
    ("99999", "2"),           # (BASE-1) * 2 = 199998, в одном блоке
    ("100000", "99999"),      # BASE * (BASE-1) = 9999900000
    ("-99999", "99999"),      # отрицательный с граничным значением
    ("99999", "0.00001"),     # граница блока * малая дробь = 0.99999
    ("100001", "99999"),      # (BASE+1) * (BASE-1) = BASE^2 - 1
])
def test_multiply_block_boundary(left, right):
    left_bigfloat = create_BigFloat(left)
    right_bigfloat = create_BigFloat(right)

    actual = Mul(left_bigfloat, right_bigfloat)

    expected = to_decimal(left) * to_decimal(right)
    actual_str = f"{Decimal(bigfloat_string(actual)):.10010f}"
    expected_str = f"{expected:.10010f}"

    assert actual_str[:10000] == expected_str[:10000]


@pytest.mark.parametrize("left, right", make_signed_random_pairs(Random(RANDOM_SEED),
                                                          RANDOM_PAIRS_COUNT,
                                                          RANDOM_NUMBER_LENGTH))
def test_multiply(left, right):
    left_bigfloat = create_BigFloat(left)
    right_bigfloat = create_BigFloat(right)

    start = perf_counter()
    actual = Mul(left_bigfloat, right_bigfloat)
    end = perf_counter()

    MUL_TIMES.append(end - start)

    expected = to_decimal(left) * to_decimal(right)
    actual_str = f"{Decimal(bigfloat_string(actual)):.10010f}"
    expected_str = f"{expected:.10010f}"

    assert actual_str[:10000] == expected_str[:10000]

@pytest.fixture(scope="module", autouse=True)
def print_average_time():
    yield

    if MUL_TIMES:
        avg_mul = sum(MUL_TIMES) / len(MUL_TIMES)
        print(f"\nСреднее время Mul: {avg_mul:.8f} сек")

# pytest -s test_multiply.py 2>&1 | tee results_mul.txt