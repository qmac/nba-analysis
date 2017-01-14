from sklearn.cluster import AffinityPropagation
import pandas as pd
import json

from webapp import db_engine

FEATURES = ['Transition', 'Isolation', 'PRBallHandler', 'PRRollMan', 
            'Postup', 'Spotup', 'Handoff', 'Cut', 'OffScreen', 'OffRebound']

# Converts clusters into dictionary compatible for visualization
def clusters_to_json(df, scope):
    vectors_df = df.drop([scope, 'cluster'], 1)
    results = {}

    results['cols'] = FEATURES
    results['min'] = vectors_df.min().min()
    results['max'] = vectors_df.max().max()
    results['rows'] = df[scope].tolist()

    # Create a list-matrix with an entry for every point and its corresponding x and y coordinates
    data = []
    row = 0
    for vector in vectors_df.values.tolist():
        augmented_vector = []
        col = 0
        for val in vector:
            augmented_vector.append([val, row, col])
            col += 1
        row += 1
        data.append(augmented_vector)
    results['data'] = data

    return results

# Performs clustering
def cluster(scope):
    # Setup data
    df = pd.read_sql('playtype_data', db_engine)

    # Manipulate data into scope
    if scope == 'Team':
        df = df.drop('Player', 1).groupby('Team', as_index=False).mean()
    elif scope == 'Player':
        df = df.drop('Team', 1)
    else:
        raise Exception('This is never supposed to happen')

    # Normalize the data
    df[FEATURES] = (df[FEATURES] - df[FEATURES].mean()) / (df[FEATURES].max() - df[FEATURES].min())

    # Run clustering
    clstr = AffinityPropagation()
    clstr.fit(df[FEATURES])

    # Clump results
    df['cluster'] = clstr.labels_
    df = df.sort('cluster')

    # Convert results to JSON for frontend
    return clusters_to_json(df, scope)
