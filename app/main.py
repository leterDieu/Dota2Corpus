import requests as req
import json


API_URL = 'https://api.opendota.com/api/'


def get_match_ids_lower_than_n(n: int) -> list[int]:
    matches = json.loads(req.get(
        API_URL + 'parsedMatches',
        params={'less_than_match_id': n}).text)
    return [el['match_id'] for el in matches]

def get_match_info(match_id: int) -> dict:
    match = json.loads(req.get(API_URL + f'matches/{match_id}').text)
    return match

def get_match_chat(match_id: int) -> list:
    chat = get_match_info(match_id)['chat']
    chat_messages = []
    for entry in chat:
        if entry['type'] == 'chat':
            chat_messages.append(entry)

    return chat_messages
