import matplotlib.pyplot as plt
import pandas as pd

import json
import time

from structs import Match


REQUESTS_PER_DAY = 2000
REQUESTS_PER_MINUTE = 60
REQUESTS_PER_MATCH = 11
MATCHES_PER_DAY = REQUESTS_PER_DAY // REQUESTS_PER_MATCH
MATCHES_PER_MINUTE = REQUESTS_PER_MINUTE // REQUESTS_PER_MATCH

with open('app/match_ids.json', 'r', encoding='utf-8') as f:
    ids = json.loads(f.read())
   
try: 
    previous_df = pd.read_csv('players_info.csv', index_col=0)
    offset = previous_df.shape[0] // 10
except:
    previous_df = pd.DataFrame()
    offset = 0
    
offset_personal = 0 # Fedor: 200, Ilya: 400

df_arr = []
for i in range(MATCHES_PER_DAY // MATCHES_PER_MINUTE):
    this_minute_ids = ids[(offset_personal + offset + i * MATCHES_PER_MINUTE):(offset_personal + offset + (i+1) * MATCHES_PER_MINUTE)]
    try:
        df_arr.append(Match.create_dataframe_by_id_list(this_minute_ids))
    except Exception as e:
        print(e)
    time.sleep(65)

new_df = pd.concat(df_arr, axis=0)
df = pd.concat([previous_df, new_df], axis=0)
df.to_csv('players_info.csv')
