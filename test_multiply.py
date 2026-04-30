from decimal import Decimal, getcontext, MAX_EMAX, MIN_EMIN
from Multiply import Mul
from BigFloat import create_BigFloat
from test_utility import make_random_pairs
from time import perf_counter
from test_utility import to_decimal, bigfloat_decimal
from random import Random

import pytest

MUL_TIMES = []

RANDOM_PAIRS_COUNT = 100
RANDOM_NUMBER_LENGTH = 10000
RANDOM_SEED = 235434

getcontext().prec = RANDOM_NUMBER_LENGTH * 2 + 10
getcontext().Emax = MAX_EMAX
getcontext().Emin = MIN_EMIN

@pytest.mark.parametrize("left, right", make_random_pairs(Random(RANDOM_SEED), 
                                                          RANDOM_PAIRS_COUNT, 
                                                          RANDOM_NUMBER_LENGTH))
def test_random_multiply_with_decimal(left, right):
    left_bigfloat = create_BigFloat(left)
    right_bigfloat = create_BigFloat(right)

    start = perf_counter()
    actual = Mul(left_bigfloat, right_bigfloat)
    end = perf_counter()

    MUL_TIMES.append(end - start)

    expected = to_decimal(left) * to_decimal(right)

    assert bigfloat_decimal(actual) == expected

@pytest.fixture(scope="module", autouse=True)
def print_average_operation_time():
    yield

    if MUL_TIMES:
        avg_mul = sum(MUL_TIMES) / len(MUL_TIMES)
        print(f"\nСреднее время Mul: {avg_mul:.8f} сек")