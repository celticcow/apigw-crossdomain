#!/usr/bin/python3 -W ignore::DeprecationWarning

import json
import requests

#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
Greg_Dunlap / CelticCow

test script to do json query to api gw

curl http://localhost:5000/crossdomain -X POST --data '{"ipaddr" : "146.18.2.137"}'
"""


def main():
    print("in main")

    ip_json = {
        "ipaddr" : "146.18.2.137"
    }

    url = "http://localhost:5000/crossdomain"
    
    r = requests.post(url, json.dumps(ip_json))

    data = r.json()

    print("-------------------------------------------------")
    print(data)

    print(data['total'])

    for x in range(data['total']):
        print(data['cmas'][x]['cma'])
        print(data['cmas'][x]['whereused'])
    

if __name__ == "__main__":
    main()
#end of program