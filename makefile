py = 'python3.9'

clean: data docker

full-test:
	${py} full-test.py

data:
	${py} clearData.py

docker:
	${py} purge-docker.py
