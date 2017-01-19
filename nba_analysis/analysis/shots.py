from nba_analysis.analysis import compare_classifiers
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

FEATURE_COLUMNS = ['period', 
                'shot_dist', 
                'dribbles', 
                'touch_time', 
                'close_def_dist', 
                'shot_clock'
                ]

CLASS_COLUMN = 'fgm'

def clean(df):
    df = df.dropna(subset=FEATURE_COLUMNS)
    df['location'] = (df['location'] == 'H').astype(int)
    return df

def classify_player_shots(df, player_name, algorithm='SVC', num_shots=100):
    df = clean(df)
    testing_set = df.sample(n=num_shots)
    training_set = df[(df['player_name'] == player_name)]

    features = training_set[FEATURE_COLUMNS]
    targets = np.array(training_set[CLASS_COLUMN]).astype(bool)

    clf = eval(algorithm)()
    if algorithm == 'SVC':
        clf.probability = True
    clf.fit(features, targets)

    prediction_set = testing_set.copy()
    prediction_set[CLASS_COLUMN] = clf.predict(testing_set[FEATURE_COLUMNS])

    return prediction_set

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python shots.py player_name'
        exit(-1)
    
    original = pd.DataFrame.from_csv('./../data/shot_data.csv')
    df = clean(original)
    df = df[(df['player_name'] == sys.argv[1])]
    data = df[FEATURE_COLUMNS]
    targets = df[CLASS_COLUMN]
    alg, score = compare_classifiers(data, targets)
    print 'Using %s which got an accuracy of %f' % (alg, score)
    print classify_player_shots(original, sys.argv[1], algorithm=alg)

