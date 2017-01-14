from nba_analysis.scraping import scrape, write_to_csv

# Get player information
players_url = "http://stats.nba.com/stats/commonallplayers?LeagueID=00&Season=2016-17&IsOnlyCurrentSeason=0"
players = scrape(players_url)[1]

data = []
for player in players:
    player_id, name = player[0], player[1]
    print player_id, name

    player_url = "http://stats.nba.com/stats/commonplayerinfo?LeagueID=00&PlayerID=%s" % (player_id)
    player_info = scrape(player_url)[1]
    position = player_info[0][14]

    shots_url = "http://stats.nba.com/stats/playercareerstats?LeagueID=00&PerMode=PerGame&PlayerID=%s" % (player_id)
    headers, season_data = scrape(shots_url)
    headers = ['name', 'position'] + headers
    season_data = [[name, position] + season_stats for season_stats in season_data]
    data.append(season_data)


if not os.path.exists('positions/data/'):
    os.makedirs('positions/data/')

write_to_csv(headers, data, 'positions/data/career_data.csv'')