from BigFloat import (
    BigFloat,
    get_BASE,
    get_exp10,
    get_mantiss,
    get_BASE_DIGITS,
    normalize,
    BigFloat_round,
    create_BigFloat,
    bigfloat_string
)
from Add import Add
from Subtraction import Sub
from Division import Div
from Multiply import Mul


BASE_DIGITS = get_BASE_DIGITS()
BASE = get_BASE()


def Sqrt(a: BigFloat, precision=2026, extra_blocks=2, max_iter=100):
    x_old = make_x0(a)

    HALF = BigFloat(1, [5], -1)

    current_precision = 2
    for _ in range(max_iter):
        if current_precision < precision:
            current_precision = min(current_precision * 2, precision)

        work_precision = current_precision + extra_blocks

        left = Add(x_old, Div(a, x_old, work_precision))
        x_new = Mul(left, HALF, work_precision)
        x_new = normalize(BigFloat_round(x_new, work_precision))

        if x_new == x_old:
            break

        x_old = x_new

    return normalize(BigFloat_round(x_old, precision))




"""
def Sqrt(a)
    1. Необходимо найти x_old, тобишь начальное приближение, x_old = make_x0(a)
    2. Цикл TRUE
        Формула: x_new = (x + a/x) * 0.5
        if x_new >= x_old
            break
        x_old = x_new

       str_x = str(x)
    
    3. return x в виде BigFloat

        



def make_x0(a)
    1. Посмотрим кол-во цифр числа a
        k = кол-во блоков * кол-во цифр в блоке
    2. Попробуем предугадать кол-во цифр корня числа a, 
        это примерно t = K/2
        ЭТО ПОСЛУЖИТ СТЕПЕНЬЮ ДЛЯ НАЧАЛЬНОГО ЧИСЛА
    
    3. И тогда возьмём x0 за 10^t


"""

def make_x0(a: BigFloat):
    a = abs(normalize(a))

    mantissa = get_mantiss(a)

    if mantissa == "0":
        return BigFloat(1, [0], 0)

    order = len(mantissa) + get_exp10(a) - 1
    t = (order + 1) // 2

    return BigFloat(1, [1], t)

if __name__ == '__main__':
    from decimal import getcontext, Decimal
    from time import perf_counter
    from test_utility import make_str_number
    from random import Random
    from BigFloat import create_BigFloat, bigfloat_string

    getcontext().prec = 50000

    rng_a = Random(123)

    for _ in range(10):
        a = create_BigFloat(make_str_number(rng_a, 1))

        expected = Decimal(bigfloat_string(a)).sqrt()
        expected = f'{expected:.10030f}'

        t1 = perf_counter()
        result = Sqrt(a)
        t2 = perf_counter()

        result_str = bigfloat_string(result)

        result_expected_format = f'{Decimal(result_str):.10030f}'
        print("OK:", result_expected_format[:10000] == expected[:10000])
        print("TIME:", t2 - t1)