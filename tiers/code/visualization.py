import os
import json

import pandas as pd
import numpy as np

import urllib2

# Helper methods needed to setup visualization

def scrape_pictures(player_clusters):
    players = np.array(player_clusters['PLAYER_NAME'])

    directory = './../visualization/pics/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    for player in players:
        # Stupid edge cases
        if player == 'Nene Hilario':
            player = 'Nene'
        if player == 'Tim Hardaway':
            player = 'Tim Hardaway Jr'
        if player == 'Jose Juan Barea':
            player = 'Jose Barea'

        url_name = player.lower().replace(' ', '_').replace('.', '').replace('\'', '')
        print url_name

        url = 'http://i.cdn.turner.com/nba/nba/.element/img/2.0/sect/statscube/players/large/%s.png' % (url_name)

        image = urllib2.urlopen(url)
        data = image.read()

        with open('%s%s.png' % (directory, url_name), 'w+') as outfile:
            outfile.write(data)

SIZE = 2000
def clusters_to_json(player_clusters):
    players_dict = {}
    players_grouped = player_clusters.groupby('tier')
    players_dict['name'] = 'vis'
    players_dict['children'] = map(lambda x:{'name':'Tier %d' % (x[0]), 'children':map(lambda x:{'name':x, 'size':SIZE}, x[1]['PLAYER_NAME'])}, players_grouped)

    with open('./../visualization/nba_clusters.json', 'w+') as outfile:
        json.dump(players_dict, outfile)