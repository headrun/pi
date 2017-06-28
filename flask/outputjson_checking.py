from flask import Flask, render_template
from flask import request
import datetime
import os
import json
from flask import jsonify
import requests
from scrapy.selector import Selector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    email = request.form['email']
    if email:
        output = open('google.json', 'r').read()
        output = json.loads(output)
        return jsonify(output)
if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=8559, debug=True)


