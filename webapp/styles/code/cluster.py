from sklearn.cluster import AffinityPropagation

import pandas as pd
import numpy as np

import json

# Converts clusters into dictionary compatible for visualization
def clusters_to_json(index, df, labels):
    results = {}
    results['cols'] = ['Transition', 'Isolation', 'PRBallHandler', 'PRRollMan', 
            'Postup', 'Spotup', 'Handoff', 'Cut', 'OffScreen', 'OffRebound']
    results['min'] = df.min().min()
    results['max'] = df.max().min()
    results['rows'] = index.tolist()

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
    fitting_data = team_df.drop('Team', 1)
    fitting_data = (fitting_data - fitting_data.mean()) / (fitting_data.max() - fitting_data.min())
    clstr.fit(fitting_data)

    fitting_data['cluster'] = clstr.labels_
    fitting_data['teams'] = team_df['Team']
    fitting_data = fitting_data.sort('cluster')
    teams = fitting_data['teams']
    fitting_data = fitting_data.drop(['teams', 'cluster'], 1)

    # Convert results to JSON for frontend
    return clusters_to_json(teams, fitting_data, clstr.labels_)
