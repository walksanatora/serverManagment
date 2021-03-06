import argparse
import json
import pickle
import random
import string
import traceback

import requests

import Utils
from servLIB import classes


def confirmMsg(question):
	resp = input(question + ': (y/n)').lower().strip()
	if resp in ['yes','y','1','true']: return True
	else: return False


try:
    with open('data.pickle', 'rb') as p:
        data = pickle.load(p)
except:
	print("failed to load data file exception: {}".format(traceback.print_exc()))

parser = argparse.ArgumentParser()
parser.add_argument('--debug','-d',action='store_true', help='enables debug logging')
parser.add_argument('--key', '-k',action='store',default=data['key'], help='sets acess key')
parser.add_argument('--host', action='store',default='0.0.0.0',help='set host ip')
parser.add_argument('--port','-p', action='store',default='8181',help='sets hostport')
parser.add_argument('--server','-s',action='store',default=None,help='pre-define server key to use (cannot be used with -ns)')
parser.add_argument('--newserver','-ns',action='store_true',help='force creation of new server (cannot be used with -s)')
opt, other = parser.parse_known_args()

BASEURL = 'http://' + ':'.join([opt.host,opt.port]) + '/'
print(BASEURL)

if opt.newserver and opt.server != None:
	print('flag error: using -ns and -s at the same time')
	exit()

if opt.server != None:
	sAuth=opt.server
elif opt.newserver:
	print("creating server")
	if confirmMsg('Do you wish to set a server name?'): name = input('input desired name: ')
	else: name = ''.join(random.choice(string.ascii_letters) for i in range(5))
	req = requests.post(f'{BASEURL}server',headers={'authToken': data['key'], 'opt': json.dumps({'Name': name})})
	if req.status_code != 200:
		print("failed to create server exiting")
		print(json.loads(req.content)['message'])
	else: print('server created')
	out = json.loads(req.content)['output']
	sAuth = out['key']
	sName = out['id']
else:
	if confirmMsg('do you have a server key?'):
		sAuth = input('please input server key: ')
		sName = input('please input the name/id of the server: ')
	else:
		print("creating server")
		if confirmMsg('Do you wish to set a server name?'): name = input('input desired name')
		else: name = ''.join(random.choice(string.ascii_letters) for i in range(5))
		req = requests.post(f'{BASEURL}server',headers={'authToken': data['key'], 'opt': json.dumps({'Name': name})})
		if req.status_code != 200:
			print("failed to create server exiting")
			print(json.loads(req.content)['message'])
		else: print('server created')
		out = json.loads(req.content)['output']
		sAuth = out['key']
		sName = out['id']

def weirdParse(input):
	tmp1 = input.split(' ')
	args = []
	kwargs = {}
	for i in tmp1:
		if '=' in i:
			tmp2 = i.split('=')
			if len(tmp2) == 2:
				kwargs[tmp2[0]] = tmp2[1]
				continue
		args.append(i)
	return args, kwargs

class endPoint:
	name: str
	args: list
	method: str
	def __init__(self,func: str,args: list,method: str):
		self.name = func
		self.args = args
		self.method = method
	def fire(self,**kwargs) -> requests.models.Response:
		if len(kwargs) == len(self.args):
			hasAllKeys = True
			for key in kwargs.keys():
				if not key in self.args:
					hasAllKeys = False
			if hasAllKeys:
				return requests.request(self.method,f'{BASEURL}server/{sName}/{self.name}',headers=kwargs)
	
	def __str__(self) -> str:
		return f'{self.name}({",".join(self.args)})'

	def __repr__(self) -> str:
		return f'<{self.name}({",".join(self.args)})>'

def migrate(abstract:dict) -> dict:
	output={}
	for k in abstract.keys():
		if type(abstract[k]) == type({}):
			output[k] = migrate(abstract[k])
		elif type(abstract[k]) == type(Utils.abstractFunction('a',[])):
			output[k] = endPoint(abstract[k].name,abstract[k].args,abstract[k].__dict__['method'])
	return output

_EndPointList_ = Utils.removeNone(Utils.dump(classes.server))
_EndPointList_ = migrate(_EndPointList_)

class REPL:
	def help(*args,**kwargs):
		helpTexts = {
			'help': 'this command, takes one arg to show specific command',
			'exit': 'exits the program',
			'pas': 'prints the args passed to it',
			'_endpoints': 'prints all found endpoints',
			'_mykey': 'prints server auth key',
			'_rawPoint': 'fires a endpoint raw using kwargs as headers uses are 0 as request type, arg 1 as endpoint'
			}
		if len(args) == 0:
			for k in helpTexts.keys(): print(k, helpTexts[k])
		else:
			try: print(helpTexts[args[0]])
			except KeyError: 
				for k in helpTexts.keys(): print(k, helpTexts[k])

	def exit(*args,**kwargs):
		raise KeyboardInterrupt
	
	def pas(*args,**kwargs):
		print('kwargs: ',kwargs)
		print('args: ',args)
	
	def _endpoints(*args,**kwargs):
		for e in Utils.dictConvertString(_EndPointList_,'/'):
			d = _EndPointList_
			for i in e.split('/'):
				d = d[i]
			print(f'path: {e}, function: {d}, method: {d.method}')

	def _mykey(*args,**kwargs):
		print('server Key: ', sAuth)
	
	def _rawPoint(*args,**kwargs):
		head = kwargs
		head['authToken'] = sAuth
		req = requests.request(args[0],f'{BASEURL}server/{sName}/{args[1]}',headers=head)
		print(req.content)

try:
	while True:
		cmd = input(f'[{BASEURL}]({sName})> ')
		pcmd = cmd.split(' ')
		try: cmdfunc = getattr(REPL,pcmd[0])
		except AttributeError: print('Command not found'); continue 
		try: 
			args, kwargs = weirdParse(' '.join(pcmd[1:]))
			cmdfunc(*args,**kwargs)
		except Exception: print('Internal Error', traceback.print_exc())
except KeyboardInterrupt:
	print('\nexiting')
