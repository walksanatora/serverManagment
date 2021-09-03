import json
import docker
from docker.types import Mount
import logging, hashlib
import random, string

dock = docker.from_env()

class server:
    HashedKey: str = ''
    State: int = 0
    Name: str = "".join(random.choice(string.ascii_letters) for i in range(20))

    def __init__(self, Key, **kwargs):
        logging.debug(f'Key: {Key}, Kwargs: {kwargs}')
        for i in kwargs.keys():
            logging.debug(f'setting value: {i} to {kwargs[i]}')
            setattr(self,i,kwargs[i])
        mnt = Mount('/mnt/data',f'{self.Name}VOL',type='volume')
        publicVOL = Mount('/mnt/public',f'publicData',type='volume')
        d = dock.containers.run('cont',environment={'STARTUP': 'exit'}, detach=True, mounts=[mnt,publicVOL], name=f'{self.Name}')
        while d.status == 'running': logging.debug('awaiting container exit')
        self.containerID = d.id
        self.HashedKey = hashlib.sha256(Key.encode()).digest()

    def checkKey(self, key):
        if hashlib.sha256(key.encode()).digest() == self.HashedKey:
            return True
        return False
    
    def getState(self,**kwargs):
        return {'failed': False,'status':200,'output': {'state': self.State},'message': 'server state'}
    
    def setState(self,State,**kwargs):
        try: int(State)
        except ValueError: return {'failed': True,'status': 400, 'message': f'{State} is not a valid int'}
        self.State = int(State)
        return {'failed': False,'status':200,'output': {'state': self.State},'message': 'server state updated'}
    
    def lsFiles(self,**kwargs):
        mnt = Mount('/mnt/data',f'{self.Name}VOL',type='volume')
        cont = dock.containers.run('cont',detach=True,mounts=[mnt],environment={'STARTUP': f'tree -J /mnt/data', 'SILENT': '1'})
        while cont.status == 'running': pass
        logs = cont.logs(stdout=True,stderr=True).decode('UTF-8')
        cont.remove(force=True)
        return {'failed': False,'status':200,'output': {'Folder': logs },'message': 'all files'}
    

    def getFile(self,File,**kwargs):
        mnt = Mount('/mnt/data',f'{self.Name}VOL',type='volume')
        cont = dock.containers.run('cont',detach=True,mounts=[mnt],environment={'STARTUP': f'cat /mnt/data/{File}', 'SILENT': '1'})
        while cont.status == 'running': pass
        logs = cont.logs(stdout=True,stderr=True).decode('UTF-8')
        cont.remove(force=True)
        return {'failed': False,'status':200,'output': {'content': logs, 'file': File},'message': 'file send'}
    
    def putFile(self,File,Data,**kwargs):
        mnt = Mount('/mnt/data',f'{self.Name}VOL',type='volume')
        cont = dock.containers.run('cont',detach=True,mounts=[mnt],environment={'STARTUP': f'echo {Data} | tee /mnt/data/{File}'})
        while cont.status == 'running': pass
        contents = cont.logs(stdout=True,stderr=True).decode('UTF-8')
        cont.remove(force=True)
        return {'failed': False,'status':200,'output': {'contents': contents, 'file': File},'message': 'file recieved'}
    
    def getName(self,**kwargs):
        return {'failed': False,'status':200,'output': {'name': self.Name},'message': 'server name'}
    