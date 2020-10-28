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

### search domain
def search_domain_4_ip(mds_ip, cma, ip_2_find):
    debug = 1

    try:
        cma_sid = apifunctions.login("roapi", "1qazxsw2", mds_ip, cma)

        if(debug == 1):
            print("session id : " + cma_sid)
        
        check_host_obj = {"type" : "host", "filter" : ip_2_find, "ip-only" : "true"}
        check_host = apifunctions.api_call(mds_ip, "show-objects", check_host_obj, cma_sid)

        print("here")
        print(check_host)

        where_used_json = {}

        check_host_len = len(check_host['objects'])
        if(check_host['total'] == 0):
            print("no host exist")
        else:
            for x in range(check_host['total']):
                print(check_host['objects'][x]['name'])
                print(check_host['objects'][x]['ipv4-address'])
                where_used_json = whereused_by_name(mds_ip, check_host['objects'][x]['name'], cma_sid)
        
        time.sleep(3)
        logout_result = apifunctions.api_call(mds_ip, "logout", {}, cma_sid)
        if(debug == 1):
            print(logout_result)
        
    except:
        if(cma_sid != ""):
            emergency_logout = apifunctions.api_call(mds_ip, "logout", {}, cma_sid)
        print("no login to cma")
    
    return(where_used_json)
#end_of_search_domain_4_ip

##where used by name
def whereused_by_name(mds_ip, name, sid):
    debug = 1

    if(debug == 1):
        print("in whereused function")

    search_where_json = {
        "name" : name
    }

    where_used_result = apifunctions.api_call(mds_ip, "where-used", search_where_json, sid)

    if(debug == 1):
        print("^^^^^^^^^^^^^^^^^^^^")
        print(json.dumps(where_used_result))
        print("!!!!!!!!!!!!!!!!!!!!")
    
    return(where_used_result)
#end of where_used


@app.route('/crossdomain', methods=['POST'])
def crossdomain():
    domain_list = get_domains()

    crossdomain_json = {}

    ip_2_find_json = request.get_json(force=True)  #"146.18.2.137"

    ip_2_find = ip_2_find_json['ipaddr']

    crossdomain_json['ip-address'] = ip_2_find
    crossdomain_json['lookup'] = "where-used"
    crossdomain_json['cmas'] = []

    for i in domain_list:
        where_result_json = search_domain_4_ip("146.18.96.16", i, ip_2_find)

        tmp = {}
        tmp['cma'] = i
        tmp['whereused'] = where_result_json
        crossdomain_json['cmas'].append(tmp)
        ##crossdomain_json[i] = "info" + str(i)

    crossdomain_json['total'] = len(crossdomain_json['cmas'])
    #dummy return var
    #return({"t1" : 0})
    return(crossdomain_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0')