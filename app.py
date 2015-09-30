from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
	return "HI"
    #return render_template('index.html')

@app.route('/tiers')
def tiers():
	return app.send_static_file('tiers.html')

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("8000"),
        debug=False
    )