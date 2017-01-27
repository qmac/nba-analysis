import sys
import pandas as pd

from webapp import db_engine
from nba_analysis.scraping import scrape_synergy, write_to_data_source

def scrape_playtypes(play_types):
    df = pd.DataFrame(columns=play_types)
    player_dicts = {}
    for play_type in play_types:
        url = 'http://stats-prod.nba.com/wp-json/statscms/v1/synergy/player/?category=%s&limit=500&names=offensive&q=2475619&season=2016&seasonType=Reg' % play_type
        players = scrape_synergy(url)
        
        for player in players:
            if isinstance(player['PlayerLastName'], (int, long)):
                continue
            name = '%s %s' % (player['PlayerFirstName'], player['PlayerLastName'])
            player_dict = {} if name not in player_dicts else player_dicts[name]
            player_dict[play_type] = player['Time']
            player_dict['Team'] = player['TeamNameAbbreviation']
            player_dicts[name] = player_dict

    headers = ['Player', 'Team'] + play_types
    data = [[p[0]] + [p[1][h] if h in p[1] else 0 for h in headers[1:]] for p in player_dicts.items()]
    return headers, data

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print 'Usage: python platype_data.py'
        exit(-1)
    
    headers, data = scrape_playtypes(['Transition', 'Isolation', 'PRBallHandler', 'PRRollMan', 
                'Postup', 'Spotup', 'Handoff', 'Cut', 'OffScreen', 'OffRebound'])
    write_to_data_source(data, headers, 'playtype_data')
    print 'Finished updating playtype data in db'
