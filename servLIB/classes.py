import os
import docker
from docker.types import Mount
import logging
import hashlib

dock = docker.from_env()

class server:
    hashedKey = ''

    def __init__(self, key):
        self.hashedKey = hashlib.sha256(key.encode()).digest()

    def checkKey(self, key):
        if hashlib.sha256(key.encode()).digest() == self.hashedKey:
            return True
        return False
    
    def onosecond(self,**kwargs):
        return kwargs, 200
