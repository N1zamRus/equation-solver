from decimal import Decimal, getcontext, MAX_EMAX, MIN_EMIN
from random import Random
from time import perf_counter

import pytest

from core.Sqrt import Sqrt
from core.BigFloat import create_BigFloat, bigfloat_string
from tests.test_utility import make_str_number


SQRT_TIMES = []

RANDOM_VALUES_COUNT = 100
RANDOM_NUMBER_LENGTH = 10000
RANDOM_SEED = 52532

getcontext().prec = 50000
getcontext().Emax = MAX_EMAX
getcontext().Emin = MIN_EMIN


def make_random_positive_numbers(rng: Random, count_test=RANDOM_VALUES_COUNT, length=RANDOM_NUMBER_LENGTH):
    numbers = []

    for _ in range(count_test):
        value = make_str_number(rng, length)
        decimal_value = Decimal(value.replace(",", "."))

        if decimal_value <= 0:
            continue

        numbers.append(value)

    return numbers


@pytest.mark.parametrize("value", [
    "1",
    "4",
    "9",
    "16",
    "100",
    "0.25",
    "0.01",
    "2",
    "10",
])
def test_sqrt_small_values(value):
    value_bigfloat = create_BigFloat(value)

    actual = Sqrt(value_bigfloat)

    expected = Decimal(bigfloat_string(value_bigfloat)).sqrt()
    expected = f"{expected:.10010f}"

    actual_str = bigfloat_string(actual)
    actual_formatted = f"{Decimal(actual_str):.10010f}"

    assert actual_formatted[:10000] == expected[:10000]


@pytest.mark.parametrize("value", [
    # нечётное число цифр (scale нечётный → scale // 2 округляется вниз)
    "9",            # 1 цифра
    "999",          # 3 цифры
    "99999",        # 5 цифр = BASE_DIGITS
    "9999999",      # 7 цифр
    "999999999",    # 9 цифр
    "99999999999",  # 11 цифр
    # чётное число цифр (scale чётный)
    "99",           # 2 цифры
    "9999",         # 4 цифры
    "999999",       # 6 цифр
    "99999999",     # 8 цифр
    "9999999999",   # 10 цифр = два блока по BASE_DIGITS
    # точные квадраты на границах блоков
    "100000",       # BASE, sqrt = 316.22...
    "10000000000",  # BASE^2, sqrt = 100000 (точное)
    "9999800001",   # 99999^2, sqrt = 99999 (точное)
    # дроби: нечётное/чётное число знаков после точки
    "0.1",          # 1 знак
    "0.01",         # 2 знака (уже есть в small_values, но важен контраст)
    "0.001",        # 3 знака
    "0.0001",       # 4 знака
    "0.00001",      # 5 знаков = BASE_DIGITS
])
def test_sqrt_digit_counts(value):
    value_bigfloat = create_BigFloat(value)

    actual = Sqrt(value_bigfloat)

    expected = Decimal(bigfloat_string(value_bigfloat)).sqrt()
    expected = f"{expected:.10010f}"

    actual_str = bigfloat_string(actual)
    actual_formatted = f"{Decimal(actual_str):.10010f}"

    assert actual_formatted[:10000] == expected[:10000]


@pytest.mark.parametrize(
    "value",
    make_random_positive_numbers(Random(RANDOM_SEED), RANDOM_VALUES_COUNT, RANDOM_NUMBER_LENGTH),
)
def test_sqrt_random(value):
    value_bigfloat = create_BigFloat(value)

    start = perf_counter()
    actual = Sqrt(value_bigfloat)
    end = perf_counter()

    SQRT_TIMES.append(end - start)

    expected = Decimal(bigfloat_string(value_bigfloat)).sqrt()
    expected = f"{expected:.10010f}"

    actual_str = bigfloat_string(actual)
    actual_formatted = f"{Decimal(actual_str):.10010f}"

    assert actual_formatted[:10000] == expected[:10000]


@pytest.fixture(scope="module", autouse=True)
def print_average_time():
    yield

    if SQRT_TIMES:
        avg_sqrt = sum(SQRT_TIMES) / len(SQRT_TIMES)
        print(f"\nСреднее время Sqrt: {avg_sqrt:.8f} сек")
