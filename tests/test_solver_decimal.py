from decimal import getcontext, MAX_EMAX, MIN_EMIN
from random import Random
from time import perf_counter

import pytest

from core.BigFloat import create_BigFloat
from solver.models import Coefs
from solver.solver import solution_calc as bigfloat_solution_calc
from solver.decimal_solver import solution_calc as decimal_solution_calc
from tests.test_utility import make_str_number, to_decimal


SOLVER_TIMES = []

RANDOM_COEFS_COUNT = 100
RANDOM_NUMBER_LENGTH = 10000
RANDOM_SEED = 5124383

getcontext().prec = 50000
getcontext().Emax = MAX_EMAX
getcontext().Emin = MIN_EMIN


def make_signed_number(rng: Random, length):
    value = make_str_number(rng, length)

    if value != '0' and rng.choice([True, False]):
        return '-' + value

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


@pytest.mark.parametrize('a, b, c', [
    ('1', '-3', '2'),
    ('1', '2', '1'),
    ('1', '0', '1'),
    ('1', '0', '-4'),
    ('1', '1', '0'),
    ('2', '4', '2'),
    ('1', '-2', '-3'),
    ('3', '0', '0'),
    ('1', '-1', '0'),
    ('1', '0', '-1'),
])
def test_solver_edge_cases(a, b, c):
    actual = bigfloat_solution_calc(Coefs(
        create_BigFloat(a), create_BigFloat(b), create_BigFloat(c),))

    expected = decimal_solution_calc(Coefs(
        to_decimal(a), to_decimal(b), to_decimal(c),))

    assert actual == expected


@pytest.mark.parametrize(
    'a, b, c',
    make_random_coefficients(Random(RANDOM_SEED), RANDOM_COEFS_COUNT, RANDOM_NUMBER_LENGTH),
)
def test_solver_quadratic_with_decimal(a, b, c):
    start = perf_counter()
    actual = bigfloat_solution_calc(Coefs(
        create_BigFloat(a), create_BigFloat(b), create_BigFloat(c),))
    end = perf_counter()

    SOLVER_TIMES.append(end - start)

    expected = decimal_solution_calc(Coefs(
        to_decimal(a), to_decimal(b), to_decimal(c),))

    assert actual == expected


@pytest.fixture(scope='module', autouse=True)
def print_average_time():
    yield

    if SOLVER_TIMES:
        avg_solver = sum(SOLVER_TIMES) / len(SOLVER_TIMES)
        print(f'\nСреднее время Solver: {avg_solver:.8f} сек')
