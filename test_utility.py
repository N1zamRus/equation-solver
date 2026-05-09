from random import Random, randint
from decimal import Decimal
from BigFloat import BigFloat, get_exp10, get_mantiss, get_sign, bigfloat_string
from models import ComplexBigFloat, ComplexDecimal, get_x1, get_x2, get_real, get_imag

PREFIX_LEN = 10000
FORMAT_DIGITS = 10010

RANDOM_SEED = randint(1, 326432134)
RANDOM_PAIRS_COUNT = 100
RANDOM_NUMBER_LENGTH = 1000

def make_signed_str_number(rng: Random, length):
    value = make_str_number(rng, length)

    if value != "0" and rng.choice([True, False]):
        return "-" + value

    return value

def make_str_number(rng: Random, length):
    from test_interpreter import make_integer, DOTS, make_digits

    use_fraction = rng.choice([True, False])

    if not use_fraction or length <= 2:
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

def make_signed_random_pairs(rng: Random, count_test, length):
    pairs = []

    for _ in range(count_test):
        left = make_signed_str_number(rng, length)
        right = make_signed_str_number(rng, length)
        pairs.append((left, right))

    return pairs


def format_decimal(value: Decimal) -> str:
    return f'{value:.{FORMAT_DIGITS}f}'


ZERO_STR = '0.' + '0' * (PREFIX_LEN - 2)


def imag_is_zero(imag: Decimal) -> bool:
    return format_decimal(abs(imag))[:PREFIX_LEN] == ZERO_STR


def normalize_root(root):
    if root[0] == 'complex' and imag_is_zero(root[2]):
        return ('real', root[1])
    return root


def any_decimal(value):
    if isinstance(value, BigFloat):
        return bigfloat_decimal(value)
    return value


def solution_to_roots(solution) -> list | str:
    name = solution.solv_type.name

    if name == 'INFINITE_SOLUTION':
        return 'infinite'
    if name == 'NO_SOLUTION':
        return 'none'

    roots = []
    for value in (get_x1(solution), get_x2(solution)):
        if value is None:
            continue
        if isinstance(value, (ComplexBigFloat, ComplexDecimal)):
            roots.append(('complex',any_decimal(get_real(value)),
                                    any_decimal(get_imag(value))
                        ))
        else:
            roots.append(('real', any_decimal(value)))

    return roots


def root_matches(actual, expected) -> bool:
    actual = normalize_root(actual)
    expected = normalize_root(expected)

    if actual[0] != expected[0]:
        return False

    if actual[0] == 'real':
        if actual[1] == 0 and expected[1] == 0:
            return True
        return format_decimal(actual[1])[:PREFIX_LEN] == format_decimal(expected[1])[:PREFIX_LEN]

    return (
        format_decimal(actual[1])[:PREFIX_LEN] == format_decimal(expected[1])[:PREFIX_LEN]
        and format_decimal(actual[2])[:PREFIX_LEN] == format_decimal(expected[2])[:PREFIX_LEN]
    )


def root_string(root) -> str:
    root = normalize_root(root)
    
    if root[0] == 'real':
        return format_decimal(root[1])[:PREFIX_LEN]
    
    real = format_decimal(root[1])[:PREFIX_LEN]
    imag = format_decimal(root[2])[:PREFIX_LEN]
    return f"{real}+{imag}i"


def roots_match(actual_roots, expected_roots) -> bool:
    if isinstance(actual_roots, str) or isinstance(expected_roots, str):
        return actual_roots == expected_roots

    if len(actual_roots) != len(expected_roots):
        return False

    actual_strings   = sorted(root_string(r) for r in actual_roots)
    expected_strings = sorted(root_string(r) for r in expected_roots)
    
    return actual_strings == expected_strings


def assert_roots_equal(actual, expected):
    assert roots_match(actual, expected)