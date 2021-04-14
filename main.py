import json
from os.path import isfile

from termcolor import cprint

from LDJAM_API.LDJAM_API import get_event_themes, get_current_event_id, get_user_votes
from LDJAM_API.Voting import start_general_voting, VotingExitReason, start_bulk_voting
from util.CONSTANTS import CONFIG_FILE
from util.Config import load_config, save_config, delete_config
from util.ConsoleFunctions import clear_console, print_file, print_version_info


def main_menu():
    print('Fetching user votes...')
    user_votes = get_user_votes(event_id)

    unvoted_theme_count = len(themes) - len(user_votes)

    clear_console()

    # print logo
    print_file('files/logo.txt')
    print_version_info()

    print(f'\n{len(themes)} themes loaded.\nUnvoted themes: {unvoted_theme_count}\n')

    print('[1] Start theme voting')
    print('[2] Start bulk theme voting')
    print('[3] Cookie setup')
    print('[4] Exit')
    print()

    selection = input('Selection > ')

    while selection not in ['1', '2', '3', '4']:
        print('Invalid selection. Try again.')
        selection = input('Selection > ')

    if selection == '1':
        voting_result = start_general_voting(themes, user_votes)

        if voting_result == VotingExitReason.USER_ABORTED:
            main_menu()

    if selection == '2':
        voting_result = start_bulk_voting(themes, user_votes)

        if voting_result == VotingExitReason.USER_ABORTED:
            main_menu()

    if selection == '3':
        cookie_setup(False)

    if selection == '4':
        print('Goodbye. Keep jamming!')
        exit(0)


def cookie_setup(first_time: bool = True):
    clear_console()

    print_file('files/logo.txt')
    print_version_info()
    print()

    if first_time:
        print_file('files/cookie_explanation.txt')

    else:
        print_file('files/cookie_reset.txt')

    print()

    cookie_cfduid = input('__cfduid > ')
    cookie_sids = input('SIDS > ')

    if cookie_cfduid == '' and cookie_sids == '':
        delete_config()
    else:
        save_config(cookie_cfduid, cookie_sids)

    if first_time is False:
        main_menu()


# if a config exists, load it
if isfile(CONFIG_FILE):
    config_data = load_config()
else:
    cookie_setup()

print('Fetching current event ID...')
event_id = get_current_event_id()

print('Fetching themes...')
request = get_event_themes(event_id)
themes = None
jsonified_themes = json.loads(request.text)

# print(jsonified)
if jsonified_themes['status'] == 200:
    themes = jsonified_themes["ideas"]
else:
    clear_console()

    cprint('There was a problem fetching themes. This indicates there might be a problem with your tokens.', 'red')
    cprint('The program will now terminate. It will ask you to re-enter your tokens on next startup.', 'red')

    delete_config()

    exit(0)

main_menu()
