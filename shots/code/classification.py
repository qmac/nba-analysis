from sklearn.naive_bayes import GaussianNB

import pandas as pd
import numpy as np
import shotcharts as charts

feature_columns = ['location', 
                'period', 
                'shot_dist', 
                'dribbles', 
                'touch_time', 
                'close_def_dist', 
                'shot_clock'
                ]

class_column = 'fgm'

df = pd.DataFrame.from_csv('./../data/shot_data.csv')
df = df[(df['player_name'] == 'Curry, Stephen')]
df = df.dropna(subset=feature_columns)
df['location'] = (df['location'] == 'H').astype(int)

classifier = GaussianNB()
training_proportion = 0.75

df['is_training'] = np.random.uniform(0, 1, len(df)) <= training_proportion

training_set = df[df['is_training']==True]
testing_set = df[df['is_training']==False]

trainingFeatures = training_set[feature_columns]
trainingTargets = np.array(training_set[class_column]).astype(bool)

classifier.fit(trainingFeatures, trainingTargets)

prediction_set = testing_set.copy()
prediction_set[class_column] = classifier.predict(testing_set[feature_columns])

#charts.show_comparison(prediction_set, testing_set)