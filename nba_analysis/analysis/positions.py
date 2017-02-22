from nba_analysis.analysis import compare_classifiers
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

FEATURE_COLUMNS = ['FGM', 
                'FGA', 
                'FG3M', 
                'FG3A', 
                'FTM', 
                'FTA',
                'OREB',
                'REB',
                'AST',
                'STL',
                'TOV',
                'BLK', 
                'PF',
                'PTS'
                ]

CLASS_COLUMN = 'position'

def predictions_to_json(predictions):
    axes = ['G', 'G-F', 'F-G', 'F-C', 'C-F', 'C', 'F']
    seasons = [{'className': row[1]['season'], 
                'axes':[{'axis': axis, 'value': row[1][axis]} for axis in axes]} 
                for row in predictions.iterrows()]
    return seasons

def classify_player_position(df, player_name, algorithm='SVC'):
    df = df.dropna(subset=FEATURE_COLUMNS+[CLASS_COLUMN])
    training = df[df['name'] != player_name]
    testing = df[df['name'] == player_name]

    # Train the classifier
    clf = eval(algorithm)()
    if algorithm == 'SVC':
        clf.probability = True
    clf.fit(training[FEATURE_COLUMNS], training[CLASS_COLUMN])

    # Run the classifier
    prediction_probabilities = clf.predict_proba(testing[FEATURE_COLUMNS])

    # Convert to JSON for frontend
    prediction_df = pd.DataFrame(prediction_probabilities, columns=['C', 'C-F', 'F', 'F-C', 'F-G', 'G', 'G-F'])
    prediction_df['season'] = np.array(testing['SEASON_ID'])
    return predictions_to_json(prediction_df)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python positions.py player_name'
        exit(-1)
    
    df = pd.DataFrame.from_csv('./../data/career_data.csv')
    df = df.dropna(subset=FEATURE_COLUMNS+[CLASS_COLUMN])
    data = df[FEATURE_COLUMNS]
    targets = df[CLASS_COLUMN]
    alg, score = compare_classifiers(data, targets)
    print 'Using %s which got an accuracy of %f' % (alg, score)
    print classify_player_position(df, sys.argv[1], algorithm=alg)

