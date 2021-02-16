#!/usr/bin/python3 -W ignore::DeprecationWarning

import requests
import json
import ipaddress
import time
import apifunctions

#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_domains(mds_ip):
    #static for now
    ##mds_ip = "146.18.96.16"
    debug = 0

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


def search_cma(mds, cma, host_ip):
    debug = 0
    print("searching cma")

    check_host_ip_json = {"type" : "host", "filter" : host_ip, "ip-only" : "true"}
    check_range_ip_json = {"type" : "address-range", "filter" : host_ip, "ip-only" : "true"}

    name_list = list()

    try:
        cma_sid = apifunctions.login("roapi", "1qazxsw2", mds, cma)

        check_host  = apifunctions.api_call(mds, "show-objects", check_host_ip_json, cma_sid)
        check_range = apifunctions.api_call(mds, "show-objects", check_range_ip_json, cma_sid)

        if(debug == 1):
            print("Results to parse")
            print(check_host)
            print("++++++++++++++")
            print(check_range)
            print("____________________")

        for i in range(check_host['total']):
            if(debug == 1):
                print(check_host['objects'][i]['name'])
            name_list.append(check_host['objects'][i]['name'])
        
        for i in range(check_range['total']):
            if(debug == 1):
                print(check_range['objects'][i]['name'])
            if(check_range['objects'][i]['name'] == "All_Internet"):
                pass
            else:
                name_list.append(check_range['objects'][i]['name'])



        time.sleep(3)
        logout_result = apifunctions.api_call(mds, "logout", {}, cma_sid)
        if(debug == 1):
            print(logout_result)

    except:
        if(cma_sid != ""):
            emergency_logout = apifunctions.api_call(mds, "logout", {}, cma_sid)
        print("no login to cma")

    return(name_list)
#end of search_cma

def main():
    print("begin")
    debug = 0

    mds_ip = "146.18.96.16"
    domains = get_domains(mds_ip)

    if(debug == 1):
        print("----------------------")
        print(domains)
        print("----------------------")

    for domain in domains:
        cma_names = search_cma(mds_ip, domain, "5.6.5.5")
        print("*******************************")
        print(domain)
        print(cma_names)

if __name__ == "__main__":
    main()
#end