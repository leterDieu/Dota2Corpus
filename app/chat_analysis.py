'''only chat analysis. probably moving this to match class'''

import json
from api_functions import get_match_info

with open('./app/constants/chat_wheel.json', 'r', encoding='utf-8') as file:
    CHAT_WHEEL = json.load(file)


def get_refactored_chat(chat: list, key_offset_seconds: int = 2) -> list[dict]:
    '''get match chat'''
    chat_refactored = []
    merge_to_previous = False
    for i, entry in enumerate(chat):
        if i:
            merge_to_previous = entry['time'] - chat[
                i - 1]['time'] <= key_offset_seconds and entry['slot'] == chat[
                    i - 1]['slot']
            # and chat[i - 1]['type'] == entry['type']

        if entry['type'] == 'chat':
            if merge_to_previous:
                chat_refactored[-1]['key'] += ' ' + entry['key']
                continue
            chat_refactored.append({
                'slot': entry['slot'],
                'key': entry['key']
            })
            continue

        if entry['key'] in CHAT_WHEEL:
            if merge_to_previous:
                chat_refactored[-1]['key'] += ' ' + CHAT_WHEEL[
                    entry['key']]['message']
                continue
            chat_refactored.append({
                'slot': entry['slot'],
                'key': CHAT_WHEEL[entry['key']]['message']
            })

    return chat_refactored

def get_refactored_chat_str(chat: list, key_offset_seconds: int = 2) -> str:
    '''display chat as dialogue'''

    chat_refactored = get_refactored_chat(chat, key_offset_seconds=key_offset_seconds)
    text = ''
    for entry in chat_refactored:
        text += f'- {entry['key']} - player {entry['slot']}.\n'
    return text
