from flask import Flask, render_template
from flask.ext.triangle import Triangle

app = Flask(__name__)
Triangle(app)

@app.route('/')
def main():
    return render_template('stats_calculator.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8555, debug=True)

