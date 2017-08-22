import os
import requests
import urllib
import pandas as pd

from nba_analysis import config
from nba_analysis.webapp import db_engine


headers = {
    'user-agent': 'Mozilla/5.0',
    'referer': 'http://stats.nba.com/scores/'
}


def scrape(url):
    try:
        response_json = requests.get(url, headers=headers).json()
        heads = response_json['resultSets'][0]['headers']
        data = response_json['resultSets'][0]['rowSet']
        return heads, data
    except Exception as e:
        print 'Encountered exception while scraping: ' + e.message


def scrape_synergy(url, num_retries=10):
    for i in range(num_retries):
        try:
            response_json = requests.get(url, headers=headers).json()
            players = response_json['results']
            return players
        except Exception as e:
            print 'Encountered exception while scraping: ' + e.message


def scrape_players(indices, current_season_only=True):
    params = urllib.urlencode({
        'LeagueID': '00',
        'Season': config.current_year,
        'IsOnlyCurrentSeason': int(current_season_only)
    })
    players_url = 'http://stats.nba.com/stats/commonallplayers?%s' % (params)
    players = scrape(players_url)[1]
    players = [[player[i] for i in indices] for player in players]
    return players


def write_to_data_source(data, headers, table_name):
    df = pd.DataFrame(data=data, columns=headers)
    if config.data_source == 'sql' and db_engine is not None:
        return df.to_sql(table_name, db_engine, if_exists='replace')
    elif config.data_source == 'local':
        if not os.path.exists('nba_analysis/data/'):
            os.makedirs('nba_analysis/data/')
        return df.to_csv('nba_analysis/data/%s.csv' % table_name, encoding='utf-8')
    else:
        raise Exception('Invalid data source configuration')
