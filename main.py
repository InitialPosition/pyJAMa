import json
from os.path import isfile

from LDJAM_API.LDJAM_API import get_event_themes, get_current_event_id
from util.CONSTANTS import CONFIG_FILE
from util.Config import load_config, save_config
from util.ConsoleFunctions import clear_console


def print_file(file):
    with open(file, 'r') as f:
        for line in f.read().splitlines():
            print(line)


def main_menu():
    print('[1] Start theme voting')
    print('[2] Start bulk theme voting')
    print('[3] Cookie setup')
    print('[4] Exit')
    print()

    selection = input('Selection > ')


def cookie_setup():
    clear_console()

    print_file('files/logo.txt')
    print()

    print_file('files/cookie_explanation.txt')
    print()

    cookie_cfduid = input('__cfduid > ')
    cookie_sids = input('SIDS > ')

    save_config(cookie_cfduid, cookie_sids)


# if a config exists, load it
if isfile(CONFIG_FILE):
    config_data = load_config()
else:
    cookie_setup()

print('Fetching current event ID...')
event_id = get_current_event_id()

print('Fetching themes...')
request = get_event_themes(event_id)

jsonified = json.loads(request.text)
# print(jsonified)
themes = jsonified["ideas"]

clear_console()

# print logo
print_file('files/logo.txt')

print(f'\n{len(themes)} themes loaded.\n')

main_menu()
