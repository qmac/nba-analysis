import requests
import csv
import os
import sys
import urllib2

import numpy as np
import pandas as pd

from webapp import db_engine

def scrape_pictures(players):
    directory = 'static/pics/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    for player in players:
        # Stupid edge cases
        if player == 'Nene Hilario':
            player = 'Nene'
        if player == 'Tim Hardaway':
            player = 'Tim Hardaway Jr'
        if player == 'Jose Juan Barea':
            player = 'Jose Barea'

        url_name = player.lower().replace(' ', '_').replace('.', '').replace('\'', '')
        print url_name

        url = 'http://i.cdn.turner.com/nba/nba/.element/img/2.0/sect/statscube/players/large/%s.png' % (url_name)

        try:  
            image = urllib2.urlopen(url)
            data = image.read()

            with open('%s%s.png' % (directory, url_name), 'w+') as outfile:
                outfile.write(data)

        except:
            continue

def scrape_advanced(years):
    YEARS = ['2014-15', '2015-16']
    dfs = []
    for year in YEARS:
        # URL
        stats_url = 'http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&'\
        'DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&'\
        'OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&'\
        'Rank=N&Season=%s&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&'\
        'VsDivision=&Weight=' % (year)

        # Scrape
        response_json = requests.get(stats_url).json()
        headers = response_json['resultSets'][0]['headers']
        data = response_json['resultSets'][0]['rowSet']

        # Manually add year data
        headers.append('YEAR')
        for row in data:
            row.append(year)

        # Write into database
        df = pd.DataFrame(data=data, columns=headers)
        dfs.append(df)

    table = pd.concat(dfs)
    table.to_sql('advanced_stats', db_engine, if_exists='replace')
    print 'Finished updating advanced stats in db'
    return

# scrape_pictures(players)

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print 'Usage: python scrape.py'
        exit(-1)
    
    scrape_advanced()
