from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

feature_columns = ['fgm', 
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

class_column = 'position'

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