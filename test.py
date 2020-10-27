#!/usr/bin/python3

import json

from flask import Flask, request
from flask_json import FlaskJSON, JsonError, json_response, as_json

def main():
    print("test code")

    domain_list = ["Dev-CMA" ,"FXS-US-EMPVPNL6", "TestCMA"]

    test_json = {}

    test_json['ip-address'] = "146.18.2.137"
    test_json['lookup'] = "where-used"
    test_json['cmas'] = []

    i = 0
    for x in domain_list:
        tmp = {}
        tmp['cma'] = x
        test_json['cmas'].append(tmp)
        i = i + 1

    print(test_json)

    print(test_json['cmas'][1]['cma'])


if __name__ == "__main__":
    main()
#end of test