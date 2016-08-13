from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation

import pandas as pd

df = pd.read_csv('playtype_data.csv')
clstr = AffinityPropagation()
team_df = df.drop('Player', 1).groupby('Team').mean()
clstr.fit(df.drop(['Player', 'Team'], 1))
#clstr.fit(team_df)
#team_df['cluster'] = clstr.labels_
#team_df.sort('cluster').to_csv('results.csv')
df['cluster'] = clstr.labels_
df.to_csv('player_results.csv')