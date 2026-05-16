from decimal import getcontext, MAX_EMAX, MIN_EMIN
from random import Random
from time import perf_counter

import pytest

from solver.solver import solution_calc as bigfloat_solution_calc
from solver.decimal_solver import solution_calc as decimal_solution_calc
from tests.test_utility import (
    make_coefs_bigfloat,
    make_coefs_decimal,
    make_str_number,
    to_decimal,
)


SOLVER_TIMES = []

RANDOM_COEFS_COUNT = 10
RANDOM_NUMBER_LENGTH = 10000
RANDOM_SEED = 674765

getcontext().prec = 50000
getcontext().Emax = MAX_EMAX
getcontext().Emin = MIN_EMIN


def make_signed_number(rng: Random, length):
    value = make_str_number(rng, length)

    if value != "0" and rng.choice([True, False]):
        return "-" + value

    return value


def make_random_coefficients(rng: Random, count_test, length):
    coefficients = []

    for _ in range(count_test):
        a = make_signed_number(rng, length)
        while to_decimal(a) == 0:
            a = make_signed_number(rng, length)

        b = make_signed_number(rng, length)
        c = make_signed_number(rng, length)

        coefficients.append((a, b, c))

    return coefficients


def check(a, b, c):
    actual = bigfloat_solution_calc(make_coefs_bigfloat(a, b, c))
    expected = decimal_solution_calc(make_coefs_decimal(a, b, c))
    assert actual == expected


@pytest.mark.parametrize("a, b, c", [
    ("1", "-3", "2"),
    ("1", "2", "1"),
    ("1", "0", "1"),
    ("1", "0", "-4"),
    ("1", "1", "0"),
    ("2", "4", "2"),
    ("1", "-2", "-3"),
    ("3", "0", "0"),
    ("1", "-1", "0"),
    ("1", "0", "-1"),
])
def test_solver_edge_cases(a, b, c):
    check(a, b, c)


@pytest.mark.parametrize("a, b, c", [
    ("0", "1", "0"),       # x = 0
    ("0", "1", "1"),       # x = -1
    ("0", "2", "-4"),      # x = 2
    ("0", "-3", "6"),      # x = 2
    ("0", "5", "-10"),     # x = 2
    ("0", "-1", "-1"),     # x = -1
    ("0", "100", "0.5"),   # x = -0.005
])
def test_solver_linear(a, b, c):
    check(a, b, c)


@pytest.mark.parametrize("a, b, c", [
    ("0", "0", "0"),       # 0 = 0 → INFINITE_SOLUTION
    ("0", "0", "1"),       # 0 = -1 → NO_SOLUTION
    ("0", "0", "-5"),      # NO_SOLUTION
    ("0", "0", "0.0001"),  # NO_SOLUTION
])
def test_solver_degenerate(a, b, c):
    check(a, b, c)


@pytest.mark.parametrize("a, b, c", [
    ("-1", "-2", "-1"),    # -(x²+2x+1)=0 → x=-1 (same roots)
    ("-1", "0", "-1"),     # -x²-1=0 → D<0, комплексные
    ("-1", "3", "-2"),     # x = 1, 2
    ("-2", "-4", "-2"),    # same roots x = -1
    ("-1", "-1", "-1"),    # D<0, комплексные
])
def test_solver_all_negative(a, b, c):
    check(a, b, c)


@pytest.mark.parametrize("a, b, c", [
    ("0.5", "1", "0.5"),       # x²+2x+1=0 → x=-1
    ("0.1", "0.2", "0.1"),     # x²+2x+1=0 → x=-1
    ("0.25", "1", "1"),        # D=1-1=0 → x=-2
    ("2.5", "0", "-10"),       # x = ±2
    ("0.001", "0", "-0.001"),  # x = ±1
])
def test_solver_decimal_coefs(a, b, c):
    check(a, b, c)


@pytest.mark.parametrize("a, b, c", [
    ("4", "4", "1"),       # (2x+1)² → x=-0.5 (D=0)
    ("9", "-12", "4"),     # (3x-2)² → x=2/3 (D=0)
    ("25", "-30", "9"),    # (5x-3)² → x=3/5 (D=0)
    ("1", "-1000000", "1"),  # очень разные коэф-ты
    ("1", "1000000", "1"),
])
def test_solver_tricky_quadratic(a, b, c):
    check(a, b, c)


@pytest.mark.parametrize(
    "a, b, c",
    make_random_coefficients(Random(RANDOM_SEED), RANDOM_COEFS_COUNT, RANDOM_NUMBER_LENGTH),
)
def test_solver_quadratic_with_decimal(a, b, c):
    start = perf_counter()
    actual = bigfloat_solution_calc(make_coefs_bigfloat(a, b, c))
    end = perf_counter()

    SOLVER_TIMES.append(end - start)

    expected = decimal_solution_calc(make_coefs_decimal(a, b, c))

    assert actual == expected


@pytest.fixture(scope="module", autouse=True)
def print_average_time():
    yield

    if SOLVER_TIMES:
        avg_solver = sum(SOLVER_TIMES) / len(SOLVER_TIMES)
        print(f"\nСреднее время Solver: {avg_solver:.8f} сек")
