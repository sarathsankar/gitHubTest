#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Author: Sarath KS
Date: 05/07/2019
E-mail: sarathks333@gmail.com
'''

# Dependencies
import requests
from configparser import SafeConfigParser
config = SafeConfigParser()
config.read('config.ini')


def get_organization_list():
    # Get organization list
    r = requests.get("https://api.github.com/organizations")
    data = [w['login'] for w in r.json()]
    with open('organisations.txt', 'w') as fobj:
        fobj.write('\n'.join(data))


def test_from_organization_list():
    '''
    Results in each row, and columns as org_name, time_in_seconds, request_status_code
    '''
    organisations = []
    with open('organisations.txt') as fobj:
        organisations = fobj.read().split('\n')

    result = []
    url = "http://0.0.0.0:{}/{}".format(config.get('server', 'port'),
                                        config.get('server', 'endpoint'))
    for n, org in enumerate(organisations):
        res = requests.post(url, json={"org": org})
        print(res.elapsed.total_seconds())
        print(res.json())
        result.append(
            [org, str(res.elapsed.total_seconds()), str(res.status_code)])
    with open('time_metrict_results.txt', 'w') as fobj:
        fobj.write('\n'.join(['\t'.join(w) for w in result]))
        if res.status_code == 200:
            print(res.json())
        else:
            print("Error {}".format(res.status_code))
    print("Results saved into 'time_metrict_results.txt'...!!")


def test_call():
    print("Post request with org=microsoft\n")
    # url = "http://0.0.0.0:{}/{}".format(config.get('server', 'port'),
    #                                     config.get('server', 'endpoint'))
    url = "http://anabeana.pythonanywhere.com/repos"
    r = requests.post(url, json={"org": "microsoft"})
    print(r.json())
    if r.status_code == 200:
        print("Response time: {} Sec.".format(r.elapsed.total_seconds()))
    else:
        print("Error {}".format(r.status_code))


test_call()
