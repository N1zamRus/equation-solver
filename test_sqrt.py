from decimal import Decimal, getcontext, MAX_EMAX, MIN_EMIN
from random import Random
from time import perf_counter

import pytest

from Sqrt import Sqrt
from BigFloat import create_BigFloat, bigfloat_string
from test_utility import make_str_number


SQRT_TIMES = []

RANDOM_VALUES_COUNT = 23
RANDOM_NUMBER_LENGTH = 10000
RANDOM_SEED = 23421

getcontext().prec = 50000
getcontext().Emax = MAX_EMAX
getcontext().Emin = MIN_EMIN


def make_random_positive_numbers(rng: Random, count_test=RANDOM_VALUES_COUNT, length=RANDOM_NUMBER_LENGTH):
    numbers = []

    for _ in range(count_test):
        value = make_str_number(rng, length)
        decimal_value = Decimal(value.replace(',', '.'))

        if decimal_value <= 0:
            continue

        numbers.append(value)

    return numbers


@pytest.mark.parametrize('value', [
    '1',
    '4',
    '9',
    '16',
    '100',
    '0.25',
    '0.01',
    '2',
    '10',
])
def test_sqrt_small_values(value):
    value_bigfloat = create_BigFloat(value)

    actual = Sqrt(value_bigfloat)

    expected = Decimal(bigfloat_string(value_bigfloat)).sqrt()
    expected = f'{expected:.10010f}'

    actual_str = bigfloat_string(actual)
    actual_formatted = f'{Decimal(actual_str):.10010f}'

    assert actual_formatted[:10000] == expected[:10000]


@pytest.mark.parametrize(
    'value',
    make_random_positive_numbers(Random(RANDOM_SEED), RANDOM_VALUES_COUNT, RANDOM_NUMBER_LENGTH),
)
def test_sqrt_random(value):
    value_bigfloat = create_BigFloat(value)

    start = perf_counter()
    actual = Sqrt(value_bigfloat)
    end = perf_counter()

    SQRT_TIMES.append(end - start)

    expected = Decimal(bigfloat_string(value_bigfloat)).sqrt()
    expected = f'{expected:.10010f}'

    actual_str = bigfloat_string(actual)
    actual_formatted = f'{Decimal(actual_str):.10010f}'

    assert actual_formatted[:10000] == expected[:10000]


@pytest.fixture(scope='module', autouse=True)
def print_average_time():
    yield

    if SQRT_TIMES:
        avg_sqrt = sum(SQRT_TIMES) / len(SQRT_TIMES)
        print(f'\nСреднее время Sqrt: {avg_sqrt:.8f} сек')
