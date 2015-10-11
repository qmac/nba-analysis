from sklearn.neighbors import KNeighborsClassifier
from positionchart import radar_graph

import pandas as pd
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

# Run the classifier
clf = KNeighborsClassifier(n_neighbors=10)
training = df.drop('Ginobili, Manu')

clf.fit(training[feature_columns], training[class_column])

player = df.loc['Ginobili, Manu']
print clf.predict(player[feature_columns])

prediction_probabilities = clf.predict_proba(player[feature_columns])
print prediction_probabilities

years = player['season_id']

for i in range(len(prediction_probabilities)):
    labels = ['C', 'C-F', 'F', 'F-C', 'F-G', 'G', 'G-F']
    values = prediction_probabilities[i]
    optimum = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    radar_graph(labels, values, optimum)

    plt.suptitle('Manu Ginobili %s' % (years[i]))
    plt.savefig('./../figures/manu_ginobili_%s' % (years[i]))
    plt.show()