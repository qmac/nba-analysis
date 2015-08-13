from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import visualization

DEFAULT_K = 11 # Rule of thumb k (k=sqrt(n/2))

# Elbow Method for determining k
def plot_inertias(cluster_data):
    inertias = []
    for k in range(2, 100):
        clstr = KMeans(n_clusters=k, random_state=42)
        clstr.fit(cluster_data)
        inertias.append(clstr.inertia_)

    plt.figure(0)
    plt.plot(inertias)
    plt.savefig('./../figures/inertias.png')

# Silhouette Method for determining k 
def plot_silhouettes(cluster_data):
    silhouettes = []
    for k in range(2, 100):
        clstr = KMeans(n_clusters=k, random_state=42)
        cluster_labels = clstr.fit_predict(cluster_data)
        silhouette = silhouette_score(cluster_data, cluster_labels)
        silhouettes.append(silhouette)

    plt.figure(1)
    plt.plot(silhouettes)
    plt.savefig('./../figures/silhouettes.png')

def cluster(cluster_data):
    clstr = KMeans(n_clusters=11)
    clstr.fit(fitting_data)

    df['tier'] = clstr.labels_
    results = df[['Player', 'tier']]

    results.to_csv('./../visualization/results.csv')
    return results

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
clustered_players = cluster(fitting_data)

# Set up for visualization
visualization.scrape_pictures(clustered_players)
visualization.clusters_to_json(clustered_players)
