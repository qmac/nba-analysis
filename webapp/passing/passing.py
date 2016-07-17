import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

import sys
import random

def strict_append(path, curr):
    path += (curr,)
    if len(path) > 3:
        path = path[1:]
    return path

def condense_dicts(dict1, dict2):
    merged = {}
    for key in dict1.keys():
        try:
            merged[key] = [dict1[key], dict2[key]]
        except KeyError:
            merged[key] = [dict1[key], 0]

    remaining = list(set(dict2.keys()) - set(dict1.keys()))
    for key in remaining:
        merged[key] = [0, dict2[key]]
    return merged

def construct_graph(df):
    graph = nx.DiGraph()
    graph.add_nodes_from(df['PLAYER_NAME_LAST_FIRST'].unique())
    passes = df.as_matrix(columns=['PLAYER_NAME_LAST_FIRST', 'PASS_TO', 'FREQUENCY'])
    graph.add_weighted_edges_from(passes, weight='label') # weight=label needed for viz
    return graph

def simulate(g, df, possessions):
    buckets = 0
    pts = {}
    asts = {}
    lineups = {}
    for i in range(possessions):
        start = np.random.choice(g.nodes())
        result = simulate_possession(g, df, None, start, ())
        buckets += result[0]
        if result[1] in pts:
            pts[result[1]] += (result[0] * 2)
        else:
            pts[result[1]] = (result[0] * 2)

        if result[2] in asts:
            asts[result[2]] += result[0]
        else:
            asts[result[2]] = result[0]

        if result[3] in lineups:
            lineups[result[3]] += (result[0] * 2)
        else:
            lineups[result[3]] = (result[0] * 2)

    return (buckets / float(possessions)), pts, asts, lineups

def simulate_possession(g, df, prev, curr, path):
    path = strict_append(path, curr)
    
    if prev is None:
        shot_prob = 0.0
    else:
        pass_row = df[((df['PLAYER_NAME_LAST_FIRST'] == prev) & (df['PASS_TO'] == curr))]
        shot_prob = pass_row['FGA'] / float(pass_row['PASS'])
        shot_prob = shot_prob.sum()
        make_prob = pass_row['FG_PCT'].sum()

    if random.random() < shot_prob:
        if random.random() < make_prob:
            return 1, curr, prev, path
        else:
            return 0, curr, prev, path
    else:
        weights = [d['label'] for (u,v,d) in g.edges(curr, data=True)]
        if len(weights) > 1:
            weights[0] = 1 - np.sum(weights[1:])
        neighbors = g.neighbors(curr)
        if len(neighbors) < 1:
            return 0, curr, prev, path
        succ = np.random.choice(neighbors, p=weights)
        return simulate_possession(g, df, curr, succ, path)

def visualize(g):
    from networkx.drawing.nx_pydot import write_dot
    nx.draw_graphviz(g)
    write_dot(g,'figures/passing_graph.dot')

def main(args):
    df = pd.read_csv('data/passing_data.csv', index_col=False)
    df = df[(df['TEAM_NAME'] == args[1])]

    g = construct_graph(df)
    game = simulate(g, df, int(args[2]))
    boxscore = condense_dicts(game[1], game[2])
    print '==============GAME SUMMARY================'
    print
    print 'FG PCT: %f' % (game[0])
    print
    print '=========================================='
    print
    print '===============BOX SCORE=================='
    print
    print 'Points\t\tAssists\t\tPlayer'
    for key in boxscore:
        print '%d\t\t%d\t\t%s' % (boxscore[key][0], boxscore[key][1], key)
    print
    print '=========================================='
    print
    print '============LINEUPS SUMMARY==============='
    for key in game[3]:
        if game[3][key] > 2:
            print key, game[3][key]
    print
    print '=========================================='
    visualize(g)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python scrape.py TEAM_NAME NUM_POSSESSIONS'
        exit(-1)
    main(sys.argv)
    