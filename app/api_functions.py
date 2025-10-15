'''API functions'''

import json
import requests as req

API_URL = 'https://api.opendota.com/api/'
LARGE_MATCH_ID = 10**12


def get_100_match_ids_lower_than_n(
        first_match_id: int = LARGE_MATCH_ID) -> list[int]:
    '''gets 100 match ids from open dota which is a limit'''
    matches = json.loads(
        req.get(API_URL + 'parsedMatches',
                params={
                    'less_than_match_id': first_match_id
                },
                timeout=1).text)
    return [el['match_id'] for el in matches]


def get_m_matches_lower_than_n(
        number_of_matches: int,
        first_match_id: int = LARGE_MATCH_ID) -> list[int]:
    '''number of matches should be divisible by 100'''
    match_ids = []
    for _ in range(number_of_matches // 100):
        match_ids.extend(get_100_match_ids_lower_than_n(first_match_id))
        first_match_id = match_ids[-1]
    return match_ids


def get_match_info(match_id: int) -> dict:
    '''gets match info'''
    match = json.loads(
        req.get(API_URL + f'matches/{match_id}', timeout=1).text)
    return match


def write_match_ids_to_file(match_ids: list[int], filename: str) -> None:
    '''write ids to file'''
    with open('app/' + filename, 'w', encoding='utf-8') as file:
        file.write(json.dumps(match_ids))


def get_and_write_match_ids_to_file(number_of_matches: int,
                                    filename: str) -> None:
    '''gets and writes ids to file'''
    match_ids = get_m_matches_lower_than_n(number_of_matches)
    write_match_ids_to_file(match_ids, filename)
