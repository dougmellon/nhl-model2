from datetime import date
import statistics as st
import csv


def isolate_teams(years):
    games = []

    with open(f'scraping/data/{years}.csv', 'r') as f:
        for i in f:
            i = i.split(",")
            raw_date = i[2].split('/')
            date_formatted = date(int(raw_date[2]), int(raw_date[0]), int(raw_date[1]))
            games.append(
                {
                    "game_id": i[1],
                    "date": date_formatted,
                    "team": i[3],
                    "venue": i[4],
                    "goals_scored": i[10],
                    "rest_days": i[11],
                    "opening_moneyline": i[-7],
                    "closing_moneyline": i[-2],
                    "closing_puckline": i[-1].replace('\n', '')
                }
            )

    return games


def generate_fav_odds_list(data):
    odds_list = []
    count = 0
    for i in data:
        if i['closing_moneyline'] in ['-', '+']:
            count += 1
        else:
            odds_list.append(int(i['closing_moneyline'].strip("+-")))

    print(f'[ALERT] {count/2} games were massing moneyline data')
    return odds_list


isolated_games = isolate_teams('2022-2023')
fav_odds = generate_fav_odds_list(isolated_games)

mean = st.mean(fav_odds)
st_dev = st.pstdev(fav_odds)
upper_st_dev = -st_dev - mean

bankroll = int(input('Enter Bankroll ($): '))
starting_bankroll = bankroll

print(f"Mean: {mean}")
print(f"Standard Deviation: {st_dev}")
print(f"Upper Standard Deviation Threshold: {upper_st_dev}")

games_to_bet = []


def find_other_team_goals(game_id, team_name):
    for i in isolated_games:
        if i['game_id'] == game_id and i['team'] is not team_name:
            return i['goals_scored']


for i in isolated_games:
    if i['closing_moneyline'] not in ['+', '-'] and int(i['closing_moneyline']) < upper_st_dev:
        games_to_bet.append(i)


def calculate_bet_size(bankroll):
    return .05 * float(bankroll)


def calculate_total_return(stake, american_odds):
    american_odds = american_odds.split(" ")[1]
    if american_odds == 'even':
        american_odds = 100
    else:
        american_odds = american_odds
        american_odds = int(american_odds)

    if int(american_odds) < 0:
        return stake + (stake * (100 / abs(american_odds)))
    else:
        return stake + (stake * (american_odds / 100))


covered_count = 0
not_covered_count = 0
covered = False


for i in games_to_bet:
    other_team_goals = int(find_other_team_goals(i['game_id'], i['team']))
    goal_diff = int(i['goals_scored']) - other_team_goals

    bet_size = calculate_bet_size(bankroll)

    if goal_diff >= 2:
        covered_count += 1
        total_return = calculate_total_return(bet_size, i['closing_puckline'])
        bankroll += total_return
    else:
        not_covered_count += 1
        bankroll -= bet_size

    print("Bet Size:", bet_size, "Spread:", goal_diff, "Bankroll after bet:", bankroll)

total_games = covered_count + not_covered_count

print(f"Total Games Bet: {total_games}")
print(f"Total Games that Covered: {covered_count}")
print(f"Total Games that did not Cover: {not_covered_count}")
print(f"Covered Percentage: {(covered_count / total_games)*100}")
print(f"Starting Bankroll: ${starting_bankroll}")
print(f"Final Bankroll: ${bankroll}")


