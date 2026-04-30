from math import pi, exp, cos, sin
from time import perf_counter
from test_utility import make_str_number
from random import Random
from test_utility import to_decimal, bigfloat_decimal
from BigFloat import (
    BigFloat,
    get_blocks,
    get_BASE,
    get_exp10,
    make_carry,
    normalize,
    get_sign,
    create_BigFloat
)
from decimal import getcontext, MAX_EMAX, MIN_EMIN

getcontext().prec = 21000
getcontext().Emax = MAX_EMAX
getcontext().Emin = MIN_EMIN


N = 0

def next_power_two(need):
    n = 1
    while n < need:
        n *= 2
    return n

def make_complex_elements(A: list[int]):
    for i in range(len(A)):
        A[i] = complex(A[i], 0)
    return A

def Mul(a: BigFloat, b: BigFloat):
    global N
    
    result_sign = get_sign(a) * get_sign(b)
    result_exp10 = get_exp10(a) + get_exp10(b)

    a_blocks = get_blocks(a).copy()
    b_blocks = get_blocks(b).copy()

    result_len = len(a_blocks) + len(b_blocks) - 1
    N = next_power_two(result_len)

    a_blocks += [0] * (N - len(a_blocks))
    b_blocks += [0] * (N - len(b_blocks))

    a_blocks = make_complex_elements(a_blocks)
    b_blocks = make_complex_elements(b_blocks)

    a_revers = Reverse_Bits(a_blocks)
    b_revers = Reverse_Bits(b_blocks)

    a_fft = FFT(a_revers)
    b_fft = FFT(b_revers)

    c_blocks = [0] * N

    for i in range(N):
        c_blocks[i] = a_fft[i] * b_fft[i]

    c_blocks = FFT(Reverse_Bits(c_blocks), True)

    coeffs = []

    for i in range(N):
        coeffs.append(round(c_blocks[i].real))

    coeffs = make_carry(coeffs)

    return normalize(BigFloat(result_sign, coeffs, result_exp10))

"""
1. Есть 2 чаисла bigfloat
2. Нужно посмотреть какой длинны может получиться результат
    N = кол-во блоков первого + кол-во блоков второго - 1
    Допустим N у нас теперь 3, но нужно ещё найти ближайшую БОЛЬШУЮ степень двойки
    Теперь N =4 
3. Преобразовываем элементы массива в комплексные make_complex_elements(A.blocks) и make_complex_elements(B.blocks)
4. Развернём индексы побитово Reverse_Bits(A) и Reverse_Bits(A)
5. Теперь преобразовываем FFT(A) и FFT(B)
6. После FFT(A) и FFT(B) перемножаем массивы покоординатно
    C = [0] * n

    for i in range(n):
        C[i] = A[i] * B[i]

    То есть:

    C[0] = A[0] * B[0]
    C[1] = A[1] * B[1]
    C[2] = A[2] * B[2]
    C[3] = A[3] * B[3]
7. Теперь снова Reverse_Bits(C) и FFT(C, TRUE)
8. Округляем
    coeffs = []

    for i in range(n):
        coeffs.append(round(C[i].real))
9. Нормализуем с помощью make_carry(C) и normalize(C)
10. Собираем в BigFloat

"""

    
def Reverse_Bits(A: list[int]):
    n = len(A)
    bits_count = (n - 1).bit_length()

    for i in range(n):
        j = reverse_bits_index(i, bits_count)

        if i < j:
            A[i], A[j] = A[j], A[i]

    return A

def reverse_bits_index(i: int, bits_count: int) -> int:
    binary = bin(i)[2:].zfill(bits_count)
    reversed_binary = binary[::-1]
    return int(reversed_binary, 2)

"""
def Reverse_Bits
    1.  Сначала нужно развернуть индексы в двоичной системе
        БУКВАЛЬНО РАЗВЕРНУТЬ! Допустим был индекс 1, в двоичной это 01
        И ВОТ ТУТ МЫ РАЗВОРАЧИВАЕМ И ЭТО СТАЛО 01 => 10 А ЭТО УЖЕ 2 В ДЕСЯТИЧНОЙ СИСТЕМЕ АШАЛЕЕЕТЬ
        и так с каждым

    например:   0 = 00 -> 00 = 0
                1 = 01 -> 10 = 2
                2 = 10 -> 01 = 1
                3 = 11 -> 11 = 3

    таким образом A=[45678, 123, 0, 0] => A=[45678, 0, 123, 0]

"""

def FFT(A: list[int], invert=False) -> list[complex]:
    length = 2
    n = len(A)

    while length <= len(A):

        if invert:
            angle = 2 * pi / length
        else:
            angle = -2 * pi / length

        w_len = complex(cos(angle), sin(angle)) # комплексноый поворот по формуле эйлера

        for start in range(0, n, length):
            w = 1

            for j in range(0, length // 2):

                u = A[start + j]
                v = A[start + j + length // 2] 

                A[start + j] = u + v * w
                A[start + j + length // 2] = u - v * w

                w = w * w_len

        length *= 2

    if invert:
        for i in range(n):
            A[i] = A[i] / n

    return A
"""

def FFT(A, invert=False)
    length = 2
    1. цикл, который идёт пока length <= len(A)
        например:   [45678, 0]   индексы 0, 1
                    [123, 0]     индексы 2, 3
        Найдём w_len, шаг поворота по окружности и наш множитель, 
                                                        что в свою очередь является комплексным числом
        if invert:
            angle = 2 * pi / length
        else:
            angle = -2 * pi / length 

        w_len = cos(angle) + i * sin(angle)

        for start in range(0, n, length): этот цикл разделит наш массив на блоки длинной length

            текущий множитель  w = 1 и В начале каждого нового блока w снова становится 1.

            for j in range(0, length // 2): этот цикл это и есть сами бабочки и ядро fft

                u = A[start + j] Это верхний элемент бабочки, то есть элемент из левой половины блока
                v = A[start + j + length // 2] * w  Это нижний элемент бабочки, то есть элемент из правой половины блока

                А ТЕПЕРЬ САМА БАБОЧКА
                A[start + j] = u + v
                A[start + j + length // 2] = u - v

                После чего w = w * w_len, увеличиваем множитель

                А если вкратце
                1. Берём пару элементов из двух половин блока.
                2. Второй элемент умножаем на текущий комплексный множитель w.
                3. На место первого элемента кладём сумму.
                4. На место второго элемента кладём разность.
                5. Обновляем w, чтобы следующая бабочка использовала следующий поворот

            
            а теперь увеличиваем размер блока length в 2 раза

        if invert:
            for i in range(n):
                A[i] = A[i] / n
"""

if __name__ == "__main__":
    a = create_BigFloat(make_str_number(Random(2143), 10000))
    b = create_BigFloat(make_str_number(Random(423), 10000))

    start = perf_counter()
    res = Mul(a, b)
    end = perf_counter()
    time = end - start

    expected = to_decimal(a) * to_decimal(b)
    print(f"{res}\n {time:.8f}\n {bigfloat_decimal(res) == expected}")