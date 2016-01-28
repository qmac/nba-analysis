from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import json

DEFAULT_K = 11 # Rule of thumb k (k=sqrt(n/2))
SIZE = 2000 # Size of tier bubbles
FEATURE_COLUMNS = [
                    'PIE', 
                    'TS_PCT', 
                    'NET_RATING', 
                    'USG_PCT'
                    ]

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

def clusters_to_json(player_clusters):
    players_dict = {}
    players_grouped = player_clusters.groupby('tier')
    players_dict['name'] = 'vis'
    players_dict['children'] = map(lambda x:{'name':'Tier %d' % (x[0]), 'children':map(lambda x:{'name':x, 'size':SIZE}, x[1]['PLAYER_NAME'])}, players_grouped)
    print players_dict
    return players_dict

def cluster(year, algorithm):
    # Load data from CSV
    df = pd.DataFrame.from_csv('webapp/tiers/data/advanced_stats_%s.csv' % (year))

    # Remove outliers
    df = df[(df['GP'] >= (0.7 * df['GP'].max()))]

    # Set up fitting data
    fitting_data = df[FEATURE_COLUMNS]
    fitting_data = (fitting_data - fitting_data.mean()) / (fitting_data.max() - fitting_data.min())

    # Run clustering
    clstr = eval(algorithm)(n_clusters=DEFAULT_K)
    clstr.fit(fitting_data)

    # Convert results to JSON for frontend
    df['tier'] = clstr.labels_
    clustered_players = df[['PLAYER_NAME', 'tier']]
    return clusters_to_json(clustered_players)
