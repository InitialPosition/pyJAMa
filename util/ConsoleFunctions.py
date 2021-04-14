from os import system, name as os_name


def clear_console():
    system('cls' if os_name == 'nt' else 'clear')


def print_file(file):
    with open(file, 'r') as f:
        for line in f.read().splitlines():
            print(line)
