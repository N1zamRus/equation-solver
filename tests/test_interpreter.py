from time import perf_counter

import pytest

from input.interpreter import is_number
from tests.test_utility import make_random_numbers


RANDOM_TESTS_COUNT = 1000
RANDOM_SEED = 412341
NUMBER_LENGTH = 10000

INTERPRETER_TIMES = []


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
    ". 1 1",
    "- 1 1",
    "1..2 0 0",
    "--1 0 0",
    "1-2 0 0",
    "1 . 1"
])
def test_invalid(value):
    assert is_number(value) is False


@pytest.mark.parametrize("value", make_random_numbers(RANDOM_TESTS_COUNT, NUMBER_LENGTH, RANDOM_SEED))
def test_random_valid(value):
    assert len(value) == NUMBER_LENGTH

    start = perf_counter()
    result = is_number(value)
    end = perf_counter()

    INTERPRETER_TIMES.append(end - start)
    assert result is True


@pytest.fixture(scope="module", autouse=True)
def print_average_time():
    yield

    if INTERPRETER_TIMES:
        avg = sum(INTERPRETER_TIMES) / len(INTERPRETER_TIMES)
        print(f"\nМаксимальное время is_number: {max(INTERPRETER_TIMES)}")
        print(f"\nСреднее время is_number: {avg:.8f} сек\n")
