#!/usr/bin/python3

import json
import requests

"""
JSON testing ... trying to debug possible issue in flask server
"""


def main():
    print("main TEST")

    tmp1 = {'cmas': [{'cma': 'Dev-CMA', 'whereused': {'cpobj': []}}, {'cma': 'FXS-US-EMPVPNL6', 'whereused': {'cpobj': []}}, {'cma': 'TestCMA', 'whereused': {'cpobj': []}}], 'ip-address': '146.18.2.13', 'lookup': 'where-used', 'total': 3}

    print(tmp1)
    print(len(tmp1))
    print(tmp1['total'])

    for x in range(0):
        print(x)

    """
    for i in range(tmp1['total']):
        print(tmp1['cmas'][i]['cma'])
        print(tmp1['cmas'][i]['whereused'])

    #D = {}
    #d = {}


    with open("small.json", "r") as json_file:
        data = json.load(json_file)
        
        print(json.dumps(data))
    
    #print(D)
    """
    """
    with open('large.json') as f:
        d = json.load(f)

    print(d)
    """

if __name__ == "__main__":
    main()
#end of program