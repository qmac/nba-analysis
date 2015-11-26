import os
import json

import pandas as pd
import numpy as np

# Helper methods needed to setup visualization

SIZE = 2000
def clusters_to_json(player_clusters):
    players_dict = {}
    players_grouped = player_clusters.groupby('tier')
    players_dict['name'] = 'vis'
    players_dict['children'] = map(lambda x:{'name':'Tier %d' % (x[0]), 'children':map(lambda x:{'name':x, 'size':SIZE}, x[1]['PLAYER_NAME'])}, players_grouped)

    with open('./../visualization/nba_clusters.json', 'w+') as outfile:
        json.dump(players_dict, outfile)