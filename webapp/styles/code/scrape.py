import requests
import csv
import os
import pandas as pd

def scrape(url):
    try:
        response_json = requests.get(url, headers={'user-agent': 'Mozilla/5.0', 'referer': 'http://stats.nba.com/scores/'}).json()
        data = response_json["resultSets"][0]["rowSet"]
        return data
    except:
        print "error"

    return

def get_headers(url):
    try:
        response_json = requests.get(url, headers={'user-agent': 'Mozilla/5.0', 'referer': 'http://stats.nba.com/scores/'}).json()
        data = response_json["resultSets"][0]["headers"]
        return data
    except:
        print "error"

    return

# Get player information
play_types = ['Transition', 'Isolation', 'PRBallHandler', 'PRRollMan', 
            'Postup', 'Spotup', 'Handoff', 'Cut', 'OffScreen', 'OffRebound']

df = pd.DataFrame(columns=play_types)
for play_type in play_types:
    url = 'http://stats.nba.com/js/data/playtype/player_%s.js' % (play_type)
    headers = get_headers(url)
    player_first_idx = headers.index('PlayerFirstName')
    player_last_idx = headers.index('PlayerLastName')
    time_idx = headers.index('Time')

    data = scrape(url)
    dicts = {}
    for stats in data:
        dicts[stats[player_first_idx] + " " + stats[player_last_idx]] = stats[time_idx]
    df[play_type] = pd.Series(index=dicts.keys(), data=dicts.values())

df = df.fillna(0)
df.to_csv('playtype_data.csv', index_label='Player')
