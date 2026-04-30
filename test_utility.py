from random import Random
from decimal import Decimal
from BigFloat import get_exp10, get_mantiss, get_sign

def make_str_number(rng: Random, length):
    from test_interpreter import make_integer, DOTS, make_digits

    use_fraction = rng.choice([True, False])

    if not use_fraction or length <= 1:
        return make_integer(rng, length)

    dot = rng.choice(DOTS)

    digits_count = length - 1
    integer_length = rng.randint(1, digits_count - 1)
    fraction_length = digits_count - integer_length

    integer = make_integer(rng, integer_length)
    fraction = make_digits(rng, fraction_length)

    return integer + dot + fraction

def to_decimal(value):
    return Decimal(str(value).replace(",", "."))

def bigfloat_decimal(value):
    sign = 1 if get_sign(value) < 0 else 0
    digits = tuple(int(digit) for digit in get_mantiss(value))
    exponent = get_exp10(value)

    return Decimal((sign, digits, exponent))