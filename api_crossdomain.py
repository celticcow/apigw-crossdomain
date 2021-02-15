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

def get_domains(mds_ip):
    #static for now
    ##mds_ip = "146.18.96.16"
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
        where_used_json['cpobj'] = []

        check_host_len = len(check_host['objects'])

        if(cma == 'TestCMA'):
            print("look here break")

        if(check_host['total'] == 0):
            print("no host exist")
        else:
            for x in range(check_host['total']):
                print(check_host['objects'][x]['name'])
                print(check_host['objects'][x]['ipv4-address'])
                #this could be a problem if more than 1
                local_where_used_json = whereused_by_name(mds_ip, check_host['objects'][x]['name'], cma_sid)
                where_used_json['cpobj'].append(local_where_used_json)

        
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

    my_where_used = {}
    my_where_used['access-control-rules'] = []
    my_where_used['objects'] = []
    my_where_used['nat-rules'] = []

    try:
        dtotal = where_used_result['used-directly']['total']
        print("Total Where Used Directly : ")
        print(dtotal)

        len_obj          = len(where_used_result['used-directly']['objects'])
        len_access_rule  = len(where_used_result['used-directly']['access-control-rules'])
        len_threat_prev  = len(where_used_result['used-directly']['threat-prevention-rules'])
        len_nat_rules    = len(where_used_result['used-directly']['nat-rules'])

        if(debug == 1):
            print(len_obj)
            print(len_access_rule)
            print(len_threat_prev)
            print(len_nat_rules)

        print("Use in Object :")
        for x in range(len_obj):
            print("Use in " + where_used_result['used-directly']['objects'][x]['name'] + " which is a " + where_used_result['used-directly']['objects'][x]['type'])
            #sub_search = where_used_result['used-directly']['objects'][x]['name']
        
        my_where_used['objects'] = where_used_result['used-directly']['objects']

        rule_count = 0
        print("Use in Access Rule :")
        for x in range(len_access_rule):
            print("use in policy : " + where_used_result['used-directly']['access-control-rules'][x]['layer']['name'] + " rule-number " + where_used_result['used-directly']['access-control-rules'][x]['position'])

            tmp_uid = where_used_result['used-directly']['access-control-rules'][x]['rule']['uid']
            tmp_layer = where_used_result['used-directly']['access-control-rules'][x]['layer']['name']

            get_access_rule = {
                'uid' : tmp_uid,
                'layer' : tmp_layer
            }
            ###note.
            access_rule_result = apifunctions.api_call(mds_ip, 'show-access-rule', get_access_rule, sid)
            print("------------------------------------------------------------------")
            print(json.dumps(access_rule_result))
            print("------------------------------------------------------------------")
            #rule_output(access_rule_result)
            """
            need to sub out len_access_rule with access_rule_result
            """
            """
            try:
                get_rule(access_rule_result)
            except:
                print("error getting rule ... what happened BREAK_2")
                pass
            """
            rule_count += 1
            my_where_used['access-control-rules'].append(access_rule_result)
        
        print("Rule Total : " + str(rule_count))

        print("Use in Threat Prevention Rules :")
        for x in range(len_threat_prev):
            print("feature not avaliable.  send greg what you searched for")
        
        print("Use in Nat Rules :")
        for x in range(len_nat_rules):
            print("use in nat rules | policy " + where_used_result['used-directly']['nat-rules'][x]['package']['name'] + " nat-rule number " + where_used_result['used-directly']['nat-rules'][x]['position'])
            print("HERE LOOK HERE\n\n\n")

            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print(where_used_result['used-directly']['nat-rules'][x])
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            
            ### need to work on this
            tmp_uid = where_used_result['used-directly']['nat-rules'][x]['rule']['uid']
            ## note2
            tmp_package = where_used_result['used-directly']['nat-rules'][x]['package']['name']

            get_nat_rule = {
                'uid' : tmp_uid,
                'package' : tmp_package
            }
            nat_rule_result = apifunctions.api_call(mds_ip, 'show-nat-rule', get_nat_rule, sid)
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print(json.dumps(nat_rule_result))
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

            my_where_used['nat-rules'].append(nat_rule_result)
            
    except:
        pass

    print("__________________________________________")
    print(json.dumps(my_where_used))
    print(len(my_where_used['objects']))
    print(len(my_where_used['access-control-rules']))
    print(len(my_where_used['nat-rules']))
    print("__________________________________________")

    ##return(where_used_result)
    return(my_where_used)
#end of where_used

###
# don't need ??
###
def get_rule(access_rule_result):
    print("in get_rule")
    debug = 1
    out = "\n"

    print("#####################", end=out)
    if(debug == 1):
        print(json.dumps(access_rule_result), end=out)
    
    s_len = len(access_rule_result['source'])
    d_len = len(access_rule_result['destination'])
    p_len = len(access_rule_result['service'])

    if(debug == 1):
        print(access_rule_result['source'], end=out)
        print("++", end=out)
        print(access_rule_result['destination'], end=out)
        print("++", end=out)
        print(access_rule_result['service'], end=out)
        print("++", end=out)
        print("#####################", end=out)
        #print(s_len) #+ "  " + d_len + "  " + p_len, end=out)

    print("SOURCE:", end=out)
    for x in range(s_len):
        #print(out)
        print(access_rule_result['source'][x]['name'], end=" : ")
        print(access_rule_result['source'][x]['type'], end=out)
        #print("______________________", end=out)
    
    print("DESTINATION:", end=out)
    for x in range(d_len):
        #print(out)
        print(access_rule_result['destination'][x]['name'], end=" : ")
        print(access_rule_result['destination'][x]['type'], end=out)
    
    print("PORTS:", end=out)
    for x in range(p_len):
        #print(out)
        print(access_rule_result['service'][x]['name'], end=out)
        #print(access_rule_result['service'][x]['type'], end=out)

    print("++++++++++++++++++++++", end=out)
#end of rule_output


@app.route('/crossdomain', methods=['POST'])
def crossdomain():

    mds_ip = "192.168.159.150"

    domain_list = get_domains(mds_ip)

    crossdomain_json = {}

    ip_2_find_json = request.get_json(force=True)  #"146.18.2.137"

    ip_2_find = ip_2_find_json['ipaddr']

    crossdomain_json['ip-address'] = ip_2_find
    crossdomain_json['lookup'] = "where-used"
    crossdomain_json['cmas'] = []

    for i in domain_list:
        where_result_json = search_domain_4_ip(mds_ip, i, ip_2_find)

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
    app.run(host='0.0.0.0', port=4000)
#end of program