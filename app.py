from flask import Flask, render_template, request

import json
import pandas as pd
import os

#import positions.code.classification as pos_classification

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

@app.route('/_get_positions')
def run_positions():
    player = request.args.get('player')
    results = pos_classification.predict_positions(player)
    return json.dumps(results)

@app.route('/_get_all_names')
def get_all_names():
    df = pd.DataFrame.from_csv('positions/data/career_data.csv')
    names_json = [{'name':name} for name in df.index.unique()]
    return json.dumps(names_json)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=int("33507"), debug=False)