from decimal import Decimal, getcontext, InvalidOperation, DivisionByZero

from solver.models import (
    Coefs,
    ComplexDecimal,
    Solution,
    SolutionState,
    get_a,
    get_b,
    get_c,
    get_x1,
    get_x2,
    get_solve_type,
    complex_decimal_string,
)


ZERO = Decimal("0")
TWO = Decimal("2")
FOUR = Decimal("4")

getcontext().traps[InvalidOperation] = False
getcontext().traps[DivisionByZero] = False


def square_b(b: Decimal) -> Decimal:
    return b * b


def calc_4ac(a: Decimal, c: Decimal) -> Decimal:
    return FOUR * a * c


def calc_discriminant(coefs: Coefs) -> Decimal:
    a = get_a(coefs)
    b = get_b(coefs)
    c = get_c(coefs)

    b2 = square_b(b)
    four_ac = calc_4ac(a, c)

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


def calc_denominator(a: Decimal) -> Decimal:
    return TWO * a


def calc_real(b: Decimal, denominator: Decimal) -> Decimal:
    return -b / denominator


def calc_imag(discriminant: Decimal, denominator: Decimal) -> Decimal:
    return (-discriminant).sqrt() / denominator


def calc_complex(coefs: Coefs, discriminant: Decimal) -> Solution:
    a = get_a(coefs)
    b = get_b(coefs)

    denominator = calc_denominator(a)
    real = calc_real(b, denominator)
    imag = calc_imag(discriminant, denominator)

    x1 = ComplexDecimal(real, imag)
    x2 = ComplexDecimal(real, -imag)

    return Solution(solv_type=SolutionState.COMPLEX_ROOTS,
                    x1=x1,
                    x2=x2
    )


def calc_q(b: Decimal, sqrt_d: Decimal) -> Decimal:
    if b >= ZERO:
        return Decimal("-0.5") * (b + sqrt_d)
    return Decimal("-0.5") * (b - sqrt_d)


def normalize_zero(value: Decimal) -> Decimal:
    return ZERO if value == ZERO else value


def roots_calc(coefs: Coefs, discriminant: Decimal):
    a = get_a(coefs)
    b = get_b(coefs)
    c = get_c(coefs)

    sqrt_d = discriminant.sqrt()
    q = calc_q(b, sqrt_d)

    x1 = normalize_zero(q / a)
    x2 = normalize_zero(c / q)

    return x1, x2


def quadratic_solve(coefs: Coefs) -> Solution:
    discriminant = calc_discriminant(coefs)

    if discriminant.is_nan():
        return Solution(solv_type=SolutionState.DIFFERENT_ROOTS,
                        x1=Decimal("NaN"),
                        x2=Decimal("NaN")
        )

    if discriminant < ZERO:
        return calc_complex(coefs, discriminant)

    if discriminant == ZERO:
        denominator = calc_denominator(get_a(coefs))
        root = calc_real(get_b(coefs), denominator)
        return Solution(solv_type=SolutionState.SAME_ROOTS, x1=root)

    root1, root2 = roots_calc(coefs, discriminant)
    return Solution(solv_type=SolutionState.DIFFERENT_ROOTS,
                    x1=root1,
                    x2=root2
    )


def solution_calc(coefs: Coefs) -> Solution:
    a, b, c = get_a(coefs), get_b(coefs), get_c(coefs)
    if a.is_nan() or b.is_nan() or c.is_nan():
        return Solution(solv_type=SolutionState.DIFFERENT_ROOTS,
                        x1=Decimal("NaN"),
                        x2=Decimal("NaN")
        )
    
    if is_linear(coefs):
        return linear_solve(coefs)
    return quadratic_solve(coefs)


def value_str(value) -> str:
    if isinstance(value, ComplexDecimal):
        return complex_decimal_string(value)
    return str(value)


def output_solution(solution: Solution) -> None:
    print(get_solve_type(solution), end=": ")

    if solution.solv_type == SolutionState.SAME_ROOTS:
        print(f"x = {value_str(get_x1(solution))}")
        return

    if solution.x1 is not None:
        print(f"x1 = {value_str(get_x1(solution))}", end=" ")
    if solution.x2 is not None:
        print(f"x2 = {value_str(get_x2(solution))}")