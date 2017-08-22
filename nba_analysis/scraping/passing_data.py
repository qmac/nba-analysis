import sys

from tqdm import tqdm
from nba_analysis.scraping import scrape, scrape_players, write_to_data_source
from nba_analysis import config


def scrape_passing(players):
    data = []
    for player in tqdm(players):
        player_id = player[0]

        passing_url = 'http://stats.nba.com/stats/playerdashptpass?College&Conference&Country&DateFrom'\
        '&DateTo&Division&DraftPick&DraftYear&PlayerID=%s&GameScope&GameSegment&Height&LastNGames=0'\
        '&LeagueID=00&Location&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome&PORound=0'\
        '&PaceAdjust=N&PerMode=Totals&PlayerExperience&PlayerPosition&PlusMinus=N&Rank=N&Season=%s'\
        '&SeasonSegment&SeasonType=Regular+Season&ShotClockRange&StarterBench&TeamID=0&VsConference'\
        '&VsDivision&Weight' % (player_id, config.current_year)

        headers, player_data = scrape(passing_url)
        data.extend(player_data)

    return headers, data


if __name__ == '__main__':
    if len(sys.argv) != 1:
        print 'Usage: python passing_data.py'
        exit(-1)

    players = scrape_players([0])
    headers, data = scrape_passing(players)
    write_to_data_source(data, headers, 'passing_data')
