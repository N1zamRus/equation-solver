from decimal import Decimal, getcontext, MAX_EMAX, MIN_EMIN
from random import Random
from Add import Add
from BigFloat import create_BigFloat, get_exp10, get_mantiss, get_sign
from Subtraction import Sub
from test_utility import make_random_pairs
from time import perf_counter
from test_utility import to_decimal, bigfloat_decimal

import pytest

ADD_TIMES = []
SUB_TIMES = []

RANDOM_PAIRS_COUNT = 1000
RANDOM_NUMBER_LENGTH = 10000
RANDOM_SEED = 321541

getcontext().prec = RANDOM_NUMBER_LENGTH * 2 + 10
getcontext().Emax = MAX_EMAX
getcontext().Emin = MIN_EMIN

@pytest.mark.parametrize("left, right", make_random_pairs(Random(RANDOM_SEED), 
                                                          RANDOM_PAIRS_COUNT, 
                                                          RANDOM_NUMBER_LENGTH))
def test_random_add_with_decimal(left, right):
    left_bigfloat = create_BigFloat(left)
    right_bigfloat = create_BigFloat(right)

    start = perf_counter()
    actual = Add(left_bigfloat, right_bigfloat)
    end = perf_counter()

    ADD_TIMES.append(end - start)

    expected = to_decimal(left) + to_decimal(right)

    assert bigfloat_decimal(actual) == expected


@pytest.mark.parametrize("left, right", make_random_pairs(Random(RANDOM_SEED), 
                                                          RANDOM_PAIRS_COUNT, 
                                                          RANDOM_NUMBER_LENGTH))
def test_random_sub_with_decimal(left, right):
    left_bigfloat = create_BigFloat(left)
    right_bigfloat = create_BigFloat(right)

    start = perf_counter()
    actual = Sub(left_bigfloat, right_bigfloat)
    end = perf_counter()

    SUB_TIMES.append(end - start)

    expected = to_decimal(left) - to_decimal(right)

    assert bigfloat_decimal(actual) == expected

    """узкие случаи"""

@pytest.fixture(scope="module", autouse=True)
def print_average_operation_time():
    yield

    if ADD_TIMES:
        avg_add = sum(ADD_TIMES) / len(ADD_TIMES)
        print(f"\nСреднее время Add: {avg_add:.8f} сек")

    if SUB_TIMES:
        avg_sub = sum(SUB_TIMES) / len(SUB_TIMES)
        print(f"Среднее время Sub: {avg_sub:.8f} сек")


# pytest -s