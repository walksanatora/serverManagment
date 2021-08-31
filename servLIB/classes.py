import os
import docker
from docker.types import Mount
import logging
import hashlib

dock = docker.from_env()

class server:
    hashedKey = ''
    state = 0

    def __init__(self, key):
        self.hashedKey = hashlib.sha256(key.encode()).digest()

    def checkKey(self, key):
        if hashlib.sha256(key.encode()).digest() == self.hashedKey:
            return True
        return False
    
    def getState(self,**kwargs):
        return {'failed': False,'status':200,'output': {'state': self.state},'message': 'server state'}

    def onosecond(self,**kwargs):
        return {'failed': False,'status': 200, 'output': kwargs, 'message': 'headers'}, 200
