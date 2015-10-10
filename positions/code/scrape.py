import requests
import csv

def scrape(url):
    try:
        response_json = requests.get(url).json()
        data = response_json["resultSets"][0]["rowSet"]
        return data
    except:
        print "error"

    return

def write_to_csv(data):
    with open('./../data/career_data.csv', 'a+') as db:
        writer = csv.writer(db, delimiter=',')
        writer.writerows(data)

# Write headers first
write_to_csv([["name", "position", "player_id","season_id","league_id","team_id","team_abbreviation","player_age",
    "gp","gs","min","fgm","fga","fg_pct","fg3m","fg3a","fg3_pct","ftm","fta","ft_pct","oreb",
    "dreb","reb","ast","stl","blk","tov","pf","pts"]])

# Get player information
players_url = "http://stats.nba.com/stats/commonallplayers?LeagueID=00&Season=2014-15&IsOnlyCurrentSeason=0"
players_data = scrape(players_url)

for player_record in players_data:
    player_id, name = player_record[0], player_record[1]
    print player_id, name

    player_url = "http://stats.nba.com/stats/commonplayerinfo?LeagueID=00&PlayerID=%s" % (player_id)
    player_info = scrape(player_url)
    position = player_info[0][14]

    shots_url = "http://stats.nba.com/stats/playercareerstats?LeagueID=00&PerMode=PerGame&PlayerID=%s" % (player_id)
    season_data = scrape(shots_url)
    season_data = [[name, position] + season_stats for season_stats in season_data]
    write_to_csv(season_data)

