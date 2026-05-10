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


def parse_literal(source: str, pos: int, literal: str) -> ParseResult:
    start = pos

    for char in literal:
        if pos >= len(source) or source[pos] != char:
            return ParseResult(False, start)
        pos += 1

    return ParseResult(True, pos)


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


def parse_full_token(source: str, parser, token_name: str) -> ParseResult:
    result = parser.parse(source, 0)

    if not result.ok:
        return result

    if result.pos != len(source):
        bad_char = source[result.pos]
        return ParseResult(
            False,
            result.pos,
            f"Некорректный символ после {token_name}: {bad_char!r} в токене {source!r}",
        )

    return result


def ShowErrorMassege(message: str) -> None:
    print(message)