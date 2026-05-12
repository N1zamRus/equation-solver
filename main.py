from input.interpreter import ThreeBigFloats
from solver.models import Coefs
from solver.solver import solution_calc, output_solution, has_special_value
from solver.decimal_solver import solution_calc as decimal_solution_calc
from tests.test_utility import bigfloat_decimal, solution_to_roots, roots_match


def read_coefficients():
    line = input().strip()
    return ThreeBigFloats().interpret(line)

def main():
    parsed = read_coefficients()

    if parsed is None:
        print("Ошибка ввода")
        return

    a, b, c = parsed

    coefs = Coefs(a, b, c)
    solution = solution_calc(coefs)
    output_solution(solution)

    if has_special_value(coefs):
        print("Проверка через Decimal пропущена для special values")
        return

    actual = solution_to_roots(solution)
    expected = solution_to_roots(decimal_solution_calc(Coefs(
        bigfloat_decimal(a), bigfloat_decimal(b), bigfloat_decimal(c),
    )))
    print("решение верно" if roots_match(actual, expected) else "решение неверно")


if __name__ == "__main__":
    main()