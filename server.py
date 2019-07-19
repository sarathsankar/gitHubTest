#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Author: Sarath KS
Date: 05/07/2019
E-mail: sarathks333@gmail.com
'''
from configparser import SafeConfigParser
from wsgiref import simple_server
import requests
import logging
import falcon
import json
import os
# import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
# if current_dir not in sys.path:
#     sys.path.insert(1, current_dir)

config = SafeConfigParser()
config.read('config.ini')
if not os.path.isfile(os.path.join(current_dir, 'server.log')):
    os.mknod(os.path.join(current_dir, 'server.log'))
logging.basicConfig(filename='server.log', filemode='a', level=logging.DEBUG)


class GitHub(object):
    def __init__(self):
        self.top = int(config.get('args', 'top'))  # no.of top results
        self.stargazers_count_key = config.get('args', 'stargazers_count_key')
        self.name_key = config.get('args', 'name_key')
        self.url = "https://api.github.com/search/repositories?q=org:{}&sort=stars&per_page=3"

    def on_post(self, req, resp):
        req_body = req.stream.read()
        json_data = json.loads(req_body.decode('utf8'))
        org = json_data.get('org')
        try:
            output = self.main(org)
            if not output:
                raise Exception("Bad input, data fetch failed...!!")
            resp.body = json.dumps({"results": output})
            resp.content_type = 'application/json'
            resp.status = falcon.HTTP_200
        except Exception as e:
            logging.error(e)
            raise falcon.HTTPBadRequest(
                'Service failed : {}'.format(e)
            )
            resp.status = falcon.HTTP_500

    def main(self, org="microsoft"):
        result = None
        url = self.url.format(org)
        try:
            res = requests.get(url, verify=False, timeout=100)
            if res.status_code == 200:
                res_data = res.json()
                result = [{'stars': w[self.stargazers_count_key],
                           'name': w[self.name_key]} for w in res_data['items']]
            else:
                raise Exception(
                    "Error while calling url: {}\nStatus code: {}".format(url, res.status_code))
        except requests.exceptions.RequestException as e:
            logging.exception(e)
        return result


APP = falcon.API()
APP.add_route(os.sep + config.get('server', 'endpoint'), GitHub())

if __name__ == '__main__':
    httpd = simple_server.make_server(config.get(
        'server', 'host'), int(config.get('server', 'port')), APP)
    logging.info("Server Started...!!")
    httpd.serve_forever()
