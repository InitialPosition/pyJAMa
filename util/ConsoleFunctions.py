from os import system, name as os_name

from util.CONSTANTS import VERSION, AUTHOR


def clear_console():
    system('cls' if os_name == 'nt' else 'clear')


def print_file(file):
    with open(file, 'r', encoding='utf8') as f:
        for line in f.read().splitlines():
            print(line)


def print_version_info():
    print(f'v{VERSION}, made by {AUTHOR}')
