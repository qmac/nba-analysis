from sklearn.cluster import KMeans

import pandas as pd
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

clstr = KMeans(n_clusters=9)
clstr.fit(fitting_data)

df['tier'] = clstr.labels_

results = df[['Player', 'tier']]
print results['tier'].value_counts()

results.to_csv('results.csv')