#!/usr/bin/python3 -W ignore::DeprecationWarning

import json
import requests

#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
Greg_Dunlap / CelticCow

test script to do json query to api gw

curl http://host:5000/crossdomain -X POST --data '{"ipaddr" : "146.18.2.137"}'
"""


def main():
    print("in main")

    ip_json = {
        "ipaddr" : "204.135.8.50"
    }

    name_json = {
        "name" : "afw-161.135.84.6-26"
    }

    url  = "http://firewall.infosec.fedex.com:4000/crossdomain"  
    url2 = "http://firewall.infosec.fedex.com:4000/crossdomain_name"
    
    r = requests.post(url, json.dumps(ip_json))

    ##r = requests.post(url2,json.dumps(name_json))

    data = r.json()

    print("-------------------------------------------------")
    print(data)

    print(data['total'])

    for x in range(data['total']):
        print("*-" *20)

        print("CMA ", end="\t")
        print(data['cmas'][x]['cma'])

        #if(data['cmas'][x]['cma'] == "TestCMA"):
        #    print("break point")
        
        print("Where-Used ", end="")

        """
        for loop going through range of cpobj. 
        if this len == 0 then there is nothing used so the loop will exist immediatly
        if not then we need to loop through each of the parts
        access-control-rules / objects / nat-rules
        """
        #if(len(data['cmas'][x]['whereused']['cpobj']) == 0):
        #    print("not used\n")
        #else:
        for j in range(len(data['cmas'][x]['whereused']['cpobj'])):
            ### need loop var here
            ## what is len of cpobj ???   maybe not hard set to [0] but to var ... need a k len
            #print(data['cmas'][x]['whereused']) 
            ##print("loop len here")
            ##print(len(data['cmas'][x]['whereused']['cpobj']))

            tmp1 = data['cmas'][x]['whereused']['cpobj'][j]['access-control-rules']
            for i in range(len(tmp1)):
                print("rule")
                print(data['cmas'][x]['whereused']['cpobj'][j]['access-control-rules'][i])
                print("\n--\n")

            tmp2 = data['cmas'][x]['whereused']['cpobj'][j]['objects']
            for k in range(len(tmp2)):
                print("object")
                print(data['cmas'][x]['whereused']['cpobj'][j]['objects'][k])
                print("\n^^\n")
            
            tmp3 = data['cmas'][x]['whereused']['cpobj'][j]['nat-rules']
            for y in range(len(tmp3)):
                print("nat")
                print(data['cmas'][x]['whereused']['cpobj'][j]['nat-rules'][y])
                print("\n!!\n")
            #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            #print(tmp3)
            #print("############################")
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
