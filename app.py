from flask import Flask, render_template, request

import json
import pandas as pd
import os

from positions.code.classification import pos_classify
from tiers.code.cluster import cluster

app = Flask(__name__)

@app.route('/')
def index():
    return "HI"
    #return render_template('index.html')

@app.route('/tiers')
def tiers():
    return app.send_static_file('tiers.html')

@app.route('/positions')
def positions():
    return app.send_static_file('positions.html')

@app.route('/_get_all_names')
def get_all_names():
    df = pd.DataFrame.from_csv('positions/data/career_data.csv')
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

    results = cluster(year, algorithm)
    return json.dumps(results)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
