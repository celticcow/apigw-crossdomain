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
        print("*-" *20)

        print("CMA ", end="\t")
        print(data['cmas'][x]['cma'])

        if(data['cmas'][x]['cma'] == "TestCMA"):
            print("break point")
        
        print("Where-Used ", end="")

        if(len(data['cmas'][x]['whereused']['cpobj']) == 0):
            print("not used\n")
        else:
            ### need loop var here
            #print(data['cmas'][x]['whereused']) 
            tmp1 = data['cmas'][x]['whereused']['cpobj'][0]['access-control-rules']
            for i in range(len(tmp1)):
                print("rule")
                print(data['cmas'][x]['whereused']['cpobj'][0]['access-control-rules'][i])
                print("\n--\n")

            tmp2 = data['cmas'][x]['whereused']['cpobj'][0]['objects']
            for j in range(len(tmp2)):
                print("object")
                print(data['cmas'][x]['whereused']['cpobj'][0]['objects'][j])
                print("\n^^\n")
            
            tmp3 = data['cmas'][x]['whereused']['cpobj'][0]['nat-rules']
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(tmp3)
            print("############################")
            #print(data['cmas'][x]['whereused']['cpobj'])
            #print("\n________________\n")
            #print(tmp1)
            #print("\n")
            #print(tmp2)
            print("\n**************\n")
            #print(data['cmas'][x]['whereused']['cpobj']['objects'])

        #tmp = data['cmas'][x]['whereused']

        print(len(data['cmas'][x]['whereused']['cpobj']))
    

if __name__ == "__main__":
    main()
#end of program