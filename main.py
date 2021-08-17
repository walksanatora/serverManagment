#!/usr/bin/env python3.9
import argparse
import hashlib
import pickle

import docker

import random
import string

srvKey = ''.join(random.choice(string.ascii_letters) for i in range(20))

with open('data.pickle', 'rb') as p:
    data = pickle.load(p)

if not 'key' in data:
    data['key'] = ''.join(random.choice(string.ascii_letters) for i in range(20))


parser = argparse.ArgumentParser()
parser.add_argument('--debug','-d',action='store_true', help='enables debug logging')
parser.add_argument('--key', '-k',action='store',default=data['key'], help='sets acess key')
parser.add_argument('--host', action='store',default='0.0.0.0',help='set host ip')
parser.add_argument('--port','-p', action='store',default='8181',help='sets hostport')


def save(d):
    with open('data.pickle', 'wb') as p:
        pickle.dump(d,p)

global argv 
argv = parser.parse_args()

if 'key' in argv:
    data['key'] = argv.key

if not 'servers' in data:
    data['servers'] = []

sK = argv.key

import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s - %(levelname)s] %(message)s',force=True)

srvKeyHash = hashlib.sha256(sK.encode()).digest()

if argv.debug:
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s-%(levelname)s] %(message)s',force=True)
    logging.debug('debug logging enabled')

logging.getLogger(docker.__name__).setLevel(logging.WARNING)


logging.info(f'your key is: {sK}')


import servLIB

save(data)

import flask
from flask import request
app = flask.Flask(__name__)

@app.route('/server', methods=['POST'])
def construct():
    if 'authToken' in request.headers:
        if not (hashlib.sha256(request.headers['authToken'].encode()).digest() == srvKeyHash):
            logging.debug('invalid auth token')
            return {'status': '403', 'message': '403 forbidden, invalid "authToken"', 'failed': True}, 403
    else:
        logging.debug('missing auth token')
        return {'status': '403', 'message': '403 forbidden, "authToken" doesn\'t exist', 'failed': True}, 403
    if 'key' in request.headers:
        key = request.headers['key']
        data['servers'].append(servLIB.server(request.headers['key']))
    else:
        key = ''.join(random.choice(string.ascii_letters) for i in range(20))
        data['servers'].append(servLIB.server(key))
    logging.debug(data)
    save(data)
    return {'status': 200, 'message': 'created server', 'failed': False,'output': {'key': key,'id': len(data['servers'])-1}},200

@app.route('/server/<index>/<path:func>')
def api(index,func):
    ind = []
    try:
        ind = data['servers'][int(index)]
    except IndexError:
        return {'status': 400, 'message': 'invalid server number', 'failed': True}, 400

    if 'authToken' in request.headers:
        if not ind.checkKey(request.headers['authToken']):
            logging.debug('invalid auth token')
            return {'status': '403', 'message': '403 forbidden, invalid "authToken"', 'failed': True}, 403
    else:
        logging.debug('missing auth token')
        return {'status': '403', 'message': '403 forbidden, "authToken" doesn\'t exist', 'failed': True}, 403

    fun = ind
    try:
        for i in func.split('/'):
            fun = getattr(fun,i)
    except AttributeError:
        return {'status': 404, 'message': '404 command not found', 'failed': True}, 404
    
    return(fun(**request.headers))

app.run(argv.host,argv.port,debug=argv.debug)