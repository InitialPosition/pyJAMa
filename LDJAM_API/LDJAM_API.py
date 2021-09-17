import json

from requests import get
from requests.exceptions import ConnectionError as RequestConnectionError
from urllib3.exceptions import NewConnectionError

from util.Config import load_config


def get_cookie_header():
    # load data from local config
    cookie_data = load_config()

    cookie1 = cookie_data.get('SIDS')

    # build header in correct format
    header = {'Cookie': f'SIDS={cookie1}'}

    return header


def get_event_themes(event_id: int):
    # call ldjam API to get all running events themes
    header = get_cookie_header()
    call_url = f'https://api.ldjam.com/vx/theme/idea/vote/get/{event_id}'

    request = get(call_url, headers=header)

    return request


def get_current_event_id():
    # call ldjam API to get running events ID (this call doesnt need auth headers)
    call_url = 'https://api.ldjam.com/vx/node2/what/1'
    request = get(call_url)

    request_json = json.loads(request.text)

    # if we got an answer, extract event ID and return, otherwise abort
    if request_json['status'] == 200:
        event_id = request_json.get('featured').get('id')

        print(f'done. ID: {event_id}')
        return event_id
    else:
        print('ERROR! Could not fetch current LDJAM ID. Aborting...')
        exit(0)


def get_user_votes(event_id: int):
    # call ldjam API to get all themes the user already voted on
    header = get_cookie_header()
    call_url = f'https://api.ldjam.com/vx/theme/idea/vote/getmy/{event_id}'

    request = get(call_url, headers=header)

    request_json = json.loads(request.text)

    # if we got an answer, extract voted themes and return, otherwise abort
    if request_json['status'] == 200:
        user_votes = request_json.get('votes')

        return user_votes
    else:
        try:
            if request_json['message'] == 'Event is not Slaughtering':
                print('Theme slaughter has not begun yet! Please try again later.')
                exit(0)

        except KeyError:
            print('ERROR! Could not fetch user votes. Aborting...')
            exit(0)

        print('ERROR! Could not fetch user votes. Aborting...')
        exit(0)


def vote_theme(theme_id: int, voting: str):
    # call ldjam API to vote on given theme ID with the given voting string
    header = get_cookie_header()

    try:
        request = get(f'https://api.ldjam.com/vx/theme/idea/vote/{voting}/{theme_id}', headers=header)

    except RequestConnectionError:
        return -1
    except NewConnectionError:
        return -1

    request_json = json.loads(request.text)

    # return whether vote was successful
    if request_json['status'] == 200:
        return 0

    return -1
