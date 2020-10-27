#!/usr/bin/python3 -W ignore::DeprecationWarning

import requests
import json
import ipaddress
import time
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

#worker functions

def get_domains():
    #static for now
    mds_ip = "146.18.96.16"
    debug = 1

    domain_list = []

    try:
        domain_sid = apifunctions.login("roapi", "1qazxsw2", mds_ip, "")
        if(debug == 1):
            print("session id : " + domain_sid)
        
        get_domain_result = apifunctions.api_call(mds_ip, "show-domains", {}, domain_sid)

        if(debug == 1):
            print(json.dumps(get_domain_result))
        
        for x in range(get_domain_result['total']):
            if(debug == 1):
                print(get_domain_result['objects'][x]['name'])
            domain_list.append(get_domain_result['objects'][x]['name'])
        
        time.sleep(3)
        logout_result = apifunctions.api_call(mds_ip, "logout", {}, domain_sid)
        if(debug == 1):
            print(logout_result)
    except:
        print("Unable to get Domain_List")
    
    return(domain_list)
#end_of_get_domains


@app.route('/crossdomain') #, methods=['POST'])
def crossdomain():
    domain_list = get_domains()

    #dummy return var
    return({"t1" : 0})

if __name__ == '__main__':
    app.run()