from dataclasses import dataclass

@dataclass(frozen=True)
class ParseResult:
    ok: bool
    pos: int
    error: str | None = None


def is_digit(now_char: str | None) -> bool:
    return now_char is not None and now_char in "0123456789"


def is_zero(now_char: str | None) -> bool:
    return now_char is not None and now_char == "0"


def is_without_zero_digit(now_char: str | None) -> bool:
    return now_char is not None and now_char in "123456789"


def is_sign(now_char: str | None) -> bool:
    return now_char is not None and now_char in "+-"


def is_dot(now_char: str | None) -> bool:
    return now_char is not None and now_char in ".,"


def is_exp(now_char: str | None) -> bool:
    return now_char is not None and now_char in "eE"


def is_underline(now_char: str | None) -> bool:
    return now_char is not None and now_char == "_"



def parse_digit_part(source: str, pos: int) -> ParseResult:
    """
    digit_part = [underline], digit
    """

    start = pos

    if pos < len(source) and is_underline(source[pos]):
        pos += 1

    if pos < len(source) and is_digit(source[pos]):
        return ParseResult(True, pos + 1)

    return ParseResult(False, start, "Ожидалась цифра после подчёркивания")


def parse_digit_parts(source: str, pos: int) -> int:
    """
    {digit_part}
    """

    result = parse_digit_part(source, pos)

    while result.ok:
        pos = result.pos
        result = parse_digit_part(source, pos)

    return pos



def ShowErrorMassege(message: str) -> None:
    print(message)