from sklearn.neighbors import KNeighborsClassifier

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import visualization

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

# Run the classifier
clf = KNeighborsClassifier(n_neighbors=10)
training = df.drop('Ginobili, Manu')

clf.fit(training[feature_columns], training[class_column])

player = df.loc['Ginobili, Manu']
print clf.predict(player[feature_columns])

prediction_probabilities = clf.predict_proba(player[feature_columns])
prediction_df = pd.DataFrame(prediction_probabilities, columns=['C', 'C-F', 'F', 'F-C', 'F-G', 'G', 'G-F'])
prediction_df['season'] = np.array(player['season_id'])
print prediction_df

visualization.predictions_to_json(prediction_df)

