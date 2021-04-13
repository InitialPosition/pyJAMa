from os import system, name as os_name


def clear_console():
    system('cls' if os_name == 'nt' else 'clear')
