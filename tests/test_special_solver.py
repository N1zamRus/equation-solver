from time import perf_counter

import pytest

from solver.solver import solution_calc as bigfloat_solution_calc
from solver.decimal_solver import solution_calc as decimal_solution_calc
from tests.test_utility import make_coefs_bigfloat, make_coefs_decimal


SPECIAL_TIMES = []


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
    ("nan", "1",   "1"),    # x1=NaN, x2=NaN
    ("1",   "nan", "1"),    # x1=NaN, x2=NaN
    ("1",   "1",   "nan"),  # x1=NaN, x2=NaN
    ("nan", "nan", "nan"),  # x1=NaN, x2=NaN
    ("nan", "inf", "1"),    # x1=NaN, x2=NaN
    ("inf", "nan", "1"),    # x1=NaN, x2=NaN
    ("inf", "1",   "nan"),  # x1=NaN, x2=NaN
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
    ("inf",  "1",  "1"),    # D=-inf  комплексные (0 ± NaN*i)
    ("inf",  "0",  "1"),    # D=-inf  комплексные (0 ± NaN*i)
    ("inf",  "0",  "0"),    # D=0     один корень 0
    ("inf",  "1",  "0"),    # D=1     два корня
    ("inf",  "1",  "-1"),   # D=1+4*inf=inf  два корня
    ("-inf", "1",  "1"),    # D=1+4*inf=inf  два корня
    ("-inf", "0",  "1"),    # D=-4*(-inf)=inf  два корня
])
def test_special_quadratic_inf_a(a, b, c):
    check(a, b, c)



@pytest.mark.parametrize("a, b, c", [
    ("1",  "inf",  "1"),    # D=inf-4=inf   два корня (-inf, 0)
    ("1",  "-inf", "1"),    # D=inf-4=inf   два корня
    ("1",  "inf",  "0"),    # D=inf         два корня
    ("1",  "inf",  "-1"),   # D=inf+4=inf   два корня
    ("2",  "inf",  "3"),    # D=inf         два корня
])
def test_special_quadratic_inf_b(a, b, c):
    check(a, b, c)



@pytest.mark.parametrize("a, b, c", [
    ("1",  "1",   "inf"),   # D=1-4*inf=-inf  комплексные
    ("1",  "0",   "inf"),   # D=-4*inf=-inf   комплексные (0 ± inf*i)
    ("1",  "-1",  "inf"),   # D=1-4*inf=-inf  комплексные
    ("2",  "1",   "-inf"),  # D=1+8*inf=inf   два корня
])
def test_special_quadratic_inf_c(a, b, c):
    check(a, b, c)



@pytest.mark.parametrize("a, b, c", [
    ("inf", "inf",  "1"),   # D=inf-inf=nan
    ("inf", "inf",  "inf"), # D=inf-inf=nan
    ("inf", "inf",  "-inf"),
    ("1",   "inf",  "inf"), # D=inf-4*inf=nan
])
def test_special_quadratic_nan_discriminant(a, b, c):
    check(a, b, c)



@pytest.mark.parametrize("a, b, c", [
    ("0", "nan", "1"),     # линейное с nan в b
    ("0", "1",   "nan"),   # линейное с nan в c
    ("0", "nan", "nan"),   # оба не определены
    ("0", "nan", "0"),
    ("0", "0",   "nan"),
])
def test_special_linear_nan(a, b, c):
    check(a, b, c)



@pytest.mark.parametrize("a, b, c", [
    ("0", "0", "inf"),     # 0 = -inf  NO_SOLUTION
    ("0", "0", "-inf"),    # 0 = inf   NO_SOLUTION
])
def test_special_degenerate_inf(a, b, c):
    check(a, b, c)



@pytest.mark.parametrize("a, b, c", [
    ("nan", "0", "0"),
    ("0",   "nan", "0"),
    ("0",   "0",  "nan"),
    ("nan", "1",  "0"),
    ("nan", "0",  "1"),
])
def test_special_nan_with_zero(a, b, c):
    check(a, b, c)



@pytest.mark.parametrize("a, b, c", [
    ("inf",  "-inf", "1"),   # D=inf-inf=nan
    ("-inf", "inf",  "1"),   # D=inf+inf=inf
    ("1",    "-inf", "-inf"),# D=inf+inf=inf
    ("-inf", "-inf", "-inf"),# D=inf-inf=nan
    ("-inf", "inf",  "-inf"),# D=inf+inf=inf
    ("-inf", "-inf", "inf"), # D=inf+inf=inf
])
def test_special_mixed_inf(a, b, c):
    check(a, b, c)



@pytest.mark.parametrize("a, b, c", [
    ("-inf", "-1",   "-1"),  # D=1-4*(-inf)*(-1)=-inf  комплексные
    ("-inf", "1",    "-1"),  # D=1-4*(-inf)*(-1)=-inf  комплексные
    ("-1",   "-inf", "-1"),  # D=inf-4=inf  два корня
    ("1",    "-inf", "-1"),  # D=inf+4=inf  два корня
    ("-1",   "1",    "-inf"),# D=1-4*(-1)*(-inf)=-inf  комплексные
    ("-1",   "0",    "-inf"),# D=-4*(-1)*(-inf)=-inf  комплексные
])
def test_special_quadratic_neg_inf(a, b, c):
    check(a, b, c)
