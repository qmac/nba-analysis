from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

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
inertias = []
for k in range(2, 100):
	clstr = KMeans(n_clusters=k, random_state=42)
	clstr.fit(fitting_data)
	inertias.append(clstr.inertia_)

plt.plot(inertias)
plt.savefig('./../figures/inertias.png')

# Silhouette Method for determining k 
silhouettes = []
for k in range(2, 100):
	clstr = KMeans(n_clusters=k, random_state=42)
	cluster_labels = clstr.fit_predict(fitting_data)
	silhouette = silhouette_score(fitting_data, cluster_labels)
	silhouettes.append(silhouette)

plt.plot(silhouettes)
plt.savefig('./../figures/silhouettes.png')

'''
clstr = KMeans(n_clusters=11) # Using rule of thumb (k=sqrt(n/2))
clstr.fit(fitting_data)

df['tier'] = clstr.labels_

results = df[['Player', 'tier']]
print results['tier'].value_counts()

results.to_csv('results.csv')
'''
