from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering

import pandas as pd
import numpy as np
import json
import math

SIZE = 2000 # Size of tier bubbles
FEATURE_COLUMNS = [
                    'PIE', 
                    'TS_PCT', 
                    'USG_PCT'
                    ]
TIER_NAMES = [
            'MVPs', 'All-Stars', 'Key Starters', 'Starters', 
            'Starters', '6th Men', 'Role Players', 'Role Players', 
            'Role Players', 'Bench Warmers', 'Scrubs'
            ]

def clean(df):
    df = df[(df['GP'] >= (0.7 * df['GP'].max()))]
    return df

# Converts clusters into dictionary compatible for visualization
def clusters_to_json(player_clusters):
    players_grouped = player_clusters.groupby('tier')
    tiers_dict = players_grouped.mean().sum(axis=1).rank(ascending=False) - 1
    
    players_dict = {}
    players_dict['name'] = 'vis'
    players_dict['children'] = map(lambda x:{'name':TIER_NAMES[int(tiers_dict[int(x[0])])], 'children':map(lambda x:{'name':x, 'size':SIZE}, x[1]['name'])}, players_grouped)
    return players_dict

# Performs clustering
def cluster(df, year, algorithm='KMeans'):
    # Clean and filter data
    df = clean(df)
    df = df[(df['YEAR'] == year)]

    # Set up fitting data
    names = df['PLAYER_NAME']
    df = df[FEATURE_COLUMNS]
    df = (df - df.min()) / (df.max() - df.min())

    # Rule of thumb k (k=sqrt(n/2))
    num_clusters = int(math.sqrt(len(df)/2))

    # Run clustering
    clstr = eval(algorithm)(n_clusters=num_clusters)
    clstr.fit(df)

    # Convert results to JSON for frontend
    df['tier'] = clstr.labels_
    df['name'] = names
    return clusters_to_json(df)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python tiers.py year algorithm'
        exit(-1)
    
    original = pd.DataFrame.from_csv('./../data/advanced_stats.csv')
    df = clean(original)
    print cluster(original, sys.argv[1], algorithm=sys.argv[2])

