from core.BigFloat import BigFloat, get_sign, bigfloat_string
from decimal import Decimal

NULL = BigFloat(1, [0], 0)

class Coefs:
    def __init__(self, a: BigFloat | Decimal = NULL, b: BigFloat | Decimal = NULL, c: BigFloat | Decimal = NULL) -> None:
        self.a = a
        self.b = b
        self.c = c

    def __repr__(self):
        return f"Coefs({self.a}, {self.b}, {self.c})"

def get_a(coefs: Coefs):
    return coefs.a


def get_b(coefs: Coefs):
    return coefs.b


def get_c(coefs: Coefs):
    return coefs.c


class Solution:
    def __init__(self, solv_type=None, x1: BigFloat | Decimal | None = None, x2: BigFloat | Decimal | None = None):
        self.solv_type = solv_type
        self.x1 = x1
        self.x2 = x2


def get_x1(solution: Solution):
    return solution.x1


def get_x2(solution: Solution):
    return solution.x2


def get_solve_type(solution: Solution):
    return solution.solv_type

class ComplexBigFloat:
    def __init__(self, real: BigFloat, imag: BigFloat):
        self.real = real
        self.imag = imag


class ComplexDecimal:
    def __init__(self, real: Decimal, imag: Decimal):
        self.real = real
        self.imag = imag


def complex_bigfloat_string(value: ComplexBigFloat):
    real = bigfloat_string(value.real)
    imag = bigfloat_string(abs(value.imag))

    if get_sign(value.imag) < 0:
        return f"{real} - {imag}i"

    return f"{real} + {imag}i"

def complex_decimal_string(value: ComplexDecimal):
    real = str(value.real)
    imag = str(abs(value.imag))

    if value.imag < Decimal('0'):
        return f'{real} - {imag}i'

    return f'{real} + {imag}i'


def get_real(value: ComplexDecimal | ComplexBigFloat):
    return value.real


def get_imag(value: ComplexDecimal | ComplexBigFloat):
    return value.imag
