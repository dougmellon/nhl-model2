import requests
import csv
from bs4 import BeautifulSoup

games = []


def get_game_object(year):
    URL = f'https://www.hockey-reference.com/leagues/NHL_{year}_games.html'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    return soup.find(id="games").find("tbody").find_all("tr")


def get_game_data(i):
    return ({
        "date": i.find("th", {"data-stat": "date_game"}).find("a").text,
        "visitor_team_name": i.find("td", {"data-stat": "visitor_team_name"}).find("a").text,
        "visitor_goals": i.find("td", {"data-stat": "visitor_goals"}).text,
        "home_team_name": i.find("td", {"data-stat": "home_team_name"}).find("a").text,
        "home_goals": i.find("td", {"data-stat": "home_goals"}).text
    })


def generate_csv(date, data):
    with open(f'data/{date}.csv', 'a') as f:
        for i in data:
            w = csv.DictWriter(f, i.keys())
            w.writerow(i)


year = input("Year: ")

game_objs = get_game_object(year)

for i in game_objs:
    games.append(get_game_data(i))

generate_csv(year, games)

