from decimal import getcontext, MAX_EMAX, MIN_EMIN
from random import Random
from time import perf_counter

import pytest

from core.Add import Add
from core.BigFloat import create_BigFloat
from tests.test_utility import make_signed_random_pairs, to_decimal, bigfloat_decimal


ADD_TIMES = []

RANDOM_PAIRS_COUNT = 10
RANDOM_NUMBER_LENGTH = 10000
RANDOM_SEED = 7536

getcontext().prec = RANDOM_NUMBER_LENGTH * 2 + 10
getcontext().Emax = MAX_EMAX
getcontext().Emin = MIN_EMIN


@pytest.mark.parametrize("left, right", [
    ("0", "0"),
    ("1", "0"),
    ("0", "1"),
    ("1", "-1"),
    ("-1", "-1"),
    ("1000000", "1"),
    ("1", "0,1"),
    ("999", "-1000"),
    ("-0,5", "0,5"),
    ("1", "0,000001"),
])
def test_add_edge_cases(left, right):
    actual = Add(create_BigFloat(left), create_BigFloat(right))
    expected = to_decimal(left) + to_decimal(right)
    assert bigfloat_decimal(actual) == expected


@pytest.mark.parametrize("left, right", [
    ("99999", "1"),               # перенос через границу блока: (BASE-1) + 1 = BASE
    ("99999", "99999"),           # сумма двух полных блоков
    ("9999999999", "1"),          # цепной перенос через два блока
    ("100000", "-1"),             # заём через границу
    ("100000", "-100000"),        # взаимная отмена, результат ноль
    ("99999", "0.00001"),         # целая часть на границе блока + дробная
    ("-99999", "-1"),             # отрицательные с переносом
    ("10000000000", "1"),         # перенос в третий блок
    ("99999999999999999999", "1"),
])
def test_add_block_boundary(left, right):
    actual = Add(create_BigFloat(left), create_BigFloat(right))
    expected = to_decimal(left) + to_decimal(right)
    assert bigfloat_decimal(actual) == expected


@pytest.mark.parametrize("left, right", make_signed_random_pairs(
    Random(RANDOM_SEED), RANDOM_PAIRS_COUNT, RANDOM_NUMBER_LENGTH,
))
def test_random_add_with_decimal(left, right):
    start = perf_counter()
    actual = Add(create_BigFloat(left), create_BigFloat(right))
    end = perf_counter()
    ADD_TIMES.append(end - start)

    expected = to_decimal(left) + to_decimal(right)
    assert bigfloat_decimal(actual) == expected


@pytest.fixture(scope="module", autouse=True)
def print_average_time():
    yield

    if ADD_TIMES:
        avg_add = sum(ADD_TIMES) / len(ADD_TIMES)
        print(f"\nМаксимальное время Add: {max(ADD_TIMES)}")
        print(f"\nСреднее время Add: {avg_add:.8f} сек\n")
