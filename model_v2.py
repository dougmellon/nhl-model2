import requests

api_root = "https://api.the-odds-api.com/v4/sports/"
api_key = "1c26947aa478b6acffa492cd101df9e5"
sport_key = "icehockey_nhl"
regions = "us"
markets = "h2h"
odds_format = "american"

req_string = f"{api_root}{sport_key}/odds/?apiKey={api_key}&regions={regions}&markets={markets}&oddsFormat={odds_format}"

response = requests.get(req_string).json()


def generate_game_data(game):
    return {
        "id": game['id'],
        "sport_key": game['sport_key'],
        "commence_time": game['commence_time'],
        "home_team": game['home_team'],
        "away_team": game['away_team'],
        "bookmakers": game['bookmakers']
    }


game_lines = []

for i in response:
    print(i)