import sys

from nba_analysis.scraping import scrape, scrape_players, write_to_data_source

def scrape_shots(players):
    data = []
    for player in players:
        shots_url = "http://stats.nba.com/stats/playerdashptshotlog?DateFrom=&DateTo=\
        &GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&Period=0\
        &PlayerID=%s&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision=" % (player[0])
        
        headers, shots_data = scrape(shots_url)
        headers = headers + ['name', 'team']
        shots_data = [shot + [player[1], player[2]] for shot in shots_data]
        data.extend(shots_data)

    return data, headers

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print 'Usage: python shot_data.py'
        exit(-1)
    
    players = scrape_players([0, 1, 9])
    data, headers = scrape_shots(players)
    write_to_data_source(data, headers, 'shot_data')
