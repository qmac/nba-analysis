import sys
import pandas as pd

from webapp import db_engine
from nba_analysis.scraping import scrape

def scrape_playtypes(play_types):
    # Scrape the data into a pandas data frame
    df = pd.DataFrame(columns=play_types)
    player_to_team = {}
    for play_type in play_types:
        url = 'http://stats.nba.com/js/data/playtype/player_%s.js' % (play_type)
        headers, data = scrape(url)

        player_first_idx = headers.index('PlayerFirstName')
        player_last_idx = headers.index('PlayerLastName')
        team_idx = headers.index('TeamNameAbbreviation')
        time_idx = headers.index('Time')

        dicts = {}
        for stats in data:
            full_name = stats[player_first_idx] + " " + stats[player_last_idx]
            dicts[full_name] = stats[time_idx]
            player_to_team[full_name] = stats[team_idx]
        df[play_type] = pd.Series(index=dicts.keys(), data=dicts.values())

    df['Team'] = pd.Series(index=player_to_team.keys(), data=player_to_team.values())
    df = df.fillna(0)

    # Save data to db
    df.to_sql('playtype_data', db_engine, if_exists='replace', index_label='Player')
    print 'Finished updating play type data in db'
    return

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print 'Usage: python scrape.py'
        exit(-1)
    
    scrape_playtypes(['Transition', 'Isolation', 'PRBallHandler', 'PRRollMan', 
                'Postup', 'Spotup', 'Handoff', 'Cut', 'OffScreen', 'OffRebound'])
