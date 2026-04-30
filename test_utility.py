from random import Random, randint
from decimal import Decimal
from BigFloat import get_exp10, get_mantiss, get_sign

RANDOM_SEED = randint(1, 326432134)
RANDOM_PAIRS_COUNT = 100
RANDOM_NUMBER_LENGTH = 1000

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

def make_random_pairs(rng=Random(RANDOM_SEED), count_test = RANDOM_PAIRS_COUNT, length = RANDOM_NUMBER_LENGTH):
    pairs = []

    for _ in range(count_test):
        left = make_str_number(rng, length)
        right = make_str_number(rng, length)

        pairs.append((left, right))

    return pairs