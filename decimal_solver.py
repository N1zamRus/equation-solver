from enum import Enum, auto
from decimal import Decimal

from models import (
    Coefs, 
    ComplexDecimal,
    Solution, 
    get_a, 
    get_b, 
    get_c, 
    get_x1, 
    get_x2, 
    get_solve_type,
    complex_decimal_string,
)


ZERO = Decimal('0')
TWO = Decimal('2')
FOUR = Decimal('4')


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

    b2 = b * b
    four_ac = FOUR * a * c

    return b2 - four_ac


def is_linear(coefs: Coefs) -> bool:
    return get_a(coefs) == ZERO


def linear_solve(coefs: Coefs) -> Solution:
    b = get_b(coefs)
    c = get_c(coefs)

    if b == ZERO:
        if c == ZERO:
            return Solution(solv_type=SolutionState.INFINITE_SOLUTION)
        return Solution(solv_type=SolutionState.NO_SOLUTION)

    x = -c / b
    return Solution(solv_type=SolutionState.LINEAR, x1=x)


def calc_complex(coefs: Coefs, discriminant: Decimal) -> Solution:
    a = get_a(coefs)
    b = get_b(coefs)

    denominator = TWO * a

    real = -b / denominator
    imag = (-discriminant).sqrt() / denominator

    x1 = ComplexDecimal(real, imag)
    x2 = ComplexDecimal(real, -imag)

    return Solution(
        solv_type=SolutionState.COMPLEX_ROOTS,
        x1=x1,
        x2=x2,
    )


def roots_calc(coefs: Coefs, discriminant: Decimal):
    a = get_a(coefs)
    b = get_b(coefs)
    c = get_c(coefs)

    sqrt_d = discriminant.sqrt()

    if b >= ZERO:
        q = Decimal('-0.5') * (b + sqrt_d)
    else:
        q = Decimal('-0.5') * (b - sqrt_d)

    x1 = q / a
    x2 = c / q

    return x1, x2


def quadratic_solve(coefs: Coefs) -> Solution:
    discriminant = calc_discriminant(coefs)

    if discriminant < ZERO:
        return calc_complex(coefs, discriminant)

    if discriminant == ZERO:
        denominator = TWO * get_a(coefs)
        root = -get_b(coefs) / denominator
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


def value_str(value):
    if isinstance(value, ComplexDecimal):
        return complex_decimal_string(value)
    return str(value)


def output_solution(solution: Solution):
    print(get_solve_type(solution), end=': ')

    if solution.solv_type == SolutionState.SAME_ROOTS:
        print(f'x = {value_str(get_x1(solution))}')
        return

    if solution.x1 is not None:
        print(f'x1 = {value_str(get_x1(solution))}', end=' ')
    if solution.x2 is not None:
        print(f'x2 = {value_str(get_x2(solution))}')
    else:
        print()
