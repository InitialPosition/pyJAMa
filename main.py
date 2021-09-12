import json
from os.path import isfile

from termcolor import cprint

from LDJAM_API.LDJAM_API import get_event_themes, get_current_event_id, get_user_votes
from LDJAM_API.Voting import start_general_voting, VotingExitReason, start_bulk_voting
from util.CONSTANTS import CONFIG_FILE
from util.Config import load_config, save_config, delete_config
from util.ConsoleFunctions import clear_console, print_file, print_version_info
from util.CookieFetch import get_cookie_firefox
from util.Updater import check_for_update, UpdateCheckResult, download_update


def main_menu():
    # update user votes and counts on return to main menu
    print('Fetching user votes...')
    user_votes = get_user_votes(event_id)

    unvoted_theme_count = len(themes) - len(user_votes)

    # default valid selections
    valid_selections = ['1', '2', '3']

    clear_console()

    # print logo and info
    print_file('files/logo.txt')
    print_version_info()

    print(f'\n{len(themes)} themes loaded.\nUnvoted themes: {max(0, unvoted_theme_count)}\n')

    # TODO implement proper final round voting
    if unvoted_theme_count < 0:
        # disable voting selections
        valid_selections.pop(0)
        valid_selections.pop(0)  # pop 0 again since every index moves once during first pop

        # print explanation
        print('This script currently does not support final theme voting rounds.\n')

    # if an update is available, say so and enable option to download update
    if update_check_result == UpdateCheckResult.UPDATE_AVAILABLE:
        cprint(f'NEW VERSION AVAILABLE: {new_update_version}\n'
               f'Changelog: https://github.com/InitialPosition/pyJAMa/releases/tag/v{new_update_version}\n', 'white',
               'on_green')
        valid_selections.append('4')

    # print default main menu
    print('[1] Start theme voting')
    print('[2] Start bulk theme voting')
    print('[3] Exit')

    if update_check_result == UpdateCheckResult.UPDATE_AVAILABLE:
        print('[4] Download Update')

    print()

    # get user selection
    selection = input('Selection > ')

    # make sure selection is valid
    while selection not in valid_selections:
        print('Invalid selection. Try again.')
        selection = input('Selection > ')

    # start normal voting mode
    if selection == '1':
        voting_result = start_general_voting(themes, user_votes)

        # reopen main menu if user typed c or no themes are left
        if voting_result == VotingExitReason.USER_ABORTED or voting_result == VotingExitReason.NO_MORE_THEMES:
            main_menu()

        # handle error
        if voting_result == VotingExitReason.GENERAL_ERROR:
            # voting failed for some reason. abort and tell the user
            clear_console()

            cprint('An error occurred during the voting process. This probably means the API is overloaded or you lost '
                   'internet connection.',
                   'red')
            cprint('The program will now terminate. Check your internet connection and try again. If voting still fails'
                   ', wait a few minutes and try again.', 'red')

            exit(0)

    # start bulk voting mode
    if selection == '2':
        voting_result = start_bulk_voting(themes, user_votes)

        # reopen main menu if user typed c or no themes are left
        if voting_result == VotingExitReason.USER_ABORTED or voting_result == VotingExitReason.NO_MORE_THEMES:
            main_menu()

        # handle error
        if voting_result == VotingExitReason.GENERAL_ERROR:
            # voting failed for some reason. abort and tell the user
            clear_console()

            cprint(
                'An error occurred during the voting process. This probably means the API is overloaded or you lost '
                'internet connection.',
                'red')
            cprint(
                'The program will now terminate. Check your internet connection and try again. If voting still fails'
                ', wait a few minutes and try again.', 'red')

            exit(0)

    # exit program
    if selection == '3':
        print('Goodbye. Keep jamming!')
        exit(0)

    # download and apply update (this is only accessible if an update is actually available)
    if selection == '4':
        download_update(new_update_version)
        exit(0)


def cookie_setup():
    # try to load cookies automatically
    cookie_fetch = get_cookie_firefox()

    if cookie_fetch != -1:
        print(f'Cookie retrieved: {cookie_fetch}')
        save_config(cookie_fetch)
        return

    clear_console()

    # print logo
    print_file('files/logo.txt')
    print_version_info()
    print()

    # explain why cookies are necessary
    print_file('files/cookie_explanation.txt')
    print()

    # get cookie input
    cookie_sids = input('SIDS > ')

    # treat empty input as deletion request, otherwise save new data
    if cookie_sids == '':
        delete_config()
        exit(0)
    else:
        save_config(cookie_sids)


# --- PROGRAM ENTRY POINT ---
# check for updates and save test result
print('Checking for updates...')
update_check_result, new_update_version = check_for_update()

if update_check_result == UpdateCheckResult.UPDATE_AVAILABLE:
    clear_console()
    print_file('files/logo.txt')
    cprint(f'\nNEW VERSION AVAILABLE: {new_update_version}\n'
           f'Changelog: https://github.com/InitialPosition/pyJAMa/releases/tag/v{new_update_version}\n', 'white',
           'on_green')

    update_now_selection = input('Update now? (Y: Yes, N: No) > ')
    if update_now_selection.upper() == 'Y':
        download_update(new_update_version)
        exit()

# if a config exists, load it
if isfile(CONFIG_FILE):
    config_data = load_config()
else:
    cookie_setup()

# get the event id for currently running LDJAM event
print('Fetching current event ID...')
event_id = get_current_event_id()

# get all themes that were submitted
print('Fetching themes...')
request = get_event_themes(event_id)
themes = None
jsonified_themes = json.loads(request.text)

if jsonified_themes['status'] == 200:
    themes = jsonified_themes["ideas"]
else:

    # if we land here, the API was not happy with our theme request, meaning something is most likely wrong with the
    # entered cookies. we delete the cookies and let the user enter them again.
    clear_console()

    cprint('There was a problem fetching themes. This indicates there might be a problem with your token.', 'red')
    cprint('The program will now exit. If you have Firefox installed, make sure you are logged in on '
           'https://ldjam.com/ .',
           'red')
    cprint('If you are, you might want to log out and back in once.',
           'red')

    print()
    print('DEBUG INFO:')
    print(jsonified_themes)
    print()

    delete_config()

    exit(0)

# prep work done, show main menu
main_menu()
