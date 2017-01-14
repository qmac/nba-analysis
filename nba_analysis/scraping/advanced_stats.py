import sys
import pandas as pd

from webapp import db_engine
from nba_analysis.scraping import scrape

def scrape_advanced(years):
    dfs = []
    for year in years:
        stats_url = 'http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&'\
        'DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&'\
        'OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&'\
        'Rank=N&Season=%s&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&'\
        'VsDivision=&Weight=' % (year)

        headers, data = scrape(stats_url)
        headers.append('YEAR')
        for row in data:
            row.append(year)

        df = pd.DataFrame(data=data, columns=headers)
        dfs.append(df)

    table = pd.concat(dfs)
    table.to_sql('advanced_stats', db_engine, if_exists='replace')

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print 'Usage: python scrape.py'
        exit(-1)
    
    scrape_advanced(['2014-15', '2015-16', '2016-17'])
    print 'Finished updating advanced stats in db'
