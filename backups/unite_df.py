import pandas as pd


df1 = pd.read_csv('players_info_leter.csv', index_col=0)
df2 = pd.read_csv('players_info_m.csv', index_col=0)
df3 = pd.read_csv('players_info_hepa.csv', index_col=0)

df = pd.concat([df1, df2, df3], axis=0)
df.to_csv('players_info_all.csv')
