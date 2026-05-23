import subprocess
import sys


TIMING_PREFIXES = ("Среднее время", "Максимальное время")

OUTPUT_FILE = "all_tests.txt"


def is_timing_line(line: str) -> bool:
    return any(prefix in line for prefix in TIMING_PREFIXES)


def run_pytest() -> subprocess.Popen:
    process = subprocess.Popen(
        [sys.executable, "-m", "pytest", "tests/", "-v", "-s"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8", #cp1251
        bufsize=1,
    )
    return process


def collect_output(process: subprocess.Popen) -> tuple[list[str], list[str], list[str]]:
    regular_lines = []
    timing_lines = []

    for line in process.stdout:
        if is_timing_line(line):
            timing_lines.append(line)
        else:
            print(line, end="")
            regular_lines.append(line)

    error_lines = process.stderr.readlines()

    return regular_lines, timing_lines, error_lines


def print_timing_section(timing_lines: list[str]) -> None:
    separator = "\n" + "=" * 40 + " Время " + "=" * 40 + "\n"
    print(separator)
    for line in timing_lines:
        print(line, end="")


def save_to_file(regular_lines: list[str], timing_lines: list[str], error_lines: list[str]) -> None:
    error_separator = "\n" + "=" * 40 + " Ошибки " + "=" * 40 + "\n"
    timing_separator = "\n" + "=" * 40 + " Время " + "=" * 40 + "\n"
    all_lines = regular_lines + [timing_separator] + timing_lines + [error_separator] + error_lines

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.writelines(all_lines)


def main() -> None:
    process = run_pytest()
    regular_lines, timing_lines, error_lines = collect_output(process)

    if timing_lines:
        print_timing_section(timing_lines)

    if error_lines:
        print("\n" + "=" * 40 + " Ошибки " + "=" * 40)
        for line in error_lines:
            print(line, end="")

    save_to_file(regular_lines, timing_lines, error_lines)

if __name__ == "__main__":
    main()
    # .\.venv\Scripts\Activate.ps1