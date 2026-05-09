import subprocess
import sys


# Строка, по которой мы определяем, что это строка с таймингом
TIMING_PREFIX = 'Среднее время'

# Файл, в который сохраняем все результаты
OUTPUT_FILE = 'all_tests.txt'


def is_timing_line(line):
    # Проверяем, является ли строка строкой с таймингом
    return line.startswith(TIMING_PREFIX)


def run_pytest():
    # Запускаем pytest как отдельную программу и читаем её вывод построчно.
    # '-v' — подробный вывод (verbose)
    # '-s' — показывать print() из тестов
    process = subprocess.Popen(
        [sys.executable, '-m', 'pytest', 'tests/', '-v', '-s'],
        stdout=subprocess.PIPE,   # перехватываем вывод программы
        stderr=subprocess.STDOUT, # ошибки тоже направляем в stdout
        text=True,
        encoding='utf-8',
        bufsize=1,                # читаем построчно, без задержки
    )
    return process


def collect_output(process):
    # Читаем вывод pytest построчно.
    # Строки с таймингом откладываем отдельно, остальные сразу печатаем.
    regular_lines = []
    timing_lines = []

    for line in process.stdout:
        if is_timing_line(line):
            timing_lines.append(line)
        else:
            print(line, end='')       # сразу показываем в терминале
            regular_lines.append(line)

    return regular_lines, timing_lines


def print_timing_section(timing_lines):
    # Печатаем все тайминги отдельным блоком в самом конце
    separator = '\n' + '=' * 40 + ' Среднее время ' + '=' * 40 + '\n'
    print(separator)
    for line in timing_lines:
        print(line, end='')


def save_to_file(regular_lines, timing_lines):
    # Собираем все строки вместе и записываем в файл
    separator = '\n' + '=' * 40 + ' Среднее время ' + '=' * 40 + '\n'
    all_lines = regular_lines + [separator] + timing_lines

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
        file.writelines(all_lines)

    print(f'\nРезультаты сохранены в {OUTPUT_FILE}')


def main():
    process = run_pytest()
    regular_lines, timing_lines = collect_output(process)

    if timing_lines:
        print_timing_section(timing_lines)

    save_to_file(regular_lines, timing_lines)


if __name__ == '__main__':
    main()
