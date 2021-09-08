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

class test:
	url: str = ''
	args: dict = {}
	output: dict = {}
	status: int = 0
	req: requests.models.Response = None
	method: str = 'GET'
	def __init__(self,**kwargs):
		for i in kwargs.keys():
			setattr(self,i,kwargs[i])
	def run(self):
		self.req = requests.request(self.method,self.url,headers=self.args)
		self.status = self.req.status_code
		try:
			self.output = json.loads(self.req.content)
		except json.JSONDecodeError: pass

from servLIB import classes

failedEndpoint = []
re = requests.post('http://localhost:8181/server',headers={'authToken': auth,'opt': json.dumps({'Name': name})})

i = json.loads(re.content)

if re.status_code != 200:
	print("ohno it failed message: '{}'".format(i['message']))
	exit()

out = i['output']
sauth = out['key']
id = out['id']
tst = []

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
				tst.append(test(args=head,url=f'http://localhost:8181/server/{id}/{i}'))


heada = {}
heada['authToken'] = auth
heada['File'] = "test.txt"
heada['Data'] = "foobar___owo"
tst.append(test(args=heada,url="http://localhost:8181/public/lsFiles"))
tst.append(test(args=heada,url="http://localhost:8181/public/putFile"))
tst.append(test(args=heada,url="http://localhost:8181/public/getFile"))


for i in tst:
	i.run()
	print(f"uri: {i.url} \nstatus: {i.status} \nargs: {i.args} \noutput: {i.output}\n\n")
	if i.status != 200:
		failedEndpoint.append(i)

de = str.lower(input('delete server?: ')).strip()
delsrv = False
if de in ['yes','y','1','true']:
    delsrv = True

if not delsrv:
	print("writing server key/id to file")
	with open('log_servers.txt', 'a') as log:
		log.write(f'sid: {id} key: {sauth}\n')
else:
	print("deleting server")
	d = test(args={'authToken': sauth},url=f'http://localhost:8181/server/{id}', method='DELETE')
	d.run()
	print(f"uri: {d.url} \nstatus: {d.status} \nargs: {d.args} \noutput: {d.output}\n\n")

print('the following endpoints failed: ')
for i in failedEndpoint:
	print(i.url)
