from dataclasses import dataclass
from abc import ABC, abstractmethod
from core.BigFloat import BigFloat

class Special(ABC):
    @abstractmethod
    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def __neg__(self):
        pass


"""
class Nan:
    
    1. +
        Вернуть nan

    2. -
        Вернуть nan

    3. *
        Вернуть nan

    4. /
        Вернуть nan
"""

class Nan(Special):
    def __add__(self, other: "Nan" | "Infinity" | float):
        return Nan()

    def __sub__(self, other: "Nan" | "Infinity" | float):
        return Nan()

    def __truediv__(self, other: "Nan" | "Infinity" | float):
        return Nan()

    def __neg__(self):
        return Nan()
    
    def __repr__(self):
        return "Nan"

"""

class Infinity:
    self.sign = sign
    1. +
        Если other == nan, то вернём nan
        Если other == inf и знаки разные то nan, если знаки одинаковые то inf * self.sign 
        Если other == BigFloat, то вернём inf * self.sign 
    2. -
        Если other == nan, то вернём nan
        Если other == inf и знаки разные то nan, если знаки одинаковые то inf * self.sign 
        Если other == BigFloat, то вернём inf * self.sign 
    3. *
        Если other == nan, то вернём nan
        Если other == inf, то inf * (self.sign * other.sign)
        Если other == BigFloat, то вернём inf * (self.sign * other.sign)
    4. /
        Если other == nan, то вернём nan
        Если other == inf, то nan
        Если other == BigFloat, то вернём inf * (self.sign * other.sign)

"""
@dataclass
class Infinity(Special):
    sign: int

    def __add__(self, other: "Nan" | "Infinity" | float):
        if isinstance(other, Nan): return Nan()
        if isinstance(other, Infinity) and self.sign != other.sign: 
            return Nan() 
        elif isinstance(other, Infinity):
            return Infinity(self.sign * other.sign)
        elif isinstance(other, float):
            return Infinity(1 if other >= 0 else -1)
        
    def __sub__(self, other: "Nan" | "Infinity" | float):
        if isinstance(other, Nan): return Nan()
        if isinstance(other, Infinity) and self.sign != other.sign: 
            return Nan() 
        elif isinstance(other, Infinity):
            return Infinity(self.sign * other.sign)
        elif isinstance(other, float):
            return Infinity(1 if other >= 0 else -1)
        
    def __mul__(self, other: "Nan" | "Infinity" | float):
        if isinstance(other, Nan):
            return Nan()
        elif isinstance(other, Infinity):
            return Infinity(self.sign * other.sign)
        elif isinstance(other, float):
            return Infinity(1 if other >= 0 else -1)
        
    def __truediv__(self, other: "Nan" | "Infinity" | float):
        if isinstance(other, Nan) or isinstance(other, Infinity):
            return Nan()
        else:
            return Infinity(1 if other >= 0 else -1)
                
if __name__ == "__main__":

    line = input().split()
    a = float(line[0])
    b = float(line[1])
    c = float(line[2])

    coefs = (a, b, c)

    def solution_calc(coefs):
        if coefs[0] == 0:
            linear_solve(coefs)
            return 0
        return quadratic_solve(coefs)
    
    def linear_solve(coefs: tuple):
        b = coefs[1]
        c = coefs[2]

        if b == 0:
            if c == 0:
                print("Бесконечно много решений")
            print("Нет решения")

        x = -c / b
        print(x)

    def quadratic_solve(coefs: tuple):
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
    
    def calc_discriminant(coefs: tuple):
        a = coefs[0]
        b = coefs[1]
        c = coefs[2]

        b2 = b*b
        four_ac = 4 * a * c

        return Sub(b2, four_ac)