import requests
import csv
import os
import sys

def scrape(url):
    response_json = requests.get(url, headers={'user-agent': 'Mozilla/5.0', 'referer': 'http://stats.nba.com/'}).json() 
    data = response_json["resultSets"][0]["rowSet"]
    return data

def write_to_csv(data):
    with open('passing_data.csv', 'a+') as db:
        writer = csv.writer(db, delimiter=',')
        writer.writerows(data)

def scrape_passing():
    # Delete file if already exists
    try:
        os.remove('../data/passing_data.csv')
    except OSError:
        pass

    # Write headers first
    write_to_csv([["PLAYER_ID","PLAYER_NAME_LAST_FIRST","TEAM_NAME","TEAM_ID",
        "PASS_TYPE","G","PASS_TO","PASS_TEAMMATE_PLAYER_ID","FREQUENCY","PASS",
        "AST","FGM","FGA","FG_PCT","FG2M","FG2A","FG2_PCT","FG3M","FG3A","FG3_PCT"]])

    # Get player information
    players_url = "http://stats.nba.com/stats/commonallplayers?LeagueID=00&Season=2015-16&IsOnlyCurrentSeason=1"
    players_data = scrape(players_url)

    for player_record in players_data:
        player_id = player_record[0]
        print player_id

        passing_url = 'http://stats.nba.com/stats/playerdashptpass?College&Conference&Country&DateFrom'\
        '&DateTo&Division&DraftPick&DraftYear&PlayerID=%s&GameScope&GameSegment&Height&LastNGames=0'\
        '&LeagueID=00&Location&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome&PORound=0'\
        '&PaceAdjust=N&PerMode=Totals&PlayerExperience&PlayerPosition&PlusMinus=N&Rank=N&Season=2015-16'\
        '&SeasonSegment&SeasonType=Regular+Season&ShotClockRange&StarterBench&TeamID=0&VsConference'\
        '&VsDivision&Weight' % (player_id)
        
        passing_data = scrape(passing_url)
        write_to_csv(passing_data)

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print 'Usage: python scrape.py'
        exit(-1)
    
    scrape_passing()


