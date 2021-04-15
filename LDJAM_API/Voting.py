from enum import Enum
from time import sleep

from LDJAM_API.LDJAM_API import vote_theme
from util.ConsoleFunctions import clear_console, print_file


class VotingExitReason(Enum):
    USER_ABORTED = 0,
    GENERAL_ERROR = 1,
    NO_MORE_THEMES = 2


def start_general_voting(themes: dict, voted_themes: dict):
    clear_console()

    # get the number of themes user still has to vote on
    theme_count = len(themes) - len(voted_themes)

    # current index to show voting progress
    current_theme_count = 1

    # loop through all themes
    for theme in themes:

        # make voting pretty
        clear_console()
        print_file('files/logo.txt')
        print_file('files/voting_explanation.txt')
        print()

        # skip themes user already voted on
        if theme in voted_themes:
            continue

        # get the actual theme from the theme ID
        theme_name = themes.get(theme)

        # (re) initialize user input
        user_input = ''

        # make sure user input is valid after showing theme
        while user_input.upper() not in ['Y', 'N', 'F', 'C']:
            user_input = input(
                f'[{current_theme_count} / {theme_count}] Would this be a good theme: "{theme_name}"? [Y/N/F/C] > ')

            # user requested cancel
            if user_input.upper() == 'C':
                return VotingExitReason.USER_ABORTED

            # user requested yes vote
            elif user_input.upper() == 'Y':
                vote_result = vote_theme(theme, 'yes')

                if vote_result != 0:
                    # there was an error posting vote
                    return VotingExitReason.GENERAL_ERROR

            # user requested no vote
            elif user_input.upper() == 'N':
                vote_result = vote_theme(theme, 'no')

                if vote_result != 0:
                    # there was an error posting vote
                    return VotingExitReason.GENERAL_ERROR

            # user requested flag vote
            elif user_input.upper() == 'F':
                vote_result = vote_theme(theme, 'flag')

                if vote_result != 0:
                    # there was an error posting vote
                    return VotingExitReason.GENERAL_ERROR

            # if no valid request was found at this point, it was invalid
            else:
                print('Invalid input. Please try again.')

        # increase theme counter
        current_theme_count += 1

    # out of themes, return with proper status code
    return VotingExitReason.NO_MORE_THEMES


def start_bulk_voting(themes: dict, voted_themes: dict):
    # array for themes we voted on while in the function
    local_voted_themes = []

    # init array for keyword matching themes
    keyword_themes = []

    while 1:
        # make voting pretty
        clear_console()
        print_file('files/logo.txt')
        print_file('files/bulk_voting_explanation.txt')
        print()

        # keyword input
        keyword = input('Keyword (Enter \'C\' to cancel) > ')

        # abort if user entered c or nothing
        if keyword == '':
            return VotingExitReason.USER_ABORTED

        if keyword.upper() == 'C':
            return VotingExitReason.USER_ABORTED

        print(f'Searching for themes containing "{keyword}"...')

        # clear keyword array
        keyword_themes.clear()

        # loop through all themes
        for theme in themes:

            # get the theme from theme ID
            theme_name = themes.get(theme)

            # skip already voted themes
            if theme in voted_themes:
                continue
            if theme in local_voted_themes:
                continue

            # add themes that match keyword
            if keyword.upper() in theme_name.upper():
                keyword_themes.append(theme)

        # if there are no themes in the keyword array, no themes matched the keyword
        if len(keyword_themes) == 0:
            print('\nThere are no unvoted themes matching your keyword.')
            sleep(3)
            continue

        print(f'Found {len(keyword_themes)} themes.')

        # assign indices to found themes to allow select voting
        theme_index = 0

        for theme in keyword_themes:
            theme_index += 1
            print(f'[{theme_index}] {themes.get(theme)}')

        # get user input
        user_input = input('What do you want to do? [Y/N/C] > ')

        # make sure input is valid
        if (user_input.upper().startswith('Y') or user_input.upper().startswith('N') or user_input.upper().startswith(
                'C')) is False:
            continue

        # cancel if user typed c
        if user_input.upper() == 'C':
            return VotingExitReason.USER_ABORTED

        # we are voting yes
        elif user_input.upper().startswith('Y'):

            input_split = user_input.upper().split(' ')

            theme_index = 0

            for theme in keyword_themes:

                theme_index += 1

                # if no numbers provided, yes vote all themes. otherwise, vote yes if index is in input list.
                if (len(input_split) > 1 and str(theme_index) in input_split[1:]) or len(input_split) == 1:
                    print(f'Voting YES on theme "{themes.get(theme)}"')
                    vote_result = vote_theme(theme, 'yes')

                    if vote_result != 0:
                        # there was an error posting vote
                        return VotingExitReason.GENERAL_ERROR

                    # add theme to local voted array so it gets removed on successive searches
                    local_voted_themes.append(theme)

                    # sleep for 1 second to give the API some breathing room
                    sleep(1)

        # same as yes but actually no
        elif user_input.upper().startswith('N'):
            input_split = user_input.upper().split(' ')

            theme_index = 0

            for theme in keyword_themes:

                theme_index += 1

                if (len(input_split) > 1 and str(theme_index) in input_split[1:]) or len(input_split) == 1:
                    print(f'Voting NO on theme "{themes.get(theme)}"')
                    vote_result = vote_theme(theme, 'no')

                    if vote_result != 0:
                        # there was an error posting vote
                        return VotingExitReason.GENERAL_ERROR

                    local_voted_themes.append(theme)
                    sleep(1)
