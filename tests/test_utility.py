from random import Random, randint
from decimal import Decimal
from core.BigFloat import BigFloat, get_exp10, get_mantiss, get_sign, bigfloat_string
from solver.models import ComplexBigFloat, ComplexDecimal, get_x1, get_x2, get_real, get_imag

PREFIX_LEN = 10000
FORMAT_DIGITS = 10010

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


def to_decimal(value: str) -> Decimal:
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


def format_decimal(value: Decimal) -> str:
    return f'{value:.{FORMAT_DIGITS}f}'


ZERO_STR = '0.' + '0' * (PREFIX_LEN - 2)


def imag_is_zero(imag: Decimal) -> bool:
    return format_decimal(abs(imag))[:PREFIX_LEN] == ZERO_STR


def normalize_root(root: tuple) -> tuple:
    if root[0] == 'complex' and imag_is_zero(root[2]):
        return ('real', root[1])
    return root


def any_decimal(value: BigFloat | Decimal) -> Decimal:
    if isinstance(value, BigFloat):
        return bigfloat_decimal(value)
    return value


def check_special_case(solution) -> str | None:
    name = solution.solv_type.name

    if name == 'INFINITE_SOLUTION':
        return 'infinite'
    if name == 'NO_SOLUTION':
        return 'none'

    return None


def root_to_tuple(value) -> tuple:
    if isinstance(value, (ComplexBigFloat, ComplexDecimal)):
        return ('complex', any_decimal(get_real(value)), any_decimal(get_imag(value)))
    return ('real', any_decimal(value))


def solution_to_roots(solution) -> list | str:
    special = check_special_case(solution)
    if special is not None:
        return special

    roots = []
    for value in (get_x1(solution), get_x2(solution)):
        if value is None:
            continue
        roots.append(root_to_tuple(value))

    return roots


def same_root_type(actual: tuple, expected: tuple) -> bool:
    return actual[0] == expected[0]


def compare_real_roots(actual: tuple, expected: tuple) -> bool:
    if actual[1] == 0 and expected[1] == 0:
        return True
    return format_decimal(actual[1])[:PREFIX_LEN] == format_decimal(expected[1])[:PREFIX_LEN]


def compare_complex_roots(actual: tuple, expected: tuple) -> bool:
    return (
        format_decimal(actual[1])[:PREFIX_LEN] == format_decimal(expected[1])[:PREFIX_LEN]
        and format_decimal(actual[2])[:PREFIX_LEN] == format_decimal(expected[2])[:PREFIX_LEN]
    )


def root_matches(actual: tuple, expected: tuple) -> bool:
    actual = normalize_root(actual)
    expected = normalize_root(expected)

    if not same_root_type(actual, expected):
        return False

    if actual[0] == 'real':
        return compare_real_roots(actual, expected)

    return compare_complex_roots(actual, expected)


def root_string(root: tuple) -> str:
    root = normalize_root(root)

    if root[0] == 'real':
        return format_decimal(root[1])[:PREFIX_LEN]

    real = format_decimal(root[1])[:PREFIX_LEN]
    imag = format_decimal(root[2])[:PREFIX_LEN]
    return f"{real}+{imag}i"


def is_special_case(roots: list | str) -> bool:
    return isinstance(roots, str)


def same_roots_count(actual_roots: list, expected_roots: list) -> bool:
    return len(actual_roots) == len(expected_roots)


def sort_roots_strings(roots: list) -> list[str]:
    return sorted(root_string(r) for r in roots)


def roots_match(actual_roots: list | str, expected_roots: list | str) -> bool:
    if is_special_case(actual_roots) or is_special_case(expected_roots):
        return actual_roots == expected_roots

    if not same_roots_count(actual_roots, expected_roots):
        return False

    return sort_roots_strings(actual_roots) == sort_roots_strings(expected_roots)


def assert_roots_equal(actual: list | str, expected: list | str) -> None:
    assert roots_match(actual, expected)