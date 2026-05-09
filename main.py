from input.interpreter import ThreeBigFloats
from solver.models import Coefs
from solver.solver import solution_calc, output_solution
from core.BigFloat import bigfloat_string


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


if __name__ == "__main__":
    main()