import docker

dock = docker.from_env()
for i in dock.containers.list(all=True):
    if i.status == 'running':
        print("container ", i.short_id, i.name, " not killing")
    else:
        print("container ", i.short_id, i.name, " deleting")
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
    for i in dock.images.list(all=True):
        print('image ', f"{i.labels}", 'removing')
        dock.images.remove(i.id, force=True)
else:
    print('not purging images')
