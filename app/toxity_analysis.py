from detoxify import Detoxify
from api_functions import get_match_info
from chat_analysis import get_match_chat


def count_toxity(a):
    toxity_dict = {}
    for i in a:
        if i['slot'] not in toxity_dict.keys():
            toxity_dict[str(i['slot'])] = [Detoxify('multilingual').predict(i['key'])['toxicity'], 1]
        else:
            toxity_dict[str(i['slot'])][0] += Detoxify('multilingual').predict(i['key'])['toxicity']
            toxity_dict[str(i['slot'])][1] += 1
    for i in toxity_dict:
        toxity_dict[i] = toxity_dict[i][0] / toxity_dict[i][1]
    return toxity_dict
print(count_toxity(get_match_chat(get_match_info(8507472882))))
# match_id
# player
# toxity
# team_toxity
# match_toxity

