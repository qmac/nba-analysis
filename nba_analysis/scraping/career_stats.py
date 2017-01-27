import sys

from nba_analysis.scraping import scrape, scrape_players, write_to_data_source

def scrape_career(players):
    data = []
    for player in players:
        player_id, name = player[0], player[1]
        print player_id, name

        player_url = "http://stats.nba.com/stats/commonplayerinfo?LeagueID=00&PlayerID=%s" % (player_id)
        player_info = scrape(player_url)[1]
        position = player_info[0][14]

        career_url = "http://stats.nba.com/stats/playercareerstats?LeagueID=00&PerMode=PerGame&PlayerID=%s" % (player_id)
        headers, season_data = scrape(career_url)
        headers = ['name', 'position'] + headers
        season_data = [[name, position] + season_stats for season_stats in season_data]
        data.extend(season_data)

    return headers, data

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print 'Usage: python career_stats.py'
        exit(-1)
    
    players = scrape_players([0, 1], current_season_only=False)
    headers, data = scrape_career(players)
    write_to_data_source(data, headers, 'career_data')
    print 'Finished updating career stats in db'