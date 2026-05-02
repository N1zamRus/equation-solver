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
    1. Берём модуль b и нормализуем
    2. Достаём блоки числа
    3. Берём до 4 старших блоков, а остальные считаем отброшенными
    4. Из старших блоков собираем число top
    5. Считаем желаемое количество цифр в x0 с небольшой запаской
    6. Увеличиваем ещё масштаб потому что top сам содержит много цифр
    7. Считаем мантиссу начального приближения 10^масштаб / top
    8. В экспоненте возвращаем масштаб обратно и учитываем отброшенные блоки
    9. Возвращаем модуль BigFloat
"""
def Inv(b: BigFloat, iteration=11, precision=2026, extra_blocks=10):
    result_sign = get_sign(b)
    b_abs = abs(normalize(b))

    x = make_x0(b_abs)
    TWO = BigFloat(1, [2], 0)

    current_blocks = 2
    max_work_precision = precision + extra_blocks

    for _ in range(iteration):
        if len(get_blocks(x)) >= precision:
            break

        current_blocks *= 2
        work_precision = min(current_blocks + extra_blocks, max_work_precision)

        # xₙ₊₁ = xₙ · (2 - b · xₙ)
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
        А максимальная рабочая будет желаемая + запаска
    3. Цикл будет идти пока не кончатся итерации
        Уввеличиваем current_blocks и выставляем рабочую область current_blocks + запаска
        Находим x по формуле
    4. Обрезаем x чтобы ошибки не шли в учёт результата
    5. Определяем знак
    6. Нормализуем и возвращаем в виде BigFloat
"""


if __name__ == '__main__':
    from decimal import getcontext, Decimal
    from time import perf_counter
    from test_utility import make_str_number
    from random import Random

    getcontext().prec = 50000
    
    rng_a = Random(123)
    rng_b = Random(511235423)

    for _ in range(10):
        a = create_BigFloat(make_str_number(rng_a, 10000))
        b = create_BigFloat(make_str_number(rng_b, 10000))  

        expected = Decimal(bigfloat_string(a)) / Decimal(bigfloat_string(b))
        expected = f'{expected:.10030f}'

        t1 = perf_counter()
        result = Div(a, b)
        t2 = perf_counter()

        result_str = bigfloat_string(result)

        print("OK:", result_str[:10000] == expected[:10000])
        print("TIME:", t2 - t1)