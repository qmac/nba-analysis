import requests
import sys
import pandas as pd

from webapp import db_engine

def scrape_advanced(years):
    dfs = []
    for year in years:
        # URL
        stats_url = 'http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&'\
        'DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&'\
        'OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&'\
        'Rank=N&Season=%s&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&'\
        'VsDivision=&Weight=' % (year)

        # Scrape
        response_json = requests.get(stats_url, headers={'user-agent': 'Mozilla/5.0', 'referer': 'http://stats.nba.com/scores/'}).json()
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

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print 'Usage: python scrape.py'
        exit(-1)
    
    scrape_advanced(['2014-15', '2015-16'])
