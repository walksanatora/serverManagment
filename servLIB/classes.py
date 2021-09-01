import json
import os
import docker
from docker.types import Mount
import logging
import hashlib
import random
import string

logging.getLogger(docker.__name__).setLevel(logging.WARNING)

dock = docker.from_env()

class server:
    hashedKey = ''
    state = 0
    name = "".join(random.choice(string.ascii_letters) for i in range(20))
    containerID = None

    def __init__(self, key, **kwargs):
        for i in kwargs.keys():
            setattr(self,i,kwargs[i])
        self.hashedKey = hashlib.sha256(key.encode()).digest()

    def checkKey(self, key,**kwargs):
        if hashlib.sha256(key.encode()).digest() == self.hashedKey:
            return True
        return False
    
    def getState(self,**kwargs):
        return {'failed': False,'status':200,'output': {'state': self.state},'message': 'server state'}
    
    def setState(self,**kwargs):
        self.state = kwargs['State']
        return {'failed': False,'status':200,'output': {'state': self.state},'message': 'server state updated'}
    
    def lsFiles(self,**kwargs):
        print(kwargs)
        mnt = Mount('/mnt/data',f'{self.name}VOL',type='volume')
        cont = dock.containers.run('cont',detach=True,mounts=[mnt],environment={'STARTUP': f'tree -J /mnt/data', 'SILENT': '1'})
        while cont.status == 'running': pass
        logs = cont.logs(stdout=True,stderr=True).decode('UTF-8')
        cont.remove(force=True)
        return {'failed': False,'status':200,'output': {'Folder': json.loads(logs) },'message': 'all files'}
    

    def getFile(self,**kwargs):
        print(kwargs)
        mnt = Mount('/mnt/data',f'{self.name}VOL',type='volume')
        cont = dock.containers.run('cont',detach=True,mounts=[mnt],environment={'STARTUP': f'cat /mnt/data/{kwargs["File"]}', 'SILENT': '1'})
        while cont.status == 'running': pass
        logs = cont.logs(stdout=True,stderr=True).decode('UTF-8')
        cont.remove(force=True)
        return {'failed': False,'status':200,'output': {'content': logs, 'file': kwargs['File']},'message': 'file send'}
    
    def putFile(self,**kwargs):
        print(kwargs)
        mnt = Mount('/mnt/data',f'{self.name}VOL',type='volume')
        cont = dock.containers.run('cont',detach=True,mounts=[mnt],environment={'STARTUP': f'echo {kwargs["Data"]} | tee /mnt/data/{kwargs["File"]}'})
        while cont.status == 'running': pass
        contents = cont.logs(stdout=True,stderr=True).decode('UTF-8')
        return {'failed': False,'status':200,'output': {'contents': contents, 'file': kwargs['File']},'message': 'file recieved'}
    
    def getName(self,**kwargs):
        return {'failed': False,'status':200,'output': {'name': self.name},'message': 'server name'}
    