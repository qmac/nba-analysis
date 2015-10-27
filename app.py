from flask import Flask, render_template, request, jsonify

import json

import sys
sys.path.append('positions/code/')
import classification

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
	results = classification.predict_positions(player)
	return json.dumps(results)

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("8000"),
        debug=False
    )