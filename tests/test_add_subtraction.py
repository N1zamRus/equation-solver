from decimal import Decimal, getcontext, MAX_EMAX, MIN_EMIN
from random import Random
from core.Add import Add
from core.BigFloat import create_BigFloat, get_exp10, get_mantiss, get_sign
from core.Subtraction import Sub
from tests.test_utility import make_signed_random_pairs
from time import perf_counter
from tests.test_utility import to_decimal, bigfloat_decimal

import pytest

ADD_TIMES = []
SUB_TIMES = []

ADD_TIMES_DEC = []
SUB_TIMES_DEC = []

RANDOM_PAIRS_COUNT = 100
RANDOM_NUMBER_LENGTH = 10000
RANDOM_SEED = 52152

getcontext().prec = RANDOM_NUMBER_LENGTH * 2 + 10
getcontext().Emax = MAX_EMAX
getcontext().Emin = MIN_EMIN

@pytest.mark.parametrize("left, right", [
    ('0', '0'),
    ('1', '0'),
    ('0', '1'),
    ('1', '-1'),
    ('-1', '-1'),
    ('1000000', '1'),
    ('1', '0,1'),
    ('999', '-1000'),
    ('-0,5', '0,5'),
    ('1', '0,000001'),
])
def test_add_edge_cases(left, right):
    left_bigfloat = create_BigFloat(left)
    right_bigfloat = create_BigFloat(right)

    actual = Add(left_bigfloat, right_bigfloat)

    expected = to_decimal(left) + to_decimal(right)

    assert bigfloat_decimal(actual) == expected


@pytest.mark.parametrize("left, right", [
    ('0', '0'),
    ('1', '1'),
    ('1', '0'),
    ('0', '1'),
    ('-1', '-1'),
    ('1000000', '999999'),
    ('1,5', '0,5'),
    ('-5', '-3'),
    ('0,1', '0,1'),
    ('100', '-100'),
])
def test_sub_edge_cases(left, right):
    left_bigfloat = create_BigFloat(left)
    right_bigfloat = create_BigFloat(right)

    actual = Sub(left_bigfloat, right_bigfloat)

    expected = to_decimal(left) - to_decimal(right)

    assert bigfloat_decimal(actual) == expected


@pytest.mark.parametrize("left, right", [
    ('99999', '1'),               # перенос через границу блока: (BASE-1) + 1 = BASE
    ('99999', '99999'),           # сумма двух полных блоков
    ('9999999999', '1'),          # цепной перенос через два блока
    ('100000', '-1'),             # заём через границу
    ('100000', '-100000'),        # взаимная отмена, результат ноль
    ('99999', '0.00001'),         # целая часть на границе блока + дробная
    ('-99999', '-1'),             # отрицательные с переносом
    ('10000000000', '1'),         # перенос в третий блок
])
def test_add_block_boundary(left, right):
    left_bigfloat = create_BigFloat(left)
    right_bigfloat = create_BigFloat(right)

    actual = Add(left_bigfloat, right_bigfloat)

    expected = to_decimal(left) + to_decimal(right)

    assert bigfloat_decimal(actual) == expected


@pytest.mark.parametrize("left, right", [
    ('100000', '1'),              # заём через границу: BASE - 1 = BASE-1
    ('10000000000', '1'),         # заём через два блока
    ('100000', '99999'),          # разность на границе: 100000 - 99999 = 1
    ('9999999999', '9999999998'), # почти равные, результат = 1
    ('100000', '100000'),         # равные, результат ноль
    ('-99999', '-100000'),        # отрицательные с займом
    ('1', '0.99999'),             # дробный заём: 1 - 0.99999 = 0.00001
    ('10000000000', '9999999999'),# большие числа, результат = 1
])
def test_sub_block_boundary(left, right):
    left_bigfloat = create_BigFloat(left)
    right_bigfloat = create_BigFloat(right)

    actual = Sub(left_bigfloat, right_bigfloat)

    expected = to_decimal(left) - to_decimal(right)

    assert bigfloat_decimal(actual) == expected


@pytest.mark.parametrize("left, right", make_signed_random_pairs(Random(RANDOM_SEED),
                                                          RANDOM_PAIRS_COUNT,
                                                          RANDOM_NUMBER_LENGTH))
def test_random_add_with_decimal(left, right):
    left_bigfloat = create_BigFloat(left)
    right_bigfloat = create_BigFloat(right)

    start = perf_counter()
    actual = Add(left_bigfloat, right_bigfloat)
    end = perf_counter()

    ADD_TIMES.append(end - start)

    start = perf_counter()
    expected = to_decimal(left) + to_decimal(right)
    end = perf_counter()

    ADD_TIMES_DEC.append(end - start)

    assert bigfloat_decimal(actual) == expected


@pytest.mark.parametrize("left, right", make_signed_random_pairs(Random(RANDOM_SEED), 
                                                          RANDOM_PAIRS_COUNT, 
                                                          RANDOM_NUMBER_LENGTH))
def test_random_sub_with_decimal(left, right):
    left_bigfloat = create_BigFloat(left)
    right_bigfloat = create_BigFloat(right)

    start = perf_counter()
    actual = Sub(left_bigfloat, right_bigfloat)
    end = perf_counter()

    SUB_TIMES.append(end - start)

    start = perf_counter()
    expected = to_decimal(left) - to_decimal(right)
    end = perf_counter()

    SUB_TIMES_DEC.append(end - start)

    assert bigfloat_decimal(actual) == expected


@pytest.fixture(scope="module", autouse=True)
def print_average_operation_time():
    yield

    if ADD_TIMES:
        avg_add = sum(ADD_TIMES) / len(ADD_TIMES)
        print(f"\nСреднее время Add: {avg_add:.8f} сек")
        avg_add_d = sum(ADD_TIMES_DEC) / len(ADD_TIMES)
        print(f"\nСреднее время Add_: {avg_add:.8f} сек")

    if SUB_TIMES:
        avg_sub = sum(SUB_TIMES) / len(SUB_TIMES)
        print(f"Среднее время Sub: {avg_sub:.8f} сек")


# pytest -s