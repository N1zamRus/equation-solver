from solver.models import (
    Coefs,
    ComplexBigFloat,
    Solution,
    SolutionState,
    get_a,
    get_b,
    get_c,
)

from core.BigFloat import BigFloat
from core.Special_values import Nan, is_nan
from core.special_math import (
    special_add,
    special_div,
    special_ge,
    special_is_zero,
    special_lt,
    special_mul,
    special_neg,
    special_short_mul,
    special_sqrt,
    special_sub,
)


ZERO = BigFloat(1, [0], 0)
TWO = BigFloat(1, [2], 0)
FOUR = BigFloat(1, [4], 0)

WORK_PRECISION = 2500


def nan_roots_solution() -> Solution:
    return Solution(solv_type=SolutionState.DIFFERENT_ROOTS, x1=Nan(), x2=Nan())


def has_nan_coefs(coefs: Coefs) -> bool:
    return (
        is_nan(get_a(coefs))
        or is_nan(get_b(coefs))
        or is_nan(get_c(coefs))
    )


def square_b(b):
    return special_mul(b, b, WORK_PRECISION)


def calc_4ac(a, c):
    four_a = special_mul(FOUR, a, WORK_PRECISION)
    return special_mul(four_a, c, WORK_PRECISION)


def calc_discriminant(coefs: Coefs):
    a = get_a(coefs)
    b = get_b(coefs)
    c = get_c(coefs)

    b2 = square_b(b)
    four_ac = calc_4ac(a, c)

    return special_sub(b2, four_ac)


def is_linear(coefs: Coefs) -> bool:
    return special_is_zero(get_a(coefs))


def linear_solve(coefs: Coefs) -> Solution:
    b = get_b(coefs)
    c = get_c(coefs)

    if special_is_zero(b):
        if special_is_zero(c):
            return Solution(solv_type=SolutionState.INFINITE_SOLUTION)
        return Solution(solv_type=SolutionState.NO_SOLUTION)

    x = special_div(special_neg(c), b, WORK_PRECISION)

    return Solution(solv_type=SolutionState.LINEAR, x1=x)


def calc_denominator(a):
    return special_mul(TWO, a, WORK_PRECISION)


def calc_real(b, denominator):
    return special_div(special_neg(b), denominator, WORK_PRECISION)


def calc_imag(discriminant, denominator):
    return special_div(special_sqrt(special_neg(discriminant), 
                                    WORK_PRECISION),
                                    denominator,
                                    WORK_PRECISION,
                                    )


def calc_complex(coefs: Coefs, discriminant) -> Solution:
    a = get_a(coefs)
    b = get_b(coefs)

    denominator = calc_denominator(a)
    real = calc_real(b, denominator)
    imag = calc_imag(discriminant, denominator)

    x1 = ComplexBigFloat(real, imag)
    x2 = ComplexBigFloat(real, special_neg(imag))

    return Solution(solv_type=SolutionState.COMPLEX_ROOTS, x1=x1, x2=x2)


def calc_q(b, sqrt_d):
    if special_ge(b, ZERO):
        return special_short_mul(special_add(b, sqrt_d), -5, -1)

    return special_short_mul(special_sub(b, sqrt_d), -5, -1)


def roots_calc(coefs: Coefs, discriminant):
    a = get_a(coefs)
    b = get_b(coefs)
    c = get_c(coefs)

    sqrt_d = special_sqrt(discriminant, WORK_PRECISION)
    q = calc_q(b, sqrt_d)

    x1 = special_div(q, a, WORK_PRECISION)
    x2 = special_div(c, q, WORK_PRECISION)

    return x1, x2


def quadratic_solve(coefs: Coefs) -> Solution:
    discriminant = calc_discriminant(coefs)

    if is_nan(discriminant):
        return nan_roots_solution()

    if special_lt(discriminant, ZERO):
        return calc_complex(coefs, discriminant)

    if special_is_zero(discriminant):
        denominator = calc_denominator(get_a(coefs))
        root = calc_real(get_b(coefs), denominator)

        return Solution(solv_type=SolutionState.SAME_ROOTS, x1=root)

    root1, root2 = roots_calc(coefs, discriminant)

    return Solution(solv_type=SolutionState.DIFFERENT_ROOTS, x1=root1, x2=root2,)

def special_solution_calc(coefs: Coefs) -> Solution:
    if has_nan_coefs(coefs):
        return nan_roots_solution()

    if is_linear(coefs):
        return linear_solve(coefs)

    return quadratic_solve(coefs)