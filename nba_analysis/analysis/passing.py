import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph

import sys

def construct_graph(df):
    graph = nx.DiGraph()
    players = df['PLAYER_NAME_LAST_FIRST'].unique()
    graph.add_nodes_from(players)
    for p in players:
        player_df = df[df['PLAYER_NAME_LAST_FIRST'] == p]
        passes = player_df.as_matrix(columns=['PLAYER_NAME_LAST_FIRST', 
            'PASS_TO', 'FREQUENCY'])
        # Normalize to account for trades
        passes[:,[2]] = passes[:,[2]] / passes[:,[2]].sum()
        graph.add_weighted_edges_from(passes, weight='label')
    
    # twos = df['FG2A']
    # thress = df['FG3A']
    return graph

def get_passing_info(df, team):
    df = df[df['TEAM_NAME'] == team]
    g = construct_graph(df)
    return json_graph.node_link_data(g)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python scrape.py team'
        exit(-1)

    df = pd.DataFrame.from_csv('./../data/passing_data.csv')
    df = df[df['TEAM_NAME'] == sys.argv[1]]
    construct_graph(df)
    print 'Drawing passing graph using matplotlib'
    nx.draw(construct_graph(df))
    plt.show()
    print 'Must use web app to run possession simulation'
    