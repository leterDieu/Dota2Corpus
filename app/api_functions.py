import requests as req
import json


API_URL = 'https://api.opendota.com/api/'
large_match_id = 10 ** 12


def get_100_match_ids_lower_than_n(first_match_id: int = large_match_id) -> list[int]:
    matches = json.loads(req.get(
        API_URL + 'parsedMatches',
        params={'less_than_match_id': first_match_id}).text)
    return [el['match_id'] for el in matches]

def get_m_matches_lower_than_n(number_of_matches: int, first_match_id: int = large_match_id) -> list[int]:
    '''number of matches should be divisible by 100'''
    match_ids = []
    for _ in range(number_of_matches // 100):
        match_ids.extend(get_100_match_ids_lower_than_n(first_match_id))
        first_match_id = match_ids[-1]
    return match_ids

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

def write_match_ids_to_file(match_ids: list[int], filename: str) -> None:
    with open('app/' + filename, 'w', encoding='utf-8') as file:
        file.write(json.dumps(match_ids))
    return None
    
def get_and_write_match_ids_to_file(number_of_matches: int, filename: str) -> None:
    match_ids = get_m_matches_lower_than_n(number_of_matches)
    write_match_ids_to_file(match_ids, filename)
    return None