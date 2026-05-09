from input.interpreter import ThreeBigFloats
from solver.models import Coefs
from solver.solver import solution_calc, output_solution
from core.BigFloat import bigfloat_string


def read_coefficients():
    print("Введите коэффициенты квадратного уравнения через пробел:")
    print("Формат: a b c")
    print("Пример: 1 -3 2")
    print()

    line = input("a b c > ").strip()
    return ThreeBigFloats().interpret(line)


def print_equation(a, b, c):
    print()
    print("Распознанное уравнение:")
    print(f"({bigfloat_string(a)}) * x^2 + ({bigfloat_string(b)}) * x + ({bigfloat_string(c)}) = 0")
    print()


def main():
    parsed = read_coefficients()

    if parsed is None:
        print("Ошибка ввода.")
        return

    a, b, c = parsed

    print_equation(a, b, c)

    coefs = Coefs(a, b, c)
    solution = solution_calc(coefs)

    print("Решение:")
    output_solution(solution)


if __name__ == "__main__":
    main()