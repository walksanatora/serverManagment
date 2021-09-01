import docker
dock = docker.from_env()
for i in dock.containers.list(all=True):
    if i.status == 'running':
        print("container ", i.id, " not killing")
    else:
        print("container ", i.id, " deleting")
        i.remove(force=True)

for i in dock.volumes.list():
    print("volume ", i.name, " removing")
    i.remove()

de = str.lower(input('purge images?: ')).strip()

purgeImages = False

if de in ['yes','y','1','true']:
    purgeImages = True 

if purgeImages:
    print('purging images')
    for i in dock.images.list():
        print('image ', f"{i.labels}", 'removing')
        dock.images.remove(i.id)
else:
    print('not purging images')
print(de)