from detoxify import Detoxify
from api_functions import get_match_chat
import json
texts = []
with open('/home/flcl/school57_prog/11/Dota2Corpus/app/match_ids.json', 'r', encoding='utf-8') as file:
    ids = json.load(file)

    
count = 0
for i in ids:
    print(i)
    count+=1
    print(count)
    texts.append(get_match_chat(i))
        
for i in texts:
    if i != []:
        print(i[0]['key'])
        print(Detoxify('multilingual').predict(i[0]['key'])['toxicity'])

