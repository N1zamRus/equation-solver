from decimal import getcontext, MAX_EMAX, MIN_EMIN
from random import Random
from time import perf_counter

import pytest

from core.Subtraction import Sub
from core.BigFloat import create_BigFloat
from tests.test_utility import make_signed_random_pairs, to_decimal, bigfloat_decimal


SUB_TIMES = []

RANDOM_PAIRS_COUNT = 100
RANDOM_NUMBER_LENGTH = 10000
RANDOM_SEED = 34568

getcontext().prec = RANDOM_NUMBER_LENGTH * 2 + 10
getcontext().Emax = MAX_EMAX
getcontext().Emin = MIN_EMIN


@pytest.mark.parametrize("left, right", [
    ("0", "0"),
    ("1", "1"),
    ("1", "0"),
    ("0", "1"),
    ("-1", "-1"),
    ("1000000", "999999"),
    ("1,5", "0,5"),
    ("-5", "-3"),
    ("0,1", "0,1"),
    ("100", "-100"),
])
def test_sub_edge_cases(left, right):
    actual = Sub(create_BigFloat(left), create_BigFloat(right))
    expected = to_decimal(left) - to_decimal(right)
    assert bigfloat_decimal(actual) == expected


@pytest.mark.parametrize("left, right", [
    ("100000", "1"),               # заём через границу: BASE - 1 = BASE-1
    ("10000000000", "1"),          # заём через два блока
    ("100000", "99999"),           # разность на границе: 100000 - 99999 = 1
    ("9999999999", "9999999998"),  # почти равные, результат = 1
    ("100000", "100000"),          # равные, результат ноль
    ("-99999", "-100000"),         # отрицательные с займом
    ("1", "0.99999"),              # дробный заём: 1 - 0.99999 = 0.00001
    ("10000000000", "9999999999"), # большие числа, результат = 1
])
def test_sub_block_boundary(left, right):
    actual = Sub(create_BigFloat(left), create_BigFloat(right))
    expected = to_decimal(left) - to_decimal(right)
    assert bigfloat_decimal(actual) == expected


@pytest.mark.parametrize("left, right", make_signed_random_pairs(
    Random(RANDOM_SEED), RANDOM_PAIRS_COUNT, RANDOM_NUMBER_LENGTH,
))
def test_random_sub_with_decimal(left, right):
    start = perf_counter()
    actual = Sub(create_BigFloat(left), create_BigFloat(right))
    end = perf_counter()
    SUB_TIMES.append(end - start)

    expected = to_decimal(left) - to_decimal(right)
    assert bigfloat_decimal(actual) == expected


@pytest.fixture(scope="module", autouse=True)
def print_average_time():
    yield

    if SUB_TIMES:
        avg_sub = sum(SUB_TIMES) / len(SUB_TIMES)
        print(f"\nСреднее время Sub: {avg_sub:.8f} сек")
