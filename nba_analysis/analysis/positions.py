from nba_analysis.analysis import compare_classifiers
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

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

def clean(df):
    df = df[(df['gp'] > 58)]
    df = df.dropna(subset=FEATURE_COLUMNS+[CLASS_COLUMN])
    return df

def predictions_to_json(predictions):
    axes = ['G', 'G-F', 'F-G', 'F-C', 'C-F', 'C', 'F']
    seasons = [{'className': row[1]['season'], 'axes':[{'axis': axis, 'value': row[1][axis]} for axis in axes]} for row in predictions.iterrows()]
    return seasons

def classify_player_position(df, player_name, algorithm='SVC'):
    df = clean(df)
    training = df.drop(player_name)

    # Train the classifier
    clf = eval(algorithm)()
    if algorithm == 'SVC':
        clf.probability = True
    clf.fit(training[FEATURE_COLUMNS], training[CLASS_COLUMN])

    # Run the classifier
    player = df.loc[player_name]
    prediction_probabilities = clf.predict_proba(player[FEATURE_COLUMNS])

    # Convert to JSON for frontend
    prediction_df = pd.DataFrame(prediction_probabilities, columns=['C', 'C-F', 'F', 'F-C', 'F-G', 'G', 'G-F'])
    prediction_df['season'] = np.array(player['season_id'])
    return predictions_to_json(prediction_df)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python positions.py player_name'
        exit(-1)
    
    original = pd.DataFrame.from_csv('./../data/career_data.csv')
    df = clean(original)
    data = df[FEATURE_COLUMNS]
    targets = df[CLASS_COLUMN]
    alg, score = compare_classifiers(data, targets)
    print 'Using %s which got an accuracy of %f' % (alg, score)
    print classify_player_position(original, sys.argv[1], algorithm=alg)

