from sklearn.neighbors import KNeighborsClassifier
from positionchart import radar_graph

import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV
df = pd.DataFrame.from_csv('./../data/stats.dat', sep=' ')

# Remove outliers
df = df[(df['pos'] != '??') & (df['pts'] > 100)]

# Run the classifier
clf = KNeighborsClassifier(n_neighbors=10)
training = df.drop('ginobili,manu')

clf.fit(training.drop('pos', 1), training['pos'])

player = df.loc['ginobili,manu']
print clf.predict(player.drop('pos', 1))

prediction_probabilities = clf.predict_proba(player.drop('pos', 1))
print prediction_probabilities

# These have to be hard coded since year info is not in the data set
years = ['2004-2005', '2005-2006', '2006-2007', '2007-2008', '2008-2009', '2009-2010', '2010-2011', '2011-2012', '2012-2013']


for i in range(len(prediction_probabilities)):
    labels = ['C', 'PF', 'PG', 'SF', 'SG']
    values = prediction_probabilities[i]
    optimum = [1.0, 1.0, 1.0, 1.0, 1.0]

    radar_graph(labels, values, optimum)

    plt.suptitle('Manu Ginobili %s' % (years[i]))
    plt.savefig('./../figures/manu_ginobili_%s' % (years[i]))
    plt.show()