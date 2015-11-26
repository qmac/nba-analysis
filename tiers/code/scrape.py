import requests
import csv
import os

def write_to_csv(path, data):
    with open(path, 'a+') as db:
        writer = csv.writer(db, delimiter=',')
        writer.writerows(data)

YEARS = ['2014-15', '2015-16']
for year in YEARS:
    path = './../data/advanced_stats_%s.csv' % (year)

    # Delete file if already exists
    try:
        os.remove(path)
    except OSError:
        pass

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
    write_to_csv(path, [headers])
    write_to_csv(path, data)
