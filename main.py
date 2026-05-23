from input.interpreter import ThreeBigFloats
from solver.models import Coefs
from solver.solver import solution_calc, output_solution
from solver.decimal_solver import solution_calc as decimal_solution_calc, output_solution as decimal_output_solution
from tests.test_utility import to_decimal


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

    expected = decimal_solution_calc(Coefs(
        to_decimal(a), to_decimal(b), to_decimal(c),
    ))

    output_solution(solution)

    print(f"\n\n{'=' * 162}\n\n")

    decimal_output_solution(expected)

    print("решение верно" if solution == expected else "решение неверно")

if __name__ == "__main__":
    main()
    