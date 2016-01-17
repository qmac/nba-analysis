from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

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

def pos_classify(player_name, algorithm):
    # Load data from CSV
    df = pd.DataFrame.from_csv('positions/data/career_data.csv')

    # Remove outliers and empty entries
    df = df[(df['gp'] > 58)]
    df = df.dropna(subset=FEATURE_COLUMNS+[CLASS_COLUMN])

    # Set up training data
    training = df.drop(player_name)

    # Initialize the classifier
    clf = eval(algorithm)()
    if algorithm == 'SVC':
        clf.probability = True

    # Perform classifier training
    clf.fit(training[FEATURE_COLUMNS], training[CLASS_COLUMN])

    # Run the classifier
    player = df.loc[player_name]
    prediction_probabilities = clf.predict_proba(player[FEATURE_COLUMNS])

    # Convert to JSON for frontend
    prediction_df = pd.DataFrame(prediction_probabilities, columns=['C', 'C-F', 'F', 'F-C', 'F-G', 'G', 'G-F'])
    prediction_df['season'] = np.array(player['season_id'])
    return predictions_to_json(prediction_df)

