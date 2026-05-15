from time import perf_counter

import pytest

from core.BigFloat import create_BigFloat
from solver.models import Coefs
from solver.solver import solution_calc as bigfloat_solution_calc
from solver.decimal_solver import solution_calc as decimal_solution_calc
from tests.test_utility import to_decimal


SPECIAL_TIMES = []


def make_coefs_bigfloat(a, b, c):
    return Coefs(create_BigFloat(a), create_BigFloat(b), create_BigFloat(c))


def make_coefs_decimal(a, b, c):
    return Coefs(to_decimal(a), to_decimal(b), to_decimal(c))


def check(a, b, c):
    start = perf_counter()
    actual = bigfloat_solution_calc(make_coefs_bigfloat(a, b, c))
    end = perf_counter()

    SPECIAL_TIMES.append(end - start)

    expected = decimal_solution_calc(make_coefs_decimal(a, b, c))
    assert actual == expected


@pytest.fixture(scope="module", autouse=True)
def print_average_time():
    yield

    if SPECIAL_TIMES:
        avg = sum(SPECIAL_TIMES) / len(SPECIAL_TIMES)
        print(f"\nСреднее время Special: {avg:.8f} сек")



@pytest.mark.parametrize("a, b, c", [
    ("nan", "1",   "1"),
    ("1",   "nan", "1"),
    ("1",   "1",   "nan"),
    ("nan", "nan", "nan"),
    ("nan", "inf", "1"),
    ("inf", "nan", "1"),
    ("inf", "1",   "nan"),
])
def test_special_nan_coef(a, b, c):
    check(a, b, c)



@pytest.mark.parametrize("a, b, c", [
    ("0", "inf",  "1"),     # x = -1/inf  = 0
    ("0", "inf",  "-1"),    # x = 1/inf   = 0
    ("0", "-inf", "1"),     # x = -1/-inf = 0
    ("0", "1",    "inf"),   # x = -inf
    ("0", "1",    "-inf"),  # x = inf
    ("0", "-1",   "inf"),   # x = inf
    ("0", "inf",  "0"),     # x = 0/inf   = 0
    ("0", "inf",  "inf"),   # x = -inf/inf = nan
    ("0", "-inf", "-inf"),  # x = inf/-inf = nan
])
def test_special_linear_inf(a, b, c):
    check(a, b, c)



@pytest.mark.parametrize("a, b, c", [
    ("inf",  "1",  "1"),    # D=-inf → комплексные (0 ± NaN*i)
    ("inf",  "0",  "1"),    # D=-inf → комплексные (0 ± NaN*i)
    ("inf",  "0",  "0"),    # D=0    → один корень 0
    ("inf",  "1",  "0"),    # D=1    → два корня
    ("inf",  "1",  "-1"),   # D=1+4*inf=inf → два корня
    ("-inf", "1",  "1"),    # D=1+4*inf=inf → два корня
    ("-inf", "0",  "1"),    # D=-4*(-inf)=inf → два корня
])
def test_special_quadratic_inf_a(a, b, c):
    check(a, b, c)



@pytest.mark.parametrize("a, b, c", [
    ("1",  "inf",  "1"),    # D=inf-4=inf  → два корня (-inf, 0)
    ("1",  "-inf", "1"),    # D=inf-4=inf  → два корня
    ("1",  "inf",  "0"),    # D=inf        → два корня
    ("1",  "inf",  "-1"),   # D=inf+4=inf  → два корня
    ("2",  "inf",  "3"),    # D=inf        → два корня
])
def test_special_quadratic_inf_b(a, b, c):
    check(a, b, c)



@pytest.mark.parametrize("a, b, c", [
    ("1",  "1",   "inf"),   # D=1-4*inf=-inf → комплексные
    ("1",  "0",   "inf"),   # D=-4*inf=-inf  → комплексные (0 ± inf*i)
    ("1",  "-1",  "inf"),   # D=1-4*inf=-inf → комплексные
    ("2",  "1",   "-inf"),  # D=1+8*inf=inf  → два корня
])
def test_special_quadratic_inf_c(a, b, c):
    check(a, b, c)



@pytest.mark.parametrize("a, b, c", [
    ("inf", "inf",  "1"),   # D=inf-inf=nan
    ("inf", "inf",  "inf"), # D=inf-inf=nan
    ("inf", "inf",  "-inf"),
    ("1",   "inf",  "inf"), # D=inf-4*inf=nan
    ("inf", "1",    "inf"), # D=1-4*inf²=nan? wait: D=1-4*inf*inf=nan
])
def test_special_quadratic_nan_discriminant(a, b, c):
    check(a, b, c)
