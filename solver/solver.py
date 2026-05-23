from solver.models import (
    Coefs,
    ComplexBigFloat,
    Solution,
    SolutionState,
    get_a,
    get_b,
    get_c,
    get_x1,
    get_x2,
    get_solve_type,
    get_real,
    get_imag,
)
from solver.special_solver import special_solution_calc

from core.Special_values import is_special_value
from core.BigFloat import BigFloat, is_zero, get_sign, bigfloat_string
from core.BigFloat_math import Add, Sub, Mul, short_Mul, Div, Sqrt
from tests.test_utility import to_decimal


ZERO = BigFloat(1, [0], 0)
TWO = BigFloat(1, [2], 0)
FOUR = BigFloat(1, [4], 0)

WORK_PRECISION = 2500


def square_b(b: BigFloat) -> BigFloat:
    return Mul(b, b, WORK_PRECISION)

def calc_4ac(a: BigFloat, c: BigFloat) -> BigFloat:
    return Mul(Mul(FOUR, a, WORK_PRECISION), c, WORK_PRECISION)

def calc_discriminant(coefs: Coefs):
    a = get_a(coefs)
    b = get_b(coefs)
    c = get_c(coefs)

    b2 = square_b(b)
    four_ac = calc_4ac(a, c)

    return Sub(b2, four_ac)


def is_linear(coefs: Coefs) -> bool:
    return is_zero(get_a(coefs))


def linear_solve(coefs: Coefs) -> Solution:
    b = get_b(coefs)
    c = get_c(coefs)

    if is_zero(b):
        if is_zero(c):
            return Solution(solv_type=SolutionState.INFINITE_SOLUTION)
        return Solution(solv_type=SolutionState.NO_SOLUTION)

    x = Div(-c, b, WORK_PRECISION)
    return Solution(solv_type=SolutionState.LINEAR, x1=x)


def calc_denominator(a: BigFloat) -> BigFloat:
    return Mul(TWO, a, WORK_PRECISION)


def calc_real(b: BigFloat, denominator: BigFloat) -> BigFloat:
    return Div(-b, denominator, WORK_PRECISION)


def calc_imag(discriminant: BigFloat, denominator: BigFloat) -> BigFloat:
    return Div(Sqrt(-discriminant, WORK_PRECISION), denominator, WORK_PRECISION)


def calc_complex(coefs: Coefs, discriminant: BigFloat) -> Solution:
    a = get_a(coefs)
    b = get_b(coefs)

    denominator = calc_denominator(a)
    real = calc_real(b, denominator)
    imag = calc_imag(discriminant, denominator)

    x1 = ComplexBigFloat(real, imag)
    x2 = ComplexBigFloat(real, -imag)

    return Solution(
        solv_type=SolutionState.COMPLEX_ROOTS,
        x1=x1,
        x2=x2,
    )


def calc_q(b: BigFloat, sqrt_d: BigFloat) -> BigFloat:
    if b >= ZERO:
        return short_Mul(Add(b, sqrt_d), -5, -1)
    return short_Mul(Sub(b, sqrt_d), -5, -1)


def roots_calc(coefs: Coefs, discriminant: BigFloat):
    a = get_a(coefs)
    b = get_b(coefs)
    c = get_c(coefs)

    sqrt_d = Sqrt(discriminant, WORK_PRECISION)
    q = calc_q(b, sqrt_d)

    x1 = Div(q, a, WORK_PRECISION)
    x2 = Div(c, q, WORK_PRECISION)

    return x1, x2

def quadratic_solve(coefs: Coefs) -> Solution:
    discriminant = calc_discriminant(coefs)

    if get_sign(discriminant) < 0:
        return calc_complex(coefs, discriminant)

    if is_zero(discriminant):
        denominator = short_Mul(get_a(coefs), 2, 0)
        root = Div(-get_b(coefs), denominator, WORK_PRECISION)
        return Solution(solv_type=SolutionState.SAME_ROOTS, x1=root)

    root1, root2 = roots_calc(coefs, discriminant)
    return Solution(
        solv_type=SolutionState.DIFFERENT_ROOTS,
        x1=root1,
        x2=root2,
    )

def has_special_value(coefs: Coefs) -> bool:
    return (
        is_special_value(get_a(coefs))
        or is_special_value(get_b(coefs))
        or is_special_value(get_c(coefs))
    )


def solution_calc(coefs: Coefs) -> Solution:
    if has_special_value(coefs):
        return special_solution_calc(coefs)
    if is_linear(coefs):
        return linear_solve(coefs)

    return quadratic_solve(coefs)


def output_solution(solution: Solution):
    print(get_solve_type(solution), end=": ")

    if solution.solv_type == SolutionState.SAME_ROOTS:
        print(f"x = {value_str(get_x1(solution))}")
        return
    if solution.x1 is not None:
        print(f"x1 = {value_str(get_x1(solution))}")
    if solution.x2 is not None:
        print(f"x2 = {value_str(get_x2(solution))}")


def value_str(value: ComplexBigFloat | BigFloat):
    if isinstance(value, ComplexBigFloat):
        return complex_string(value)
    elif isinstance(value, BigFloat):
        return bigfloat_string(value)

    return str(value)

def complex_string(value: ComplexBigFloat):
    real = f"{to_decimal(get_real(value)):.10010f}"[:10000]

    imag_value = get_imag(value)
    imag_abs = abs(imag_value)
    imag = f"{to_decimal(imag_abs):.10010f}"[:10000]

    if isinstance(imag_value, BigFloat):
        sign = get_sign(imag_value)
    elif hasattr(imag_value, "sign"):
        sign = imag_value.sign
    else:
        sign = 1

    if sign < 0:
        return f"{real} - {imag}i"

    return f"{real} + {imag}i"