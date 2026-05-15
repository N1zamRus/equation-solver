from __future__ import annotations

from abc import ABC, abstractmethod

from core.BigFloat import create_BigFloat
from input.interpreter_utility import (
    ParseResult,
    ShowErrorMassege,
    is_digit,
    is_dot,
    is_exp,
    is_sign,
    is_without_zero_digit,
    is_zero,
    parse_digit_parts,
)


class Node(ABC):
    @abstractmethod
    def interpret(self, source: str, pos: int = 0) -> ParseResult:
        pass


class Integer(Node):
    """integer = zero | without_zero_digit, {digit_part}"""

    def interpret(self, source: str, pos: int = 0) -> ParseResult:
        start = pos

        if pos >= len(source):
            return ParseResult(False, start, "Ожидалось целое число")

        if is_zero(source[pos]):
            return ParseResult(True, pos + 1)

        if is_without_zero_digit(source[pos]):
            pos += 1
            pos = parse_digit_parts(source, pos)
            return ParseResult(True, pos)

        return ParseResult(False, start, "Ожидалось целое число")


class Exponent(Node):
    """exponent = exp, [sign], integer"""

    def interpret(self, source: str, pos: int = 0) -> ParseResult:
        start = pos

        if pos >= len(source) or not is_exp(source[pos]):
            return ParseResult(False, start)

        pos += 1

        if pos < len(source) and is_sign(source[pos]):
            pos += 1

        result = Integer().interpret(source, pos)
        if not result.ok:
            return ParseResult(False, start, "После exponent ожидалось целое число")

        return ParseResult(True, result.pos)


class FractionAfterInteger(Node):
    """frac_after_integer = dot, [digit, {digit_part}]"""

    def interpret(self, source: str, pos: int = 0) -> ParseResult:
        start = pos

        if pos >= len(source) or not is_dot(source[pos]):
            return ParseResult(False, start)

        pos += 1

        if pos < len(source) and is_digit(source[pos]):
            pos += 1
            pos = parse_digit_parts(source, pos)

        return ParseResult(True, pos)


class FractionWithoutInteger(Node):
    """frac_without_integer = dot, digit, {digit_part}"""

    def interpret(self, source: str, pos: int = 0) -> ParseResult:
        start = pos

        if pos >= len(source) or not is_dot(source[pos]):
            return ParseResult(False, start)

        pos += 1

        if pos >= len(source) or not is_digit(source[pos]):
            return ParseResult(False, start, "После точки или запятой ожидалась цифра")

        pos += 1
        pos = parse_digit_parts(source, pos)

        return ParseResult(True, pos)


class Number(Node):
    """number = (integer, [frac_after_integer] | frac_without_integer), [exponent]"""

    def interpret(self, source: str, pos: int = 0) -> ParseResult:
        start = pos

        result = Integer().interpret(source, pos)

        if result.ok:
            pos = result.pos

            frac_result = FractionAfterInteger().interpret(source, pos)
            if frac_result.ok:
                pos = frac_result.pos

        else:
            result = FractionWithoutInteger().interpret(source, pos)
            if not result.ok:
                return ParseResult(False, start, "Ожидалось число")

            pos = result.pos

        exp_result = Exponent().interpret(source, pos)
        if exp_result.ok:
            pos = exp_result.pos
        elif pos < len(source) and is_exp(source[pos]):
            return exp_result

        return ParseResult(True, pos)


class Nan(Node):
    """nan = "nan" | "NaN" | "NAN"""

    def interpret(self, source: str, pos: int = 0) -> ParseResult:
        if source[pos:].lower().startswith("nan"):
            return ParseResult(True, pos + 3)
        return ParseResult(False, pos)


class Infinity(Node):
    """infinity = "Infinity" | "infinity" | "inf"""

    def interpret(self, source: str, pos: int = 0) -> ParseResult:
        start = pos

        fragment = source[pos:].lower()
        for special_value in ("infinity", "inf"):
            if fragment.find(special_value) == 0:
                return ParseResult(True, pos + len(special_value))
            
        return ParseResult(False, start)



class AbsValue(Node):
    """abs_value = number | infinity | nan"""

    def interpret(self, source: str, pos: int = 0) -> ParseResult:
        start = pos

        result = Number().interpret(source, pos)
        if result.ok:
            return result

        result = Infinity().interpret(source, start)
        if result.ok:
            return result

        result = Nan().interpret(source, start)
        if result.ok:
            return result

        return ParseResult(False, start, "Ожидалось число, infinity, inf или nan")


class Float(Node):
    """float = [sign], abs_value"""

    def interpret(self, source: str, pos: int = 0) -> ParseResult:
        start = pos

        if pos < len(source) and is_sign(source[pos]):
            pos += 1

        result = AbsValue().interpret(source, pos)
        if not result.ok:
            return ParseResult(False, start, result.error)

        return ParseResult(True, result.pos)


class ThreeBigFloats:
    def interpret(self, text: str):
        numbers = text.split()

        if len(numbers) != 3:
            ShowErrorMassege("Числа должно быть ровно 3")
            return None

        for number in numbers:
            result = parse_float_token(number)
            if not result.ok:
                ShowErrorMassege(result.error)
                return None

        return (
            create_BigFloat(numbers[0]),
            create_BigFloat(numbers[1]),
            create_BigFloat(numbers[2]),
        )


def parse_float_token(source: str) -> ParseResult:
    result = Float().interpret(source, 0)

    if not result.ok:
        return result

    if result.pos != len(source):
        bad_char = source[result.pos]
        return ParseResult(False, result.pos, f"Некорректный символ после float: {bad_char} в токене {source}",)

    return result


def is_number(source: str) -> bool:
    result = parse_float_token(source)
    return result.ok
