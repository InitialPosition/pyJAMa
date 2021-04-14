from enum import Enum

from LDJAM_API.LDJAM_API import vote_theme
from util.ConsoleFunctions import clear_console, print_file


class VotingExitReason(Enum):
    USER_ABORTED = 0,
    GENERAL_ERROR = 1,
    NO_MORE_THEMES = 2


def start_general_voting(themes: dict, voted_themes: dict):
    clear_console()

    theme_count = len(themes) - len(voted_themes)
    current_theme_count = 1

    for theme in themes:

        # make voting pretty
        clear_console()
        print_file('files/logo.txt')
        print_file('files/voting_explanation.txt')
        print()

        # skip themes user already voted on
        if theme in voted_themes:
            continue

        theme_name = themes.get(theme)

        user_input = ''

        while user_input.upper() not in ['Y', 'N', 'F', 'C']:
            user_input = input(
                f'[{current_theme_count} / {theme_count}] Would this be a good theme: "{theme_name}"? [Y/N/F/C]: ')

            if user_input.upper() == 'C':
                return VotingExitReason.USER_ABORTED

            elif user_input.upper() == 'Y':
                vote_result = vote_theme(theme, 'yes')

                if vote_result != 0:
                    # there was an error posting vote
                    return VotingExitReason.GENERAL_ERROR

            elif user_input.upper() == 'N':
                vote_result = vote_theme(theme, 'no')

                if vote_result != 0:
                    # there was an error posting vote
                    return VotingExitReason.GENERAL_ERROR

            elif user_input.upper() == 'F':
                vote_result = vote_theme(theme, 'flag')

                if vote_result != 0:
                    # there was an error posting vote
                    return VotingExitReason.GENERAL_ERROR

            else:
                print('Invalid input. Please try again.')

        current_theme_count += 1

    return VotingExitReason.NO_MORE_THEMES
