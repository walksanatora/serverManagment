import json
import docker
from docker.types import Mount
import logging, hashlib
import random, string

dock = docker.from_env()

contImage=False
containerName: str = ''
for img in dock.images.list():
        logging.debug(img.attrs['RepoTags'][0])
        if '-srv' in img.attrs['RepoTags'][0]:
            contImage=True
            if containerName == '':
                containerName = img.attrs['RepoTags']
if not contImage:
    logging.error('no image that has the -srv in it\'s name')
    exit()

class server:
    HashedKey: str = ''
    State: int = 0
    Name: str = "".join(random.choice(string.ascii_letters) for i in range(20))
    Startup: str = 'echo HelloWorld'
    Env: dict = {}
    Ports: dict = {}
    Image: str = containerName

    def __init__(self, Key, **kwargs):
        logging.debug(f'Key: {Key}, Kwargs: {kwargs}')
        for i in kwargs.keys():
            logging.debug(f'setting value: {i} to {kwargs[i]}')
            setattr(self,i,kwargs[i])
        mnt = Mount('/mnt/data',f'{self.Name}VOL',type='volume')
        publicVOL = Mount('/mnt/public',f'publicData',type='volume')
        d = dock.containers.run(self.Image,environment={'STARTUP': 'exit'}, detach=True, mounts=[mnt,publicVOL], name=f'{self.Name}')
        while d.status == 'running': logging.debug('awaiting container exit')
        self.containerID = d.id
        self.HashedKey = hashlib.sha256(Key.encode()).digest()
    
    def __getContainer__(self) -> docker.models.containers.Container:
        cont: None
        for container in dock.containers.list(all=True):
            if container.name == self.Name:
                cont = container
        if cont == None:
            logging.debug("creating container")
            mnt = Mount('/mnt/data',f'{self.Name}VOL',type='volume')
            publicVOL = Mount('/mnt/public',f'publicData',type='volume')
            env = self.Env
            env.startup = 'exit'
            cont = dock.containers.run(self.Image,environment=env, detach=True, mounts=[mnt,publicVOL], name=f'{self.Name}',ports=self.Ports)
        return cont

    def checkKey(self, key):
        if hashlib.sha256(key.encode()).digest() == self.HashedKey:
            return True
        return False
    
    def getState(self,**kwargs):
        """
        gets the server state
        """
        return {'failed': False,'status':200,'output': {'state': self.State},'message': 'server state'}
    
    def setState(self,State,**kwargs):
        """
        sets the server state
        """
        try: int(State) #make sure it can be a int
        except ValueError: return {'failed': True,'status': 400, 'message': f'{State} is not a valid int'}
        self.State = int(State)
        return {'failed': False,'status':200,'output': {'state': self.State},'message': 'server state updated'}
    
    def lsFiles(self,**kwargs):
        """
        list files that are inside the server Volume
        """
        mnt = Mount('/mnt/data',f'{self.Name}VOL',type='volume')
        cont = dock.containers.run(containerName,detach=True,mounts=[mnt],environment={'STARTUP': f'tree -J /mnt/data', 'SILENT': '1'})
        while cont.status == 'running': pass
        logs = cont.logs(stdout=True,stderr=True).decode('UTF-8')
        cont.remove(force=True)
        return {'failed': False,'status':200,'output': {'Folder': logs },'message': 'all files'}
    
    def getFile(self,File,**kwargs):
        """
        extract a file from the container
        """
        mnt = Mount('/mnt/data',f'{self.Name}VOL',type='volume')
        cont = dock.containers.run(containerName,detach=True,mounts=[mnt],environment={'STARTUP': f'cat /mnt/data/{File}', 'SILENT': '1'})
        exi = cont.wait()
        if exi['StatusCode'] == 0:
            logs = cont.logs(stdout=True,stderr=True).decode('UTF-8')
            cont.remove(force=True)
            return {'failed': False,'status':200,'output': {'content': logs, 'file': File},'message': 'file send'}
        else:
            cont.remove(force=True)
            return {'failed': True,'status': 400,'message': "ls exited with code {}"}
    
    def putFile(self,File,Data,**kwargs):
        mnt = Mount('/mnt/data',f'{self.Name}VOL',type='volume')
        cont = dock.containers.run(containerName,detach=True,mounts=[mnt],environment={'STARTUP': f'echo {Data} | tee /mnt/data/{File}'})
        while cont.status == 'running': pass
        contents = cont.logs(stdout=True,stderr=True).decode('UTF-8')
        cont.remove(force=True)
        return {'failed': False,'status':200,'output': {'contents': contents, 'file': File},'message': 'file recieved'}
    
    def getName(self,**kwargs):
        return {'failed': False,'status':200,'output': {'name': self.Name},'message': 'server name'}
    
    def getLogs(self,**kwargs):
        cont = self.__getContainer__()
        logging.debug('located container')
        return {'failed': False, 'status': 200, 'message': 'container logs', 'output': {'logs': cont.logs(stdout=True,stderr=True).decode('UTF-8')}}

    def setStartup(self,Startup,**kwargs):
        self.Startup = Startup
        return {'failed': False, 'status': 200,'message': 'set startup cmd','output': {'Startup': self.Startup}}
    
    def getStartup(self,**kwargs):
        return {'failed': False, 'status': 200,'message': 'get startup cmd','output': {'Startup': self.Startup}}
    
    def setEnv(self,Key,Value,**kwargs):
        tmp = self.Env
        if type(tmp) != type({}): tmp = {}
        tmp[Key] = Value
        self.Env = tmp
        return {'failed': False, 'status': 200,'message': 'set env','output': {'Key': Key,'Value': self.Env[Key]}}
    
    def getEnv(self,**kwargs):
        return {'failed': False, 'status': 200,'message': 'set env','output': {'env': self.Env}}
    
    def lsPorts(self,**kwargs):
        return {'failed': False, 'status': 200,'message': 'port fowards (Host: container)','output': {'ports': self.Ports}}
    
    def setPort(self,HostPort,ContPort,**kwargs):
        self.Ports[ContPort] = HostPort
        return {'failed': False, 'status': 200,'message': 'set port foward','output': {'HostPort': HostPort, 'ContPort': ContPort}}

    def delPort(self,ContPort,**kwargs):
        self.Ports.pop(ContPort)
        return {'failed': False, 'status': 200,'message': 'removed port foward','output': {'ContPort': ContPort}}
    
    def startServer(self,**kwargs):
        cont = self.__getContainer__()
        if cont.status == 'running': return {'failed': True,'status': 400, 'message': 'server is allready running'}
        env = self.Env
        env['STARTUP'] = self.Startup
        cont.exec_run(detach=True,environment=env)
        return {'failed': False,'status':200,'message':'starting server','output':{}}

    def stopServer(self,**kwargs):
        cont = self.__getContainer__()
        if cont.status == 'running':
            cont.kill()
            return {'failed': False,'status':200,'message':'server killed/stopping','output':{}}
        else:
            return {'failed': True,'status':500,'message':'server isn\'t running'}
    
    def reloadContainer(self,**kwargs):
        cont = self.__getContainer__()
        if cont.status == 'running': return {'failed': True,'status': 400, 'message': 'container is running, cannot reload'}
        cont.remove(force=True)
        cont = self.__getContainer__()
        return {'failed': False,'status': 200,'message': 'container reset','output': {}}
