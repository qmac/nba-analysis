from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

import json
import pandas as pd
import os

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
db_engine = db.get_engine(app)

from .positions.code.classification import pos_classify
from .tiers.code.cluster import cluster as tier_cluster
from .styles.code.cluster import cluster as style_cluster

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

@app.route('/_get_all_names')
def get_all_names():
    df = pd.DataFrame.from_csv('webapp/positions/data/career_data.csv')
    names_json = [{'name':name} for name in df.index.unique()]
    return json.dumps(names_json)

@app.route('/_get_positions')
def get_positions():
    player = request.args.get('player')
    algorithm = request.args.get('algorithm')

    results = pos_classify(player, algorithm)
    return json.dumps(results)

@app.route('/_get_tiers')
def get_tiers():
    year = request.args.get('year')
    algorithm = request.args.get('algorithm')

    results = tier_cluster(year, algorithm)
    return json.dumps(results)

@app.route('/_get_styles')
def get_styles():
    scope = request.args.get('scope')

    results = style_cluster(scope)
    return json.dumps(results)
