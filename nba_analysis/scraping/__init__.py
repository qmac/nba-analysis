import requests
import pandas as pd

from nba_analysis import config
from nba_analysis.webapp import db_engine

def scrape(url):
    try:
        response_json = requests.get(url, headers={'user-agent': 'Mozilla/5.0', 'referer': 'http://stats.nba.com/scores/'}).json()
        headers = response_json['resultSets'][0]['headers']
        data = response_json["resultSets"][0]["rowSet"]
        return headers, data
    except:
        print "Encountered exception while scraping"

    return

def scrape_players(indices, current_season_only=True):
    players_url = "http://stats.nba.com/stats/commonallplayers?LeagueID=00&Season=%s&IsOnlyCurrentSeason=%d" % (config.current_year, current_season_only)
    players = scrape(players_url)[1]
    players = [[player[i] for i in indices] for player in players]
    return players

def write_to_data_source(data, headers, table_name):
    df = pd.DataFrame(data=data, columns=headers)
    if config.data_source == 'sql' and db_engine is not None:
        return df.to_sql(table_name, db_engine, if_exists='replace')
    elif config.data_source == 'local':
        return df.to_csv('nba_analysis/data/%s.csv' % table_name)
    else:
        raise Exception('Invalid data source configuration')