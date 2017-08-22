import sys

from tqdm import tqdm
from nba_analysis.scraping import scrape, write_to_data_source


def scrape_advanced(years):
    all_data = []
    for year in tqdm(years):
        stats_url = 'http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&'\
        'DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&'\
        'OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&'\
        'Rank=N&Season=%s&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&'\
        'VsDivision=&Weight=' % (year)

        headers, data = scrape(stats_url)
        headers.append('YEAR')
        for row in data:
            row.append(year)

        all_data.extend(data)

    return headers, all_data


if __name__ == '__main__':
    if len(sys.argv) != 1:
        print 'Usage: python advanced_stats.py'
        exit(-1)

    headers, data = scrape_advanced(['2014-15', '2015-16', '2016-17'])
    write_to_data_source(data, headers, 'advanced_stats')
    print 'Finished updating advanced stats in db'
