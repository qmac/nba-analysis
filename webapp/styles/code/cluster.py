from sklearn.cluster import AffinityPropagation
from sklearn.cluster import DBSCAN

import pandas as pd
import numpy as np

import json

# Converts clusters into dictionary compatible for visualization
def clusters_to_json(index, df, labels):
    results = {}
    results['cols'] = ['Transition', 'Isolation', 'PRBallHandler', 'PRRollMan', 
            'Postup', 'Spotup', 'Handoff', 'Cut', 'OffScreen', 'OffRebound']
    results['min'] = 0.0
    results['max'] = 50.0
    results['rows'] = index.tolist()
    print index.tolist()

    data = []
    row = 0
    for vector in df.values.tolist():
        d = []
        col = 0
        for val in vector:
            d.append([val, row, col])
            col += 1
        row += 1
        data.append(d)
    results['data'] = data

    return results

# Performs clustering
def cluster():
    # Setup data
    df = pd.read_csv('webapp/styles/code/playtype_data.csv')
    team_df = df.drop('Player', 1).groupby('Team', as_index=False).mean()

    # Run clustering
    clstr = AffinityPropagation()
    clstr.fit(team_df.drop('Team', 1))
    team_df['cluster'] = clstr.labels_
    team_df = team_df.sort('cluster')
    teams = team_df['Team']
    team_df = team_df.drop(['Team', 'cluster'], 1)

    # Convert results to JSON for frontend
    return clusters_to_json(teams, team_df, clstr.labels_)
