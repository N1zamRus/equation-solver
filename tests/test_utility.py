from random import Random, randint
from decimal import Decimal
from core.BigFloat import BigFloat, get_exp10, get_mantiss, get_sign, bigfloat_string
from core.Special_values import (
    Nan,
    Infinity,
    is_nan,
    is_infinity
)

RANDOM_SEED = randint(1, 326432134)
RANDOM_PAIRS_COUNT = 100
RANDOM_NUMBER_LENGTH = 1000


def make_signed_str_number(rng: Random, length: int) -> str:
    value = make_str_number(rng, length)

    if value != "0" and rng.choice([True, False]):
        return "-" + value

    return value


def use_integer_only(use_fraction: bool, length: int) -> bool:
    return not use_fraction or length <= 2


def make_str_number(rng: Random, length: int) -> str:
    from tests.test_interpreter import make_integer, DOTS, make_digits

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
        return Decimal('NaN')
    if is_infinity(value):
        return Decimal('Infinity') if value.sign > 0 else Decimal('-Infinity')
    if isinstance(value, BigFloat):
        return Decimal(bigfloat_string(value))
    return Decimal(str(value).replace(",", "."))


def bigfloat_decimal(value: BigFloat) -> Decimal:
    sign = 1 if get_sign(value) < 0 else 0
    digits = tuple(int(digit) for digit in get_mantiss(value))
    exponent = get_exp10(value)

    return Decimal((sign, digits, exponent))


def make_signed_random_pairs(rng: Random, count_test: int, length: int) -> list[tuple[str, str]]:
    pairs = []

    for _ in range(count_test):
        left = make_signed_str_number(rng, length)
        right = make_signed_str_number(rng, length)
        pairs.append((left, right))

    return pairs