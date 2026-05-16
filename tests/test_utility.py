from random import Random, randint
from decimal import Decimal
from core.BigFloat import BigFloat, create_BigFloat, get_exp10, get_mantiss, get_sign, bigfloat_string
from core.Special_values import (
    Nan,
    Infinity,
    is_nan,
    is_infinity
)

RANDOM_SEED = randint(1, 326432134)
RANDOM_PAIRS_COUNT = 100
RANDOM_NUMBER_LENGTH = 1000

DIGITS = "0123456789"
NON_ZERO_DIGITS = "123456789"
DOTS = ".,"
SIGNS = "+-"
EXPS = "eE"


def make_digits(rng: Random, length: int) -> str:
    result = ""
    for _ in range(length):
        result += rng.choice(DIGITS)
    return result


def make_integer(rng: Random, length: int) -> str:
    if length == 1:
        return rng.choice(DIGITS)
    first_digit = rng.choice(NON_ZERO_DIGITS)
    other_digits = make_digits(rng, length - 1)
    return first_digit + other_digits


def make_signed_integer(rng: Random, length: int) -> str:
    if length == 1:
        return make_integer(rng, length)
    use_sign = rng.choice([True, False])
    if use_sign:
        sign = rng.choice(SIGNS)
        integer = make_integer(rng, length - 1)
        return sign + integer
    return make_integer(rng, length)


def make_exponent_integer(rng: Random, length: int) -> str:
    if length == 1:
        return rng.choice(NON_ZERO_DIGITS)
    use_sign = rng.choice([True, False])
    if use_sign:
        sign = rng.choice(SIGNS)
        integer = rng.choice(NON_ZERO_DIGITS) + make_digits(rng, length - 2)
        return sign + integer
    return rng.choice(NON_ZERO_DIGITS) + make_digits(rng, length - 1)


def make_random_number(rng: Random, length: int) -> str:
    number_type = rng.choice([
        "integer",
        "signed_integer",
        "fraction_with_integer",
        "fraction_without_integer",
        "signed_integer_exponent",
        "fraction_with_exponent",
    ])

    if number_type == "integer":
        return make_integer(rng, length)

    if number_type == "signed_integer":
        return make_signed_integer(rng, length)

    if number_type == "fraction_with_integer":
        sign = rng.choice(["", "+", "-"])
        body_length = length - len(sign)
        integer_length = rng.randint(1, body_length - 2)
        fraction_length = body_length - integer_length - 1
        integer = make_integer(rng, integer_length)
        dot = rng.choice(DOTS)
        fraction = make_digits(rng, fraction_length)
        return sign + integer + dot + fraction

    if number_type == "fraction_without_integer":
        sign = rng.choice(["", "+", "-"])
        body_length = length - len(sign)
        dot = rng.choice(DOTS)
        fraction = make_digits(rng, body_length - 1)
        return sign + dot + fraction

    if number_type == "signed_integer_exponent":
        sign = rng.choice(["", "+", "-"])
        body_length = length - len(sign)
        exponent_length = rng.randint(1, body_length - 2)
        integer_length = body_length - exponent_length - 1
        integer = make_integer(rng, integer_length)
        exp = rng.choice(EXPS)
        exponent = make_exponent_integer(rng, exponent_length)
        return sign + integer + exp + exponent

    if number_type == "fraction_with_exponent":
        sign = rng.choice(["", "+", "-"])
        body_length = length - len(sign)
        free_length = body_length - 2
        integer_length = rng.randint(1, free_length - 2)
        fraction_length = rng.randint(1, free_length - integer_length - 1)
        exponent_length = free_length - integer_length - fraction_length
        integer = make_integer(rng, integer_length)
        dot = rng.choice(DOTS)
        fraction = make_digits(rng, fraction_length)
        exp = rng.choice(EXPS)
        exponent = make_exponent_integer(rng, exponent_length)
        return sign + integer + dot + fraction + exp + exponent


def make_random_numbers(count: int, length: int, seed: int) -> list[str]:
    rng = Random(seed)
    return [make_random_number(rng, length) for _ in range(count)]


def make_signed_str_number(rng: Random, length: int) -> str:
    value = make_str_number(rng, length)
    if value != "0" and rng.choice([True, False]):
        return "-" + value
    return value


def use_integer_only(use_fraction: bool, length: int) -> bool:
    return not use_fraction or length <= 2


def make_str_number(rng: Random, length: int) -> str:
    use_fraction = rng.choice([True, False])

    if use_integer_only(use_fraction, length):
        return make_integer(rng, length)

    dot = rng.choice(DOTS)
    digits_count = length - 1
    integer_length = rng.randint(1, digits_count - 1)
    fraction_length = digits_count - integer_length
    integer = make_integer(rng, integer_length)
    fraction = make_digits(rng, fraction_length)
    return integer + dot + fraction


def to_decimal(value: str | Nan | Infinity | BigFloat) -> Decimal:
    if is_nan(value):
        return Decimal("NaN")
    if is_infinity(value):
        return Decimal("Infinity") if value.sign > 0 else Decimal("-Infinity")
    if isinstance(value, BigFloat):
        return Decimal(bigfloat_string(value))
    if isinstance(value, Decimal):
        return Decimal("0") if value.is_zero() else value
    return Decimal(str(value).replace(",", "."))


def bigfloat_decimal(value: BigFloat) -> Decimal:
    sign = 1 if get_sign(value) < 0 else 0
    digits = tuple(int(digit) for digit in get_mantiss(value))
    exponent = get_exp10(value)
    return Decimal((sign, digits, exponent))


def make_coefs_bigfloat(a: str, b: str, c: str):
    from solver.models import Coefs
    return Coefs(create_BigFloat(a), create_BigFloat(b), create_BigFloat(c))


def make_coefs_decimal(a: str, b: str, c: str):
    from solver.models import Coefs
    return Coefs(to_decimal(a), to_decimal(b), to_decimal(c))


def make_signed_random_pairs(rng: Random, count_test: int, length: int) -> list[tuple[str, str]]:
    pairs = []
    for _ in range(count_test):
        left = make_signed_str_number(rng, length)
        right = make_signed_str_number(rng, length)
        pairs.append((left, right))
    return pairs
