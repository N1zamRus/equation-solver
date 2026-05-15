from decimal import Decimal, getcontext, MAX_EMAX, MIN_EMIN
from core.Division import Div
from core.BigFloat import create_BigFloat, bigfloat_string
from time import perf_counter
from tests.test_utility import make_signed_random_pairs, to_decimal
from random import Random

import pytest


DIV_TIMES = []

RANDOM_PAIRS_COUNT = 10
RANDOM_NUMBER_LENGTH = 10000
RANDOM_SEED = 235434

getcontext().prec = 50000
getcontext().Emax = MAX_EMAX
getcontext().Emin = MIN_EMIN


@pytest.mark.parametrize("left, right", [
    ("1", "1"),
    ("0", "1"),
    ("-1", "1"),
    ("1", "-1"),
    ("-1", "-1"),
    ("4", "2"),
    ("1", "2"),
    ("-6", "3"),
    ("1", "3"),
    ("100", "1000"),
])
def test_division_edge_cases(left, right):
    left_bigfloat = create_BigFloat(left)
    right_bigfloat = create_BigFloat(right)

    actual = Div(left_bigfloat, right_bigfloat)

    expected = to_decimal(left) / to_decimal(right)
    actual_str = f"{Decimal(bigfloat_string(actual)):.10010f}"
    expected_str = f"{expected:.10010f}"

    assert actual_str[:10000] == expected_str[:10000]


@pytest.mark.parametrize("left, right", [
    ("1", "3"),           # бесконечная дробь: 0.333...
    ("1", "7"),           # бесконечная дробь: 0.142857...
    ("1", "99999"),       # знаменатель на границе блока
    ("100000", "99999"),  # числитель BASE, знаменатель BASE-1, результат чуть больше 1
    ("99999", "100000"),  # числитель BASE-1, знаменатель BASE, результат чуть меньше 1
    ("99999", "99999"),   # одинаковые граничные значения: результат = 1
    ("1", "100000"),      # 1 / BASE = 0.00001 (точное значение)
    ("100000", "3"),      # BASE / 3 = бесконечная дробь с большим числителем
])
def test_division_block_boundary(left, right):
    left_bigfloat = create_BigFloat(left)
    right_bigfloat = create_BigFloat(right)

    actual = Div(left_bigfloat, right_bigfloat)

    expected = to_decimal(left) / to_decimal(right)
    actual_str = f"{Decimal(bigfloat_string(actual)):.10010f}"
    expected_str = f"{expected:.10010f}"

    assert actual_str[:10000] == expected_str[:10000]


@pytest.mark.parametrize("left, right", make_signed_random_pairs(Random(RANDOM_SEED), RANDOM_PAIRS_COUNT, RANDOM_NUMBER_LENGTH))
def test_division(left, right):
    left_bigfloat = create_BigFloat(left)
    right_bigfloat = create_BigFloat(right)

    start = perf_counter()
    actual = Div(left_bigfloat, right_bigfloat)
    end = perf_counter()

    DIV_TIMES.append(end - start)

    expected = to_decimal(left) / to_decimal(right)
    actual_str = f"{Decimal(bigfloat_string(actual)):.10010f}"
    expected_str = f"{expected:.10010f}"

    assert actual_str[:10000] == expected_str[:10000]


@pytest.fixture(scope="module", autouse=True)
def print_average_time():
    yield

    if DIV_TIMES:
        avg_div = sum(DIV_TIMES) / len(DIV_TIMES)
        print(f"\nСреднее время Div: {avg_div:.8f} сек")