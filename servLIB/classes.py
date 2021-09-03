import json
import docker
from docker.types import Mount
import logging, hashlib
import random, string

logging.getLogger(docker.__name__).setLevel(logging.WARNING)

dock = docker.from_env()

class server:
    hashedKey: str = ''
    state: int = 0
    name: str = "".join(random.choice(string.ascii_letters) for i in range(20))
    containerID: str = None

    def __init__(self, key, **kwargs):
        for i in kwargs.keys():
            setattr(self,i,kwargs[i])
        mnt = Mount('/mnt/data',f'{self.name}VOL',type='volume')
        publicVOL = Mount('/mnt/public',f'publicData',type='volume')
        d = dock.containers.run('cont',environment={'STARTUP': 'exit'}, detach=True, mounts=[mnt,publicVOL])
        while d.status == 'running': logging.debug('awaiting container exit')
        self.containerID = d.id
        self.hashedKey = hashlib.sha256(key.encode()).digest()

    def checkKey(self, key):
        if hashlib.sha256(key.encode()).digest() == self.hashedKey:
            return True
        return False
    
    def getState(self,**kwargs):
        return {'failed': False,'status':200,'output': {'state': self.state},'message': 'server state'}
    
    def setState(self,State,**kwargs):
        self.state = int(State)
        return {'failed': False,'status':200,'output': {'state': self.state},'message': 'server state updated'}
    
    def lsFiles(self,**kwargs):
        mnt = Mount('/mnt/data',f'{self.name}VOL',type='volume')
        cont = dock.containers.run('cont',detach=True,mounts=[mnt],environment={'STARTUP': f'tree -J /mnt/data', 'SILENT': '1'})
        while cont.status == 'running': pass
        logs = cont.logs(stdout=True,stderr=True).decode('UTF-8')
        cont.remove(force=True)
        return {'failed': False,'status':200,'output': {'Folder': logs },'message': 'all files'}
    

    def getFile(self,File,**kwargs):
        mnt = Mount('/mnt/data',f'{self.name}VOL',type='volume')
        cont = dock.containers.run('cont',detach=True,mounts=[mnt],environment={'STARTUP': f'cat /mnt/data/{File}', 'SILENT': '1'})
        while cont.status == 'running': pass
        logs = cont.logs(stdout=True,stderr=True).decode('UTF-8')
        cont.remove(force=True)
        return {'failed': False,'status':200,'output': {'content': logs, 'file': File},'message': 'file send'}
    
    def putFile(self,File,Data,**kwargs):
        mnt = Mount('/mnt/data',f'{self.name}VOL',type='volume')
        cont = dock.containers.run('cont',detach=True,mounts=[mnt],environment={'STARTUP': f'echo {Data} | tee /mnt/data/{File}'})
        while cont.status == 'running': pass
        contents = cont.logs(stdout=True,stderr=True).decode('UTF-8')
        return {'failed': False,'status':200,'output': {'contents': contents, 'file': File},'message': 'file recieved'}
    
    def getName(self,**kwargs):
        return {'failed': False,'status':200,'output': {'name': self.name},'message': 'server name'}
    