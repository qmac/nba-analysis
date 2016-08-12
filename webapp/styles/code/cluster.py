from sklearn.cluster import KMeans

import pandas as pd

df = pd.read_csv('playtype_data.csv')
clstr = KMeans(10)
clstr.fit(df.drop('Player', 1))
df['cluster'] = clstr.labels_
df[['Player', 'cluster']].sort('cluster').to_csv('results.csv')