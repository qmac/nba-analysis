from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame.from_csv('./../data/steph_shots.csv')

feature_columns = ['period', 
				'minutes_remaining', 
				'shot_distance', 
				'x', 
				'y', 
				'dribbles', 
				'touch_time', 
				'defender_distance', 
				'shot_clock'
				]

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
		trainingTargets = np.array(training_set['shot_made_flag']).astype(bool)

		testingFeatures = testing_set[feature_columns]
		testingTargets = np.array(testing_set['shot_made_flag']).astype(bool)

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