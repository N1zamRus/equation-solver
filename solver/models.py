from core.BigFloat import BigFloat
from core.Special_values import Nan, Infinity
from tests.test_utility import to_decimal
from decimal import Decimal, getcontext, MAX_EMAX, MIN_EMIN
from enum import Enum, auto

NULL = BigFloat(1, [0], 0)

getcontext().prec = 50000
getcontext().Emax = MAX_EMAX
getcontext().Emin = MIN_EMIN

class SolutionState(Enum):
    INFINITE_SOLUTION = auto()
    NO_SOLUTION = auto()
    LINEAR = auto()
    COMPLEX_ROOTS = auto()
    SAME_ROOTS = auto()
    DIFFERENT_ROOTS = auto()


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

    def __eq__(self, other: "Solution"):
        if not same_solv_type(self, other):
            return False
        
        if is_special_solv(self) or is_special_solv(other):
            return True
        
        if self.solv_type == SolutionState.COMPLEX_ROOTS:
            return complex_eq(self.x1, other.x1) and complex_eq(self.x2, other.x2)


        self_roots = pack_roots(self)
        other_roots = pack_roots(other)
        
        self_strs = sorted(root_to_str(r) for r in self_roots)
        other_strs = sorted(root_to_str(r) for r in other_roots)

        return self_strs == other_strs 

def same_solv_type(self: Solution, other: Solution):
    return self.solv_type == other.solv_type

def is_special_solv(self: Solution):
    return self.solv_type in (SolutionState.INFINITE_SOLUTION, SolutionState.NO_SOLUTION)

def pack_roots(self: Solution):
    return [x for x in (self.x1,  self.x2) if x is not None]


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


def get_real(value: ComplexDecimal | ComplexBigFloat):
    return value.real


def get_imag(value: ComplexDecimal | ComplexBigFloat):
    return value.imag


def complex_decimal_string(value: ComplexDecimal):
    real = f"{get_real(value):.10010f}"[:10000]
    imag_val = get_imag(value)
    imag = f"{abs(imag_val):.10010f}"[:10000]

    if imag_val < Decimal("0"):
        return f"{real} - {imag}i"

    return f"{real} + {imag}i"

def complex_eq(a: ComplexBigFloat | ComplexDecimal, b: ComplexBigFloat | ComplexDecimal) -> bool:
    real_a = get_real(a)
    imag_a = get_imag(a)
    real_b = get_real(b)
    imag_b = get_imag(b)

    real_a_decimal = to_decimal(real_a)
    imag_a_decimal = to_decimal(imag_a)
    real_b_decimal = to_decimal(real_b)
    imag_b_decimal = to_decimal(imag_b)

    real_a_str = f"{real_a_decimal:.10010f}"[:10000]
    imag_a_str = f"{imag_a_decimal:.10010f}"[:10000]
    real_b_str = f"{real_b_decimal:.10010f}"[:10000]
    imag_b_str = f"{imag_b_decimal:.10010f}"[:10000]

    return real_a_str == real_b_str and imag_a_str == imag_b_str

def root_to_str(root: BigFloat | Decimal | Nan | Infinity) -> str:
    root_decimal = to_decimal(root)
    if root_decimal.is_nan():
        return "Nan"
    if root_decimal.is_infinite():
        return str(root_decimal)
    return f"{root_decimal:.10010f}"[:10000]
