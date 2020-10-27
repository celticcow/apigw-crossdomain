#!/usr/bin/python3 -W ignore::DeprecationWarning

import requests
import json
import ipaddress
import apifunctions

from flask import Flask, request
from flask_json import FlaskJSON, JsonError, json_response, as_json


#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
pip install Flask-JSON
apt-get install python3-flask
"""


"""
api gw for crossdomain
"""

app = Flask(__name__)
FlaskJSON(app)

@app.route('/crossdomain', methods=['POST'])
def crossdomain():
    pass

if __name__ == '__main__':
    app.run()