from BigFloat import (
    BigFloat,
    get_BASE,
    get_exp10,
    get_mantiss,
    get_BASE_DIGITS,
    normalize,
    BigFloat_round,
    create_BigFloat,
    bigfloat_string,
    get_blocks,
    bigfloat_string,
    slice_blocks
)
from Add import Add
from Subtraction import Sub
from Division import Div
from Multiply import Mul, short_Mul

from math import floor

ROOT_TEN = BigFloat(1, [79331, 1683, 27766, 3162], -18)

BASE_DIGITS = get_BASE_DIGITS()
BASE = get_BASE()


def make_x0(a, extra_blocks = 9):
    a = abs(normalize(a))
    a_blocks = get_blocks(a)

    take = min(4, len(a_blocks))
    take_digits = take * BASE_DIGITS + extra_blocks

    dropped = len(a_blocks) - take

    top = 0
    for i in range(len(a_blocks) - 1, dropped - 1, -1):
        top = top * BASE + a_blocks[i]

    scale = dropped * BASE_DIGITS + get_exp10(a)

    if scale % 2 != 0:
        scale -= 1
        top *= 10
    
    sqrt_digits = (len(str(top)) + 1) // 2 

    k = take_digits + sqrt_digits - 1

    res_mantiss = floor(10**k / top**0.5)
    res_exp = -k - scale // 2

    res_bgf = BigFloat(1, slice_blocks(str(res_mantiss)), res_exp)

    return normalize(res_bgf)


"""
def make_x0(a, запаска = 2)
    1. Возьмём блоки из a = abs(normilize(a))
        a_blocks = get_blocks(a)
    2. Определим кол-во блоков которых мы возьмём, а это по умолчанию 4, либо все блоки
        take = min(4, len(a_blocks))
        take_digits = take * BASE_DIGITS + запаска
    3. Определим сколько блоков мы отбросили
        dropped = len(a_blocks) - take
    4. Преобразуем взятые блоки в целое число
        top = 0
        for i in range(len(a_blocks) - 1, dropped - 1, -1)
            top = top * BASE + a_blocks[i]
    5. Определим сколько разрядов осталось за пределами top, это scale = dropped * BASE_DIGITS + get_exp10(a) 
        он будет использоваться для расчёта res_exp
    6. Проверим на чётность scale, так как при возврате экспоненты у нас НЕ ДОЛЖНО ПОЛУЧИТЬСЯ ДРОБНОЙ ЧАСТИ
        Если scale НЕчётный, то top *= 10, scale -= 1
        иначе ничего не трогаем
    7. Теперь найдём k, это будет степенью 10, в 10^k/sqrt(top)
        Определим кол-во цифр в sqrt(top), это примерно (len(top) + 1) // 2 
                sqrt_digits = (len(str(top)) + 1) // 2
        Теперь дадим степень для 10, это k = take_digits + sqrt_digits - 1
    8. Теперь посчитаем нашу мантиссу по формуле 10^k / sqrt(top), с отбрасыванием дробной части вниз, 
            и в результате получим целое число, которое потом разделим на блоки
        res_mantiss = floor(10**k / sqrt(top))
    9. Теперь масштабируем результат обратно, для этого нужно 
        res_exp = -k - scale // 2
    10. Соберём наше число bigfloat(1, slice_blocks(str(res_mantiss)), res_exp)
"""        

def Sqrt(a: BigFloat, precision = 2026, extra_blocks = 2, iteration = 10):
    x_old = make_x0(a, 4)
    current_blocks = 2
    THREE = BigFloat(1, [3], 0)
    max_work_precision = precision + extra_blocks
    for _ in range(iteration):
        current_blocks *= 2
        work_precision = min(current_blocks + extra_blocks, max_work_precision)

        a_work = BigFloat_round(a, work_precision)

        qx = Mul(x_old, x_old, work_precision)
        ax2 = Mul(a_work, qx, work_precision)

        staple = Sub(THREE, ax2)
        x_staple = Mul(x_old, staple, work_precision)

        x_new = short_Mul(x_staple, 5, -1)
        x_new = BigFloat_round(normalize(x_new), work_precision)

        x_old = x_new

        if current_blocks >= precision:
            break

    result = Mul(a, x_old, precision)
    return normalize(result)


""" 
def Sqrt(a, точность в блоках, запаска, макс_кол_во_итераций)
    1. Найдём x_old = make_x0(a)
    2. Начальная точность current_blocks = 2
    3. Создадим константу THREE = BigFloat(1, [3], 0)
    4. Определим максимальную рабочую область = точность в блоках + запаска
    5. Цикл до макс_кол_во_итераций

        Умножим current_blocks в 2 раза
        Определим рабочую зону = min(current_blocks + запаска, максимальная рабочая область)

        применяем формулу x_new = x_old * (3 - a * x_old²) * 0.5
        и округлим до нужной точности, чтобы не брать ошибочные блоки
        x_new = BigFloat_round(normalize(x_new), work_precision)


        Проверяем достигли ли мы нужной точности и изменился ли x
        if current_blocks >= precision and x_new == x_old:
            то выходим из цикла
        x_old = x_new

    6. Умножаем a на x_old, и обрезаем точность
        result = Mul(a, x_old, precision)

    return normalize(result)
"""







if __name__ == '__main__':
    from decimal import getcontext, Decimal
    from time import perf_counter
    from test_utility import make_str_number
    from random import Random
    from BigFloat import create_BigFloat, bigfloat_string

    getcontext().prec = 50000

    rng_a = Random(23421)

    for _ in range(10):
        a = create_BigFloat(make_str_number(rng_a, 10000))

        expected = Decimal(bigfloat_string(a)).sqrt()
        expected = f'{expected:.10030f}'

        t1 = perf_counter()
        result = Sqrt(a)
        t2 = perf_counter()

        result_str = bigfloat_string(result)

        result_expected_format = f'{Decimal(result_str):.10030f}'
        print("OK:", result_expected_format[:10000] == expected[:10000])
        print("TIME:", t2 - t1)