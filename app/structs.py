import requests
import json

class Behaviour:
    account_id: int
    name: str
    rating: float
    pings: int
    hero_id: int
    party_size: int
    kda: tuple[int, int, int]
    gold_per_minute: int
    hero_healing_per_minute: int
    winner: bool
    buyback_count: int

    def get_player_data(self):
        player_data = json.loads(requests.get('https://api.opendota.com/api/' + f'players/{self.account_id}', timeout=10).text)  # api url might be transered to constants file
        return player_data['computed_rating'], player_data['profile']['personaname']

    def __init__(self, player_info: dict) -> None:  # add rank tiers
        self.account_id = player_info['account_id']
        player_data = self.get_player_data()
        self.name = player_data[1]
        self.rating = player_data[0]
        self.pings = player_info['pings']
        self.hero_id = player_info['hero_id']
        self.party_size = player_info['party_size']
        self.kda = (player_info['kills'], player_info['deaths'], player_info['assists'])
        self.gold_per_minute = 60 * player_info['gold'] / player_info['duration']
        self.hero_healing_per_minute = 60 * player_info['hero_healing'] / player_info['duration']
        self.winner = player_info['win']
        self.buyback_count = player_info['buyback_count']
    
    def __str__(self) -> str:
        return f"""{self.account_id}: {self.name}, {self.rating}, {self.pings}, {self.hero_id}, {self.party_size}, {self.kda}, {self.gold_per_minute}, {self.hero_healing_per_minute}, {self.winner}, {self.buyback_count}"""

class Match:
    match_id: int
    chat: list[dict]
    duration: int
    game_mode: int  # переделать на str (?)
    radiant_score: int
    dire_score: int
    radiant_win: bool
    start_time: int
    behaviours: list[Behaviour]
    region: int  # переделать на str (?)
    # skill: int | None

    def __init__(self, match_resp: dict) -> None:
        self.match_id = match_resp['match_id']
        self.chat = match_resp['chat']
        self.duration = match_resp['duration']
        self.game_mode = match_resp['game_mode']
        self.radiant_score = match_resp['radiant_score']
        self.dire_score = match_resp['dire_score']
        self.radiant_win = match_resp['radiant_win']
        self.start_time = match_resp['start_time']
        self.region = match_resp['region']

        self.behaviours = [Behaviour(info) for info in match_resp['players']]
    
    def __str__(self) -> str:
        return f"""{self.match_id}: (chat is hided), {self.duration}, {self.game_mode}, {self.radiant_score}, {self.dire_score}, {self.start_time}, {self.region}"""