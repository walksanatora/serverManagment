import docker
from docker.types import Mount
import os
import time
dock = docker.from_env()
mnt = Mount('/mnt/data','testVOL',type='volume')
cont = dock.containers.run('cont',detach=True,mounts=[mnt],environment={'STARTUP': 'echo asdf > /mnt/data/asdf.foo'})

try:
    print('waiting for exit')
    while cont.status == 'running': pass
    print(cont.diff())
    dir = cont.diff()[-1]['Path']
    print(dir)
    print(f'docker cp {cont.short_id}:{dir} {os.getcwd()}/123.txt')
    print(os.system(f'docker cp {cont.short_id}:{dir} {os.getcwd()}/123.txt'))
    while True:
        print('output')
        print(cont.logs(stdout=True,stderr=True).decode('UTF-8'))
        time.sleep(1)
except KeyboardInterrupt:
    pass