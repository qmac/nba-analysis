from nba_analysis.scraping import scrape, write_to_csv

# Get player information
players_url = "http://stats.nba.com/stats/commonallplayers?LeagueID=00&Season=2016-17&IsOnlyCurrentSeason=1"
players_data = scrape(players_url)[1]

data
for player_record in players_data:
    player_id = player_record[0]
    name = player_record[1]
    team = player_record[9]

    shots_url = "http://stats.nba.com/stats/playerdashptshotlog?DateFrom=&DateTo=\
    &GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&Period=0\
    &PlayerID=%s&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision=" % (player_id)
    
    headers, shots_data = scrape(shots_url)
    headers = headers + ['name', 'team']
    shots_data = [shot + [name, team] for shot in shots_data]
    data.extend(shots_data)


# Delete file if already exists
try:
    os.remove('./../data/shot_data.csv')
except OSError:
    pass

write_to_csv(headers, data, './../data/shot_data.csv')
