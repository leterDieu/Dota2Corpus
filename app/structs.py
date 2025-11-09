import pandas as pd

import requests
import json

from chat_analysis import get_refactored_chat, get_refactored_chat_str
from toxicity_analysis import count_toxicity


API_URL = 'https://api.opendota.com/api/'


with open('app/constants/game_mode.json') as f:
    GAME_MODES = json.loads(f.read())
with open('app/constants/lobby_type.json') as f:
    LOBBY_TYPES = json.loads(f.read())
with open('app/constants/region.json') as f:
    REGIONS = json.loads(f.read())


class Behaviour:
    account_id: int
    name: str | None
    rating: float | None
    rank_universal: int | None # rank * 5 + stars
    party_size: int
    hero_id: int
    is_radiant: bool
    winner: bool
    duration: int
    kda_per_minute: tuple[float, float, float]
    gold_per_minute: int
    hero_healing_per_minute: float
    pings: int | None
    buyback_count_per_minute: float
    buyback_before_20: bool

    def get_player_data(self):
        player_data = json.loads(requests.get(API_URL + f'players/{self.account_id}', timeout=10).text)
        computed_rating = None
        name = None
        if 'computed_rating' in player_data:
            computed_rating = player_data['computed_rating']
        if 'profile' in player_data:
            if 'personaname' in player_data['profile']:
                name = player_data['profile']['personaname']
        return computed_rating, name

    def __init__(self, player_info: dict) -> None:
        self.account_id = player_info['account_id']
        self.rating, self.name = self.get_player_data()
        
        rank_tier = player_info['rank_tier']
        self.rank_universal = None
        if rank_tier is not None:
            self.rank_universal = rank_tier - rank_tier // 10 * 5
            
        self.party_size = player_info['party_size']
        self.hero_id = player_info['hero_id']
        self.is_radiant = player_info['isRadiant']
        self.winner = player_info['win']
        self.duration = player_info['duration']
        self.kda_per_minute = (
            60 * player_info['kills'] / self.duration,
            60 * player_info['deaths'] / self.duration,
            60 * player_info['assists'] / self.duration)
        self.gold_per_minute = 60 * player_info['gold'] / self.duration
        self.hero_healing_per_minute = 60 * player_info['hero_healing'] / self.duration
        
        self.pings = None
        if 'pings' in player_info:
            self.pings = player_info['pings']
        
        self.buyback_count_per_minute = 60 * player_info['buyback_count'] / self.duration
        self.buyback_before_20 = False
        if player_info['buyback_log']:
            self.buyback_before_20 = player_info['buyback_log'][0]['time'] // 60 < 20

    def __str__(self) -> str:
        return f"""{self.account_id}: {self.name}, {self.rating}, {self.pings}, {self.hero_id}, {self.party_size}, {self.kda}, {self.gold_per_minute}, {self.hero_healing_per_minute}, {self.winner}, {self.buyback_count}"""

class Match:
    match_id: int
    chat: list[dict]
    estimated_rank_universal: int | None # rank * 5 + stars
    duration: int
    game_mode_str: str
    radiant_score: int
    dire_score: int
    radiant_win: bool
    start_time: int
    region_str: str
    lobby_type_str: str
    estimated_rank_universal:  float | None
    behaviours: list[Behaviour]

    def analyze(self, match_id) -> None:
        match_responce = json.loads(requests.get(API_URL + f'matches/{match_id}', timeout=10).text)
        self.__init__(match_responce)

    def __init__(self, match_resp) -> None:
        self.match_id = match_resp['match_id']
        self.chat = match_resp['chat']
        self.duration = match_resp['duration']
        self.radiant_score = match_resp['radiant_score']
        self.dire_score = match_resp['dire_score']
        self.radiant_win = match_resp['radiant_win']
        self.start_time = match_resp['start_time']

        game_mode = match_resp['game_mode']
        self.game_mode_str = GAME_MODES[str(game_mode)]['name']
        region = match_resp['region']
        self.region_str = REGIONS[str(region)]
        lobby_type = match_resp['lobby_type']
        self.lobby_type_str = LOBBY_TYPES[str(lobby_type)]['name']

        self.behaviours = [Behaviour(info) for info in match_resp['players']]
        self.estimated_rank_universal = 0
        number_of_not_none_ranks = 0
        for behaviour in self.behaviours:
            if behaviour.rank_universal is not None:
                self.estimated_rank_universal += behaviour.rank_universal
                number_of_not_none_ranks += 1
        if number_of_not_none_ranks:
            self.estimated_rank_universal //= number_of_not_none_ranks
        else:
            self.estimated_rank_universal = None
            
    def get_refactored_chat(self, key_offset_seconds: int = 2) -> list[dict]:
        return get_refactored_chat(self.chat, key_offset_seconds)
        
    def get_refactored_chat_str(self, key_offset_seconds: int = 2) -> str:
        return get_refactored_chat_str(self.chat, key_offset_seconds)
        
    def count_toxicity(self, key_offset_seconds: int = 2) -> dict:
        return count_toxicity(self.get_refactored_chat(key_offset_seconds))
        
    def to_df(self) -> pd.DataFrame:
        behavior_df_arr = []
        for behaviour in self.behaviours:
                behavior_df_arr.append(pd.DataFrame(data={
                'match_id': self.match_id,
                'chat': None,
                'estimated_rank_universal': self.estimated_rank_universal,
                'duration': self.duration,
                'game_mode_str': self.game_mode_str,
                'radiant_score': self.radiant_score,
                'dire_score': self.dire_score,
                'radiant_win': self.radiant_win,
                'start_time': self.start_time,
                'region_str': self.region_str,
                'lobby_type_str': self.lobby_type_str,
                'account_id': behaviour.account_id,
                'name': behaviour.name,
                'rating': behaviour.rating,
                'rank_universal': behaviour.rank_universal,
                'party_size': behaviour.party_size,
                'hero_id': behaviour.hero_id,
                'is_radiant': behaviour.is_radiant,
                'winner': behaviour.winner,
                'kills_per_minute': behaviour.kda_per_minute[0],
                'deaths_per_minutes': behaviour.kda_per_minute[1],
                'assists': behaviour.kda_per_minute[2],
                'gold_per_minute': behaviour.gold_per_minute,
                'hero_healing_per_minute': behaviour.hero_healing_per_minute,
                'pings': behaviour.pings,
                'buyback_count_per_minute': behaviour.buyback_count_per_minute,
                'buyback_before_20': behaviour.buyback_before_20
            }))
        return pd.concat(behavior_df_arr, axis=1)
        
     def __str__(self) -> str:
         return f"""{self.match_id}: (chat is hided), {self.duration}, {self.game_mode_str}, {self.lobby_type_str}, {self.start_time}, {self.region_str}, {self.estimated_rank_universal}"""

    class MatchStack:
        match_arr: list[Match]
        
        def __init__(self, match_arr: list[Match]) -> None:
            self.match_arr = match_arr
            
        def to_df(self) -> pd.DataFrame:
            return concat([match.to_df() for match in self.match_arr], axis=1)    

   