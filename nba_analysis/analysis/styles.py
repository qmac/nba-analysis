from sklearn.cluster import AffinityPropagation
import pandas as pd
import sys

FEATURES = ['Transition', 'Isolation', 'PRBallHandler', 'PRRollMan',
            'Postup', 'Spotup', 'Handoff', 'Cut', 'OffScreen', 'OffRebound']


def clusters_to_json(df, scope):
    # Converts clusters into dictionary compatible for visualization
    vectors_df = df[FEATURES]
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


def cluster(df, scope):
    # Performs clustering
    # Manipulate data into scope
    if scope == 'Team':
        df = df.drop('Player', 1).groupby('Team', as_index=False).mean()
    elif scope == 'Player':
        df = df.drop('Team', 1)

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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python styles.py scope'
        exit(-1)

    df = pd.DataFrame.from_csv('./../data/playtype_data.csv')
    print cluster(df, sys.argv[1])
