import json

from requests import get

from util.Config import load_config


def get_cookie_header():
    cookie_data = load_config()

    cookie1 = cookie_data.get('__cfduid')
    cookie2 = cookie_data.get('SIDS')

    header = {'Cookie': f'__cfduid={cookie1}; SIDS={cookie2}'}

    return header


def get_event_themes(event_id: int):
    header = get_cookie_header()
    call_url = f'https://api.ldjam.com/vx/theme/idea/vote/get/{event_id}'

    request = get(call_url, headers=header)

    return request


def get_current_event_id():
    print('Fetching LDJAM event ID...')

    call_url = 'https://api.ldjam.com/vx/node2/what/1'
    request = get(call_url)

    request_json = json.loads(request.text)

    if request_json['status'] == 200:
        event_id = request_json.get('featured').get('id')

        print(f'done. ID: {event_id}')
        return event_id
    else:
        print('ERROR! Could not fetch current LDJAM ID. Aborting...')
        exit(0)


def get_user_votes(event_id: int):
    header = get_cookie_header()
    call_url = f'https://api.ldjam.com/vx/theme/idea/vote/getmy/{event_id}'

    request = get(call_url, headers=header)

    request_json = json.loads(request.text)

    if request_json['status'] == 200:
        user_votes = request_json.get('votes')

        return user_votes
    else:
        print('ERROR! Could not fetch user votings. Aborting...')
        exit(0)


def vote_theme(theme_id: int, voting: str):
    header = get_cookie_header()
    request = get(f'https://api.ldjam.com/vx/theme/idea/vote/{voting}/{theme_id}', headers=header)

    request_json = json.loads(request.text)

    if request_json['status'] == 200:
        return 0

    return -1


def flag_theme(theme_id: int):
    print('TODO vote flag')
