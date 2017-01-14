from sklearn import metrics
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

def classify_player_position(player_name, algorithm):
    # Load data from CSV
    df = pd.DataFrame.from_csv('webapp/positions/data/career_data.csv')

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

def compare_classifiers():
    df = pd.DataFrame.from_csv('./../data/career_data.csv')
    df = df[(df['gp'] > 58)]
    df = df.dropna(subset=feature_columns+[class_column])

    classifiers = [GaussianNB(), SVC(), KNeighborsClassifier(), DecisionTreeClassifier()]
    training_range = np.arange(0.50, 0.90, 0.02)
    results = dict((clf, dict((tr, 0) for tr in training_range)) for clf in classifiers)
    n_trials = 30

    for i in training_range:
        for j in range(n_trials):
            df['is_training'] = np.random.uniform(0, 1, len(df)) <= i
            training_set = df[df['is_training']==True]
            testing_set = df[df['is_training']==False]

            trainingFeatures = training_set[feature_columns]
            trainingTargets = training_set[class_column]

            testingFeatures = testing_set[feature_columns]
            testingTargets = testing_set[class_column]

            for classifier in classifiers:
                print "------------------------------------------"
                print classifier

                classifier.fit(trainingFeatures, trainingTargets)
                results[classifier][i] += classifier.score(testingFeatures, testingTargets)

                predictions = classifier.predict(testingFeatures)
                print metrics.classification_report(testingTargets, predictions)

    for classifier in classifiers:
        plt.plot(training_range, [(results[classifier][d]/float(n_trials)) for d in training_range], label=type(classifier))
        
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.03), ncol=2)
    plt.show()

