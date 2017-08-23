from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering

import pandas as pd
import math
import sys

SIZE = 2000  # Size of tier bubbles
FEATURE_COLUMNS = ['PIE', 'TS_PCT', 'USG_PCT']
TIER_NAMES = ['MVPs', 'All-Stars', 'Key Starters', 'Starters',
              'Starters', '6th Men', 'Role Players', 'Role Players',
              'Role Players', 'Bench Warmers', 'Scrubs']


def clusters_to_json(player_clusters):
    # Converts clusters into dictionary compatible for visualization
    players_grouped = player_clusters.groupby('tier')
    tiers_dict = players_grouped.mean().sum(axis=1).rank(ascending=False) - 1

    players_dict = {}
    players_dict['name'] = 'vis'
    children = []
    for tier_num, tier in players_grouped:
        players = map(lambda x: {
            'name': x[1]['name'],
            'id': x[1]['id'],
            'size': SIZE
        }, tier.iterrows())
        children.append({
            'name': TIER_NAMES[int(tiers_dict[int(tier_num)])],
            'children': players
        })
    players_dict['children'] = children
    return players_dict


def cluster(df, year, algorithm='KMeans'):
    # Performs clustering
    # Clean and filter data
    df = df[(df['YEAR'] == year)]
    df = df[(df['GP'] >= (0.7 * df['GP'].max()))]

    # Set up fitting data
    names = df['PLAYER_NAME']
    ids = df['PLAYER_ID'].astype(str)
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
    df['id'] = ids
    return clusters_to_json(df)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python tiers.py year algorithm'
        exit(-1)

    df = pd.DataFrame.from_csv('./../data/advanced_stats.csv')
    print cluster(df, sys.argv[1], algorithm=sys.argv[2])
