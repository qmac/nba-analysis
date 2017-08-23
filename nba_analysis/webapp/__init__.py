from nba_analysis.analysis.positions import classify_player_position
from nba_analysis.analysis.tiers import cluster as tier_cluster
from nba_analysis.analysis.styles import cluster as style_cluster
from nba_analysis.analysis.passing import (get_passing_info,
                                           get_usage_clusters,
                                           get_passing_clusters)
from nba_analysis import config

from flask import Flask, render_template, request, json
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

import pandas as pd
import os

app = Flask(__name__)
Bootstrap(app)
if 'DATABASE_URL' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    db = SQLAlchemy(app)
    db_engine = db.get_engine(app)
else:
    db_engine = None


def get_data_source(table_name):
    if config.data_source == 'sql':
        return pd.read_sql(table_name, db_engine)
    elif config.data_source == 'local':
        return pd.DataFrame.from_csv('nba_analysis/data/%s.csv' % table_name, encoding='utf-8')
    else:
        raise Exception('Invalid data source configuration')


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/tiers')
def tiers():
    return render_template('tiers.html')


@app.route('/positions')
def positions():
    return render_template('positions.html')


@app.route('/styles')
def styles():
    return render_template('styles.html')


@app.route('/passing')
def passing():
    return render_template('passing.html')


@app.route('/_get_all_names')
def get_all_names():
    df = get_data_source('career_data')
    names_json = [{'name': name} for name in df['name'].unique()]
    return json.dumps(names_json)


@app.route('/_get_passing')
def get_passing():
    team = request.args.get('team')

    df = get_data_source('passing_data')
    graph_json, shots = get_passing_info(df, team)
    packaged_json = {'graph': graph_json, 'shot_probs': shots}
    return json.dumps(packaged_json)


@app.route('/_get_pass_clusters')
def get_pass_clusters():
    clst_type = request.args.get('type')
    team = request.args.get('team')
    df = get_data_source('passing_data')

    if clst_type == 'usage':
        results = get_usage_clusters(df, team)
    elif clst_type == 'passing':
        results = get_passing_clusters(df, team)
    results = {'clusters': results.tolist()}
    return json.dumps(results)


@app.route('/_get_positions')
def get_positions():
    player = request.args.get('player')
    algorithm = request.args.get('algorithm')

    df = get_data_source('career_data')
    results = classify_player_position(df, player, algorithm=algorithm)
    return json.dumps(results)


@app.route('/_get_tiers')
def get_tiers():
    year = request.args.get('year')
    algorithm = request.args.get('algorithm')

    df = get_data_source('advanced_stats')
    results = tier_cluster(df, year, algorithm=algorithm)
    return json.dumps(results)


@app.route('/_get_styles')
def get_styles():
    scope = request.args.get('scope')

    df = get_data_source('playtype_data')
    results = style_cluster(df, scope)
    return json.dumps(results)
