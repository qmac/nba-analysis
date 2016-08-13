import requests
import csv
import os
import pandas as pd

def scrape(url):
    try:
        response_json = requests.get(url, headers={'user-agent': 'Mozilla/5.0', 'referer': 'http://stats.nba.com/scores/'}).json()
        headers = response_json["resultSets"][0]["headers"]
        data = response_json["resultSets"][0]["rowSet"]
        return headers, data
    except:
        print "error"

    return

# Get player information
play_types = ['Transition', 'Isolation', 'PRBallHandler', 'PRRollMan', 
            'Postup', 'Spotup', 'Handoff', 'Cut', 'OffScreen', 'OffRebound']

df = pd.DataFrame(columns=play_types)
player_to_team = {}
for play_type in play_types:
    url = 'http://stats.nba.com/js/data/playtype/player_%s.js' % (play_type)
    headers, data = scrape(url)

    player_first_idx = headers.index('PlayerFirstName')
    player_last_idx = headers.index('PlayerLastName')
    team_idx = headers.index('TeamNameAbbreviation')
    time_idx = headers.index('Time')

    dicts = {}
    for stats in data:
        full_name = stats[player_first_idx] + " " + stats[player_last_idx]
        dicts[full_name] = stats[time_idx]
        player_to_team[full_name] = stats[team_idx]
    df[play_type] = pd.Series(index=dicts.keys(), data=dicts.values())

df['Team'] = pd.Series(index=player_to_team.keys(), data=player_to_team.values())
df = df.fillna(0)
df.to_csv('playtype_data.csv', index_label='Player')
