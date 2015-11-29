from sklearn.neighbors import KNeighborsClassifier

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FEATURE_COLUMNS = ['fgm', 
                'fga', 
                'fg3m', 
                'fg3a', 
                'ftm', 
                'fta',
                'oreb',
                'reb',
                'ast',
                'stl',
                'tov',
                'blk', 
                'pf',
                'pts',
                ]

CLASS_COLUMN = 'position'

def predictions_to_json(predictions):
    axes = ['G', 'G-F', 'F-G', 'F-C', 'C-F', 'C', 'F']
    seasons = [{'className': row[1]['season'], 'axes':[{'axis': axis, 'value': row[1][axis]} for axis in axes]} for row in predictions.iterrows()]
    return seasons

def predict_positions(player_name):
    df = pd.DataFrame.from_csv('positions/data/career_data.csv')
    df = df[(df['gp'] > 58)]
    df = df.dropna(subset=FEATURE_COLUMNS+[CLASS_COLUMN])

    # Run the classifier
    clf = KNeighborsClassifier(n_neighbors=10)
    training = df.drop(player_name)

    clf.fit(training[FEATURE_COLUMNS], training[CLASS_COLUMN])

    player = df.loc[player_name]
    #print clf.predict(player[FEATURE_COLUMNS])

    prediction_probabilities = clf.predict_proba(player[FEATURE_COLUMNS])
    prediction_df = pd.DataFrame(prediction_probabilities, columns=['C', 'C-F', 'F', 'F-C', 'F-G', 'G', 'G-F'])
    prediction_df['season'] = np.array(player['season_id'])

    return predictions_to_json(prediction_df)

