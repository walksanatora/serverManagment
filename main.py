#!/usr/bin/env python3.9
import argparse, hashlib
import pickle, json
import markdown, os, glob
import random, string
import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s - %(levelname)s] %(message)s',force=True)

srvKey = ''.join(random.choice(string.ascii_letters) for i in range(20))
try:
    with open('data.pickle', 'rb') as p:
        data = pickle.load(p)
except FileNotFoundError:
    data = {}
if not 'key' in data:
    data['key'] = ''.join(random.choice(string.ascii_letters) for i in range(20))

parser = argparse.ArgumentParser()
parser.add_argument('--debug','-d',action='store_true', help='enables debug logging')
parser.add_argument('--key', '-k',action='store',default=data['key'], help='sets acess key')
parser.add_argument('--host', action='store',default='0.0.0.0',help='set host ip')
parser.add_argument('--port','-p', action='store',default='8181',help='sets hostport')

global argv 
argv = parser.parse_args()

if 'key' in argv:
    data['key'] = argv.key
if not 'servers' in data:
    data['servers'] = []

sK = argv.key
srvKeyHash = hashlib.sha256(sK.encode()).digest()

if argv.debug:
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s-%(levelname)s] %(message)s',force=True)
    logging.debug('debug logging enabled')

import docker
from docker.types import Mount
logging.getLogger(docker.__name__).setLevel(logging.WARNING)
dock = docker.from_env()

contImage=False
for img in dock.images.list():
    if img.attrs['RepoTags'] == ['cont:latest']:
        contImage = True

if not contImage:
    print('missing docker container "cont:latest"')
    exit

pubVol=True
for vol in dock.volumes.list():
    logging.debug(vol.name)
    if vol.name == 'publicData':
        logging.debug('publicData Volume located')
        pubVOL = False
if pubVol:
    dock.volumes.create('publicData')
    logging.info('created publicData docker volume')

def save(d):
    with open('data.pickle', 'wb') as p:
        pickle.dump(d,p)

logging.info(f'your key is: {sK}')


import servLIB

save(data)

import flask
from flask import request, url_for
app = flask.Flask(__name__)

@app.route('/server', methods=['POST'])
def server():
    if 'authToken' in request.headers:
        if not (hashlib.sha256(request.headers['authToken'].encode()).digest() == srvKeyHash):
            logging.debug('invalid auth token')
            return {'status': '403', 'message': '403 forbidden, invalid "authToken"', 'failed': True}, 403
    else:
        logging.debug('missing auth token')
        return {'status': '403', 'message': '403 forbidden, "authToken" doesn\'t exist', 'failed': True}, 403
    try:
        opt = json.loads(request.headers['opt'])
    except KeyError:
        opt = {}
    if 'key' in request.headers:
        key = request.headers['key']
        data['servers'].append(servLIB.server(request.headers['key'],**opt))
    else:
        key = ''.join(random.choice(string.ascii_letters) for i in range(20))
        data['servers'].append(servLIB.server(key,**opt))
    logging.debug(data)
    save(data)
    return {'status': 200, 'message': 'created server', 'failed': False,'output': {'key': key,'id': len(data['servers'])-1}},200

@app.route('/server/<index>', methods=['GET','DELETE'])
def basic(index):
    ind = []
    try:
        ind = data['servers'][int(index)]
    except IndexError:
        return {'status': 400, 'message': 'invalid server number', 'failed': True}, 400
    if ind == None:
        return {'status': 400, 'message': 'invalid server number', 'failed': True}, 400

    if 'authToken' in request.headers:
        if not ind.checkKey(request.headers['authToken']):
            logging.debug('invalid auth token')
            return {'status': '403', 'message': '403 forbidden, invalid "authToken"', 'failed': True}, 403
    else:
        logging.debug('missing auth token')
        return {'status': '403', 'message': '403 forbidden, "authToken" doesn\'t exist', 'failed': True}, 403
    
    if request.method == 'GET':
        return {'status': 200, 'message': 'server dump', 'failed': False, 'output': {'dump': json.dumps(ind)}}, 200
    elif request.method == 'DELETE':
        data['servers'][int(index)] = None
        return {'failed': False,'status': 200,'message': 'server deleted','output': {}}, 200

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
    out = fun(**request.headers)
    return out, out['status']

@app.route('/public/<cmd>')
def publicVOL(cmd):
    if 'authToken' in request.headers:
        if not (hashlib.sha256(request.headers['authToken'].encode()).digest() == srvKeyHash):
            logging.debug('invalid auth token')
            return {'status': '403', 'message': '403 forbidden, invalid "authToken"', 'failed': True}, 403
    else:
        logging.debug('missing auth token')
        return {'status': '403', 'message': '403 forbidden, "authToken" doesn\'t exist', 'failed': True}, 403
    
    if not cmd in ['getFile','putFile','lsFiles']:
        return {'status': 404, 'message': '404 command not found', 'failed': True}, 404
    kwargs = request.headers
    if cmd == 'getFile':
        mnt = Mount('/mnt/public',f'publicData',type='volume')
        cont = dock.containers.run('cont',detach=True,mounts=[mnt],environment={'STARTUP': f'cat /mnt/public/{kwargs["File"]}', 'SILENT': '1'})
        while cont.status == 'running': pass
        logs = cont.logs(stdout=True,stderr=True).decode('UTF-8')
        cont.remove(force=True)
        return {'failed': False,'status':200,'output': {'content': logs, 'file': kwargs['File']},'message': 'file send'}, 200
    elif cmd == 'putFile':
        mnt = Mount('/mnt/data','publicData',type='volume')
        cont = dock.containers.run('cont',detach=True,mounts=[mnt],environment={'STARTUP': f'echo {kwargs["Data"]} | tee /mnt/data/{kwargs["File"]}'})
        while cont.status == 'running': pass
        contents = cont.logs(stdout=True,stderr=True).decode('UTF-8')
        return {'failed': False,'status':200,'output': {'contents': contents, 'file': kwargs['File']},'message': 'file recieved'}
    elif cmd == 'lsFiles':
        mnt = Mount('/mnt/data','publicData',type='volume')
        cont = dock.containers.run('cont',detach=True,mounts=[mnt],environment={'STARTUP': f'tree -J /mnt/data', 'SILENT': '1'})
        while cont.status == 'running': pass
        logs = cont.logs(stdout=True,stderr=True).decode('UTF-8')
        cont.remove(force=True)
        return {'failed': False,'status':200,'output': {'Folder': json.loads(logs) },'message': 'all files'}


@app.route('/docs/<path:page>')
def documentation(page):
    with open(f'docs/{page}.md', 'r') as doc:
        html = markdown.markdown(doc.read())
        url = str.split(page,'/')
        code = '<h1>Navigation</h1><p><a href="/docs/index">index</a>&gt;'
        uri = ""
        if not page == 'index':
            for v in url:
                code = code + f"<a href=\"/docs{uri}/{v}\">{v}</a>&gt;"
                uri = uri + '/' + v
            code = code + '</p> <p>'
            path = os.getcwd()
            li = glob.glob(f'{path}/docs{uri}/*')
            subpages = []
            for v in li:
                if v.startswith('_'):
                    continue
                parsed = v.split('/')
                parsed = parsed[len(parsed)-1]
                subpages.append(parsed[:-3])
            for page in subpages:
                code = code + f'<a href="/docs{uri}/{page}">{page}</a> '
            print(li)
        else:
            code = ''
        css = f'<link rel= "stylesheet" type= "text/css" href= "{url_for("static",filename="docs.css") }">'
       
        return css + code + html, 200

app.run(argv.host,argv.port,debug=argv.debug)