import pickle, json
import inspect

import random, string
name = "".join(random.choice(string.ascii_letters) for i in range(20))

namei = input('server name?: ')
if namei != '':
	print('setting name')
	name = namei

import requests

with open('data.pickle', 'rb') as f:
	auth = pickle.load(f)['key']

def exampleFunc():
	pass

from servLIB import classes

failedEndpoint = []

i = json.loads(requests.post('http://localhost:8181/server',headers={'authToken': auth,'opt': json.dumps({'Name': name})}).content)

out = i['output']

sid = out['id']
sauth = out['key']

d = dir(classes.server)
d.reverse()
for i in d:
	if not i.startswith('_'):
		attr = getattr(classes.server,i)
		if inspect.isfunction(attr):
			hasKwarg = False
			Params = inspect.signature(attr).parameters
			args = []
			print(f'firing: {i}')
			for arg in list(Params)[1:]:
				targ = Params[arg]
				if targ.kind == targ.VAR_KEYWORD:
					hasKwarg = True
				else:
					args.append(arg)
			if hasKwarg:
				head = {}
				for arg in args:
					head[arg]=input(f'need a value for {arg}: ')
				head['authToken'] = sauth
				req = requests.get(f'http://localhost:8181/server/{sid}/{i}',headers=head)
				if req.status_code == 200:
					print(json.loads(req.content),'\n')
				else: failedEndpoint.append([i,req.content])

print('the following endpoints failed :(')
print(failedEndpoint)
