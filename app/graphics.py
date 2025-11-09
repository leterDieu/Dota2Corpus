import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
df = pd.read_csv('players_info.csv')
df['kda'] = (df['kills_per_minute'] + df['assists']) / np.where(df['deaths_per_minutes'] == 0, 1, df['deaths_per_minutes'])
df['total_score'] = df['radiant_score'] + df['dire_score']
plt.figure(figsize=(10, 15))

# 1. Непрерывные переменные - scatter plots
continuous_vars = [
    'estimated_rank_universal', 'duration',
    'total_score', 'gold_per_minute', 'hero_healing_per_minute',
    'pings', 'buyback_count_per_minute', 'kda'
]

for i, var in enumerate(continuous_vars, 1):
    plt.subplot(3, 3, i)
    plt.scatter(df[var], df['toxicity_context_2'], alpha=0.5, s=10)
    plt.xlabel(var)
    plt.ylabel('Toxicity')
    plt.title(f'Toxicity vs {var}')

plt.tight_layout()
plt.show()

# Создаем heatmap для зависимости токсичности от party_size
plt.figure(figsize=(10, 6))

# Группируем данные по party_size и вычисляем среднюю токсичность
rank_toxicity = df.groupby('estimated_rank_universal')['toxicity'].mean().reset_index()

# Создаем матрицу для heatmap (в данном случае это будет просто строка)
heatmap_data = rank_toxicity['toxicity'].values.reshape(1, -1)
# Создаем heatmap
sns.heatmap(heatmap_data, 
            annot=False, 
            fmt='.3f',
            cmap='RdYlBu_r',  # Красный-желтый-синий (обратный)
            cbar_kws={'label': 'Average Rank'},
            xticklabels=rank_toxicity['estimated_rank_universal'].values,
            yticklabels=[''])

plt.xlabel('Rank')
plt.title('Toxicity by Rank Heatmap')
plt.tight_layout()
plt.show()

df_copy = df.copy()

# Создаем интервалы для party_size
df_copy['party_size_interval'] = pd.cut(df_copy['party_size'], 
                                       bins=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
                                       labels=['Solo', 'Duo', 'Trio', 'Quad', 'Full','6', '7', '8', '9' 'Lobby'])

# Создаем интервалы для toxicity (например, низкая/средняя/высокая токсичность)
df_copy['toxicity_level'] = pd.cut(df_copy['toxicity'], 
                                  bins=[0, 0.33, 0.66, 1.0], 
                                  labels=['Low', 'Medium', 'High'])

# Heatmap: количество матчей по размерам партий и уровням токсичности
plt.figure(figsize=(10, 6))

heatmap_data = pd.crosstab(df_copy['party_size_interval'], 
                          df_copy['toxicity_level'])

sns.heatmap(heatmap_data, 
            annot=True, 
            fmt='d',
            cmap='YlOrRd',
            cbar_kws={'label': 'Number of Matches'})

plt.xlabel('Toxicity Level')
plt.ylabel('Party Size')
plt.title('Number of Matches by Party Size and Toxicity Level')
plt.tight_layout()
plt.show()

# # 2. Время - преобразуем start_time в формат времени дня
# plt.figure(figsize=(12, 6))
# df['time_of_day'] = pd.to_datetime(df['start_time'], unit='s').dt.time
# # Сортируем по времени для лучшего отображения
# time_df = df.groupby('time_of_day')['toxicity_context_2'].mean().reset_index()
# time_df['time_of_day'] = pd.to_datetime(time_df['time_of_day'], format='%H:%M:%S')
# #time_df = time_df.sort_values('time_of_day')

# plt.scatter(time_df['time_of_day'], time_df['toxicity_context_2'])
# plt.xlabel('Time of Day')
# plt.ylabel('Average Toxicity')
# plt.title('Toxicity by Time of Day')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# 3. Категориальные переменные - box plots
plt.figure(figsize=(20, 15))

categorical_vars = ['game_mode_str', 'lobby_type_str', 'region_str', 'winner', 'buyback_before_20', 'party_size']

for i, var in enumerate(categorical_vars, 1):
    plt.subplot(2, 3, i)
    df.boxplot(column='toxicity_context_2', by=var, ax=plt.gca())
    plt.title(f'Toxicity by {var}')
    plt.suptitle('')  # Убираем автоматический суперзаголовок
    plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# 4. KDA отдельно
colors = np.where(df['winner'] > 0.5, 'green', 'red')
plt.figure(figsize=(10, 6))
plt.scatter(df['kda'], df['toxicity_context_2'], alpha=0.5, s = df['toxicity_context_2'] * 100, c=colors)
plt.xlabel('KDA ((kills + assists) / deaths)')
plt.ylabel('Toxicity')
kda_df = df.groupby('kda')['toxicity_context_2'].mean().reset_index()
kda_df = kda_df.sort_values('kda')
# plt.plot(kda_df['kda'], kda_df['toxicity'])
plt.xlim(0, 20)
plt.title('Toxicity vs KDA')
plt.show()