from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.metrics import pairwise_distances

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data from CSV
df = pd.DataFrame.from_csv('./../data/leagues_NBA_2015_advanced.csv')

# Remove outliers
df = df[(df['G'] >= 58)]

feature_columns = [
				'PER', 
				'TS%', 
				'USG%', 
				'WS/48', 
				'BPM'
				]

fitting_data = df[feature_columns]

# Elbow Method for determining k
# inertias = []
# for k in range(2, 100):
# 	clstr = KMeans(n_clusters=k)
# 	clstr.fit(fitting_data)
# 	inertias.append(clstr.inertia_)
# 	print clstr.inertia_
# plt.plot(inertias)
# plt.show()

# Silhouette Method for determining k 
silhouettes = []
for k in range(8, 100):
	clstr = KMeans(n_clusters=k)
	clstr.fit(fitting_data)
	labels = clstr.labels_
	sscore = metrics.silhouette_score(fitting_data, labels, metric='euclidean')
	print sscore
	silhouettes.append(sscore)
plt.plot(silhouettes)
plt.show()

'''
clstr = KMeans(n_clusters=91) # Using rule of thumb (k=sqrt(n/2))
clstr.fit(fitting_data)

df['tier'] = clstr.labels_

results = df[['Player', 'tier']]
print results['tier'].value_counts()

results.to_csv('results.csv')
'''
