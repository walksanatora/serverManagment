#!/usr/bin/env python3
import requests
import json

r = requests.post('http://localhost:8181/server',headers={'authToken': input('authToken: ')})
jso = json.loads(r.content)
print(jso)
r2 = requests.get(f'http://localhost:8181/server/{jso["output"]["id"]}/onosecond',headers={'authToken': jso['output']['key']})
print(json.loads(r2.content))
