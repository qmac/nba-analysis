from sklearn.neighbors import KNeighborsClassifier

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data from CSV
df = pd.DataFrame.from_csv('./../data/stats.dat', sep=' ')

# Remove outliers
df = df[(df['pos'] != '??') & (df['pts'] > 100)]

# Run the classifier
clf = KNeighborsClassifier()
training = df.drop('ginobili,manu')

clf.fit(training.drop('pos', 1), training['pos'])
print clf.score(training.drop('pos', 1), training['pos'])

player = df.loc['ginobili,manu']
print clf.predict(player.drop('pos', 1))