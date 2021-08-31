import docker
dock = docker.from_env()
for i in dock.containers.list(all=True):
    if i.status == 'running':
        print(i.id, " not killing")
    else:
        print(i.id, " killing")
        i.remove(force=True)