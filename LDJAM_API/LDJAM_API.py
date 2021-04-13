from requests import get
import json


def get_event_themes(event_id: int):
    # TODO read header from config file
    header = {}
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
