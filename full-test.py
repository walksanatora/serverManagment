from os import stat_result
import requests
import json
import random
import string

from requests.api import head

def rep(end,token,id,**kwargs):
	print('\n\ncalling endpoint:', end)
	headers = kwargs
	headers['authToken'] = token
	print('headers: ', headers)
	con = requests.get(f'http://localhost:8181/server/{id}/{end}',headers=headers)
	print('statusCode: ', con.status_code)
	if con.status_code == 200:
		data = json.loads(con.content)
		print(data['message'])
		print(data['output'])
		print(data)
		return data
	return None

auth = input('AuthToken: ')

name = input('input server name (blank for random): ')

if name == '':
	name = "".join(random.choice(string.ascii_letters) for i in range(20)) 

jso = json.loads(requests.post("http://localhost:8181/server",headers={'authToken': auth,'opt': json.dumps({'name': name})}).content)


serverToken = jso['output']['key']
serverID = jso['output']['id']
print(jso)

rep('getState',serverToken,serverID)
rep('setState',serverToken,serverID,state='1')
rep('lsFiles',serverToken,serverID)
rep('putFile',serverToken,serverID,data='FILECONTENTSGOBRR',file='testFile')
rep('getFile',serverToken,serverID,file='testFile')
rep('getName',serverToken,serverID)
