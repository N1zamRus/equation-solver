from BigFloat import(
    create_BigFloat,
    BigFloat,
    get_BASE,
    get_blocks,
    get_exp10,
    get_sign,
    BigFloat_round,
    normalize,
    slice_blocks,
    bigfloat_string,
    get_BASE_DIGITS
)
from Multiply import Mul
from Subtraction import Sub

BASE = get_BASE()

def Div(a: BigFloat, b: BigFloat, precision=2026):
    inv_b = Inv(b, precision=precision)
    return Mul(a, inv_b, precision)

def make_x0(b: BigFloat):
    b = abs(normalize(b))

    b_blocks = get_blocks(b)

    take = min(4, len(b_blocks))
    dropped = len(b_blocks) - take

    BASE = get_BASE()
    BASE_DIGITS = get_BASE_DIGITS()

    top = 0
    for i in range(len(b_blocks) - 1, len(b_blocks) - 1 - take, -1):
        top = top * BASE + b_blocks[i]

    x0_digits = take * BASE_DIGITS + 2
    div_digits = x0_digits + len(str(top)) - 1

    int_x0 = 10 ** div_digits // top
    res_exp = -div_digits - dropped * BASE_DIGITS - get_exp10(b)

    return normalize(BigFloat(1, slice_blocks(str(int_x0)), res_exp))
"""
def make_x0(b)
    1. Возьмём модуль из числа b и нормализуем на всякий
    2. Втащим из b его блоки
    3. Возьмём 4 блока для начала, ну либо весь массив если он меньше 4
    4. Сделаем из старших блоков мантиссу 
        От n-1 до n-1-сколько взяли
            top = top * base(100000) + элемент
    5. А теперь посмотрим сколько цифр мы ожидаем увидеть
        сколько взяли блоков * сколько в блоке цифр + запаска
       А числа которые мы отрубили мы представим в виде exp
        кол-во отрубленых блоков * кол-во цифр в блоке + изначальная экспонента
    6. Найдём мантиссу x0, для этого
        10**ожидаемое кол-во цифр + запас // top
        Если мы не маштабируем это и оставим 1, то мы будем всегда получать 0
    7. Найдём экспоненту для результата
        экспонентой будет вычитание нашего маштаба - остальные числа которые мы не учитывали
    8. Возвращаем x0 в виде BigFloat
"""
def Inv(b: BigFloat, iteration=11, precision=2026, guard_blocks=20):
    result_sign = get_sign(b)
    b_abs = abs(normalize(b))

    x = make_x0(b_abs)
    TWO = BigFloat(1, [2], 0)

    current_blocks = 2
    max_work_precision = precision + guard_blocks

    for _ in range(iteration):
        if len(get_blocks(x)) >= precision:
            break

        current_blocks *= 2
        work_precision = min(current_blocks + guard_blocks, max_work_precision)

        bx = Mul(BigFloat_round(b_abs, current_blocks + 10), x, work_precision)
        right = Sub(TWO, bx)
        x = Mul(x, right, work_precision)

    x = BigFloat_round(normalize(x), precision)

    if result_sign < 0:
        x = -x

    return normalize(x)
"""
def Inv(b, кол-во итераций)
    1. Найдём начальное приближение с помощью make_x0
    2. Начальная точность у нас будет 2 блока
    3. Цикл, который идёт n итераций, по умолчанию 11
        увеличим маштаб в 2 раза

        по формуле x = x * (2 - b * x) находим xЮ добавляя к b новые блоки

    4. Возвращаем последний x, это и есть наше обратное число
"""


if __name__ == '__main__':
    from decimal import getcontext, Decimal
    from time import perf_counter
    from test_utility import make_str_number
    from random import Random

    getcontext().prec = 50000

    for _ in range(10):
        a = create_BigFloat(make_str_number(Random(21342143), 10000))
        b = create_BigFloat(make_str_number(Random(515423), 10000))

        expected = Decimal(bigfloat_string(a)) / Decimal(bigfloat_string(b))
        expected = f'{expected:.10030f}'

        t1 = perf_counter()
        result = Div(a, b)
        t2 = perf_counter()

        result_str = bigfloat_string(result)

        print("OK:", result_str[:10000] == expected[:10000])
        print("TIME:", t2 - t1)