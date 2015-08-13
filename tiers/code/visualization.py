import os

import pandas as pd
import numpy as np

import urllib2

# Helper methods needed to setup visualization

def scrape_pictures(player_clusters):
    players = np.array(player_clusters['Player'])

    directory = './../visualization/pics/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    for player in players:
        # Stupid edge cases
        if player == 'Nene Hilario':
            player = 'Nene'

        url_name = player.lower().replace(' ', '_').replace('.', '').replace('\'', '')
        print url_name

        url = 'http://i.cdn.turner.com/nba/nba/.element/img/2.0/sect/statscube/players/large/%s.png' % (url_name)

        image = urllib2.urlopen(url)
        data = image.read()

        file = open('%s%s.png' % (directory, player), 'w+')
        file.write(data)
        file.close()

def clusters_to_json(player_clusters):
    return