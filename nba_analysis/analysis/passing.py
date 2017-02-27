import pandas as pd
import networkx as nx
from networkx.readwrite import json_graph

import sys

def construct_graph(df):
    graph = nx.DiGraph()
    graph.add_nodes_from(df['PLAYER_NAME_LAST_FIRST'].unique())
    passes = df.as_matrix(columns=['PLAYER_NAME_LAST_FIRST', 'PASS_TO', 'FREQUENCY'])
    twos = df['FG2A']
    thress = df['FG3A']
    # Add make and miss shots
    graph.add_weighted_edges_from(passes, weight='label')
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
    print 'Drawing passing graph using matplotlib'
    nx.draw(construct_graph(df))
    print 'Must use web app to run possession simulation'
    