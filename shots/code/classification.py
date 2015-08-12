from sklearn.naive_bayes import GaussianNB

import pandas as pd
import numpy as np
import shotcharts as charts

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

classifier = GaussianNB()
training_proportion = 0.75

df['is_training'] = np.random.uniform(0, 1, len(df)) <= training_proportion

training_set = df[df['is_training']==True]
testing_set = df[df['is_training']==False]

trainingFeatures = training_set[feature_columns]
trainingTargets = np.array(training_set['shot_made_flag']).astype(bool)

classifier.fit(trainingFeatures, trainingTargets)

prediction_set = testing_set.copy()
prediction_set['shot_made_flag'] = classifier.predict(testing_set[feature_columns])

charts.show_comparison(prediction_set, testing_set)