from enum import Enum, auto

from models import Coefs, ComplexBigFloat, complex_bigfloat_string, Solution, get_a, get_b, get_c, get_x1, get_x2, get_solve_type
from BigFloat import BigFloat, is_zero, get_sign, bigfloat_string
from BigFloat_math import Add, Sub, Mul, short_Mul, Div, Sqrt


ZERO = BigFloat(1, [0], 0)
TWO = BigFloat(1, [2], 0)
FOUR = BigFloat(1, [4], 0)


class SolutionState(Enum):
    INFINITE_SOLUTION = auto()
    NO_SOLUTION = auto()
    LINEAR = auto()
    COMPLEX_ROOTS = auto()
    SAME_ROOTS = auto()
    DIFFERENT_ROOTS = auto()


def calc_discriminant(coefs: Coefs):
    a = get_a(coefs)
    b = get_b(coefs)
    c = get_c(coefs)

    b2 = Mul(b, b)
    four_ac = Mul(Mul(FOUR, a), c)

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

    x = Div(-c, b)
    return Solution(solv_type=SolutionState.LINEAR, x1=x)


def calc_complex(coefs: Coefs, discriminant: BigFloat) -> Solution:
    a = get_a(coefs)
    b = get_b(coefs)

    denominator = Mul(TWO, a)

    real = Div(-b, denominator)
    imag = Div(Sqrt(-discriminant), denominator)

    x1 = ComplexBigFloat(real, imag)
    x2 = ComplexBigFloat(real, -imag)

    return Solution(
        solv_type=SolutionState.COMPLEX_ROOTS,
        x1=x1,
        x2=x2,
    )


def roots_calc(coefs: Coefs, discriminant: BigFloat):
    b = get_b(coefs)
    a = get_a(coefs)

    sqrt_d = Sqrt(discriminant)
    denominator = Mul(TWO, a)

    x1 = Div(Add(-b, sqrt_d), denominator)
    x2 = Div(Sub(-b, sqrt_d), denominator)

    return x1, x2


def quadratic_solve(coefs: Coefs) -> Solution:
    discriminant = calc_discriminant(coefs)

    if get_sign(discriminant) < 0:
        return calc_complex(coefs, discriminant)

    if is_zero(discriminant):
        denominator = Mul(TWO, get_a(coefs))
        root = Div(-get_b(coefs), denominator)
        return Solution(solv_type=SolutionState.SAME_ROOTS, x1=root)

    root1, root2 = roots_calc(coefs, discriminant)
    return Solution(
        solv_type=SolutionState.DIFFERENT_ROOTS,
        x1=root1,
        x2=root2,
    )


def solution_calc(coefs: Coefs) -> Solution:
    if is_linear(coefs):
        return linear_solve(coefs)
    return quadratic_solve(coefs)


def output_solution(solution: Solution):
    print(get_solve_type(solution), end=": ")

    if solution.solv_type == SolutionState.INFINITE_SOLUTION:
        print("бесконечно много решений")
        return

    if solution.solv_type == SolutionState.NO_SOLUTION:
        print("решений нет")
        return

    if solution.solv_type == SolutionState.LINEAR:
        print(f"x = {bigfloat_string(get_x1(solution))}")
        return

    if solution.solv_type == SolutionState.COMPLEX_ROOTS:
        print()
        print(f"x1 = {complex_bigfloat_string(get_x1(solution))}")
        print(f"x2 = {complex_bigfloat_string(get_x2(solution))}")
        return

    if solution.solv_type == SolutionState.SAME_ROOTS:
        print(f"x = {bigfloat_string(get_x1(solution))}")
        return

    if solution.x1 is not None:
        print(f"x1 = {bigfloat_string(get_x1(solution))}", end=" ")

    if solution.x2 is not None:
        print(f"x2 = {bigfloat_string(get_x2(solution))}")
    else:
        print()
