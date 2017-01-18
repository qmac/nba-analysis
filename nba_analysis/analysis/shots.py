from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shotcharts as charts

FEAUTURE_COLUMNS = ['location', 
                'period', 
                'shot_dist', 
                'dribbles', 
                'touch_time', 
                'close_def_dist', 
                'shot_clock'
                ]

CLASS_COLUMN = 'fgm'

def classify_player_shots(player_name, algorithm):
    # TODO: change structure to be classify on random shots
    df = pd.DataFrame.from_csv('./../data/shot_data.csv')
    df = df[(df['player_name'] == player_name)]
    df = df.dropna(subset=feature_columns)
    df['location'] = (df['location'] == 'H').astype(int)

    classifier = eval(algorithm)()
    training_proportion = 0.75

    df['is_training'] = np.random.uniform(0, 1, len(df)) <= training_proportion

    training_set = df[df['is_training']==True]
    testing_set = df[df['is_training']==False]

    trainingFeatures = training_set[feature_columns]
    trainingTargets = np.array(training_set[class_column]).astype(bool)

    classifier.fit(trainingFeatures, trainingTargets)

    prediction_set = testing_set.copy()
    prediction_set[class_column] = classifier.predict(testing_set[feature_columns])

    return prediction_set

def compare_classifiers():
    df = pd.DataFrame.from_csv('./../data/shot_data.csv')
    #df = df[(df['player_name'] == 'Curry, Stephen')]
    df = df[(df['player_team'] == 'GSW')]
    df = df.dropna(subset=feature_columns)
    df['location'] = (df['location'] == 'H').astype(int)

    data = df[FEATURE_COLUMNS]
    targets = df[CLASS_COLUMN]

    classifiers = [GaussianNB(), SVC(), KNeighborsClassifier(), DecisionTreeClassifier()]

    for clf in classifiers:
        score = cross_val_score(clf, data, targets, cv=10)
        print '------------------------------------------'
        print '%s got a 10-fold cross-validation score of %f' % (clf, score)

