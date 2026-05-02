"""
digit                = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
without_Null_digit   = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
dot                  = "." | ","
sign                 = "+" | "-"
exp                  = "e" | "E"
zero                 = "0"


integer         = zero | without_Null_digit, {digit}
signed_integer  = [sign], integer

exponent        = exp, [sign], without_Null_digit, {digit}
frac            = dot, digit, {digit}

number          = [sign], (integer, [frac] | frac), [exponent]
"""

from abc import ABC, abstractmethod
from BigFloat import create_BigFloat


class Text:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def current_char(self):
        if self.is_end():
            return None
        return self.text[self.pos]

    def next_char(self):
        self.pos += 1

    def is_end(self) -> bool:
        return self.pos >= len(self.text)


class Node(ABC):
    @abstractmethod
    def interpret(self, text: Text):
        pass


class Integer(Node):
    """integer = zero | without_Null_digit, {digit}"""

    def interpret(self, text: Text):
        start_pos = text.pos

        if is_zero(text.current_char()):
            text.next_char()
            return True

        if is_without_null_digit(text.current_char()):
            text.next_char()
            while is_digit(text.current_char()):
                text.next_char()

            return True

        text.pos = start_pos
        return False


class SignedInteger(Node):
    """signed_integer = [sign], integer"""

    def interpret(self, text: Text):
        start_pos = text.pos

        if is_sign(text.current_char()):
            text.next_char()

        if Integer().interpret(text):
            return True

        text.pos = start_pos
        return False


class Fraction(Node):
    """frac = dot, digit, {digit}"""

    def interpret(self, text: Text):
        start_pos = text.pos
        if not is_dot(text.current_char()):
            text.pos = start_pos
            return False

        text.next_char()
        if not is_digit(text.current_char()):
            text.pos = start_pos
            return False

        text.next_char()
        while is_digit(text.current_char()):
            text.next_char()

        return True


class Exponent(Node):
    """exponent = exp, [sign], without_Null_digit, {digit}"""

    def interpret(self, text: Text):
        start_pos = text.pos

        if not is_exp(text.current_char()):
            text.pos = start_pos
            return False

        text.next_char()

        if is_sign(text.current_char()):
            text.next_char()

        if not is_without_null_digit(text.current_char()):
            text.pos = start_pos
            return False

        text.next_char()

        while is_digit(text.current_char()):
            text.next_char()

        return True


class Number(Node):
    """number = [sign], (integer, [frac] | frac), [exponent]"""

    def interpret(self, text: Text):
        start_pos = text.pos

        if is_sign(text.current_char()):
            text.next_char()

        if Integer().interpret(text):
            Fraction().interpret(text)

        elif Fraction().interpret(text): # на случай .3123
            pass

        else:
            text.pos = start_pos
            ShowErrorMassege(f"Не обработался токен: {text.text}, '{text.current_char()}'")
            return False

        Exponent().interpret(text)

        if not text.is_end():
            text.pos = start_pos
            ShowErrorMassege(f"Обработались не все символы у Number: {text.text}, '{text.current_char()}'")
            return False

        return True

class ThreeBigFloats:
    def interpret(self, text: str):
        numbers = text.split()

        if len(numbers) != 3:
            ShowErrorMassege("Числа должно быть ровно 3")
            return None

        for number in numbers:
            if not is_number(number):
                ShowErrorMassege(f"Некорректное число: {number}")
                return None

        return (create_BigFloat(numbers[0]),
                create_BigFloat(numbers[1]),
                create_BigFloat(numbers[2]),)

def is_digit(now_char: str)-> bool:
    if now_char is not None and now_char in ("1234567890"):
        return True
    return False

def is_zero(now_char: str)-> bool:
    if now_char is not None and now_char == "0":
        return True
    return False

def is_without_null_digit(now_char: str)-> bool:
    if now_char is not None and now_char in ("123456789"):
        return True
    return False

def is_sign(now_char: str)-> bool:
    if now_char is not None and now_char in "-+":
        return True
    return False

def is_dot(now_char: str)-> bool:
    if now_char is not None and now_char in ".,":
        return True
    return False

def is_exp(now_char: str):
    if now_char is not None and now_char in "eE":
        return True
    return False

def ShowErrorMassege(mess):
    print(mess)

def is_number(text: str) -> bool:
    return Number().interpret(Text(text))