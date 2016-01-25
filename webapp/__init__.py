from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

import json
import pandas as pd
import os

from .positions.code import classification as pos_classification
from .tiers.code import cluster as clstr

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
db_engine = db.get_engine(app)

@app.route('/')
def index():
    return "HI"

@app.route('/tiers')
def tiers():
    return app.send_static_file('tiers.html')

@app.route('/positions')
def positions():
    return app.send_static_file('positions.html')

@app.route('/_get_positions')
def run_positions():
    player = request.args.get('player')
    results = pos_classification.predict_positions(player)
    return json.dumps(results)

@app.route('/_get_all_names')
def get_all_names():
    df = pd.DataFrame.from_csv('webapp/positions/data/career_data.csv')
    names_json = [{'name':name} for name in df.index.unique()]
    return json.dumps(names_json)

@app.route('/_get_tiers')
def get_tiers():
    year = request.args.get('year')
    tiers_results = clstr.run_clustering(year)
    return json.dumps(tiers_results)
