from random import Random

import pytest

from input.interpreter import is_number


RANDOM_TESTS_COUNT = 100
RANDOM_SEED = 52152135
NUMBER_LENGTH = 10000

DIGITS = "0123456789"
NON_ZERO_DIGITS = "123456789"
DOTS = ".,"
SIGNS = "+-"
EXPS = "eE"


def make_digits(rng: Random, length):
    result = ""

    for _ in range(length):
        result += rng.choice(DIGITS)

    return result


def make_integer(rng: Random, length):
    if length == 1:
        return rng.choice(DIGITS)

    first_digit = rng.choice(NON_ZERO_DIGITS)
    other_digits = make_digits(rng, length - 1)

    return first_digit + other_digits


def make_signed_integer(rng: Random, length):
    if length == 1:
        return make_integer(rng, length)

    use_sign = rng.choice([True, False])

    if use_sign:
        sign = rng.choice(SIGNS)
        integer = make_integer(rng, length - 1)
        return sign + integer

    return make_integer(rng, length)

def make_exponent_integer(rng: Random, length):
    if length == 1:
        return rng.choice(NON_ZERO_DIGITS)

    use_sign = rng.choice([True, False])

    if use_sign:
        sign = rng.choice(SIGNS)
        integer = rng.choice(NON_ZERO_DIGITS) + make_digits(rng, length - 2)
        return sign + integer

    return rng.choice(NON_ZERO_DIGITS) + make_digits(rng, length - 1)

def make_random_number(rng: Random, length=NUMBER_LENGTH):
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

def make_random_numbers(count=RANDOM_TESTS_COUNT, length=NUMBER_LENGTH):
    rng = Random(RANDOM_SEED)
    numbers = []

    for _ in range(count):
        numbers.append(make_random_number(rng, length))

    return numbers


@pytest.mark.parametrize("value", [
    "0",
    "1",
    "9",
    "10",
    "123",
    "+123",
    "-123",
    "1.5",
    "1,5",
    "0.5",
    "0,5",
    ".5",
    ",5",
    "+.5",
    "-.5",
    "1e2",
    "1E2",
    "1e+2",
    "1e-2",
    "-1.5e+10",
    "+.5E-3",
    "1.23e+456",
])
def test_valid(value):
    assert is_number(value) is True


@pytest.mark.parametrize("value", [
    "",
    "+",
    "-",
    ".",
    ",",
    "01",
    "00",
    "0123",
    "+.",
    "-.",
    "e10",
    "1e",
    "1e+",
    "1e-",
    "abc",
    "1abc",
    "abc1",
    "1 2",
    "1.2.3",
    "-1-2-3",
])
def test_invalid(value):
    assert is_number(value) is False


@pytest.mark.parametrize("value", make_random_numbers())
def test_random_valid(value):
    assert len(value) == NUMBER_LENGTH
    assert is_number(value) is True
