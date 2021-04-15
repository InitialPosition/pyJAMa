import json
from os.path import isfile
from webbrowser import open as web_open

from termcolor import cprint

from LDJAM_API.LDJAM_API import get_event_themes, get_current_event_id, get_user_votes
from LDJAM_API.Voting import start_general_voting, VotingExitReason, start_bulk_voting
from util.CONSTANTS import CONFIG_FILE
from util.Config import load_config, save_config, delete_config
from util.ConsoleFunctions import clear_console, print_file, print_version_info
from util.Updater import check_for_update, UpdateCheckResult


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

    print(f'\n{len(themes)} themes loaded.\nUnvoted themes: {unvoted_theme_count}\n')

    # if an update is available, say so and enable option to open web browser
    if update_check_result == UpdateCheckResult.UPDATE_AVAILABLE:
        print('UPDATE AVAILABLE!\n')
        valid_selections.append('4')

    # print default main menu
    print('[1] Start theme voting')
    print('[2] Start bulk theme voting')
    print('[3] Exit')

    if update_check_result == UpdateCheckResult.UPDATE_AVAILABLE:
        print('[4] Open update page')

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

        # reopen main menu if user typed c
        if voting_result == VotingExitReason.USER_ABORTED:
            main_menu()

    # start bulk voting mode
    if selection == '2':
        voting_result = start_bulk_voting(themes, user_votes)

        # reopen main menu if user typed c
        if voting_result == VotingExitReason.USER_ABORTED:
            main_menu()

    # exit program
    if selection == '3':
        print('Goodbye. Keep jamming!')
        exit(0)

    # open update page in new tab (this is only accessible if an update is actually available)
    if selection == '4':
        web_open('https://github.com/InitialPosition/pyJAMa/releases', new=2)
        exit(0)


def cookie_setup():
    clear_console()

    # print logo
    print_file('files/logo.txt')
    print_version_info()
    print()

    # explain why cookies are necessary
    print_file('files/cookie_explanation.txt')
    print()

    # get cookie input
    cookie_cfduid = input('__cfduid > ')
    cookie_sids = input('SIDS > ')

    # treat empty input as deletion request, otherwise save new data
    if cookie_cfduid == '' and cookie_sids == '':
        delete_config()
        exit(0)
    else:
        save_config(cookie_cfduid, cookie_sids)


# --- PROGRAM ENTRY POINT ---
# check for updates and save test result
print('Checking for updates...')
update_check_result = check_for_update()

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

    cprint('There was a problem fetching themes. This indicates there might be a problem with your tokens.', 'red')
    cprint('The program will now terminate. It will ask you to re-enter your tokens on next startup.', 'red')

    delete_config()

    exit(0)

# prep work done, show main menu
main_menu()
