from os import stat_result
import requests
import json

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

jso = json.loads(requests.post("http://localhost:8181/server",headers={'authToken': auth}).content)
serverToken = jso['output']['key']
serverID = jso['output']['id']
print(jso)

rep('getState',serverToken,serverID)
rep('setState',serverToken,serverID,state='1')
rep('lsFiles',serverToken,serverID)
rep('putFile',serverToken,serverID,data='FILECONTENTSGOBRR',file='testFile')
rep('getFile',serverToken,serverID,file='testFile')
