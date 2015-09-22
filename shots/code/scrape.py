import requests
import csv

def scrape_shots(name, team, url):
    shots_data = []
    try:
        response_json = requests.get(players_url).json() 
        shots_data = response_json["resultSets"][0]["rowSet"]
        shots_data = [shot + [name, team] for shot in shots_data]
    except:
        print "error"

    write_to_csv(shots_data)

def write_to_csv(data):
    with open('./../data/shot_data.csv', 'a+') as db:
        writer = csv.writer(db, delimiter=',')
        writer.writerows(data)

# Write headers first
write_to_csv([["game_id","matchup","location","w","final_margin",
    "shot_number","period","game_clock","shot_clock","dribbles",
    "touch_time","shot_dist","pts_type","shot_result","closest_defender",
    "closest_defender_player_id","close_def_dist","fgm","pts", "player_name", "player_team"]])

players_url = "http://stats.nba.com/stats/commonallplayers?LeagueID=00&Season=2014-15&IsOnlyCurrentSeason=1"
response_json = requests.get(players_url).json() 
players_data = response_json["resultSets"][0]["rowSet"]

for player_record in players_data:
    player_id = player_record[0]
    name = player_record[1]
    team = player_record[9]
    print player_id, name, team

    shots_url = "http://stats.nba.com/stats/playerdashptshotlog?DateFrom=&DateTo=\
    &GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&Period=0\
    &PlayerID=%s&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision=" % (player_id)
    
    scrape_shots(name, team, shots_url)




