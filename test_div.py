from decimal import Decimal, getcontext, MAX_EMAX, MIN_EMIN
from Division import Div
from BigFloat import create_BigFloat, bigfloat_string
from time import perf_counter
from test_utility import make_random_pairs
from random import Random

import pytest


DIV_TIMES = []

RANDOM_PAIRS_COUNT = 10
RANDOM_NUMBER_LENGTH = 10000
RANDOM_SEED = 235434

getcontext().prec = 50000
getcontext().Emax = MAX_EMAX
getcontext().Emin = MIN_EMIN


@pytest.mark.parametrize("left, right",make_random_pairs(Random(RANDOM_SEED), RANDOM_PAIRS_COUNT, RANDOM_NUMBER_LENGTH))
def test_division(left, right):
    left_bigfloat = create_BigFloat(left)
    right_bigfloat = create_BigFloat(right)

    start = perf_counter()
    actual = Div(left_bigfloat, right_bigfloat)
    end = perf_counter()

    DIV_TIMES.append(end - start)

    expected = Decimal(bigfloat_string(left_bigfloat)) / Decimal(bigfloat_string(right_bigfloat))
    expected = f"{expected:.10010f}"

    actual_str = bigfloat_string(actual)

    assert actual_str[:10000] == expected[:10000]


@pytest.fixture(scope="module", autouse=True)
def print_average_time():
    yield

    if DIV_TIMES:
        avg_div = sum(DIV_TIMES) / len(DIV_TIMES)
        print(f"\nСреднее время Div: {avg_div:.8f} сек")